# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: skip-file
# flake8: noqa

from azure.cli.core.aaz import *


@register_command(
    "reservations reservation-order list",
)
class List(AAZCommand):
    """List of all the `ReservationOrder`s that the user has access to in the current tenant.

    :example: List of all the reservation orders that the user has access to in the current tenant.
        az reservations reservation-order list
    """

    _aaz_info = {
        "version": "2022-03-01",
        "resources": [
            ["mgmt-plane", "/providers/microsoft.capacity/reservationorders", "2022-03-01"],
        ]
    }

    def _handler(self, command_args):
        super()._handler(command_args)
        return self.build_paging(self._execute_operations, self._output)

    def _execute_operations(self):
        self.pre_operations()
        self.ReservationOrderList(ctx=self.ctx)()
        self.post_operations()

    # @register_callback
    def pre_operations(self):
        pass

    # @register_callback
    def post_operations(self):
        pass

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance.value, client_flatten=True)
        next_link = self.deserialize_output(self.ctx.vars.instance.next_link)
        return result, next_link

    class ReservationOrderList(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [200]:
                return self.on_200(session)

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/providers/Microsoft.Capacity/reservationOrders",
                **self.url_parameters
            )

        @property
        def method(self):
            return "GET"

        @property
        def error_format(self):
            return "ODataV4Format"

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2022-03-01",
                    required=True,
                ),
            }
            return parameters

        @property
        def header_parameters(self):
            parameters = {
                **self.serialize_header_param(
                    "Accept", "application/json",
                ),
            }
            return parameters

        def on_200(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200
            )

        _schema_on_200 = None

        @classmethod
        def _build_schema_on_200(cls):
            if cls._schema_on_200 is not None:
                return cls._schema_on_200

            cls._schema_on_200 = AAZObjectType()

            _schema_on_200 = cls._schema_on_200
            _schema_on_200.next_link = AAZStrType(
                serialized_name="nextLink",
            )
            _schema_on_200.value = AAZListType()

            value = cls._schema_on_200.value
            value.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element
            _element.etag = AAZIntType()
            _element.id = AAZStrType(
                flags={"read_only": True},
            )
            _element.name = AAZStrType(
                flags={"read_only": True},
            )
            _element.properties = AAZObjectType(
                flags={"client_flatten": True},
            )
            _element.system_data = AAZObjectType(
                serialized_name="systemData",
                flags={"read_only": True},
            )
            _build_schema_system_data_read(_element.system_data)
            _element.type = AAZStrType(
                flags={"read_only": True},
            )

            properties = cls._schema_on_200.value.Element.properties
            properties.benefit_start_time = AAZStrType(
                serialized_name="benefitStartTime",
            )
            properties.billing_plan = AAZStrType(
                serialized_name="billingPlan",
            )
            properties.created_date_time = AAZStrType(
                serialized_name="createdDateTime",
            )
            properties.display_name = AAZStrType(
                serialized_name="displayName",
            )
            properties.expiry_date = AAZStrType(
                serialized_name="expiryDate",
            )
            properties.original_quantity = AAZIntType(
                serialized_name="originalQuantity",
            )
            properties.plan_information = AAZObjectType(
                serialized_name="planInformation",
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
            )
            properties.request_date_time = AAZStrType(
                serialized_name="requestDateTime",
            )
            properties.reservations = AAZListType()
            properties.term = AAZStrType()

            plan_information = cls._schema_on_200.value.Element.properties.plan_information
            plan_information.next_payment_due_date = AAZStrType(
                serialized_name="nextPaymentDueDate",
            )
            plan_information.pricing_currency_total = AAZObjectType(
                serialized_name="pricingCurrencyTotal",
            )
            _build_schema_price_read(plan_information.pricing_currency_total)
            plan_information.start_date = AAZStrType(
                serialized_name="startDate",
            )
            plan_information.transactions = AAZListType()

            transactions = cls._schema_on_200.value.Element.properties.plan_information.transactions
            transactions.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element.properties.plan_information.transactions.Element
            _element.billing_account = AAZStrType(
                serialized_name="billingAccount",
            )
            _element.billing_currency_total = AAZObjectType(
                serialized_name="billingCurrencyTotal",
            )
            _build_schema_price_read(_element.billing_currency_total)
            _element.due_date = AAZStrType(
                serialized_name="dueDate",
            )
            _element.extended_status_info = AAZObjectType(
                serialized_name="extendedStatusInfo",
            )
            _build_schema_extended_status_info_read(_element.extended_status_info)
            _element.payment_date = AAZStrType(
                serialized_name="paymentDate",
            )
            _element.pricing_currency_total = AAZObjectType(
                serialized_name="pricingCurrencyTotal",
            )
            _build_schema_price_read(_element.pricing_currency_total)
            _element.status = AAZStrType()

            reservations = cls._schema_on_200.value.Element.properties.reservations
            reservations.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element.properties.reservations.Element
            _element.etag = AAZIntType()
            _element.id = AAZStrType(
                flags={"read_only": True},
            )
            _element.kind = AAZStrType()
            _element.location = AAZStrType()
            _element.name = AAZStrType(
                flags={"read_only": True},
            )
            _element.properties = AAZObjectType()
            _element.sku = AAZObjectType()
            _build_schema_sku_name_read(_element.sku)
            _element.system_data = AAZObjectType(
                serialized_name="systemData",
                flags={"read_only": True},
            )
            _build_schema_system_data_read(_element.system_data)
            _element.type = AAZStrType(
                flags={"read_only": True},
            )

            properties = cls._schema_on_200.value.Element.properties.reservations.Element.properties
            properties.applied_scope_properties = AAZObjectType(
                serialized_name="appliedScopeProperties",
            )
            properties.applied_scope_type = AAZStrType(
                serialized_name="appliedScopeType",
            )
            properties.applied_scopes = AAZListType(
                serialized_name="appliedScopes",
            )
            _build_schema_applied_scopes_read(properties.applied_scopes)
            properties.archived = AAZBoolType()
            properties.benefit_start_time = AAZStrType(
                serialized_name="benefitStartTime",
            )
            properties.billing_plan = AAZStrType(
                serialized_name="billingPlan",
            )
            properties.billing_scope_id = AAZStrType(
                serialized_name="billingScopeId",
            )
            properties.capabilities = AAZStrType()
            properties.display_name = AAZStrType(
                serialized_name="displayName",
            )
            properties.display_provisioning_state = AAZStrType(
                serialized_name="displayProvisioningState",
                flags={"read_only": True},
            )
            properties.effective_date_time = AAZStrType(
                serialized_name="effectiveDateTime",
            )
            properties.expiry_date = AAZStrType(
                serialized_name="expiryDate",
            )
            properties.extended_status_info = AAZObjectType(
                serialized_name="extendedStatusInfo",
            )
            _build_schema_extended_status_info_read(properties.extended_status_info)
            properties.instance_flexibility = AAZStrType(
                serialized_name="instanceFlexibility",
            )
            properties.last_updated_date_time = AAZStrType(
                serialized_name="lastUpdatedDateTime",
                flags={"read_only": True},
            )
            properties.merge_properties = AAZObjectType(
                serialized_name="mergeProperties",
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
            )
            properties.provisioning_sub_state = AAZStrType(
                serialized_name="provisioningSubState",
                flags={"read_only": True},
            )
            properties.purchase_date = AAZStrType(
                serialized_name="purchaseDate",
            )
            properties.quantity = AAZIntType()
            properties.renew = AAZBoolType()
            properties.renew_destination = AAZStrType(
                serialized_name="renewDestination",
            )
            properties.renew_properties = AAZObjectType(
                serialized_name="renewProperties",
            )
            properties.renew_source = AAZStrType(
                serialized_name="renewSource",
            )
            properties.reserved_resource_type = AAZStrType(
                serialized_name="reservedResourceType",
            )
            properties.sku_description = AAZStrType(
                serialized_name="skuDescription",
            )
            properties.split_properties = AAZObjectType(
                serialized_name="splitProperties",
            )
            properties.swap_properties = AAZObjectType(
                serialized_name="swapProperties",
            )
            properties.term = AAZStrType()
            properties.user_friendly_applied_scope_type = AAZStrType(
                serialized_name="userFriendlyAppliedScopeType",
                flags={"read_only": True},
            )
            properties.user_friendly_renew_state = AAZStrType(
                serialized_name="userFriendlyRenewState",
                flags={"read_only": True},
            )
            properties.utilization = AAZObjectType(
                flags={"read_only": True},
            )

            applied_scope_properties = cls._schema_on_200.value.Element.properties.reservations.Element.properties.applied_scope_properties
            applied_scope_properties.display_name = AAZStrType(
                serialized_name="displayName",
            )
            applied_scope_properties.management_group_id = AAZStrType(
                serialized_name="managementGroupId",
            )
            applied_scope_properties.tenant_id = AAZStrType(
                serialized_name="tenantId",
            )

            merge_properties = cls._schema_on_200.value.Element.properties.reservations.Element.properties.merge_properties
            merge_properties.merge_destination = AAZStrType(
                serialized_name="mergeDestination",
            )
            merge_properties.merge_sources = AAZListType(
                serialized_name="mergeSources",
            )

            merge_sources = cls._schema_on_200.value.Element.properties.reservations.Element.properties.merge_properties.merge_sources
            merge_sources.Element = AAZStrType()

            renew_properties = cls._schema_on_200.value.Element.properties.reservations.Element.properties.renew_properties
            renew_properties.billing_currency_total = AAZObjectType(
                serialized_name="billingCurrencyTotal",
            )
            renew_properties.pricing_currency_total = AAZObjectType(
                serialized_name="pricingCurrencyTotal",
            )
            renew_properties.purchase_properties = AAZObjectType(
                serialized_name="purchaseProperties",
            )

            billing_currency_total = cls._schema_on_200.value.Element.properties.reservations.Element.properties.renew_properties.billing_currency_total
            billing_currency_total.amount = AAZFloatType()
            billing_currency_total.currency_code = AAZStrType(
                serialized_name="currencyCode",
            )

            pricing_currency_total = cls._schema_on_200.value.Element.properties.reservations.Element.properties.renew_properties.pricing_currency_total
            pricing_currency_total.amount = AAZFloatType()
            pricing_currency_total.currency_code = AAZStrType(
                serialized_name="currencyCode",
            )

            purchase_properties = cls._schema_on_200.value.Element.properties.reservations.Element.properties.renew_properties.purchase_properties
            purchase_properties.location = AAZStrType()
            purchase_properties.properties = AAZObjectType(
                flags={"client_flatten": True},
            )
            purchase_properties.sku = AAZObjectType()
            _build_schema_sku_name_read(purchase_properties.sku)

            properties = cls._schema_on_200.value.Element.properties.reservations.Element.properties.renew_properties.purchase_properties.properties
            properties.applied_scope_type = AAZStrType(
                serialized_name="appliedScopeType",
            )
            properties.applied_scopes = AAZListType(
                serialized_name="appliedScopes",
            )
            _build_schema_applied_scopes_read(properties.applied_scopes)
            properties.billing_plan = AAZStrType(
                serialized_name="billingPlan",
            )
            properties.billing_scope_id = AAZStrType(
                serialized_name="billingScopeId",
            )
            properties.display_name = AAZStrType(
                serialized_name="displayName",
            )
            properties.quantity = AAZIntType()
            properties.renew = AAZBoolType()
            properties.reserved_resource_properties = AAZObjectType(
                serialized_name="reservedResourceProperties",
            )
            properties.reserved_resource_type = AAZStrType(
                serialized_name="reservedResourceType",
            )
            properties.term = AAZStrType()

            reserved_resource_properties = cls._schema_on_200.value.Element.properties.reservations.Element.properties.renew_properties.purchase_properties.properties.reserved_resource_properties
            reserved_resource_properties.instance_flexibility = AAZStrType(
                serialized_name="instanceFlexibility",
            )

            split_properties = cls._schema_on_200.value.Element.properties.reservations.Element.properties.split_properties
            split_properties.split_destinations = AAZListType(
                serialized_name="splitDestinations",
            )
            split_properties.split_source = AAZStrType(
                serialized_name="splitSource",
            )

            split_destinations = cls._schema_on_200.value.Element.properties.reservations.Element.properties.split_properties.split_destinations
            split_destinations.Element = AAZStrType()

            swap_properties = cls._schema_on_200.value.Element.properties.reservations.Element.properties.swap_properties
            swap_properties.swap_destination = AAZStrType(
                serialized_name="swapDestination",
            )
            swap_properties.swap_source = AAZStrType(
                serialized_name="swapSource",
            )

            utilization = cls._schema_on_200.value.Element.properties.reservations.Element.properties.utilization
            utilization.aggregates = AAZListType(
                flags={"read_only": True},
            )
            utilization.trend = AAZStrType(
                flags={"read_only": True},
            )

            aggregates = cls._schema_on_200.value.Element.properties.reservations.Element.properties.utilization.aggregates
            aggregates.Element = AAZObjectType(
                flags={"read_only": True},
            )

            _element = cls._schema_on_200.value.Element.properties.reservations.Element.properties.utilization.aggregates.Element
            _element.grain = AAZFloatType(
                flags={"read_only": True},
            )
            _element.grain_unit = AAZStrType(
                serialized_name="grainUnit",
                flags={"read_only": True},
            )
            _element.value = AAZFloatType(
                flags={"read_only": True},
            )
            _element.value_unit = AAZStrType(
                serialized_name="valueUnit",
                flags={"read_only": True},
            )

            return cls._schema_on_200


