# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import sys

from pkg_resources import parse_version
from knack.log import get_logger
from azext_confcom.config import DEFAULT_REGO_FRAGMENTS
from azext_confcom import os_util
from azext_confcom.template_util import pretty_print_func, print_func
from azext_confcom.init_checks import run_initial_docker_checks
from azext_confcom.template_util import inject_policy_into_template, print_existing_policy_from_arm_template
from azext_confcom import security_policy


logger = get_logger(__name__)


def acipolicygen_confcom(
    input_path: str,
    arm_template: str,
    arm_template_parameters: str,
    image_name: str,
    infrastructure_svn: str,
    tar_mapping_location: str,
    use_json: bool = False,
    outraw: bool = False,
    outraw_pretty_print: bool = False,
    diff: bool = False,
    validate_sidecar: bool = False,
    save_to_file: str = None,
    debug_mode: bool = False,
    print_policy_to_terminal: bool = False,
    disable_stdio: bool = False,
    print_existing_policy: bool = False,
):

    if sum(map(bool, [input_path, arm_template, image_name])) != 1:
        logger.error("Can only generate CCE policy from one source at a time")
        sys.exit(1)
    if sum(map(bool, [print_policy_to_terminal, outraw, outraw_pretty_print])) > 1:
        logger.error("Can only print in one format at a time")
        sys.exit(1)
    elif (diff and input_path) or (diff and image_name):
        logger.error("Can only diff CCE policy from ARM Template")
        sys.exit(1)
    elif arm_template_parameters and not arm_template:
        logger.error(
            "Can only use ARM Template Parameters if ARM Template is also present"
        )
        sys.exit(1)

    if print_existing_policy:
        if not arm_template:
            logger.error("Can only print existing policy from ARM Template")
            sys.exit(1)
        else:
            print_existing_policy_from_arm_template(arm_template, arm_template_parameters)
            sys.exit(0)

    tar_mapping = tar_mapping_validation(tar_mapping_location)

    output_type = get_output_type(outraw, outraw_pretty_print)

    container_group_policies = None

    # warn user that input infrastructure_svn is less than the configured default value
    if infrastructure_svn and parse_version(infrastructure_svn) < parse_version(
        DEFAULT_REGO_FRAGMENTS[0]["minimum_svn"]
    ):
        logger.warning(
            "Input Infrastructure Fragment Software Version Number is less than the default Infrastructure SVN: %s",
            DEFAULT_REGO_FRAGMENTS[0]["minimum_svn"],
        )

    # telling the user what operation we're doing
    logger.warning(
        "Generating security policy for %s: %s in %s",
        "ARM Template" if arm_template else "Image" if image_name else "Input File",
        input_path or arm_template or image_name,
        "base64"
        if output_type == security_policy.OutputType.DEFAULT
        else "clear text",
    )
    # error checking for making sure an input is provided is above
    if input_path:
        container_group_policies = security_policy.load_policy_from_file(
            input_path, debug_mode=debug_mode,
        )
    elif arm_template:
        container_group_policies = security_policy.load_policy_from_arm_template_file(
            infrastructure_svn,
            arm_template,
            arm_template_parameters,
            debug_mode=debug_mode,
            disable_stdio=disable_stdio,
        )
    elif image_name:
        container_group_policies = security_policy.load_policy_from_image_name(
            image_name, debug_mode=debug_mode, disable_stdio=disable_stdio
        )

    exit_code = 0

    # standardize the output so we're only operating on arrays
    # this makes more sense than making the "from_file" and "from_image" outputting arrays
    # since they can only ever output a single image's policy
    if not isinstance(container_group_policies, list):
        container_group_policies = [container_group_policies]

    for count, policy in enumerate(container_group_policies):
        policy.populate_policy_content_for_all_images(
            individual_image=bool(image_name), tar_mapping=tar_mapping
        )

        if validate_sidecar:
            exit_code = validate_sidecar_in_policy(policy, output_type == security_policy.OutputType.PRETTY_PRINT)
        elif diff:
            exit_code = get_diff_outputs(policy, output_type == security_policy.OutputType.PRETTY_PRINT)
        elif arm_template and (not print_policy_to_terminal and not outraw and not outraw_pretty_print):
            result = inject_policy_into_template(arm_template, arm_template_parameters,
                                                 policy.get_serialized_output(output_type, use_json), count)
            if result:
                print("CCE Policy successfully injected into ARM Template")
        else:
            # output to terminal
            print(f"{policy.get_serialized_output(output_type, use_json)}\n\n")
            # output to file
            if save_to_file:
                policy.save_to_file(save_to_file, output_type, use_json)

    sys.exit(exit_code)


def update_confcom(cmd, instance, tags=None):
    with cmd.update_context(instance) as c:
        c.set_param("tags", tags)
    return instance


def validate_sidecar_in_policy(policy: security_policy.AciPolicy, outraw_pretty_print: bool):
    is_valid, output = policy.validate_sidecars()

    if outraw_pretty_print:
        formatted_output = pretty_print_func(output)
    else:
        formatted_output = print_func(output)

    if is_valid:
        print("Sidecar containers will pass with its generated policy")
        return 0

    print(
        f"Sidecar containers will not pass with its generated policy: {formatted_output}"
    )
    return 2


def get_diff_outputs(policy: security_policy.AciPolicy, outraw_pretty_print: bool):
    exit_code = 0
    is_valid, output = policy.validate_cce_policy()

    if outraw_pretty_print:
        formatted_output = pretty_print_func(output)
    else:
        formatted_output = print_func(output)

    print(
        "Existing policy and ARM Template match"
        if is_valid
        else formatted_output
    )
    fragment_diff = policy.compare_fragments()

    if fragment_diff != {}:
        logger.warning(
            "Fragments in the existing policy are not the defaults. If this is expected, ignore this warning."
        )
    if not is_valid:
        logger.warning(
            "Existing Policy and ARM Template differ. Consider recreating the base64-encoded policy."
        )
        exit_code = 2
    return exit_code


def tar_mapping_validation(tar_mapping_location: str):
    tar_mapping = None
    if tar_mapping_location:
        if not os.path.isfile(tar_mapping_location):
            print(
                "--tar input must either be a path to a json file with "
                + "image to tar location mappings or the location to a single tar file."
            )
            sys.exit(2)
        # file is mapping images to tar file locations
        elif tar_mapping_location.endswith(".json"):
            tar_mapping = os_util.load_tar_mapping_from_file(tar_mapping_location)
        # passing in a single tar location for a single image policy
        else:
            tar_mapping = tar_mapping_location
    else:
        # only need to do the docker checks if we're not grabbing image info from tar files
        error_msg = run_initial_docker_checks()
        if error_msg:
            logger.warning(error_msg)
            sys.exit(1)
    return tar_mapping


def get_output_type(outraw, outraw_pretty_print):
    output_type = security_policy.OutputType.DEFAULT
    if outraw:
        output_type = security_policy.OutputType.RAW
    elif outraw_pretty_print:
        output_type = security_policy.OutputType.PRETTY_PRINT
    return output_type