_schema_applied_scopes_read = None


def _build_schema_applied_scopes_read(_schema):
    global _schema_applied_scopes_read
    if _schema_applied_scopes_read is not None:
        _schema.Element = _schema_applied_scopes_read.Element
        return

    _schema_applied_scopes_read = AAZListType()

    applied_scopes_read = _schema_applied_scopes_read
    applied_scopes_read.Element = AAZStrType()

    _schema.Element = _schema_applied_scopes_read.Element


_schema_extended_status_info_read = None


def _build_schema_extended_status_info_read(_schema):
    global _schema_extended_status_info_read
    if _schema_extended_status_info_read is not None:
        _schema.message = _schema_extended_status_info_read.message
        _schema.status_code = _schema_extended_status_info_read.status_code
        return

    _schema_extended_status_info_read = AAZObjectType()

    extended_status_info_read = _schema_extended_status_info_read
    extended_status_info_read.message = AAZStrType()
    extended_status_info_read.status_code = AAZStrType(
        serialized_name="statusCode",
    )

    _schema.message = _schema_extended_status_info_read.message
    _schema.status_code = _schema_extended_status_info_read.status_code


_schema_price_read = None


def _build_schema_price_read(_schema):
    global _schema_price_read
    if _schema_price_read is not None:
        _schema.amount = _schema_price_read.amount
        _schema.currency_code = _schema_price_read.currency_code
        return

    _schema_price_read = AAZObjectType()

    price_read = _schema_price_read
    price_read.amount = AAZFloatType()
    price_read.currency_code = AAZStrType(
        serialized_name="currencyCode",
    )

    _schema.amount = _schema_price_read.amount
    _schema.currency_code = _schema_price_read.currency_code


_schema_sku_name_read = None


def _build_schema_sku_name_read(_schema):
    global _schema_sku_name_read
    if _schema_sku_name_read is not None:
        _schema.name = _schema_sku_name_read.name
        return

    _schema_sku_name_read = AAZObjectType()

    sku_name_read = _schema_sku_name_read
    sku_name_read.name = AAZStrType()

    _schema.name = _schema_sku_name_read.name


_schema_system_data_read = None


def _build_schema_system_data_read(_schema):
    global _schema_system_data_read
    if _schema_system_data_read is not None:
        _schema.created_at = _schema_system_data_read.created_at
        _schema.created_by = _schema_system_data_read.created_by
        _schema.created_by_type = _schema_system_data_read.created_by_type
        _schema.last_modified_at = _schema_system_data_read.last_modified_at
        _schema.last_modified_by = _schema_system_data_read.last_modified_by
        _schema.last_modified_by_type = _schema_system_data_read.last_modified_by_type
        return

    _schema_system_data_read = AAZObjectType(
        flags={"read_only": True}
    )

    system_data_read = _schema_system_data_read
    system_data_read.created_at = AAZStrType(
        serialized_name="createdAt",
        flags={"read_only": True},
    )
    system_data_read.created_by = AAZStrType(
        serialized_name="createdBy",
        flags={"read_only": True},
    )
    system_data_read.created_by_type = AAZStrType(
        serialized_name="createdByType",
        flags={"read_only": True},
    )
    system_data_read.last_modified_at = AAZStrType(
        serialized_name="lastModifiedAt",
        flags={"read_only": True},
    )
    system_data_read.last_modified_by = AAZStrType(
        serialized_name="lastModifiedBy",
        flags={"read_only": True},
    )
    system_data_read.last_modified_by_type = AAZStrType(
        serialized_name="lastModifiedByType",
        flags={"read_only": True},
    )

    _schema.created_at = _schema_system_data_read.created_at
    _schema.created_by = _schema_system_data_read.created_by
    _schema.created_by_type = _schema_system_data_read.created_by_type
    _schema.last_modified_at = _schema_system_data_read.last_modified_at
    _schema.last_modified_by = _schema_system_data_read.last_modified_by
    _schema.last_modified_by_type = _schema_system_data_read.last_modified_by_type


__all__ = ["List"]
