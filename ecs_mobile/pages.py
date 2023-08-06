import frappe
import erpnext
from frappe import auth
import random
import datetime
import json, ast
from erpnext.accounts.utils import get_balance_on
from six import iteritems, string_types

from .helpers import remove_html_tags, get_timesheet_task_count

from frappe.utils import (
    flt,
    getdate,
    get_url,
    now,
    nowtime,
    get_time,
    today,
    get_datetime,
    add_days,
)
from frappe.utils import add_to_date, now, nowdate
from frappe.utils import cstr
from frappe.utils.make_random import get_random


@frappe.whitelist()
def lead(name):
    led = {}
    doc_data = frappe.db.get_all(
        "Lead",
        filters={"name": name},
        fields=[
            "name",
            "lead_name",
            "organization_lead",
            "company_name",
            "lead_owner",
            "status",
            "source",
            "email_id",
            "mobile_no",
            "address_title",
            "address_line1",
            "city",
            "country",
            "campaign_name",
            "contact_by",
            "contact_date",
            "request_type",
            "market_segment",
            "territory",
            "industry",
            "docstatus",
        ],
    )
    for x in doc_data:
        led["name"] = x.name
        led["status"] = x.status
        led["lead_name"] = x.lead_name
        led["organization_lead"] = x.organization_lead
        led["company_name"] = x.company_name
        led["industry"] = x.industry
        led["market_segment"] = x.market_segment
        led["territory"] = x.territory
        led["address_title"] = x.address_title
        led["address_line1"] = x.address_line1
        led["city"] = x.city
        led["country"] = x.country
        led["mobile_no"] = x.mobile_no
        led["email_id"] = x.email_id
        led["source"] = x.source
        led["campaign_name"] = x.campaign_name
        led["request_type"] = x.request_type
        led["lead_owner"] = x.lead_owner
        led["contact_by"] = x.contact_by
        led["contact_date"] = x.contact_date

        led["docstatus"] = x.docstatus

    attachments = frappe.db.sql(
        """ Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                    from `tabFile`  where `tabFile`.attached_to_doctype = "Lead"
                                    and `tabFile`.attached_to_name = "{name}"
                                    order by `tabFile`.creation
                                """.format(
            name=name
        ),
        as_dict=1,
    )

    led["attachments"] = attachments

    comments = frappe.db.sql(
        """ Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Lead"
                                        and `tabComment`.reference_name = "{name}"
                                        and `tabComment`.comment_type = "Comment"
                                        order by `tabComment`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )

    led["comments"] = comments

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Lead" and disabled = 0 """,
        as_dict=1,
    )
    led["print_formats"] = print_formats
    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)

    quotation_count = frappe.db.count("Quotation", filters={"party_name": name})
    opportunity_count = frappe.db.count("Opportunity", filters={"party_name": name})
    # quotation_name = frappe.db.get_all('Quotation', filters={'party_name': name}, fields=['name'])
    # opportunity_name = frappe.db.get_all('Opportunity', filters={'party_name': name}, fields=['name'])

    qtn_connections = {}
    opp_connections = {}
    connections = []

    if quotation_count > 0 and doc_data:
        qtn_connections["name"] = "Quotation"
        qtn_connections["count"] = quotation_count
        qtn_connections["icon"] = "https://erpcloud.systems/files/quotation.png"
        connections.append(qtn_connections)

    if opportunity_count > 0 and doc_data:
        opp_connections["name"] = "Opportunity"
        opp_connections["count"] = opportunity_count
        opp_connections["icon"] = "https://erpcloud.systems/files/opportunity.png"
        connections.append(opp_connections)

    led["conn"] = connections

    if doc_data:
        return led
    else:
        return "لا يوجد عميل محتمل بهذا الاسم"


@frappe.whitelist()
def opportunity(name):
    opp = {}
    doc_data = frappe.db.get_all(
        "Opportunity",
        filters={"name": name},
        fields=[
            "name",
            "opportunity_from",
            "party_name",
            "customer_name",
            "governorate",
            "source",
            "opportunity_type",
            "status",
            "order_lost_reason",
            "contact_by",
            "contact_date",
            "to_discuss",
            "with_items",
            "customer_address",
            "address_display",
            "territory",
            "customer_group",
            "contact_person",
            "contact_email",
            "contact_mobile",
            "campaign",
            "transaction_date",
            "docstatus",
        ],
    )
    for x in doc_data:
        opp["name"] = x.name
        opp["opportunity_from"] = x.opportunity_from
        opp["party_name"] = x.party_name
        opp["customer_name"] = x.customer_name
        opp["source"] = x.source
        opp["opportunity_type"] = x.opportunity_type
        opp["status"] = x.status
        opp["order_lost_reason"] = x.order_lost_reason
        opp["contact_by"] = x.contact_by
        opp["contact_date"] = x.contact_date
        opp["to_discuss"] = x.to_discuss
        opp["with_items"] = x.with_items
        opp["customer_address"] = x.customer_address
        opp["address_display"] = x.address_display
        opp["territory"] = x.territory
        opp["customer_group"] = x.customer_group
        opp["contact_person"] = x.contact_person
        opp["contact_email"] = x.contact_email
        opp["contact_mobile"] = x.contact_mobile
        opp["campaign"] = x.campaign
        opp["transaction_date"] = x.transaction_date
        opp["docstatus"] = x.docstatus

    child_data = frappe.db.get_all(
        "Opportunity Item",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "item_code",
            "item_name",
            "item_group",
            "brand",
            "description",
            "image",
            "qty",
            "uom",
        ],
    )

    if child_data and doc_data:
        opp["items"] = child_data

    attachments = frappe.db.sql(
        """ Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                    from `tabFile`  where `tabFile`.attached_to_doctype = "Opportunity"
                                    and `tabFile`.attached_to_name = "{name}"
                                    order by `tabFile`.creation
                                """.format(
            name=name
        ),
        as_dict=1,
    )

    opp["attachments"] = attachments

    comments = frappe.db.sql(
        """ Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Opportunity"
                                        and `tabComment`.reference_name = "{name}"
                                        and `tabComment`.comment_type = "Comment"
                                        order by `tabComment`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )

    opp["comments"] = comments

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Opportunity" and disabled = 0 """,
        as_dict=1,
    )
    opp["print_formats"] = print_formats
    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)

    quotation_count = frappe.db.count("Quotation", filters={"opportunity": name})
    sup_quotation_count = frappe.db.count(
        "Supplier Quotation", filters={"opportunity": name}
    )
    # quotation_name = frappe.db.get_all('Quotation', filters={'opportunity': name}, fields=['name'])
    # sup_quotation_name = frappe.db.get_all('Supplier Quotation', filters={'opportunity': name}, fields=['name'])

    qtn_connections = {}
    sup_qtn_connections = {}
    connections = []

    if quotation_count > 0 and doc_data:
        qtn_connections["name"] = "Quotation"
        qtn_connections["count"] = quotation_count
        qtn_connections["icon"] = "https://erpcloud.systems/files/quotation.png"
        connections.append(qtn_connections)

    if sup_quotation_count > 0 and doc_data:
        sup_qtn_connections["name"] = "Supplier Quotation"
        sup_qtn_connections["count"] = sup_quotation_count
        sup_qtn_connections[
            "icon"
        ] = "https://erpcloud.systems/files/supplier_quotation.png"
        connections.append(sup_qtn_connections)

    opp["conn"] = connections

    if doc_data:
        return opp
    else:
        return "لا يوجد فرصة بيعية بهذا الاسم"


@frappe.whitelist()
def quotation(name):
    qtn = {}
    doc_data = frappe.db.get_all(
        "Quotation",
        filters={"name": name},
        fields=[
            "name",
            "quotation_to",
            "party_name",
            "customer_name",
            "transaction_date",
            "valid_till",
            "order_type",
            "customer_address",
            "address_display",
            "contact_person",
            "contact_display",
            "contact_mobile",
            "contact_email",
            "customer_group",
            "territory",
            "currency",
            "conversion_rate",
            "selling_price_list",
            "price_list_currency",
            "plc_conversion_rate",
            "ignore_pricing_rule",
            "total_qty",
            "base_total",
            "base_net_total",
            "total",
            "net_total",
            "taxes_and_charges",
            "base_total_taxes_and_charges",
            "total_taxes_and_charges",
            "apply_discount_on",
            "base_discount_amount",
            "additional_discount_percentage",
            "discount_amount",
            "base_grand_total",
            "base_in_words",
            "grand_total",
            "in_words",
            "payment_terms_template",
            "tc_name",
            "terms",
            "campaign",
            "source",
            "order_lost_reason",
            "status",
            "docstatus",
        ],
    )
    amended_to = frappe.db.get_value("Quotation", {"amended_from": name}, ["name"])
    for x in doc_data:
        qtn["name"] = x.name
        qtn["quotation_to"] = x.quotation_to
        qtn["amended_to"] = amended_to
        qtn["party_name"] = x.party_name
        qtn["customer_name"] = x.customer_name
        qtn["transaction_date"] = x.transaction_date
        qtn["valid_till"] = x.valid_till
        qtn["order_type"] = x.order_type

        ####START OF ADDRESS & CONTACT####
        qtn["customer_address"] = x.customer_address
        qtn["address_line1"] = frappe.db.get_value(
            "Address", x.customer_address, "address_line1"
        )
        qtn["city"] = frappe.db.get_value("Address", x.customer_address, "city")
        qtn["country"] = frappe.db.get_value("Address", x.customer_address, "country")
        qtn["contact_person"] = x.contact_person
        qtn["contact_display"] = frappe.db.get_value(
            "Contact", x.contact_person, "first_name"
        )
        qtn["mobile_no"] = frappe.db.get_value("Contact", x.contact_person, "mobile_no")
        qtn["phone"] = frappe.db.get_value("Contact", x.contact_persont, "phone")
        qtn["email_id"] = frappe.db.get_value("Contact", x.contact_person, "email_id")
        ####END OF ADDRESS & CONTACT####

        qtn["address_display"] = x.address_display
        # qtn["contact_display"] = x.contact_display
        qtn["contact_mobile"] = x.contact_mobile
        qtn["contact_email"] = x.contact_email
        qtn["customer_group"] = x.customer_group
        qtn["territory"] = x.territory
        qtn["currency"] = x.currency
        qtn["conversion_rate"] = x.conversion_rate
        qtn["selling_price_list"] = x.selling_price_list
        qtn["price_list_currency"] = x.price_list_currency
        qtn["plc_conversion_rate"] = x.plc_conversion_rate
        qtn["ignore_pricing_rule"] = x.ignore_pricing_rule
        qtn["total_qty"] = x.total_qty
        qtn["base_total"] = x.base_total
        qtn["base_net_total"] = x.base_net_total
        qtn["total"] = x.total
        qtn["net_total"] = x.net_total
        qtn["taxes_and_charges"] = x.taxes_and_charges
        qtn["base_total_taxes_and_charges"] = x.base_total_taxes_and_charges
        qtn["total_taxes_and_charges"] = x.total_taxes_and_charges
        qtn["apply_discount_on"] = x.apply_discount_on
        qtn["base_discount_amount"] = x.base_discount_amount
        qtn["additional_discount_percentage"] = x.additional_discount_percentage
        qtn["discount_amount"] = x.discount_amount
        qtn["base_grand_total"] = x.base_grand_total
        qtn["base_in_words"] = x.base_in_words
        qtn["grand_total"] = x.grand_total
        qtn["in_words"] = x.in_words
        qtn["payment_terms_template"] = x.payment_terms_template
        qtn["tc_name"] = x.tc_name
        qtn["terms"] = x.terms
        qtn["campaign"] = x.campaign
        qtn["source"] = x.source
        qtn["order_lost_reason"] = x.order_lost_reason
        qtn["status"] = x.status
        qtn["docstatus"] = x.docstatus

    child_data_1 = frappe.db.get_all(
        "Quotation Item",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "item_code",
            "item_name",
            "description",
            "item_group",
            "brand",
            "image",
            "qty",
            "stock_uom",
            "uom",
            "conversion_factor",
            "stock_qty",
            "price_list_rate",
            "base_price_list_rate",
            "margin_type",
            "margin_rate_or_amount",
            "rate_with_margin",
            "discount_percentage",
            "discount_amount",
            "base_rate_with_margin",
            "rate",
            "net_rate",
            "amount",
            "net_amount",
            "item_tax_template",
            "base_rate",
            "base_net_rate",
            "base_amount",
            "base_net_amount",
            "stock_uom_rate",
            "valuation_rate",
            "gross_profit",
            "warehouse",
            "prevdoc_doctype",
            "prevdoc_docname",
            "projected_qty",
            "actual_qty",
        ],
    )

    child_data_2 = frappe.db.get_all(
        "Sales Taxes and Charges",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "charge_type",
            "row_id",
            "account_head",
            "description",
            "cost_center",
            "rate",
            "account_currency",
            "tax_amount",
            "total",
            "tax_amount_after_discount_amount",
            "base_tax_amount",
            "base_total",
            "base_tax_amount_after_discount_amount",
        ],
    )

    child_data_3 = frappe.db.get_all(
        "Payment Schedule",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "payment_term",
            "description",
            "due_date",
            "mode_of_payment",
            "invoice_portion",
            "discount_type",
            "discount_date",
            "discount",
            "payment_amount",
            "outstanding",
            "paid_amount",
            "discounted_amount",
            "base_payment_amount",
        ],
    )

    if child_data_1 and doc_data:
        qtn["items"] = child_data_1

    if child_data_2 and doc_data:
        qtn["taxes"] = child_data_2

    if child_data_3 and doc_data:
        qtn["payment_schedule"] = child_data_3

    attachments = frappe.db.sql(
        """ Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                    from `tabFile`  where `tabFile`.attached_to_doctype = "Quotation"
                                    and `tabFile`.attached_to_name = "{name}"
                                    order by `tabFile`.creation
                                """.format(
            name=name
        ),
        as_dict=1,
    )

    qtn["attachments"] = attachments

    comments = frappe.db.sql(
        """ Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Quotation"
                                        and `tabComment`.reference_name = "{name}"
                                        and `tabComment`.comment_type = "Comment"
                                        order by `tabComment`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )

    qtn["comments"] = comments

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Quotation" and disabled = 0 """,
        as_dict=1,
    )
    qtn["print_formats"] = print_formats
    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)

    sales_order_name = frappe.db.get_all(
        "Sales Order Item",
        filters={"prevdoc_docname": name},
        fields=["parent"],
        group_by="parent",
    )
    sales_order_count = len(sales_order_name)

    so_connections = {}
    connections = []

    if sales_order_count > 0 and doc_data:
        so_connections["name"] = "Sales Order"
        so_connections["count"] = sales_order_count
        so_connections["icon"] = "https://erpcloud.systems/files/sales_order.png"
        connections.append(so_connections)

    qtn["conn"] = connections

    if doc_data:
        return qtn
    else:
        return "لا يوجد عرض سعر بهذا الاسم"


@frappe.whitelist()
def customer(name):
    #
    cust = {}
    # quotation_validaty_days = frappe.db.get_single_value(
    #     "Selling Settings", "default_valid_till"  # quotation
    # )
    cust["quotation_validaty_days"] = 14

    balance = get_balance_on(
        account=None,
        date=getdate(nowdate()),
        party_type="Customer",
        party=name,
        company=None,
        in_account_currency=True,
        cost_center=None,
        ignore_account_permission=False,
    )
    cust["balance"] = balance
    doc_data = frappe.db.get_all(
        "Customer",
        filters={"name": name},
        fields=[
            "name",
            "customer_name",
            "sales_person",
            "disabled",
            "customer_type",
            "customer_group",
            "territory",
            "governorate",
            "market_segment",
            "industry",
            "tax_id",
            "lead_name",
            "customer_primary_address",
            "primary_address",
            "customer_primary_contact",
            "mobile2",
            "email_id",
            "default_currency",
            "default_price_list",
            "default_sales_partner",
            "payment_terms",
            "longitude",
            "latitude",
            "docstatus",
        ],
    )
    for x in doc_data:
        cust["name"] = x.name
        if x.sales_team:
            cust["sales_person"] = x.sales_team[0].sales_person
        cust["customer_name"] = x.customer_name
        cust["lead_name"] = x.lead_name
        cust["disabled"] = x.disabled
        cust["customer_type"] = x.customer_type
        cust["customer_group"] = x.customer_group
        cust["territory"] = x.territory
        cust["market_segment"] = x.market_segment
        cust["industry"] = x.industry
        cust["tax_id"] = x.tax_id
        cust["governorate"] = x.governorate
        cust["mobile2"] = x.mobile2
        cust["customer_primary_address"] = x.customer_primary_address
        cust["address_line1"] = frappe.db.get_value(
            "Address", x.customer_primary_address, "address_line1"
        )
        cust["city"] = frappe.db.get_value(
            "Address", x.customer_primary_address, "city"
        )
        cust["country"] = frappe.db.get_value(
            "Address", x.customer_primary_address, "country"
        )
        cust["customer_primary_contact"] = x.customer_primary_contact
        cust["contact_display"] = frappe.db.get_value(
            "Contact", x.customer_primary_contact, "first_name"
        )
        cust["mobile_no"] = frappe.db.get_value(
            "Contact", x.customer_primary_contact, "mobile_no"
        )
        cust["phone"] = frappe.db.get_value(
            "Contact", x.customer_primary_contact, "phone"
        )
        cust["email_id"] = frappe.db.get_value(
            "Contact", x.customer_primary_contact, "email_id"
        )
        cust["primary_address"] = x.primary_address
        cust["default_currency"] = x.default_currency
        cust["default_price_list"] = x.default_price_list
        cust["default_sales_partner"] = x.default_sales_partner
        cust["payment_terms"] = x.payment_terms
        cust["longitude"] = x.longitude
        cust["latitude"] = x.latitude
        cust["docstatus"] = x.docstatus
        if x.payment_terms:
            cust["credit_days"] = frappe.db.get_value(
                "Payment Terms Template Detail",
                {"parent": x.payment_terms},
                "credit_days",
            )
        else:
            cust["credit_days"] = 0

    child_data = frappe.db.get_all(
        "Customer Credit Limit",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "company",
            "credit_limit",
            "bypass_credit_limit_check",
        ],
    )
    sales_team = frappe.db.get_all(
        "Sales Team",
        filters={"parent": name},
        fields=[
            "sales_person",
            "allocated_percentage",
            "allocated_amount",
            "commission_rate",
            "incentives"
        ])
    if sales_team:
        cust["sales_person"] = sales_team[0]["sales_person"]
    if child_data and doc_data:
        cust["credit_limits"] = child_data

    attachments = frappe.db.sql(
        """ Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                        from `tabFile`  where `tabFile`.attached_to_doctype = "Customer"
                                        and `tabFile`.attached_to_name = "{name}"
                                        order by `tabFile`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )

    cust["attachments"] = attachments

    comments = frappe.db.sql(
        """ Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Customer"
                                        and `tabComment`.reference_name = "{name}"
                                        and `tabComment`.comment_type = "Comment"
                                        order by `tabComment`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )

    cust["comments"] = comments

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Customer" and disabled = 0 """,
        as_dict=1,
    )
    cust["print_formats"] = print_formats
    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)

    quotation_count = frappe.db.count("Quotation", filters={"party_name": name})
    opportunity_count = frappe.db.count("Opportunity", filters={"party_name": name})
    sales_order_count = frappe.db.count("Sales Order", filters={"customer": name})
    delivery_note_count = frappe.db.count("Delivery Note", filters={"customer": name})
    sales_invoice_count = frappe.db.count("Sales Invoice", filters={"customer": name})
    payment_entry_count = frappe.db.count("Payment Entry", filters={"party": name})
    # quotation_name = frappe.db.get_all('Quotation', filters={'party_name': name}, fields=['name'])
    # opportunity_name = frappe.db.get_all('Opportunity', filters={'party_name': name}, fields=['name'])
    # sales_order_name = frappe.db.get_all('Sales Order', filters={'customer': name}, fields=['name'])
    # delivery_note_name = frappe.db.get_all('Delivery Note', filters={'customer': name}, fields=['name'])
    # sales_invoice_name = frappe.db.get_all('Sales Invoice', filters={'customer': name}, fields=['name'])
    # payment_entry_name = frappe.db.get_all('Payment Entry', filters={'party': name}, fields=['name'])

    qtn_connections = {}
    opp_connections = {}
    so_connections = {}
    dn_connections = {}
    sinv_connections = {}
    pe_connections = {}
    connections = []

    if quotation_count > 0 and doc_data:
        qtn_connections["name"] = "Quotation"
        qtn_connections["count"] = quotation_count
        qtn_connections["icon"] = "https://erpcloud.systems/files/quotation.png"
        connections.append(qtn_connections)

    if opportunity_count > 0 and doc_data:
        opp_connections["name"] = "Opportunity"
        opp_connections["count"] = opportunity_count
        opp_connections["icon"] = "https://erpcloud.systems/files/opportunity.png"
        connections.append(opp_connections)

    if sales_order_count > 0 and doc_data:
        so_connections["name"] = "Sales Order"
        so_connections["count"] = sales_order_count
        so_connections["icon"] = "https://erpcloud.systems/files/sales_order.png"
        connections.append(so_connections)

    if delivery_note_count > 0 and doc_data:
        dn_connections["name"] = "Delivery Note"
        dn_connections["count"] = delivery_note_count
        dn_connections["icon"] = "https://erpcloud.systems/files/delivery_note.png"
        connections.append(dn_connections)

    if sales_invoice_count > 0 and doc_data:
        sinv_connections["name"] = "Sales Invoice"
        sinv_connections["count"] = sales_invoice_count
        sinv_connections["icon"] = "https://erpcloud.systems/files/sales_invoice.png"
        connections.append(sinv_connections)

    if payment_entry_count > 0 and doc_data:
        pe_connections["name"] = "Payment Entry"
        pe_connections["count"] = payment_entry_count
        pe_connections["icon"] = "https://erpcloud.systems/files/payment_entry.png"
        connections.append(pe_connections)

    cust["conn"] = connections

    if doc_data:
        return cust
    else:
        return "لا يوجد عميل بهذا الاسم"


@frappe.whitelist()
def customer_visit(name):
    response = {}

    doc_data = frappe.db.get_all(
        "Customer Visit",
        filters={"name": name},
        fields=[
            "name",
            "docstatus",
            "customer",
            "customer_address",
            "posting_date",
            "time",
            "description",
            "longitude",
            "latitude",
            "location",
            "docstatus",
        ],
    )
    amended_to = frappe.db.get_value("Customer Visit", {"amended_from": name}, ["name"])
    if not doc_data:
        return "لا يوجد"
    address_line1, city, country = frappe.db.get_value(
        "Address",
        {"name": doc_data[0].customer_address},
        ["address_line1", "city", "country"],
    )
    response["name"] = doc_data[0].name
    response["amended_to"] = amended_to
    response["customer"] = doc_data[0].customer
    response["customer_address"] = doc_data[0].customer_address
    response["address_line1"] = address_line1
    response["city"] = city
    response["country"] = country
    response["posting_date"] = doc_data[0].posting_date
    response["time"] = doc_data[0].time
    response["description"] = doc_data[0].description
    response["longitude"] = doc_data[0].longitude
    response["latitude"] = doc_data[0].latitude
    response["location"] = doc_data[0].location
    response["docstatus"] = doc_data[0].docstatus

    attachments = frappe.db.sql(
        """ Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                        from `tabFile`  where `tabFile`.attached_to_doctype = "Customer Visit"
                                        and `tabFile`.attached_to_name = "{name}"
                                        order by `tabFile`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )

    response["attachments"] = attachments

    comments = frappe.db.sql(
        """ Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Customer Visit"
                                        and `tabComment`.reference_name = "{name}"
                                        and `tabComment`.comment_type = "Comment"
                                        order by `tabComment`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )

    response["comments"] = comments

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Customer Visit" and disabled = 0 """,
        as_dict=1,
    )
    response["print_formats"] = print_formats
    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)

    if doc_data:
        return response
    else:
        return "لا يوجد عميل بهذا الاسم"


@frappe.whitelist()
def sales_order(name):
    so = {}
    doc_data = frappe.db.get_all(
        "Sales Order",
        filters={"name": name},
        fields=[
            "name",
            "total_free_items",
            "select",
            "customer",
            "customer_name",
            "transaction_date",
            "delivery_date",
            "status",
            "tax_id",
            "customer_group",
            "territory",
            "customer_address",
            "address_display",
            "contact_person",
            "contact_display",
            "contact_mobile",
            "contact_email",
            "project",
            "order_type",
            "currency",
            "conversion_rate",
            "selling_price_list",
            "price_list_currency",
            "plc_conversion_rate",
            "ignore_pricing_rule",
            "set_warehouse",
            "campaign",
            "source",
            "tc_name",
            "terms",
            "taxes_and_charges",
            "payment_terms_template",
            "sales_partner",
            "commission_rate",
            "total_commission",
            "total_qty",
            "base_total",
            "base_net_total",
            "total",
            "net_total",
            "base_total_taxes_and_charges",
            "total_taxes_and_charges",
            "apply_discount_on",
            "base_discount_amount",
            "additional_discount_percentage",
            "discount_amount",
            "base_grand_total",
            "base_in_words",
            "grand_total",
            "in_words",
            "docstatus",
        ],
    )
    amended_to = frappe.db.get_value("Sales Order", {"amended_from": name}, ["name"])
    for x in doc_data:
        so["name"] = x.name
        so["amended_to"] = amended_to
        so["select"] = x.select
        so["customer"] = x.customer
        so["customer_name"] = x.customer_name
        so["transaction_date"] = x.transaction_date
        so["delivery_date"] = x.delivery_date
        so["status"] = x.status
        so["tax_id"] = x.order_type
        so["customer_group"] = x.customer_group
        so["territory"] = x.territory
        ####START OF ADDRESS & CONTACT####
        so["customer_address"] = x.customer_address
        so["address_line1"] = frappe.db.get_value(
            "Address", x.customer_address, "address_line1"
        )
        so["city"] = frappe.db.get_value("Address", x.customer_address, "city")
        so["country"] = frappe.db.get_value("Address", x.customer_address, "country")
        so["contact_person"] = x.contact_person
        so["contact_display"] = frappe.db.get_value(
            "Contact", x.contact_person, "first_name"
        )
        so["mobile_no"] = frappe.db.get_value("Contact", x.contact_person, "mobile_no")
        so["phone"] = frappe.db.get_value("Contact", x.contact_persont, "phone")
        so["email_id"] = frappe.db.get_value("Contact", x.contact_person, "email_id")
        ####END OF ADDRESS & CONTACT####

        so["address_display"] = x.address_display
        # so["contact_display"] = x.contact_display
        so["contact_mobile"] = x.contact_mobile
        so["contact_email"] = x.contact_email
        so["project"] = x.project
        so["order_type"] = x.order_type
        so["currency"] = x.currency
        so["conversion_rate"] = x.conversion_rate
        so["selling_price_list"] = x.selling_price_list
        so["price_list_currency"] = x.price_list_currency
        so["plc_conversion_rate"] = x.plc_conversion_rate
        so["set_warehouse"] = x.set_warehouse
        so["campaign"] = x.campaign
        so["source"] = x.source
        so["tc_name"] = x.tc_name
        so["terms"] = x.terms
        so["taxes_and_charges"] = x.taxes_and_charges
        so["payment_terms_template"] = x.payment_terms_template
        so["sales_partner"] = x.sales_partner
        so["commission_rate"] = x.commission_rate
        so["total_commission"] = x.total_commission
        so["total_qty"] = x.total_qty
        so["base_total"] = x.base_total
        so["base_net_total"] = x.base_net_total
        so["total"] = x.total
        so["net_total"] = x.net_total
        so["base_total_taxes_and_charges"] = x.base_total_taxes_and_charges
        so["total_taxes_and_charges"] = x.total_taxes_and_charges
        so["apply_discount_on"] = x.apply_discount_on
        so["base_discount_amount"] = x.base_discount_amount
        so["additional_discount_percentage"] = x.additional_discount_percentage
        so["discount_amount"] = x.discount_amount
        so["base_grand_total"] = x.base_grand_total
        so["base_in_words"] = x.base_in_words
        so["grand_total"] = x.grand_total
        so["total_free_items"] = x.total_free_items
        so["in_words"] = x.in_words
        so["docstatus"] = x.docstatus

    sales_teams = frappe.db.get_all(
        "Sales Team",
        filters={"parent": name},
        fields=[
            "sales_person",
            "allocated_percentage",
            "allocated_amount",
            "commission_rate",
            "incentives"
        ])

    child_data_1 = frappe.db.get_all(
        "Sales Order Item",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "delivery_date",
            "item_code",
            "item_name",
            "description",
            "item_group",
            "brand",
            "image",
            "qty",
            "stock_uom",
            "uom",
            "conversion_factor",
            "stock_qty",
            "price_list_rate",
            "base_price_list_rate",
            "margin_type",
            "margin_rate_or_amount",
            "rate_with_margin",
            "discount_percentage",
            "discount_amount",
            "base_rate_with_margin",
            "rate",
            "net_rate",
            "amount",
            "item_tax_template",
            "net_amount",
            "base_rate",
            "base_net_rate",
            "base_amount",
            "base_net_amount",
            "billed_amt",
            "valuation_rate",
            "gross_profit",
            "warehouse",
            "prevdoc_docname",
            "projected_qty",
            "actual_qty",
            "ordered_qty",
            "planned_qty",
            "work_order_qty",
            "delivered_qty",
            "produced_qty",
            "returned_qty",
            "additional_notes",
        ],
    )

    child_data_2 = frappe.db.get_all(
        "Sales Taxes and Charges",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "charge_type",
            "row_id",
            "account_head",
            "description",
            "cost_center",
            "rate",
            "account_currency",
            "tax_amount",
            "total",
            "tax_amount_after_discount_amount",
            "base_tax_amount",
            "base_total",
            "base_tax_amount_after_discount_amount",
        ],
    )

    child_data_3 = frappe.db.get_all(
        "Payment Schedule",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "payment_term",
            "description",
            "due_date",
            "mode_of_payment",
            "invoice_portion",
            "discount_type",
            "discount_date",
            "discount",
            "payment_amount",
            "outstanding",
            "paid_amount",
            "discounted_amount",
            "base_payment_amount",
        ],
    )
    child_data_4 = frappe.db.get_all(
        "Free Items",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "name",
            "item_code",
            "item_name",
            "item_group",
            "stock_uom",
            "qty",
            "uom",
            "price_list_rate",
            "rate",
            "amount",
        ],
    )
    if sales_teams and doc_data:
        so["sales_team"] = sales_teams

    if child_data_1 and doc_data:
        so["items"] = child_data_1

    if child_data_4 and doc_data:
        so["free_items"] = child_data_4

    if child_data_2 and doc_data:
        so["taxes"] = child_data_2

    if child_data_3 and doc_data:
        so["payment_schedule"] = child_data_3

    attachments = frappe.db.sql(
        """ Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                        from `tabFile`  where `tabFile`.attached_to_doctype = "Sales Order"
                                        and `tabFile`.attached_to_name = "{name}"
                                        order by `tabFile`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )

    so["attachments"] = attachments

    comments = frappe.db.sql(
        """ Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Sales Order"
                                        and `tabComment`.reference_name = "{name}"
                                        and `tabComment`.comment_type = "Comment"
                                        order by `tabComment`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )

    so["comments"] = comments

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Sales Order" and disabled = 0 """,
        as_dict=1,
    )
    so["print_formats"] = print_formats
    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)

    sales_invoice = frappe.db.get_all(
        "Sales Invoice Item",
        filters={"sales_order": name},
        fields=["parent"],
        group_by="parent",
    )
    delivery_note = frappe.db.get_all(
        "Delivery Note Item",
        filters={"against_sales_order": name},
        fields=["parent"],
        group_by="parent",
    )
    material_request = frappe.db.get_all(
        "Material Request Item",
        filters={"sales_order": name},
        fields=["parent"],
        group_by="parent",
    )
    purchase_order = frappe.db.get_all(
        "Purchase Order Item",
        filters={"sales_order": name},
        fields=["parent"],
        group_by="parent",
    )
    quotation = frappe.db.get_all(
        "Sales Order Item",
        filters={"parent": name, "prevdoc_docname": ["!=", ""]},
        fields=["prevdoc_docname"],
        group_by="prevdoc_docname",
    )
    payment_entry = frappe.db.get_all(
        "Payment Entry Reference",
        filters={"reference_name": name},
        fields=["parent"],
        group_by="parent",
    )
    sales_invoice_count = len(sales_invoice)
    delivery_note_count = len(delivery_note)
    material_request_count = len(material_request)
    purchase_order_count = len(purchase_order)
    quotation_count = len(quotation)
    payment_entry_count = len(payment_entry)

    sinv_connections = {}
    dn_connections = {}
    mr_connections = {}
    po_connections = {}
    qtn_connections = {}
    pe_connections = {}
    connections = []

    if sales_invoice_count > 0 and doc_data:
        sinv_connections["name"] = "Sales Invoice"
        sinv_connections["count"] = sales_invoice_count
        sinv_connections["icon"] = "https://erpcloud.systems/files/sales_invoice.png"
        connections.append(sinv_connections)

    if delivery_note_count > 0 and doc_data:
        dn_connections["name"] = "Delivery Note"
        dn_connections["count"] = delivery_note_count
        dn_connections["icon"] = "https://erpcloud.systems/files/delivery_note.png"
        connections.append(dn_connections)

    if material_request_count > 0 and doc_data:
        mr_connections["name"] = "Material Request"
        mr_connections["count"] = material_request_count
        mr_connections["icon"] = "https://erpcloud.systems/files/material_request.png"
        connections.append(mr_connections)

    if purchase_order_count > 0 and doc_data:
        po_connections["name"] = "Purchase Order"
        po_connections["count"] = purchase_order_count
        po_connections["icon"] = "https://erpcloud.systems/files/purchase_order.png"
        connections.append(po_connections)

    if quotation_count > 0 and doc_data:
        qtn_connections["name"] = "Quotation"
        qtn_connections["count"] = quotation_count
        qtn_connections["qtn_no"] = quotation
        qtn_connections["icon"] = "https://erpcloud.systems/files/quotation.png"
        connections.append(qtn_connections)

    if payment_entry_count > 0 and doc_data:
        pe_connections["name"] = "Payment Entry"
        pe_connections["count"] = payment_entry_count
        pe_connections["icon"] = "https://erpcloud.systems/files/payment_entry.png"
        connections.append(pe_connections)

    so["conn"] = connections

    if doc_data:
        return so
    else:
        return "لا يوجد أمر بيع بهذا الاسم"


@frappe.whitelist()
def sales_invoice(name):
    doc_data = frappe.db.get_all(
        "Sales Invoice",
        filters={"name": name},
        fields=[
            "name",
            "select",
            "customer",
            "sales_team.sales_person",
            "customer_name",
            "posting_date",
            "due_date",
            "status",
            "is_return",
            "tax_id",
            "customer_group",
            "territory",
            "customer_address",
            "address_display",
            "contact_person",
            "contact_display",
            "contact_mobile",
            "contact_email",
            "project",
            "cost_center",
            "currency",
            "conversion_rate",
            "selling_price_list",
            "price_list_currency",
            "plc_conversion_rate",
            "ignore_pricing_rule",
            "set_warehouse",
            "set_target_warehouse",
            "update_stock",
            "campaign",
            "source",
            "tc_name",
            "terms",
            "taxes_and_charges",
            "payment_terms_template",
            "sales_partner",
            "commission_rate",
            "total_commission",
            "total_qty",
            "base_total",
            "base_net_total",
            "total",
            "net_total",
            "base_total_taxes_and_charges",
            "total_taxes_and_charges",
            "apply_discount_on",
            "base_discount_amount",
            "additional_discount_percentage",
            "discount_amount",
            "base_grand_total",
            "base_in_words",
            "grand_total",
            "in_words",
            "longitude",
            "latitude",
            "docstatus",
            "select",
            "total_free_items",
            "bouns_amount",
            "remaining_bonus_amount",
        ],
    )

    if not doc_data:
        return "لا يوجد فاتورة مبيعات بهذا الاسم"

    sinv = {}

    if doc_data:
        customer_code = frappe.db.get_value("Customer", {"name": doc_data[0]["customer"]}, ["code"])

    amended_to = frappe.db.get_value("Sales Invoice", {"amended_from": name}, ["name"])
    for x in doc_data:
        sinv["name"] = x.name
        sinv["amended_to"] = amended_to
        sinv["select"] = x.select
        sinv["customer"] = x.customer
        sinv["customer_name"] = x.customer_name
        sinv["customer_code"] = customer_code
        sinv["posting_date"] = x.posting_date
        sinv["discount_type"] = x.select
        sinv["total_free_items"] = x.total_free_items
        sinv["due_date"] = x.due_date
        sinv["status"] = x.status
        sinv["is_return"] = x.is_return
        sinv["tax_id"] = x.order_type
        sinv["customer_group"] = x.customer_group
        sinv["territory"] = x.territory

        ####START OF ADDRESS & CONTACT####
        sinv["customer_address"] = x.customer_address
        sinv["address_line1"] = frappe.db.get_value(
            "Address", x.customer_address, "address_line1"
        )
        sinv["city"] = frappe.db.get_value("Address", x.customer_address, "city")
        sinv["country"] = frappe.db.get_value("Address", x.customer_address, "country")
        sinv["contact_person"] = x.contact_person
        sinv["contact_display"] = frappe.db.get_value(
            "Contact", x.contact_person, "first_name"
        )
        sinv["mobile_no"] = frappe.db.get_value(
            "Contact", x.contact_person, "mobile_no"
        )
        sinv["phone"] = frappe.db.get_value("Contact", x.contact_persont, "phone")
        sinv["email_id"] = frappe.db.get_value("Contact", x.contact_person, "email_id")
        ####END OF ADDRESS & CONTACT####

        sinv["address_display"] = x.address_display
        # sinv["contact_display"] = x.contact_display
        sinv["contact_mobile"] = x.contact_mobile
        sinv["contact_email"] = x.contact_email
        sinv["project"] = x.project
        sinv["cost_center"] = x.cost_center
        sinv["currency"] = x.currency
        sinv["conversion_rate"] = x.conversion_rate
        sinv["selling_price_list"] = x.selling_price_list
        sinv["price_list_currency"] = x.price_list_currency
        sinv["plc_conversion_rate"] = x.plc_conversion_rate
        sinv["update_stock"] = x.update_stock
        sinv["set_warehouse"] = x.set_warehouse
        sinv["set_target_warehouse"] = x.set_target_warehouse
        sinv["tc_name"] = x.tc_name
        sinv["terms"] = x.terms
        sinv["taxes_and_charges"] = x.taxes_and_charges
        sinv["payment_terms_template"] = x.payment_terms_template
        sinv["sales_partner"] = x.sales_partner
        sinv["commission_rate"] = x.commission_rate
        sinv["total_commission"] = x.total_commission
        sinv["total_qty"] = x.total_qty
        sinv["base_total"] = x.base_total
        sinv["base_net_total"] = x.base_net_total
        sinv["total"] = x.total
        sinv["net_total"] = x.net_total
        sinv["base_total_taxes_and_charges"] = x.base_total_taxes_and_charges
        sinv["total_taxes_and_charges"] = x.total_taxes_and_charges
        sinv["apply_discount_on"] = x.apply_discount_on
        sinv["base_discount_amount"] = x.base_discount_amount
        sinv["additional_discount_percentage"] = x.additional_discount_percentage
        sinv["discount_amount"] = x.discount_amount
        sinv["base_grand_total"] = x.base_grand_total
        sinv["base_in_words"] = x.base_in_words
        sinv["grand_total"] = x.grand_total
        sinv["in_words"] = x.in_words
        sinv["longitude"] = x.longitude
        sinv["latitude"] = x.latitude
        sinv["docstatus"] = x.docstatus

        sinv["bouns_amount"] = x.bouns_amount
        sinv["remaining_bonus_amount"] = x.remaining_bonus_amount

    sales_teams = frappe.db.get_all(
        "Sales Team",
        filters={"parent": name},
        fields=[
            "sales_person",
            "allocated_percentage",
            "allocated_amount",
            "commission_rate",
            "incentives"
        ])

    child_data_1 = frappe.db.get_all(
        "Sales Invoice Item",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "item_code",
            "item_name",
            "description",
            "item_group",
            "brand",
            "image",
            "qty",
            "stock_uom",
            "uom",
            "conversion_factor",
            "stock_qty",
            "price_list_rate",
            "base_price_list_rate",
            "margin_type",
            "margin_rate_or_amount",
            "rate_with_margin",
            "discount_percentage",
            "discount_amount",
            "base_rate_with_margin",
            "rate",
            "net_rate",
            "amount",
            "item_tax_template",
            "net_amount",
            "base_rate",
            "base_net_rate",
            "base_amount",
            "base_net_amount",
            "warehouse",
            "actual_qty",
            "delivered_qty",
        ],
    )

    child_data_2 = frappe.db.get_all(
        "Sales Taxes and Charges",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "charge_type",
            "row_id",
            "account_head",
            "description",
            "cost_center",
            "rate",
            "account_currency",
            "tax_amount",
            "total",
            "tax_amount_after_discount_amount",
            "base_tax_amount",
            "base_total",
            "base_tax_amount_after_discount_amount",
        ],
    )

    child_data_3 = frappe.db.get_all(
        "Payment Schedule",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "payment_term",
            "description",
            "due_date",
            "mode_of_payment",
            "invoice_portion",
            "discount_type",
            "discount_date",
            "discount",
            "payment_amount",
            "outstanding",
            "paid_amount",
            "discounted_amount",
            "base_payment_amount",
        ],
    )
    child_data_4 = frappe.db.get_all(
        "Free Items",
        filters={"parent": name},
        fields=[
            "idx",
            "name",
            "item_code",
            "item_name",
            "description",
            "item_group",
            "brand",
            "image",
            "qty",
            "stock_uom",
            "uom",
            "conversion_factor",
            "stock_qty",
            "price_list_rate",
            "base_price_list_rate",
            "margin_type",
            "margin_rate_or_amount",
            "rate_with_margin",
            "discount_percentage",
            "discount_amount",
            "base_rate_with_margin",
            "rate",
            "net_rate",
            "amount",
            "item_tax_template",
            "net_amount",
            "base_rate",
            "base_net_rate",
            "base_amount",
            "base_net_amount",
            "warehouse",
            "actual_qty",
            "delivered_qty"

        ],
    )

    if child_data_1 and doc_data:
        sinv["items"] = child_data_1

    if child_data_2 and doc_data:
        sinv["taxes"] = child_data_2

    if child_data_3 and doc_data:
        sinv["payment_schedule"] = child_data_3

    if child_data_4 and doc_data:
        sinv["free_items"] = child_data_4

    if sales_teams and doc_data:
        sinv["sales_team"] = sales_teams

    attachments = frappe.db.sql(
        """ Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                        from `tabFile`  where `tabFile`.attached_to_doctype = "Sales Invoice"
                                        and `tabFile`.attached_to_name = "{name}"
                                        order by `tabFile`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )

    sinv["attachments"] = attachments

    comments = frappe.db.sql(
        """ Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Sales Invoice"
                                        and `tabComment`.reference_name = "{name}"
                                        and `tabComment`.comment_type = "Comment"
                                        order by `tabComment`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )

    sinv["comments"] = comments

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Sales Invoice" and disabled = 0 """,
        as_dict=1,
    )
    sinv["print_formats"] = print_formats
    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)

    sales_order = frappe.db.get_all(
        "Sales Invoice Item",
        filters={
            "sales_order": ["!=", ""],
            "parent": name,
        },
        group_by="sales_order",
    )
    delivery_note = frappe.db.get_all(
        "Delivery Note Item",
        filters={"against_sales_invoice": name},
        fields=["parent"],
        group_by="parent",
    )
    payment_entry = frappe.db.get_all(
        "Payment Entry Reference",
        filters={"reference_name": name},
        fields=["parent"],
        group_by="parent",
    )
    sales_order_count = len(sales_order)
    delivery_note_count = len(delivery_note)
    payment_entry_count = len(payment_entry)

    so_connections = {}
    dn_connections = {}
    pe_connections = {}
    connections = []

    if sales_order_count > 0 and doc_data:
        so_connections["name"] = "Sales Order"
        so_connections["count"] = sales_order_count
        so_connections["icon"] = "https://erpcloud.systems/files/sales_order.png"
        connections.append(so_connections)

    if delivery_note_count > 0 and doc_data:
        dn_connections["name"] = "Delivery Note"
        dn_connections["count"] = delivery_note_count
        dn_connections["icon"] = "https://erpcloud.systems/files/delivery_note.png"
        connections.append(dn_connections)

    if payment_entry_count > 0 and doc_data:
        pe_connections["name"] = "Payment Entry"
        pe_connections["count"] = payment_entry_count
        pe_connections["icon"] = "https://erpcloud.systems/files/payment_entry.png"
        connections.append(pe_connections)

    sinv["conn"] = connections

    return sinv


@frappe.whitelist()
def payment_entry(name):
    pe = {}
    doc_data = frappe.db.get_all(
        "Payment Entry",
        filters={"name": name},
        fields=[
            "name",
            "party_type",
            "party",
            "party_name",
            "sales_person",
            "posting_date",
            "status",
            "reference_no",
            "reference_date",
            "payment_type",
            "mode_of_payment",
            "mode_of_payment_2",
            "paid_from_account_balance",
            "paid_to_account_balance",
            "paid_from_account_currency",
            "paid_from",
            "paid_to",
            "paid_amount",
            "customer_code_new",
            "docstatus",
        ],
    )
    amended_to = frappe.db.get_value("Payment Entry", {"amended_from": name}, ["name"])
    for x in doc_data:
        pe["name"] = x.name
        pe["amended_to"] = amended_to
        pe["party_type"] = x.party_type
        pe["party"] = x.party
        pe["party_name"] = x.party_name
        pe["posting_date"] = x.posting_date
        pe["status"] = x.status
        pe["reference_no"] = x.reference_no
        pe["reference_date"] = x.reference_date
        pe["payment_type"] = x.payment_type
        pe["mode_of_payment"] = x.mode_of_payment
        pe["mode_of_payment_2"] = x.mode_of_payment_2
        pe["paid_from"] = x.paid_from
        pe["paid_from_account_balance"] = x.paid_from_account_balance
        pe["paid_from_account_currency"] = x.paid_from_account_currency
        pe["paid_to"] = x.paid_to
        pe["paid_to_account_balance"] = x.paid_to_account_balance
        pe["paid_amount"] = x.paid_amount
        pe["docstatus"] = x.docstatus
        pe["customer_code"] = x.customer_code_new
        pe["sales_person"] = x.sales_person
    attachments = frappe.db.sql(
        """ Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                    from `tabFile`  where `tabFile`.attached_to_doctype = "Payment Entry"
                                    and `tabFile`.attached_to_name = "{name}"
                                    order by `tabFile`.creation
                                """.format(
            name=name
        ),
        as_dict=1,
    )

    pe["attachments"] = attachments

    comments = frappe.db.sql(
        """ Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Payment Entry"
                                        and `tabComment`.reference_name = "{name}"
                                        and `tabComment`.comment_type = "Comment"
                                        order by `tabComment`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )

    pe["comments"] = comments

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Payment Entry" and disabled = 0 """,
        as_dict=1,
    )
    pe["print_formats"] = print_formats
    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)

    if doc_data:
        return pe
    else:
        return "لا يوجد مدفوعات ومقبوضات بهذا الاسم"


@frappe.whitelist()
def journal_entry(name):
    response = {}
    doc_data = frappe.db.get_all(
        "Journal Entry",
        filters={"name": name},
        fields=[
            "name",
            "docstatus",
            "voucher_type",
            "posting_date",
            "total_debit",
            "total_credit",
            "difference",
            "multi_currency",
            "total_amount_currency",
            "total_amount",
            "total_amount_in_words",
            "remark",
            "user_remark",
            "mode_of_payment",
            "cheque_no",
            "cheque_date",
            "write_off_based_on",
            "write_off_amount",
            "pay_to_recd_from",
            "is_opening",
            "mode_of_payment",
        ],
    )
    amended_to = frappe.db.get_value("Journal Entry", {"amended_from": name}, ["name"])
    if not doc_data:
        return "لا يوجد"

    response["name"] = doc_data[0].name
    response["amended_to"] = amended_to
    response["docstatus"] = doc_data[0].docstatus
    response["voucher_type"] = doc_data[0].voucher_type
    response["posting_date"] = doc_data[0].posting_date
    response["total_debit"] = doc_data[0].total_debit
    response["total_credit"] = doc_data[0].total_credit
    response["difference"] = doc_data[0].difference
    response["multi_currency"] = doc_data[0].multi_currency
    response["total_amount_currency"] = doc_data[0].total_amount_currency
    response["total_amount"] = doc_data[0].total_amount
    response["total_amount_in_words"] = doc_data[0].total_amount_in_words
    response["remark"] = doc_data[0].remark
    response["user_remark"] = doc_data[0].user_remark
    response["mode_of_payment"] = doc_data[0].mode_of_payment
    response["cheque_no"] = doc_data[0].cheque_no
    response["cheque_date"] = doc_data[0].cheque_date

    response["write_off_based_on"] = doc_data[0].write_off_based_on
    response["write_off_amount"] = doc_data[0].write_off_amount
    response["pay_to_recd_from"] = doc_data[0].pay_to_recd_from
    response["is_opening"] = doc_data[0].is_opening
    response["paid_amount"] = doc_data[0].paid_amount
    response["status"] = doc_data[0].status

    attachments = frappe.db.sql(
        """ Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                    from `tabFile`  where `tabFile`.attached_to_doctype = "Journal Entry"
                                    and `tabFile`.attached_to_name = "{name}"
                                    order by `tabFile`.creation
                                """.format(
            name=name
        ),
        as_dict=1,
    )

    response["attachments"] = attachments

    comments = frappe.db.sql(
        """ Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Journal Entry"
                                        and `tabComment`.reference_name = "{name}"
                                        and `tabComment`.comment_type = "Comment"
                                        order by `tabComment`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )

    response["comments"] = comments
    journal_entry_account = frappe.db.get_all(
        "Journal Entry Account",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "balance",
            "idx",
            "name",
            "parenttype",
            "account",
            "account_type",
            "party_type",
            "party",
            "party_balance",
            "cost_center",
            "account_currency",
            "exchange_rate",
            "debit_in_account_currency",
            "debit",
            "credit_in_account_currency",
            "credit",
            "is_advance",
        ],
    )
    for index in range(len(journal_entry_account)):
        for key in journal_entry_account[index]:
            if key == "balance":
                journal_entry_account[index][key] = (
                        str(journal_entry_account[index]["balance"])
                        + " "
                        + str(
                    frappe.db.get_value(
                        "Account",
                        str(journal_entry_account[index]["account"]),
                        "account_currency",
                    )
                )
                )
    if journal_entry_account and doc_data:
        response["accounts"] = journal_entry_account

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Journal Entry" and disabled = 0 """,
        as_dict=1,
    )
    response["print_formats"] = print_formats
    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)

    if doc_data:
        return response
    else:
        return "لا يوجد مدفوعات ومقبوضات بهذا الاسم"


@frappe.whitelist()
def item(name):
    item_ = {}
    doc_data = frappe.db.get_all(
        "Item",
        filters={"name": name},
        fields=[
            "name",
            "item_code",
            "item_name",
            "item_group",
            "brand",
            "stock_uom",
            "description",
            "image",
            "disabled",
            "is_stock_item",
            "include_item_in_manufacturing",
            "is_fixed_asset",
            "asset_category",
            "is_purchase_item",
            "purchase_uom",
            "is_sales_item",
            "sales_uom",
            "docstatus",
        ],
    )
    for x in doc_data:
        item_["name"] = x.name
        item_["image"] = x.image
        item_["item_name"] = x.item_name
        item_["item_code"] = x.item_code
        item_["disabled"] = x.disabled
        item_["item_group"] = x.item_group
        item_["brand"] = x.brand
        item_["stock_uom"] = x.stock_uom
        item_["description"] = x.description
        item_["is_stock_item"] = x.is_stock_item
        item_["include_item_in_manufacturing"] = x.include_item_in_manufacturing
        item_["is_fixed_asset"] = x.is_fixed_asset
        item_["asset_category"] = x.asset_category
        item_["is_sales_item"] = x.is_sales_item
        item_["sales_uom"] = x.sales_uom
        item_["is_purchase_item"] = x.is_purchase_item
        item_["purchase_uom"] = x.purchase_uom
        item_["docstatus"] = x.docstatus

    child_data1 = frappe.db.get_all(
        "UOM Conversion Detail",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "uom",
            "conversion_factor",
        ],
    )

    if child_data1 and doc_data:
        item_["uoms"] = child_data1

    child_data2 = frappe.db.get_all(
        "Item Price",
        filters={"item_code": name, "selling": 1},
        order_by="price_list",
        fields=[
            "price_list",
            "price_list_rate",
            "currency",
        ],
    )

    if child_data2 and doc_data:
        item_["selling_price_lists_rate"] = child_data2

    balances = frappe.db.sql(
        """ select
                                    tabBin.warehouse as warehouse,
                                    (select warehouse_type from tabWarehouse where tabWarehouse.name = tabBin.warehouse ) as warehouse_type,
                                    tabBin.actual_qty as actual_qty,
                                    tabBin.reserved_qty as reserved_qty,
                                    tabBin.ordered_qty as ordered_qty,
                                    tabBin.indented_qty as indented_qty,
                                    tabBin.projected_qty as projected_qty
                                from
                                    tabBin
                                    inner join tabItem on tabBin.item_code = tabItem.item_code
                                where
                                    tabBin.item_code = '{name}'
                                    and tabItem.has_variants = 0
                                    and tabBin.actual_qty >0
                            """.format(
            name=name
        ),
        as_dict=1,
    )

    result = []
    for item_dict in balances:
        data = {
            "warehouse": item_dict.warehouse,
            "warehouse_type": item_dict.warehouse_type,
            "actual_qty": item_dict.actual_qty,
            "reserved_qty": item_dict.reserved_qty,
            "ordered_qty": item_dict.ordered_qty,
            "indented_qty": item_dict.indented_qty,
            "projected_qty": item_dict.projected_qty,
        }
        result.append(data)

    if result and doc_data:
        item_["stock_balances"] = result

    attachments = frappe.db.sql(
        """ Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                        from `tabFile`  where `tabFile`.attached_to_doctype = "Item"
                                        and `tabFile`.attached_to_name = "{name}"
                                        order by `tabFile`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )

    item_["attachments"] = attachments

    comments = frappe.db.sql(
        """ Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Item"
                                        and `tabComment`.reference_name = "{name}"
                                        and `tabComment`.comment_type = "Comment"
                                        order by `tabComment`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )

    item_["comments"] = comments

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Item" and disabled = 0 """,
        as_dict=1,
    )
    item_["print_formats"] = print_formats
    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)

    quotation = frappe.db.get_all(
        "Quotation Item",
        filters={"item_code": name},
        fields=["item_code"],
        group_by="parent",
    )
    sales_order = frappe.db.get_all(
        "Sales Order Item",
        filters={"item_code": name},
        fields=["item_code"],
        group_by="parent",
    )
    delivery_note = frappe.db.get_all(
        "Delivery Note Item",
        filters={"item_code": name},
        fields=["item_code"],
        group_by="parent",
    )
    sales_invoice = frappe.db.get_all(
        "Sales Invoice Item",
        filters={"item_code": name},
        fields=["item_code"],
        group_by="parent",
    )
    material_request = frappe.db.get_all(
        "Material Request Item",
        filters={"item_code": name},
        fields=["item_code"],
        group_by="parent",
    )
    supplier_quotation = frappe.db.get_all(
        "Supplier Quotation Item",
        filters={"item_code": name},
        fields=["item_code"],
        group_by="parent",
    )
    purchase_order = frappe.db.get_all(
        "Purchase Order Item",
        filters={"item_code": name},
        fields=["item_code"],
        group_by="parent",
    )
    purchase_receipt = frappe.db.get_all(
        "Purchase Receipt Item",
        filters={"item_code": name},
        fields=["item_code"],
        group_by="parent",
    )
    purchase_invoice = frappe.db.get_all(
        "Purchase Invoice Item",
        filters={"item_code": name},
        fields=["item_code"],
        group_by="parent",
    )
    stock_entry = frappe.db.get_all(
        "Stock Entry Detail",
        filters={"item_code": name},
        fields=["item_code"],
        group_by="parent",
    )

    quotation_count = len(quotation)
    sales_order_count = len(sales_order)
    delivery_note_count = len(delivery_note)
    sales_invoice_count = len(sales_invoice)
    material_request_count = len(material_request)
    supplier_quotation_count = len(supplier_quotation)
    purchase_order_count = len(purchase_order)
    purchase_receipt_count = len(purchase_receipt)
    purchase_invoice_count = len(purchase_invoice)
    stock_entry_count = len(stock_entry)

    qtn_connections = {}
    so_connections = {}
    dn_connections = {}
    sinv_connections = {}
    mr_connections = {}
    sup_qtn_connections = {}
    po_connections = {}
    pr_connections = {}
    pinv_connections = {}
    se_connections = {}
    connections = []

    if quotation_count > 0 and doc_data:
        qtn_connections["name"] = "Quotation"
        qtn_connections["count"] = quotation_count
        qtn_connections["icon"] = "https://erpcloud.systems/files/quotation.png"
        connections.append(qtn_connections)

    if sales_order_count > 0 and doc_data:
        so_connections["name"] = "Sales Order"
        so_connections["count"] = sales_order_count
        so_connections["icon"] = "https://erpcloud.systems/files/sales_order.png"
        connections.append(so_connections)

    if delivery_note_count > 0 and doc_data:
        dn_connections["name"] = "Delivery Note"
        dn_connections["count"] = delivery_note_count
        dn_connections["icon"] = "https://erpcloud.systems/files/delivery_note.png"
        connections.append(dn_connections)

    if sales_invoice_count > 0 and doc_data:
        sinv_connections["name"] = "Sales Invoice"
        sinv_connections["count"] = sales_invoice_count
        sinv_connections["icon"] = "https://erpcloud.systems/files/sales_invoice.png"
        connections.append(sinv_connections)

    if material_request_count > 0 and doc_data:
        mr_connections["name"] = "Material Request"
        mr_connections["count"] = material_request_count
        mr_connections["icon"] = "https://erpcloud.systems/files/material_request.png"
        connections.append(mr_connections)

    if supplier_quotation_count > 0 and doc_data:
        sup_qtn_connections["name"] = "Supplier Quotation"
        sup_qtn_connections["count"] = supplier_quotation_count
        sup_qtn_connections[
            "icon"
        ] = "https://erpcloud.systems/files/supplier_quotation.png"
        connections.append(sup_qtn_connections)

    if purchase_order_count > 0 and doc_data:
        po_connections["name"] = "Purchase Order"
        po_connections["count"] = purchase_order_count
        po_connections["icon"] = "https://erpcloud.systems/files/purchase_order.png"
        connections.append(po_connections)

    if purchase_receipt_count > 0 and doc_data:
        pr_connections["name"] = "Purchase Receipt"
        pr_connections["count"] = purchase_receipt_count
        pr_connections["icon"] = "https://erpcloud.systems/files/purchase_receipt.png"
        connections.append(pr_connections)

    if purchase_invoice_count > 0 and doc_data:
        pinv_connections["name"] = "Purchase Invoice"
        pinv_connections["count"] = purchase_invoice_count
        pinv_connections["icon"] = "https://erpcloud.systems/files/purchase_invoice.png"
        connections.append(pinv_connections)

    if stock_entry_count > 0 and doc_data:
        se_connections["name"] = "Stock Entry"
        se_connections["count"] = stock_entry_count
        se_connections["icon"] = "https://erpcloud.systems/files/stock_entry.png"
        connections.append(se_connections)

    item_["conn"] = connections

    if doc_data:
        return item_
    else:
        return "لا يوجد صنف بهذا الاسم"


@frappe.whitelist()
def stock_entry(name):
    se = {}
    doc_data = frappe.db.get_all(
        "Stock Entry",
        filters={"name": name},
        fields=[
            "name",
            "stock_entry_type",
            "purpose",
            "posting_date",
            "docstatus",
            "from_warehouse",
            "to_warehouse",
            "project",
            "docstatus",
            "customer1",
        ],
    )
    amended_to = frappe.db.get_value("Stock Entry", {"amended_from": name}, ["name"])
    for x in doc_data:
        se["name"] = x.name
        se["amended_to"] = amended_to
        se["stock_entry_type"] = x.stock_entry_type
        se["purpose"] = x.purpose
        se["posting_date"] = x.posting_date
        if x.docstatus == 0:
            se["status"] = "Draft"
        if x.docstatus == 1:
            se["status"] = "Submitted"
        if x.docstatus == 2:
            se["status"] = "Cancelled"
        se["from_warehouse"] = x.from_warehouse
        se["to_warehouse"] = x.to_warehouse
        se["project"] = x.project
        se["docstatus"] = x.docstatus
        se["customer1"] = x.customer1

    child_data = frappe.db.get_all(
        "Stock Entry Detail",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "name",
            "idx",
            "item_code",
            "item_name",
            "description",
            "item_group",
            "image",
            "qty",
            "transfer_qty",
            "stock_uom",
            "uom",
            "conversion_factor",
            "s_warehouse",
            "t_warehouse",
            "cost_center",
            "project",
            "actual_qty",
            "transferred_qty",
            "basic_rate",
        ],
    )

    if child_data and doc_data:
        se["items"] = child_data

    attachments = frappe.db.sql(
        """ Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                        from `tabFile`  where `tabFile`.attached_to_doctype = "Stock Entry"
                                        and `tabFile`.attached_to_name = "{name}"
                                        order by `tabFile`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )

    se["attachments"] = attachments

    comments = frappe.db.sql(
        """ Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Stock Entry"
                                        and `tabComment`.reference_name = "{name}"
                                        and `tabComment`.comment_type = "Comment"
                                        order by `tabComment`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )

    se["comments"] = comments

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Stock Entry" and disabled = 0 """,
        as_dict=1,
    )
    se["print_formats"] = print_formats
    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)

    if doc_data:
        return se
    else:
        return "لا يوجد حركة مخزنية بهذا الاسم"


@frappe.whitelist()
def delivery_note(name):
    dn = {}
    doc_data = frappe.db.get_all(
        "Delivery Note",
        filters={"name": name},
        fields=[
            "name",
            "customer",
            "customer_name",
            "posting_date",
            "status",
            "is_return",
            "tax_id",
            "customer_group",
            "territory",
            "customer_address",
            "address_display",
            "contact_person",
            "contact_display",
            "contact_mobile",
            "contact_email",
            "project",
            "cost_center",
            "currency",
            "conversion_rate",
            "selling_price_list",
            "price_list_currency",
            "plc_conversion_rate",
            "ignore_pricing_rule",
            "set_warehouse",
            "set_target_warehouse",
            "tc_name",
            "sales_partner",
            "commission_rate",
            "total_commission",
            "total_qty",
            "base_total",
            "base_net_total",
            "total",
            "net_total",
            "base_total_taxes_and_charges",
            "total_taxes_and_charges",
            "apply_discount_on",
            "base_discount_amount",
            "additional_discount_percentage",
            "discount_amount",
            "base_grand_total",
            "base_in_words",
            "grand_total",
            "in_words",
            "docstatus",
        ],
    )
    amended_to = frappe.db.get_value("Delivery Note", {"amended_from": name}, ["name"])
    for x in doc_data:
        dn["name"] = x.name
        dn["amended_to"] = amended_to
        dn["customer"] = x.customer
        dn["customer_name"] = x.customer_name
        dn["posting_date"] = x.posting_date
        dn["status"] = x.status
        dn["is_return"] = x.is_return
        dn["tax_id"] = x.order_type
        dn["customer_group"] = x.customer_group
        dn["territory"] = x.territory

        ####START OF ADDRESS & CONTACT####
        dn["customer_address"] = x.customer_address
        dn["address_line1"] = frappe.db.get_value(
            "Address", x.customer_address, "address_line1"
        )
        dn["city"] = frappe.db.get_value("Address", x.customer_address, "city")
        dn["country"] = frappe.db.get_value("Address", x.customer_address, "country")
        dn["contact_person"] = x.contact_person
        dn["contact_display"] = frappe.db.get_value(
            "Contact", x.contact_person, "first_name"
        )
        dn["mobile_no"] = frappe.db.get_value("Contact", x.contact_person, "mobile_no")
        dn["phone"] = frappe.db.get_value("Contact", x.contact_persont, "phone")
        dn["email_id"] = frappe.db.get_value("Contact", x.contact_person, "email_id")
        ####END OF ADDRESS & CONTACT####

        dn["address_display"] = x.address_display
        # dn["contact_display"] = x.contact_display
        dn["contact_mobile"] = x.contact_mobile
        dn["contact_email"] = x.contact_email
        dn["project"] = x.project
        dn["cost_center"] = x.cost_center
        dn["currency"] = x.currency
        dn["conversion_rate"] = x.conversion_rate
        dn["selling_price_list"] = x.selling_price_list
        dn["price_list_currency"] = x.price_list_currency
        dn["plc_conversion_rate"] = x.plc_conversion_rate
        dn["set_warehouse"] = x.set_warehouse
        dn["set_target_warehouse"] = x.set_target_warehouse
        dn["tc_name"] = x.tc_name
        dn["sales_partner"] = x.sales_partner
        dn["commission_rate"] = x.commission_rate
        dn["total_commission"] = x.total_commission
        dn["total_qty"] = x.total_qty
        dn["base_total"] = x.base_total
        dn["base_net_total"] = x.base_net_total
        dn["total"] = x.total
        dn["net_total"] = x.net_total
        dn["base_total_taxes_and_charges"] = x.base_total_taxes_and_charges
        dn["total_taxes_and_charges"] = x.total_taxes_and_charges
        dn["apply_discount_on"] = x.apply_discount_on
        dn["base_discount_amount"] = x.base_discount_amount
        dn["additional_discount_percentage"] = x.additional_discount_percentage
        dn["discount_amount"] = x.discount_amount
        dn["base_grand_total"] = x.base_grand_total
        dn["base_in_words"] = x.base_in_words
        dn["grand_total"] = x.grand_total
        dn["in_words"] = x.in_words
        dn["docstatus"] = x.docstatus

    child_data_1 = frappe.db.get_all(
        "Delivery Note Item",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "item_code",
            "item_name",
            "description",
            "item_group",
            "brand",
            "image",
            "qty",
            "stock_uom",
            "uom",
            "conversion_factor",
            "stock_qty",
            "price_list_rate",
            "base_price_list_rate",
            "margin_type",
            "margin_rate_or_amount",
            "rate_with_margin",
            "discount_percentage",
            "discount_amount",
            "base_rate_with_margin",
            "rate",
            "net_rate",
            "amount",
            "item_tax_template",
            "net_amount",
            "base_rate",
            "base_net_rate",
            "base_amount",
            "base_net_amount",
            "warehouse",
            "actual_qty",
        ],
    )

    child_data_2 = frappe.db.get_all(
        "Sales Taxes and Charges",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "charge_type",
            "row_id",
            "account_head",
            "description",
            "cost_center",
            "rate",
            "account_currency",
            "tax_amount",
            "total",
            "tax_amount_after_discount_amount",
            "base_tax_amount",
            "base_total",
            "base_tax_amount_after_discount_amount",
        ],
    )

    child_data_3 = frappe.db.get_all(
        "Payment Schedule",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "payment_term",
            "description",
            "due_date",
            "mode_of_payment",
            "invoice_portion",
            "discount_type",
            "discount_date",
            "discount",
            "payment_amount",
            "outstanding",
            "paid_amount",
            "discounted_amount",
            "base_payment_amount",
        ],
    )

    if child_data_1 and doc_data:
        dn["items"] = child_data_1

    if child_data_2 and doc_data:
        dn["taxes"] = child_data_2

    if child_data_3 and doc_data:
        dn["payment_schedule"] = child_data_3

    attachments = frappe.db.sql(
        """ Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                        from `tabFile`  where `tabFile`.attached_to_doctype = "Delivery Note"
                                        and `tabFile`.attached_to_name = "{name}"
                                        order by `tabFile`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )

    dn["attachments"] = attachments

    comments = frappe.db.sql(
        """ Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Delivery Note"
                                        and `tabComment`.reference_name = "{name}"
                                        and `tabComment`.comment_type = "Comment"
                                        order by `tabComment`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )

    dn["comments"] = comments

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Delivery Note" and disabled = 0 """,
        as_dict=1,
    )
    dn["print_formats"] = print_formats
    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)

    if doc_data:
        return dn
    else:
        return "لا يوجد إذن تسليم بهذا الاسم"


@frappe.whitelist(allow_guest=True)
def purchase_receipt(name):
    response = {}
    doc_data = frappe.db.get_all(
        "Purchase Receipt",
        filters={"name": name},
        fields=[
            "name",
            "supplier",
            "supplier_name",
            "status",
            "posting_date",
            "supplier_address",
            "address_display",
            "contact_person",
            "contact_display",
            "contact_mobile",
            "contact_email",
            "project",
            "cost_center",
            "currency",
            "conversion_rate",
            "buying_price_list",
            "price_list_currency",
            "plc_conversion_rate",
            "ignore_pricing_rule",
            "set_warehouse",
            "tc_name",
            "total_qty",
            "base_total",
            "base_net_total",
            "total",
            "net_total",
            "base_total_taxes_and_charges",
            "total_taxes_and_charges",
            "additional_discount_percentage",
            "apply_discount_on",
            "discount_amount",
            "base_discount_amount",
            "base_grand_total",
            "grand_total",
            "in_words",
            "base_in_words",
            "is_return",
            "docstatus",
        ],
    )

    amended_to = frappe.db.get_value("Purchase Receipt", {"amended_from": name}, ["name"])
    for x in doc_data:
        response["name"] = x.name
        response["amended_to"] = amended_to
        response["supplier"] = x.supplier
        response["supplier_name"] = x.supplier_name
        response["status"] = x.status
        response["posting_date"] = x.posting_date

        ####START OF ADDRESS & CONTACT####
        response["supplier_address"] = x.supplier_address
        response["address_line1"] = frappe.db.get_value(
            "Address", x.supplier_address, "address_line1"
        )
        response["city"] = frappe.db.get_value("Address", x.supplier_address, "city")
        response["country"] = frappe.db.get_value(
            "Address", x.supplier_address, "country"
        )
        response["contact_person"] = x.contact_person
        response["contact_display"] = frappe.db.get_value(
            "Contact", x.contact_person, "first_name"
        )
        response["mobile_no"] = frappe.db.get_value(
            "Contact", x.contact_person, "mobile_no"
        )
        response["phone"] = frappe.db.get_value("Contact", x.contact_persont, "phone")
        response["email_id"] = frappe.db.get_value(
            "Contact", x.contact_person, "email_id"
        )
        ####END OF ADDRESS & CONTACT####

        # response["contact_person"] = x.contact_person
        response["address_display"] = x.address_display
        # response["contact_display"] = x.contact_display
        response["contact_mobile"] = x.contact_mobile
        response["contact_email"] = x.contact_email
        response["is_return"] = x.is_return
        response["currency"] = x.currency
        response["project"] = x.project
        response["cost_center"] = x.cost_center
        response["conversion_rate"] = x.conversion_rate
        response["buying_price_list"] = x.buying_price_list
        response["price_list_currency"] = x.price_list_currency
        response["plc_conversion_rate"] = x.plc_conversion_rate
        response["ignore_pricing_rule"] = x.ignore_pricing_rule
        response["set_warehouse"] = x.set_warehouse
        response["tc_name"] = x.tc_name
        response["total_qty"] = x.total_qty
        response["base_total"] = x.base_total
        response["base_net_total"] = x.base_net_total
        response["total"] = x.total
        response["net_total"] = x.net_total
        response["base_total_taxes_and_charges"] = x.base_total_taxes_and_charges
        response["total_taxes_and_charges"] = x.total_taxes_and_charges
        response["apply_discount_on"] = x.apply_discount_on
        response["additional_discount_percentage"] = x.additional_discount_percentage
        response["discount_amount"] = x.discount_amount
        response["base_discount_amount"] = x.discount_amount
        response["in_words"] = x.in_words
        response["base_in_words"] = x.in_words
        response["docstatus"] = x.docstatus
        response["grand_total"] = x.grand_total
        response["base_grand_total"] = x.grand_total

    attachments = frappe.db.sql(
        """ Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                        from `tabFile`  where `tabFile`.attached_to_doctype = "Purchase Receipt"
                                        and `tabFile`.attached_to_name = "{name}"
                                        order by `tabFile`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )
    response["attachments"] = attachments

    comments = frappe.db.sql(
        """ Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Purchase Receipt"
                                        and `tabComment`.reference_name = "{name}"
                                        and `tabComment`.comment_type = "Comment"
                                        order by `tabComment`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )
    # dssss
    response["comments"] = comments

    purchase_receipt_item_child_table = frappe.db.get_all(
        "Purchase Receipt Item",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "item_code",
            "item_name",
            "description",
            "item_group",
            "image",
            "qty",
            "uom",
            "stock_uom",
            "conversion_factor",
            "stock_qty",
            "returned_qty",
            "base_price_list_rate",
            "price_list_rate",
            "discount_amount",
            "rate",
            "amount",
            "base_rate",
            "base_amount",
            "stock_uom_rate",
            "is_free_item",
            "net_rate",
            "net_amount",
            "base_net_rate",
            "base_net_amount",
            "valuation_rate",
            "item_tax_amount",
            "warehouse",
            "total_weight",
            "expense_account",
            "cost_center",
            "docstatus",
        ],
    )

    child_table_taxes_and_charges = frappe.db.get_all(
        "Purchase Taxes and Charges",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "add_deduct_tax",
            "charge_type",
            "row_id",
            "included_in_print_rate",
            "included_in_paid_amount",
            "account_head",
            "description",
            "rate",
            "cost_center",
            "account_currency",
            "tax_amount",
            "tax_amount_after_discount_amount",
            "total",
            "base_tax_amount",
            "base_total",
            "base_tax_amount_after_discount_amount",
            "item_wise_tax_detail",
        ],
    )

    # child_pricing_rule_detail = frappe.db.get_all(
    #     "Pricing Rule Detail",
    #     filters={"parent": name},
    #     order_by="idx",
    #     fields=[
    #         "idx",
    #         "pricing_rule",
    #         "item_code",
    #         "margin_type",
    #         "rate_or_discount",
    #         "child_docname",
    #         "rule_applied",
    #     ],
    # )

    if purchase_receipt_item_child_table and doc_data:
        response["items"] = purchase_receipt_item_child_table

    if child_table_taxes_and_charges and doc_data:
        response["taxes"] = child_table_taxes_and_charges

    # if child_pricing_rule_detail and doc_data:
    #     response["pricing_rule"] = child_pricing_rule_detail

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Purchase Receipt" and disabled = 0 """,
        as_dict=1,
    )
    response["print_formats"] = print_formats
    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)

    con_purchase_order = frappe.db.get_all(
        "Purchase Receipt Item",
        filters={"parent": name, "purchase_order": ["!=", "null%"]},
    )
    count_purchase_order = len(con_purchase_order)
    purchase_orders = {}

    con_purchase_invoice = frappe.db.get_all(
        "Purchase Invoice Item",
        filters={"purchase_receipt": name},
        fields=["parent"],
        group_by="parent",
    )
    count_purchase_invoice = len(con_purchase_invoice)
    purchase_invoices = {}

    con_purchase_receipt = frappe.db.get_all(
        "Purchase Receipt",
        filters={"amended_from": name},
        fields=["name"],
        group_by="name",
    )
    count_purchase_receipt = len(con_purchase_receipt)
    purchase_receipts = {}

    connections = []
    if count_purchase_order > 0 and doc_data:
        purchase_orders["name"] = "Purchase Order"
        purchase_orders["count"] = count_purchase_order
        purchase_orders["icon"] = "https://erpcloud.systems/files/purchase_order.png"
        connections.append(purchase_orders)

    if count_purchase_invoice > 0 and doc_data:
        purchase_invoices["name"] = "Purchase Invoice"
        purchase_invoices["count"] = count_purchase_invoice
        purchase_invoices[
            "icon"
        ] = "https://erpcloud.systems/files/purchase_invoice.png"
        connections.append(purchase_invoices)

    if count_purchase_receipt > 0 and doc_data:
        purchase_receipts["name"] = "Purchase Receipt"
        purchase_receipts["count"] = count_purchase_receipt
        purchase_receipts[
            "icon"
        ] = "https://erpcloud.systems/files/purchase_receipt.png"
        connections.append(purchase_receipts)
    response["conn"] = connections

    if doc_data:
        return response
    else:
        return "لا يوجد إذن إستلام مشتريات بهذا الاسم"


@frappe.whitelist()
def default_tax_template():
    tax = {}
    child_data = frappe.db.get_all(
        "Sales Taxes and Charges",
        filters={"parent": "Default Tax Template"},
        fields=[
            "charge_type",
            "description",
            "account_head",
        ],
    )

    if child_data:
        tax["sales_taxes_table"] = child_data
        return tax


@frappe.whitelist(allow_guest=True)
def filtered_address(name):
    addresses = frappe.db.get_all(
        "Dynamic Link", filters={"link_name": name}, fields=["parent"]
    )
    result = []
    for item_dict in frappe.db.get_all(
            "Dynamic Link", filters={"link_name": name}, fields=["parent"]
    ):
        adddd = frappe.db.get_all(
            "Address",
            filters={"name": item_dict.parent},
            fields=["name", "address_title", "address_line1", "city", "phone"],
        )
        for x in adddd:
            data = {
                "name": x.name,
                "address_title": x.address_title,
                "address_line1": x.address_line1,
                "city": x.city,
                "phone": x.phone,
            }

            result.append(data)

    if addresses:
        return result
    else:
        return "لا يوجد عنوان !"


@frappe.whitelist()
def filtered_contact(name):
    contacts = frappe.db.get_all(
        "Dynamic Link", filters={"link_name": name}, fields=["parent"]
    )
    result = []
    for item_dict in frappe.db.get_all(
            "Dynamic Link", filters={"link_name": name}, fields=["parent"]
    ):
        adddd = frappe.db.get_all(
            "Contact",
            filters={"name": item_dict.parent},
            fields=["name", "email_id", "phone", "mobile_no", "company_name"],
        )
        for x in adddd:
            data = {
                "name": x.name,
                "email_id": x.email_id,
                "phone": x.phone,
                "mobile_no": x.mobile_no,
                "company_name": x.company_name,
            }
            result.append(data)

    if contacts:
        return result
    else:
        return "لا يوجد جهة اتصال !"


@frappe.whitelist()
def supplier(name):
    supp = {}
    balance = get_balance_on(
        account=None,
        date=getdate(nowdate()),
        party_type="Supplier",
        party=name,
        company=None,
        in_account_currency=True,
        cost_center=None,
        ignore_account_permission=False,
    )
    supp["balance"] = balance
    doc_data = frappe.db.get_all(
        "Supplier",
        filters={"name": name},
        fields=[
            "name",
            "supplier_name",
            "disabled",
            "supplier_type",
            "supplier_group",
            "country",
            "tax_id",
            "supplier_primary_address",
            "primary_address",
            "supplier_primary_contact",
            "mobile_no",
            "email_id",
            "default_currency",
            "default_price_list",
            "payment_terms",
            "docstatus",
        ],
    )
    for x in doc_data:
        supp["name"] = x.name
        supp["supplier_name"] = x.supplier_name
        supp["disabled"] = x.disabled
        supp["supplier_type"] = x.supplier_type
        supp["supplier_group"] = x.supplier_group
        supp["country"] = x.country
        supp["tax_id"] = x.tax_id
        supp["supplier_primary_address"] = x.supplier_primary_address
        supp["address_line1"] = frappe.db.get_value(
            "Address", x.supplier_primary_address, "address_line1"
        )
        supp["city"] = frappe.db.get_value(
            "Address", x.supplier_primary_address, "city"
        )
        supp["country"] = frappe.db.get_value(
            "Address", x.supplier_primary_address, "country"
        )
        supp["supplier_primary_contact"] = x.supplier_primary_contact
        supp["contact_display"] = frappe.db.get_value(
            "Contact", x.supplier_primary_contact, "first_name"
        )
        supp["mobile_no"] = frappe.db.get_value(
            "Contact", x.supplier_primary_contact, "mobile_no"
        )
        supp["phone"] = frappe.db.get_value(
            "Contact", x.supplier_primary_contact, "phone"
        )
        supp["email_id"] = frappe.db.get_value(
            "Contact", x.supplier_primary_contact, "email_id"
        )
        supp["primary_address"] = x.primary_address
        supp["default_currency"] = x.default_currency
        supp["default_price_list"] = x.default_price_list
        supp["payment_terms"] = x.payment_terms
        supp["docstatus"] = x.docstatus
        if x.payment_terms:
            supp["credit_days"] = frappe.db.get_value(
                "Payment Terms Template Detail",
                {"parent": x.payment_terms},
                "credit_days",
            )
        else:
            supp["credit_days"] = 0

    attachments = frappe.db.sql(
        """ Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                        from `tabFile`  where `tabFile`.attached_to_doctype = "Supplier"
                                        and `tabFile`.attached_to_name = "{name}"
                                        order by `tabFile`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )

    supp["attachments"] = attachments

    comments = frappe.db.sql(
        """ Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Supplier"
                                        and `tabComment`.reference_name = "{name}"
                                        and `tabComment`.comment_type = "Comment"
                                        order by `tabComment`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )

    supp["comments"] = comments

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Supplier" and disabled = 0 """,
        as_dict=1,
    )
    supp["print_formats"] = print_formats
    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)

    supplier_quotation_count = frappe.db.count(
        "Supplier Quotation", filters={"supplier": name}
    )
    purchase_order_count = frappe.db.count("Purchase Order", filters={"supplier": name})
    purchase_receipt_count = frappe.db.count(
        "Purchase Receipt", filters={"supplier": name}
    )
    purchase_invoice_count = frappe.db.count(
        "Purchase Invoice", filters={"supplier": name}
    )
    payment_entry_count = frappe.db.count("Payment Entry", filters={"party": name})

    supp_qtn_connections = {}
    po_connections = {}
    pr_connections = {}
    pinv_connections = {}
    pe_connections = {}
    #
    # conn_request_for_quotation = frappe.db.get_all(
    # "Request for Quotation Supplier",
    # filters={"supplier": name},
    # )
    # count_request_for_quotations =len(conn_request_for_quotation)
    # request_for_quotation = {}
    #
    # conn_bank_account = frappe.db.get_all(
    # "Bank Account",
    # filters={"party":name},
    # )
    # count_bank_acocunt = len(conn_bank_account)
    # bank_account = {}
    #
    #
    # conn_pricing_rule = frappe.db.get_all(
    # "Pricing Rule",
    # filters={"supplier": name},
    # )
    # count_conn_pricing_rule = len(conn_pricing_rule)
    # pricing_rule = {}
    #
    # conn_party_spcecific_item = frappe.db.get_all(
    # "Party Specific Item",
    # filters={"party": name}
    # )
    # count_party_specific_item = len(conn_party_spcecific_item)
    # party_specific_item = {}

    connections = []
    #
    # if count_party_specific_item and doc_data:
    #     party_specific_item["name"] = "Party Specific Item"
    #     party_specific_item["count"] = count_party_specific_item
    #     party_specific_item["icon"] = "https://erpcloud.systems/files/party_specific_item.png"
    #     connections.append(party_specific_item)
    #
    # if count_conn_pricing_rule and doc_data:
    #     pricing_rule["name"] = "Pricing Rule"
    #     pricing_rule["count"] = count_conn_pricing_rule
    #     pricing_rule["icon"] = "https://erpcloud.systems/files/pricing_rule.png"
    #     connections.append(pricing_rule)
    #
    # if count_bank_acocunt and doc_data:
    #     bank_account["name"] = "Bank Acount"
    #     bank_account["count"] = count_bank_acocunt
    #     bank_account["icon"] = "https://erpcloud.systems/files/bank_account.png"
    #     connections.append(bank_account)
    #
    #
    # if count_request_for_quotations and doc_data:
    #     request_for_quotation["name"] = "Request For Quotation"
    #     request_for_quotation["count"] = count_request_for_quotations
    #     request_for_quotation["icon"] = "https://erpcloud.systems/files/request_for_quotation.png"
    # connections.append(request_for_quotation)
    if supplier_quotation_count > 0 and doc_data:
        supp_qtn_connections["name"] = "Supplier Quotation"
        supp_qtn_connections["count"] = supplier_quotation_count
        supp_qtn_connections[
            "icon"
        ] = "https://erpcloud.systems/files/supplier_quotation.png"
        connections.append(supp_qtn_connections)

    if purchase_order_count > 0 and doc_data:
        po_connections["name"] = "Purchase Order"
        po_connections["count"] = purchase_order_count
        po_connections["icon"] = "https://erpcloud.systems/files/purchase_order.png"
        connections.append(po_connections)

    if purchase_receipt_count > 0 and doc_data:
        pr_connections["name"] = "Purchase Receipt"
        pr_connections["count"] = purchase_receipt_count
        pr_connections["icon"] = "https://erpcloud.systems/files/purchase_receipt.png"
        connections.append(pr_connections)

    if purchase_invoice_count > 0 and doc_data:
        pinv_connections["name"] = "Purchase Invoice"
        pinv_connections["count"] = purchase_invoice_count
        pinv_connections["icon"] = "https://erpcloud.systems/files/purchase_invoice.png"
        connections.append(pinv_connections)

    if payment_entry_count > 0 and doc_data:
        pe_connections["name"] = "Payment Entry"
        pe_connections["count"] = payment_entry_count
        pe_connections["icon"] = "https://erpcloud.systems/files/payment_entry.png"
        connections.append(pe_connections)

    supp["conn"] = connections

    if doc_data:
        return supp
    else:
        return "لا يوجد مورد بهذا الاسم"


@frappe.whitelist(allow_guest=True)
def supplier_quotation(name):
    response = {}
    doc_data = frappe.db.get_all(
        "Supplier Quotation",
        filters={"name": name},
        fields=[
            "name",
            "supplier",
            "supplier_name",
            "transaction_date",
            "valid_till",
            "supplier_address",
            "contact_person",
            "contact_display",
            "address_display",
            "contact_mobile",
            "contact_email",
            "currency",
            "buying_price_list",
            "ignore_pricing_rule",
            "price_list_currency",
            "plc_conversion_rate",
            "conversion_rate",
            "total_qty",
            "taxes_and_charges",
            "total_taxes_and_charges",
            "base_total_taxes_and_charges",
            "apply_discount_on",
            "additional_discount_percentage",
            "base_discount_amount",
            "discount_amount",
            "grand_total",
            "base_grand_total",
            "total",
            "base_total",
            "base_net_total",
            "net_total",
            "in_words",
            "base_in_words",
            "status",
            "docstatus",
            "tc_name",
        ],
    )
    amended_to = frappe.db.get_value("Supplier Quotation", {"amended_from": name}, ["name"])
    for row in doc_data:
        response["name"] = row.name
        response["amended_to"] = amended_to
        response["supplier"] = row.supplier
        response["supplier_name"] = row.supplier_name
        response["transaction_date"] = row.transaction_date
        response["valid_till"] = row.valid_till
        response["status"] = row.status

        ####START OF ADDRESS & CONTACT####
        response["supplier_address"] = row.supplier_address
        response["address_line1"] = frappe.db.get_value(
            "Address", row.supplier_address, "address_line1"
        )
        response["city"] = frappe.db.get_value("Address", row.supplier_address, "city")
        response["country"] = frappe.db.get_value(
            "Address", row.supplier_address, "country"
        )
        response["contact_person"] = row.contact_person
        response["contact_display"] = frappe.db.get_value(
            "Contact", row.contact_person, "first_name"
        )
        response["mobile_no"] = frappe.db.get_value(
            "Contact", row.contact_person, "mobile_no"
        )
        response["phone"] = frappe.db.get_value("Contact", row.contact_persont, "phone")
        response["email_id"] = frappe.db.get_value(
            "Contact", row.contact_person, "email_id"
        )
        ####END OF ADDRESS & CONTACT####

        # response["contact_display"] = row.contact_display
        # response["contact_person"] = row.contact_person
        response["contact_mobile"] = row.contact_mobile
        response["address_display"] = row.address_display
        response["contact_email"] = row.contact_email
        response["currency"] = row.currency
        response["conversion_rate"] = row.conversion_rate
        response["buying_price_list"] = row.buying_price_list
        response["price_list_currency"] = row.price_list_currency
        response["plc_conversion_rate"] = row.plc_conversion_rate
        response["ignore_pricing_rule"] = row.ignore_pricing_rule
        response["tc_name"] = row.tc_name
        response["total_qty"] = row.total_qty
        response["total"] = row.total
        response["base_total"] = row.base_total
        response["net_total"] = row.net_total
        response["base_net_total"] = row.base_net_total
        response["total_taxes_and_charges"] = row.total_taxes_and_charges
        response["base_total_taxes_and_charges"] = row.base_total_taxes_and_charges
        response["apply_discount_on"] = row.apply_discount_on
        response["additional_discount_percentage"] = row.additional_discount_percentage
        response["discount_amount"] = row.discount_amount
        response["base_discount_amount"] = row.base_discount_amount
        response["grand_total"] = row.grand_total
        response["in_words"] = row.in_words
        response["base_grand_total"] = row.base_grand_total
        response["base_in_words"] = row.base_in_words
        response["docstatus"] = row.docstatus

    attachments = frappe.db.sql(
        """ Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                        from `tabFile`  where `tabFile`.attached_to_doctype = "Supplier Quotation"
                                        and `tabFile`.attached_to_name = "{name}"
                                        order by `tabFile`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )
    response["attachments"] = attachments

    comments = frappe.db.sql(
        """ Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Supplier Quotation"
                                        and `tabComment`.reference_name = "{name}"
                                        and `tabComment`.comment_type = "Comment"
                                        order by `tabComment`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )
    # dssss
    response["comments"] = comments
    child_table_items = frappe.db.get_all(
        "Supplier Quotation Item",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "item_code",
            "supplier_part_no",
            "item_name",
            "lead_time_days",
            "expected_delivery_date",
            "is_free_item",
            "description",
            "item_group",
            "brand",
            "image",
            "qty",
            "stock_uom",
            "uom",
            "conversion_factor",
            "stock_qty",
            "price_list_rate",
            "discount_percentage",
            "discount_amount",
            "base_price_list_rate",
            "rate",
            "amount",
            "item_tax_template",
            "base_rate",
            "base_amount",
            "pricing_rules",
            "net_rate",
            "net_amount",
            "base_net_rate",
            "base_net_amount",
            "weight_per_unit",
            "total_weight",
            "weight_uom",
            "warehouse",
            "prevdoc_doctype",
            "material_request",
            "sales_order",
            "request_for_quotation",
            "material_request_item",
            "request_for_quotation_item",
            "item_tax_rate",
            "manufacturer",
            "manufacturer_part_no",
            "project",
        ],
    )

    child_table_taxes_and_charges = frappe.db.get_all(
        "Purchase Taxes and Charges",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "add_deduct_tax",
            "charge_type",
            "row_id",
            "included_in_print_rate",
            "included_in_paid_amount",
            "account_head",
            "description",
            "rate",
            "cost_center",
            "account_currency",
            "tax_amount",
            "tax_amount_after_discount_amount",
            "total",
            "base_tax_amount",
            "base_total",
            "base_tax_amount_after_discount_amount",
            "item_wise_tax_detail",
        ],
    )

    if child_table_items and doc_data:
        response["items"] = child_table_items
    if child_table_taxes_and_charges and doc_data:
        response["taxes"] = child_table_taxes_and_charges

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Supplier Quotation" and disabled = 0 """,
        as_dict=1,
    )
    response["print_formats"] = print_formats
    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)

    quotation_count = frappe.db.count("Quotation", filters={"supplier_quotation": name})
    purchase_order = frappe.db.get_all(
        "Purchase Order Item",
        filters={"supplier_quotation": name},
        group_by="supplier_quotation",
    )
    purchase_order_count = len(purchase_order)
    material_request = frappe.db.get_all(
        "Supplier Quotation Item", filters={"parent": name}, group_by="material_request"
    )
    material_request_count = len(material_request)

    quotation_count_connections = {}
    purchase_order_count_connections = {}
    material_request_count_connections = {}

    connections = []

    if quotation_count > 0 and doc_data:
        quotation_count_connections["name"] = "Quotation"
        quotation_count_connections["count"] = quotation_count
        quotation_count_connections[
            "icon"
        ] = "https://erpcloud.systems/files/quotation.png"
        connections.append(quotation_count_connections)

    if purchase_order_count > 0 and doc_data:
        purchase_order_count_connections["name"] = "Purchase Order"
        purchase_order_count_connections["count"] = purchase_order_count
        purchase_order_count_connections[
            "icon"
        ] = "https://erpcloud.systems/files/purchase_order.png"
        connections.append(purchase_order_count_connections)

    if material_request_count > 0 and doc_data:
        material_request_count_connections["name"] = "Material Request"
        material_request_count_connections["count"] = material_request_count
        material_request_count_connections[
            "icon"
        ] = "https://erpcloud.systems/files/material_request.png"
        connections.append(material_request_count_connections)

    response["conn"] = connections

    if doc_data:
        return response
    else:
        return "لا يوجد مورد بهذا الاسم"


@frappe.whitelist(allow_guest=True)
def purchase_order(name):
    response = {}
    doc_data = frappe.db.get_all(
        "Purchase Order",
        filters={"name": name},
        fields={
            "name",
            "title",
            "naming_series",
            "supplier",
            "supplier_name",
            "apply_tds",
            "tax_withholding_category",
            "company",
            "transaction_date",
            "schedule_date",
            "order_confirmation_no",
            "order_confirmation_date",
            "amended_from",
            "cost_center",
            "project",
            "customer",
            "customer_name",
            "customer_contact_person",
            "customer_contact_display",
            "customer_contact_mobile",
            "customer_contact_email",
            "supplier_address",
            "address_display",
            "contact_person",
            "contact_display",
            "contact_mobile",
            "contact_email",
            "docstatus",
            "shipping_address",
            "shipping_address_display",
            "billing_address",
            "billing_address_display",
            "currency",
            "conversion_rate",
            "buying_price_list",
            "plc_conversion_rate",
            "ignore_pricing_rule",
            "is_subcontracted",
            "supplier_warehouse",
            "scan_barcode",
            "set_warehouse",
            "total_qty",
            "base_total",
            "base_net_total",
            "total_net_weight",
            "total",
            "net_total",
            "set_reserve_warehouse",
            "tax_category",
            "shipping_rule",
            "taxes_and_charges",
            "other_charges_calculation",
            "base_taxes_and_charges_added",
            "base_taxes_and_charges_deducted",
            "base_total_taxes_and_charges",
            "taxes_and_charges_added",
            "taxes_and_charges_deducted",
            "total_taxes_and_charges",
            "apply_discount_on",
            "base_discount_amount",
            "discount_amount",
            "base_grand_total",
            "base_rounding_adjustment",
            "base_in_words",
            "base_rounded_total",
            "grand_total",
            "rounding_adjustment",
            "rounded_total",
            "disable_rounded_total",
            "in_words",
            "advance_paid",
            "payment_terms_template",
            "status",
            "per_billed",
            "per_received",
            "tc_name",
            "terms",
            "letter_head",
            "select_print_heading",
            "price_list_currency",
            "language",
            "group_same_items",
            "from_date",
            "to_date",
            "auto_repeat",
            "ref_sq",
            "party_account_currency",
            "is_internal_supplier",
            "represents_company",
            "inter_company_order_reference",
        },
    )
    amended_to = frappe.db.get_value("Quotation", {"Purchase Order": name}, ["name"])
    for row in doc_data:
        response["name"] = row.name
        response["amended_to"] = amended_to
        response["supplier"] = row.supplier
        response["supplier_name"] = row.supplier_name
        response["transaction_date"] = row.transaction_date
        response["schedule_date"] = row.schedule_date
        response["status"] = row.status

        ####START OF ADDRESS & CONTACT####
        response["supplier_address"] = row.supplier_address
        response["address_line1"] = frappe.db.get_value(
            "Address", row.supplier_address, "address_line1"
        )
        response["city"] = frappe.db.get_value("Address", row.supplier_address, "city")
        response["country"] = frappe.db.get_value(
            "Address", row.supplier_address, "country"
        )
        response["contact_person"] = row.contact_person
        response["contact_display"] = frappe.db.get_value(
            "Contact", row.contact_person, "first_name"
        )
        response["mobile_no"] = frappe.db.get_value(
            "Contact", row.contact_person, "mobile_no"
        )
        response["phone"] = frappe.db.get_value("Contact", row.contact_persont, "phone")
        response["email_id"] = frappe.db.get_value(
            "Contact", row.contact_person, "email_id"
        )
        ####END OF ADDRESS & CONTACT####

        response["address_display"] = row.address_display
        # response["contact_person"] = row.contact_person
        response["contact_mobile"] = row.contact_mobile
        response["contact_email"] = row.contact_email

        response["currency"] = row.currency
        response["conversion_rate"] = row.conversion_rate
        response["buying_price_list"] = row.buying_price_list
        response["ignore_pricing_rule"] = row.ignore_pricing_rule
        response["plc_conversion_rate"] = row.plc_conversion_rate
        response["tc_name"] = row.tc_name
        response["payment_terms_template"] = row.payment_terms_template
        response["cost_center"] = row.cost_center
        response["project"] = row.project
        response["total_qty"] = row.total_qty
        response["total"] = row.total
        response["base_total"] = row.base_total
        response["net_total"] = row.net_total
        response["base_net_total"] = row.base_net_total
        response["total_taxes_and_charges"] = row.total_taxes_and_charges
        response["base_total_taxes_and_charges"] = row.base_total_taxes_and_charges
        response["apply_discount_on"] = row.apply_discount_on
        response["discount_amount"] = row.discount_amount
        response["base_discount_amount"] = row.base_discount_amount
        response["grand_total"] = row.grand_total
        response["in_words"] = row.in_words
        response["base_grand_total"] = row.base_grand_total
        response["base_in_words"] = row.base_in_words
        response["docstatus"] = row.docstatus
        response["price_list_currency"] = row.price_list_currency
        # response["tax_withholding_category"] = row.tax_withholding_category
        # response["company"] = row.company
        # response["schedule_date"] = row.schedule_date
        # response["order_confirmation_no"] = row.order_confirmation_no
        # response["order_confirmation_date"] = row.order_confirmation_date
        # response["amended_from"] = row.amended_from
        # response["drop_ship"] = row.drop_ship
        # response["customer"] = row.customer
        # response["customer_name"] = row.customer_name
        # response["customer_contact_person"] = row.customer_contact_person
        # response["customer_contact_display"] = row.customer_contact_display
        # response["customer_contact_mobile"] = row.customer_contact_mobile
        # response["customer_contact_email"] = row.customer_contact_email
        response["contact_display"] = row.contact_display
        # response["shipping_address"] = row.shipping_address
        # response["shipping_address_display"] = row.shipping_address_display
        # response["billing_address"] = row.billing_address
        # response["billing_address_display"] = row.billing_address_display
        # response["is_subcontracted"] = row.is_subcontracted
        # response["supplier_warehouse"] = row.supplier_warehouse
        # response["scan_barcode"] = row.scan_barcode
        response["set_warehouse"] = row.set_warehouse
        # response["total_net_weight"] = row.total_net_weight
        # response["set_reserve_warehouse"] = row.set_reserve_warehouse
        # response["tax_category"] = row.tax_category
        # response["shipping_rule"] = row.shipping_rule
        # response["taxes_and_charges"] = row.taxes_and_charges
        # response["other_charges_calculation"] = row.other_charges_calculation
        # response["base_taxes_and_charges_added"] = row.base_taxes_and_charges_added
        # response[
        #     "base_taxes_and_charges_deducted"
        # ] = row.base_taxes_and_charges_deducted
        # response["taxes_and_charges_added"] = row.taxes_and_charges_added
        # response["taxes_and_charges_deducted"] = row.taxes_and_charges_deducted
        # response["base_rounding_adjustment"] = row.base_rounding_adjustment
        # response["base_rounded_total"] = row.base_rounded_total
        # response["rounding_adjustment"] = row.rounding_adjustment
        # response["rounded_total"] = row.rounded_total
        # response["disable_rounded_total"] = row.disable_rounded_total
        # response["advance_paid"] = row.advance_paid
        # response["per_billed"] = row.per_billed
        # response["per_received"] = row.per_received
        # response["terms"] = row.terms
        # response["letter_head"] = row.letter_head
        # response["select_print_heading"] = row.select_print_heading
        # response["language"] = row.language
        # response["group_same_items"] = row.group_same_items
        # response["from_date"] = row.from_date
        # response["to_date"] = row.to_date
        # response["auto_repeat"] = row.auto_repeat
        # response["ref_sq"] = row.ref_sq
        # response["party_account_currency"] = row.party_account_currency
        # response["is_internal_supplier"] = row.is_internal_supplier
        # response["represents_company"] = row.represents_company
        # response["inter_company_order_reference"] = row.inter_company_order_reference

    attachments = frappe.db.sql(
        """ Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                        from `tabFile`  where `tabFile`.attached_to_doctype = "Purchase Order"
                                        and `tabFile`.attached_to_name = "{name}"
                                        order by `tabFile`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )
    response["attachments"] = attachments

    comments = frappe.db.sql(
        """ Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Purchase Order"
                                        and `tabComment`.reference_name = "{name}"
                                        and `tabComment`.comment_type = "Comment"
                                        order by `tabComment`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )
    # dssss
    response["comments"] = comments

    purchase_order_item_child_table = frappe.db.get_all(
        "Purchase Order Item",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "item_code",
            "supplier_part_no",
            "item_name",
            "product_bundle",
            "schedule_date",
            "expected_delivery_date",
            "description",
            "image",
            "qty",
            "stock_uom",
            "uom",
            "conversion_factor",
            "stock_qty",
            "price_list_rate",
            "last_purchase_rate",
            "margin_type",
            "margin_rate_or_amount",
            "rate_with_margin",
            "discount_percentage",
            "discount_amount",
            "base_rate_with_margin",
            "rate",
            "amount",
            "item_tax_template",
            "base_rate",
            "base_amount",
            "pricing_rules",
            "stock_uom_rate",
            "is_free_item",
            "net_rate",
            "net_amount",
            "base_net_rate",
            "base_net_amount",
            "warehouse",
            "actual_qty",
            "company_total_stock",
            "material_request",
            "material_request_item",
            "sales_order",
            "sales_order_item",
            "sales_order_packed_item",
            "supplier_quotation",
            "supplier_quotation_item",
            "delivered_by_supplier",
            "against_blanket_order",
            "blanket_order",
            "blanket_order_rate",
            "item_group",
            "brand",
            "received_qty",
            "returned_qty",
            "billed_amt",
            "expense_account",
            "manufacturer",
            "manufacturer_part_no",
            "bom",
            "weight_per_unit",
            "total_weight",
            "weight_uom",
            "project",
            "cost_center",
            "is_fixed_asset",
            "item_tax_rate",
            "production_plan",
            "production_plan_item",
            "production_plan_sub_assembly_item",
        ],
    )
    # s

    child_table_taxes_and_charges = frappe.db.get_all(
        "Purchase Taxes and Charges",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "add_deduct_tax",
            "charge_type",
            "row_id",
            "included_in_print_rate",
            "included_in_paid_amount",
            "account_head",
            "description",
            "rate",
            "cost_center",
            "account_currency",
            "tax_amount",
            "tax_amount_after_discount_amount",
            "total",
            "base_tax_amount",
            "base_total",
            "base_tax_amount_after_discount_amount",
            "item_wise_tax_detail",
        ],
    )

    child_payment_schedule = frappe.db.get_all(
        "Payment Schedule",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "payment_term",
            "description",
            "due_date",
            "mode_of_payment",
            "invoice_portion",
            "discount_type",
            "discount_date",
            "discount",
            "payment_amount",
            "outstanding",
            "paid_amount",
            "discounted_amount",
            "base_payment_amount",
        ],
    )

    if purchase_order_item_child_table and doc_data:
        response["purchase_order_items"] = purchase_order_item_child_table

    if child_table_taxes_and_charges and doc_data:
        response["taxes"] = child_table_taxes_and_charges

    if child_payment_schedule and doc_data:
        response["payment_schedule"] = child_payment_schedule

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Purchase Order" and disabled = 0 """,
        as_dict=1,
    )
    response["print_formats"] = print_formats
    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)
    purchase_receipt = frappe.db.get_all(
        "Purchase Receipt Item",
        filters={"purchase_order": name},
    )
    count_purchase_receipt = len(purchase_receipt)
    purchase_receipts = {}

    purchase_invoice = frappe.db.get_all(
        "Purchase Invoice Item",
        filters={"purchase_order": name},
    )

    count_purchase_invoice = len(purchase_invoice)
    purchase_invoices = {}

    payment_entire_connection = frappe.db.get_all(
        "Payment Entry Reference",
        filters={"reference_name": name},
        fields=["parent"],
        group_by="parent",
    )
    count_payment_entries = len(payment_entire_connection)
    payment_entries = {}

    get_current_purchase_order_items = frappe.db.get_all(
        "Purchase Order Item",
        filters={"material_request": ["!=", "null"], "parent": name},
        fields=[
            "material_request",
        ],
    )
    count_current_purchase_order_items = len(get_current_purchase_order_items)
    material_requests = {}
    get_supplier_quotations = frappe.db.get_all(
        "Purchase Order Item",
        filters={"supplier_quotation": ["!=", "null"], "parent": name},
        fields=[
            "supplier_quotation",
        ],
    )
    count_get_supplier_quotations = len(get_supplier_quotations)
    supplier_quotation = {}
    # purchase_order_item = frappe.db.get_all("Purchase Order Item", filters={"material_request":})
    connections = []
    if count_purchase_receipt > 0 and doc_data:
        purchase_receipts["name"] = "Purchase Receipt"
        purchase_receipts["count"] = count_purchase_receipt
        purchase_receipts[
            "icon"
        ] = "https://erpcloud.systems/files/purchase_receipt.png"
        connections.append(purchase_receipts)

    if count_purchase_invoice > 0 and doc_data:
        purchase_invoices["name"] = "Purchase Invoice"
        purchase_invoices["count"] = count_purchase_invoice
        purchase_invoices[
            "icon"
        ] = "https://erpcloud.systems/files/purchase_invoice.png"
        connections.append(purchase_invoices)
    if count_payment_entries > 0 and doc_data:
        payment_entries["name"] = "Payment Entry"
        payment_entries["count"] = count_payment_entries
        payment_entries["icon"] = "https://erpcloud.systems/files/payment_entry.png"
        connections.append(payment_entries)
    if count_current_purchase_order_items > 0 and doc_data:
        material_requests["name"] = "Material Request"
        material_requests["count"] = count_current_purchase_order_items
        material_requests[
            "icon"
        ] = "https://erpcloud.systems/files/material_request.png"
        connections.append(material_requests)

    if count_get_supplier_quotations > 0 and doc_data:
        supplier_quotation["name"] = "Supplier Quotation"
        supplier_quotation["count"] = count_get_supplier_quotations
        supplier_quotation[
            "icon"
        ] = "https://erpcloud.systems/files/supplier_quotation.png"
        connections.append(supplier_quotation)
    response["conn"] = connections

    if doc_data:
        return response
    else:
        return "لا يوجد مورد بهذا الاسم"


@frappe.whitelist(allow_guest=True)
def purchase_invoice(name):
    response = {}

    doc_data = frappe.db.get_all(
        "Purchase Invoice",
        filters={"name": name},
        fields=[
            "name",
            "title",
            "docstatus",
            "naming_series",
            "supplier",
            "supplier_name",
            "tax_id",
            "due_date",
            "posting_date",
            "set_posting_time",
            "is_return",
            "cost_center",
            "project",
            "supplier_address",
            "address_display",
            "contact_person",
            "contact_display",
            "contact_mobile",
            "contact_email",
            "billing_address",
            "currency",
            "conversion_rate",
            "buying_price_list",
            "price_list_currency",
            "plc_conversion_rate",
            "ignore_pricing_rule",
            "set_warehouse",
            "set_from_warehouse",
            "supplier_warehouse",
            "update_stock",
            "total_qty",
            "base_total",
            "base_net_total",
            "total_net_weight",
            "total",
            "net_total",
            "tax_category",
            "shipping_rule",
            "taxes_and_charges",
            "other_charges_calculation",
            "base_taxes_and_charges_added",
            "base_taxes_and_charges_deducted",
            "base_total_taxes_and_charges",
            "taxes_and_charges_added",
            "taxes_and_charges_deducted",
            "total_taxes_and_charges",
            "apply_discount_on",
            "base_discount_amount",
            "additional_discount_account",
            "additional_discount_percentage",
            "discount_amount",
            "base_grand_total",
            "base_rounding_adjustment",
            "base_rounded_total",
            "base_in_words",
            "grand_total",
            "rounding_adjustment",
            "rounded_total",
            "in_words",
            "total_advance",
            "outstanding_amount",
            "disable_rounded_total",
            "mode_of_payment",
            "cash_bank_account",
            "clearance_date",
            "paid_amount",
            "base_paid_amount",
            "write_off_amount",
            "base_write_off_amount",
            "write_off_account",
            "write_off_cost_center",
            "allocate_advances_automatically",
            "payment_terms_template",
            "ignore_default_payment_terms_template",
            "tc_name",
            "terms",
            "letter_head",
            "select_print_heading",
            "group_same_items",
            "language",
            "on_hold",
            "release_date",
            "hold_comment",
            "status",
            "inter_company_invoice_reference",
            "represents_company",
            "is_internal_supplier",
            "credit_to",
            "party_account_currency",
            "is_opening",
            "against_expense_account",
            "unrealized_profit_loss_account",
            "remarks",
            "from_date",
            "to_date",
        ],
    )
    amended_to = frappe.db.get_value("Purchase Invoice", {"amended_from": name}, ["name"])
    for row in doc_data:
        response["name"] = row.name
        response["amended_to"] = amended_to
        response["supplier"] = row.supplier
        response["supplier_name"] = row.supplier_name
        response["posting_date"] = row.posting_date
        response["due_date"] = row.due_date
        response["tax_id"] = row.tax_id
        response["status"] = row.status

        ####START OF ADDRESS & CONTACT####
        response["supplier_address"] = row.supplier_address
        response["address_line1"] = frappe.db.get_value(
            "Address", row.supplier_address, "address_line1"
        )
        response["city"] = frappe.db.get_value("Address", row.supplier_address, "city")
        response["country"] = frappe.db.get_value(
            "Address", row.supplier_address, "country"
        )
        response["contact_person"] = row.contact_person
        response["contact_display"] = frappe.db.get_value(
            "Contact", row.contact_person, "first_name"
        )
        response["mobile_no"] = frappe.db.get_value(
            "Contact", row.contact_person, "mobile_no"
        )
        response["phone"] = frappe.db.get_value("Contact", row.contact_persont, "phone")
        response["email_id"] = frappe.db.get_value(
            "Contact", row.contact_person, "email_id"
        )
        ####END OF ADDRESS & CONTACT####

        response["address_display"] = row.address_display
        # response["contact_person"] = row.contact_person
        # response["contact_display"]= row.contact_display
        response["contact_mobile"] = row.contact_mobile
        response["contact_email"] = row.contact_email
        response["currency"] = row.currency
        response["cost_center"] = row.cost_center
        response["conversion_rate"] = row.conversion_rate
        response["buying_price_list"] = row.buying_price_list
        response["price_list_currency"] = row.price_list_currency
        response["set_warehouse"] = row.set_warehouse
        response["update_stock"] = row.update_stock
        response["project"] = row.project
        response["is_return"] = row.is_return
        response["ignore_pricing_rule"] = row.ignore_pricing_rule
        response["plc_conversion_rate"] = row.plc_conversion_rate
        response["payment_terms_template"] = row.payment_terms_template
        response["tc_name"] = row.tc_name
        response["total_qty"] = row.total_qty
        response["total"] = row.total
        response["base_total"] = row.base_total
        response["net_total"] = row.net_total
        response["base_net_total"] = row.base_net_total
        response["total_taxes_and_charges"] = row.total_taxes_and_charges
        response["base_total_taxes_and_charges"] = row.base_total_taxes_and_charges
        response["apply_discount_on"] = row.apply_discount_on
        response["additional_discount_percentage"] = row.additional_discount_percentage
        response["discount_amount"] = row.discount_amount
        response["base_discount_amount"] = row.base_discount_amount
        response["grand_total"] = row.grand_total
        response["base_grand_total"] = row.base_grand_total
        response["in_words"] = row.in_words
        response["base_in_words"] = row.base_in_words
        response["docstatus"] = row.docstatus

    # attachments and comments
    attachments = frappe.db.sql(
        """ Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                        from `tabFile`  where `tabFile`.attached_to_doctype = "Purchase Order"
                                        and `tabFile`.attached_to_name = "{name}"
                                        order by `tabFile`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )
    response["attachments"] = attachments

    comments = frappe.db.sql(
        """ Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Purchase Order"
                                        and `tabComment`.reference_name = "{name}"
                                        and `tabComment`.comment_type = "Comment"
                                        order by `tabComment`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )
    response["comments"] = comments

    # print_formats
    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Pruchase Invoice" and disabled = 0 """,
        as_dict=1,
    )
    response["print_formats"] = print_formats
    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)
    # Child Tables from here
    purchase_invoice_item = frappe.db.get_all(
        "Purchase Invoice Item",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "item_code",
            "item_name",
            "product_bundle",
            "description",
            "image",
            "qty",
            "stock_uom",
            "uom",
            "conversion_factor",
            "stock_qty",
            "price_list_rate",
            "margin_type",
            "margin_rate_or_amount",
            "rate_with_margin",
            "discount_percentage",
            "discount_amount",
            "base_rate_with_margin",
            "rate",
            "amount",
            "item_tax_template",
            "base_rate",
            "base_amount",
            "pricing_rules",
            "stock_uom_rate",
            "is_free_item",
            "net_rate",
            "net_amount",
            "base_net_rate",
            "base_net_amount",
            "warehouse",
            "item_group",
            "brand",
            "received_qty",
            "expense_account",
            "manufacturer",
            "manufacturer_part_no",
            "bom",
            "weight_per_unit",
            "total_weight",
            "weight_uom",
            "project",
            "cost_center",
            "is_fixed_asset",
            "item_tax_rate",
        ],
    )
    if purchase_invoice_item and doc_data:
        response["purchase_invoice_item"] = purchase_invoice_item

    """
    child_pricing_rule_detail = frappe.db.get_all(
        "Pricing Rule Detail",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "pricing_rule",
            "item_code",
            "margin_type",
            "rate_or_discount",
            "child_docname",
            "rule_applied",
        ],
    )

    if child_pricing_rule_detail and doc_data:
        response["child_pricing_rule_detail"] = child_pricing_rule_detail

    child_purchase_receipt_item_supplied = frappe.db.get_all(
        "Purchase Receipt Item Supplied",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "main_item_code",
            "rm_item_code",
            "item_name",
            "bom_detail_no",
            "description",
            "stock_uom",
            "conversion_factor",
            "reference_name",
            "rate",
            "amount",
            "required_qty",
            "consumed_qty",
            "current_stock",
            "batch_no",
            "serial_no",
            "purchase_order",
        ],
    )
    if child_pricing_rule_detail and doc_data:
        response[
            "child_purchase_receipt_item_supplied"
        ] = child_purchase_receipt_item_supplied
    """
    child_purchase_taxes_and_charges = frappe.db.get_all(
        "Purchase Taxes and Charges",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "category",
            "add_deduct_tax",
            "charge_type",
            "row_id",
            "included_in_print_rate",
            "included_in_paid_amount",
            "account_head",
            "description",
            "rate",
            "cost_center",
            "account_currency",
            "tax_amount",
            "tax_amount_after_discount_amount",
            "total",
            "base_tax_amount",
            "base_total",
            "base_tax_amount_after_discount_amount",
            "item_wise_tax_detail",
        ],
    )
    if child_purchase_taxes_and_charges and doc_data:
        response["child_purchase_taxes_and_charges"] = child_purchase_taxes_and_charges
    """
    child_purchase_invice_advance = frappe.db.get_all(
        "Purchase Invoice Advance",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "reference_type",
            "reference_name",
            "remarks",
            "reference_row",
            "advance_amount",
            "allocated_amount",
            "exchange_gain_loss",
            "ref_exchange_rate",
        ],
    )  # ssssss

    if child_purchase_invice_advance and doc_data:
        response["child_purchase_invice_advance"] = child_purchase_invice_advance

    child_advance_tax = frappe.db.get_all(
        "Advance Tax",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "reference_type",
            "reference_name",
            "reference_detail",
            "account_head",
            "allocated_amount",
        ],
    )

    if child_advance_tax and doc_data:
        response["child_advance_tax"] = child_advance_tax
    """
    child_payment_schedule = frappe.db.get_all(
        "Payment Schedule",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "payment_term",
            "description",
            "due_date",
            "mode_of_payment",
            "invoice_portion",
            "discount_type",
            "discount_date",
            "discount",
            "payment_amount",
            "outstanding",
            "paid_amount",
            "discounted_amount",
            "base_payment_amount",
        ],
    )

    if child_payment_schedule and doc_data:
        response["payment_schedule"] = child_payment_schedule

    # child_payment_schedule = frappe.db.get_all(
    #     "Payment Schedule",
    #     filters={"parent": name},
    #     order_by="idx",
    #     fields=[
    #         "idx",
    #         "payment_term",
    #         "description",
    #         "due_date",
    #         "mode_of_payment",
    #         "invoice_portion",
    #         "discount_type",
    #         "discount_date",
    #         "discount",
    #         "payment_amount",
    #         "outstanding",
    #         "paid_amount",
    #         "discounted_amount",
    #         "base_payment_amount",
    #     ],
    # )
    # if child_payment_schedule and doc_data:
    #     response["payment_schedule"]: child_payment_schedule

    # Connections
    payment_entire_connection = frappe.db.get_all(
        "Payment Entry Reference",
        filters={"reference_name": name},
        fields=["parent"],
        group_by="parent",
    )
    count_payment_entries = len(payment_entire_connection)
    payment_entries = {}

    purchase_invoice = frappe.db.get_all(
        "Purchase Invoice",
        filters={"return_against": name},
    )

    count_purchase_invoice = len(purchase_invoice)
    purchase_invoices = {}

    con_purchase_order = frappe.db.get_all(
        "Purchase Invoice Item",
        filters={"parent": name},
    )
    count_purchase_order = len(con_purchase_order)
    purchase_orders = {}

    # con_payment_requests = frappe.db.get_all(
    #      "Payment Request",
    #      filters={"reference_name": name},)
    # count_payment_requests = len(con_payment_requests)
    # payment_requests = {}
    # get_current_purchase_order_items = frappe.db.get_all(
    #     "Purchase Order Item",
    #     filters={"parent": name},
    #     fields=[
    #         "material_request",
    #     ],
    # )
    # count_current_purchase_order_items = len(get_current_purchase_order_items)
    # material_requests = {}
    # get_supplier_quotations = frappe.db.get_all(
    #     "Purchase Order Item",
    #     filters={"parent": name},
    #     fields=[
    #         "supplier_quotation",
    #     ],
    # )
    # count_get_supplier_quotations = len(get_supplier_quotations)
    # supplier_quotation = {}
    # purchase_order_item = frappe.db.get_all("Purchase Order Item", filters={"material_request":})
    connections = []
    if count_purchase_order > 0 and doc_data:
        purchase_orders["name"] = "Purchase Order"
        purchase_orders["count"] = count_purchase_order
        purchase_orders["icon"] = "https://erpcloud.systems/files/purchase_order.png"
        connections.append(purchase_orders)

    if count_purchase_invoice > 0 and doc_data:
        purchase_invoices["name"] = "Purchase Invoice"
        purchase_invoices["count"] = count_purchase_invoice
        purchase_invoices["icon"] = "https://erpcloud.systems/files/purcase_invoice.png"
        connections.append(purchase_invoices)
    if count_payment_entries > 0 and doc_data:
        payment_entries["name"] = "Payment Entry"
        payment_entries["count"] = count_payment_entries
        payment_entries["icon"] = "https://erpcloud.systems/files/payment_entry.png"
        connections.append(payment_entries)
    # if count_payment_requests > 0 and doc_data:
    #     payment_requests["name"] = "Payment Request"
    #     payment_requests["count"] = count_payment_requests
    #     payment_requests["icon"] = "https://erpcloud.systems/files/payment_request.png"
    #     connections.append(payment_requests)
    # if count_current_purchase_order_items > 0 and doc_data:
    #     material_requests["name"] = "Material Request"
    #     material_requests["count"] = count_current_purchase_order_items
    #     material_requests[
    #         "icon"
    #     ] = "https://erpcloud.systems/files/material_request.png"
    #     connections.append(material_requests)

    # if count_get_supplier_quotations > 0 and doc_data:
    #     supplier_quotation["name"] = "Supplier Quotation"
    #     supplier_quotation["count"] = count_get_supplier_quotations
    #     supplier_quotation[
    #         "icon"
    #     ] = "https://erpcloud.systems/files/supplier_quotation.png"
    #     connections.append(supplier_quotation)
    response["conn"] = connections

    if doc_data:
        return response
    else:
        return "لا يوجد مورد بهذا الاسم"


@frappe.whitelist(allow_guest=True)
def get_price_list(name):
    if str(name).lower() in ["buying", "buy", "1"]:
        return frappe.db.get_all(
            "Price List",
            filters={"buying": 1},
            fields=[
                "name",
                "currency",
            ],
        )
    elif str(name).lower() in ["selling", "sell", "0"]:
        return frappe.db.get_all(
            "Price List",
            filters={"selling": 1},
            fields=[
                "name",
                "currency",
            ],
        )

    else:
        return "لا يوجد"


@frappe.whitelist(allow_guest=True)
def material_request(name):
    response = {}
    doc_data = frappe.db.get_all(
        "Material Request",
        filters={"name": name},
        fields=[
            "name",
            "material_request_type",
            "status",
            "docstatus",
            "transfer_status",
            "transaction_date",
            "schedule_date",
            "company",
            "set_warehouse",
            "set_from_warehouse",
            "customer",
            "per_ordered",
            "per_received",
        ],
    )
    amended_to = frappe.db.get_value("Material Request", {"amended_from": name}, ["name"])
    response["name"] = doc_data[0].name
    response["amended_to"] = amended_to
    response["material_request_type"] = doc_data[0].material_request_type
    response["status"] = doc_data[0].status
    response["docstatus"] = doc_data[0].docstatus

    response["transaction_date"] = doc_data[0].transaction_date
    response["schedule_date"] = doc_data[0].schedule_date

    response["set_warehouse"] = doc_data[0].set_warehouse
    response["set_from_warehouse"] = doc_data[0].set_warehouse
    response["customer"] = doc_data[0].customer

    attachments = frappe.db.sql(
        """ Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                        from `tabFile`  where `tabFile`.attached_to_doctype = "Material Request"
                                        and `tabFile`.attached_to_name = "{name}"
                                        order by `tabFile`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )
    response["attachments"] = attachments

    comments = frappe.db.sql(
        """ Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Material Request"
                                        and `tabComment`.reference_name = "{name}"
                                        and `tabComment`.comment_type = "Comment"
                                        order by `tabComment`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )
    # dssss
    response["comments"] = comments

    material_request_item = frappe.db.get_all(
        "Material Request Item",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "image",
            "item_code",
            "item_name",
            "schedule_date",
            "description",
            "item_group",
            "qty",
            "stock_uom",
            "warehouse",
            "uom",
            "conversion_factor",
            "stock_qty",
            "min_order_qty",
            "projected_qty",
            "actual_qty",
            "ordered_qty",
            "received_qty",
            "rate",
            "amount",
            "cost_center",
            "expense_account",
            "docstatus",
        ],
    )

    if material_request_item and doc_data:
        response["items"] = material_request_item

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Material Request" and disabled = 0 """,
        as_dict=1,
    )
    response["print_formats"] = print_formats
    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)

    con_material_request = frappe.db.get_all(
        "Supplier Quotation Item",
        filters={"material_request": name},
    )
    count_material_request = len(con_material_request)
    supplier_quotation = {}

    con_purchase_order = frappe.db.get_all(
        "Purchase Order Item",
        filters={"material_request": name},
    )
    count_purchase_order = len(con_purchase_order)
    purchase_order = {}

    con_purchase_receipt = frappe.db.get_all(
        "Purchase Receipt Item",
        filters={"material_request": name},
    )
    count_purchase_receipt = len(con_purchase_receipt)
    purchase_receipt = {}

    con_stock_entry = frappe.db.get_all(
        "Stock Entry Detail",
        filters={"material_request": name},
    )
    count_stock_entry = len(con_stock_entry)
    stock_entry = {}

    connections = []

    if count_material_request > 0 and doc_data:
        supplier_quotation["name"] = "Supplier Quotation"
        supplier_quotation["count"] = count_material_request
        supplier_quotation[
            "icon"
        ] = "https://erpcloud.systems/files/supplier_quotation.png"
        connections.append(supplier_quotation)

    if count_purchase_order > 0 and doc_data:
        purchase_order["name"] = "Purchase Order"
        purchase_order["count"] = count_purchase_order
        purchase_order["icon"] = "https://erpcloud.systems/files/purchase_order.png"
        connections.append(purchase_order)

    if count_purchase_receipt > 0 and doc_data:
        purchase_receipt["name"] = "Purchase Receipt"
        purchase_receipt["count"] = count_purchase_receipt
        purchase_receipt["icon"] = "https://erpcloud.systems/files/purchase_receipt.png"
        connections.append(purchase_receipt)
    if count_stock_entry > 0 and doc_data:
        stock_entry["name"] = "Stock Entry"
        stock_entry["count"] = count_stock_entry
        stock_entry["icon"] = "https://erpcloud.systems/files/stock_entry.png"
        connections.append(stock_entry)
    response["conn"] = connections

    if doc_data:
        return response
    else:
        return "لا يوجد"


################################################## HR section ########################################################################


@frappe.whitelist(allow_guest=True)
def leave_application(name):
    response = {}
    doc_data = frappe.db.get_all(
        "Leave Application",
        filters={"name": name},
        fields=[
            "name",
            "docstatus",
            "employee",
            "description",
            "employee_name",
            "leave_type",
            "department",
            "leave_balance",
            "from_date",
            "to_date",
            "half_day",
            "total_leave_days",
            "leave_approver",
            "leave_approver_name",
            "status",
            "posting_date",
            "follow_via_email",
            "department",
        ],
    )
    amended_to = frappe.db.get_value("Leave Application", {"amended_from": name}, ["name"])
    if not doc_data:
        return "لا يوجد"
    response["name"] = doc_data[0].name
    response["amended_to"] = amended_to
    response["docstatus"] = doc_data[0].docstatus
    response["employee"] = doc_data[0].employee
    response["employee_name"] = doc_data[0].employee_name
    response["leave_type"] = doc_data[0].leave_type

    response["leave_balance"] = doc_data[0].leave_balance
    response["from_date"] = doc_data[0].from_date
    response["to_date"] = doc_data[0].to_date
    response["half_day"] = doc_data[0].half_day
    response["total_leave_days"] = doc_data[0].total_leave_days
    response["leave_approver"] = doc_data[0].leave_approver
    response["leave_approver_name"] = doc_data[0].leave_approver_name
    response["status"] = doc_data[0].status
    response["posting_date"] = doc_data[0].posting_date
    response["department"] = doc_data[0].department
    response["description"] = doc_data[0].description

    attachments = frappe.db.sql(
        """ Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                        from `tabFile`  where `tabFile`.attached_to_doctype = "Leave Application"
                                        and `tabFile`.attached_to_name = "{name}"
                                        order by `tabFile`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )
    response["attachments"] = attachments

    comments = frappe.db.sql(
        """ Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Leave Application"
                                        and `tabComment`.reference_name = "{name}"
                                        and `tabComment`.comment_type = "Comment"
                                        order by `tabComment`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )
    # dssss
    response["comments"] = comments

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Leave Application" and disabled = 0 """,
        as_dict=1,
    )
    response["print_formats"] = print_formats
    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)

    if doc_data:
        return response
    else:
        return "لا يوجد"


@frappe.whitelist(allow_guest=True)
def employee_checkin(name):
    response = {}
    doc_data = frappe.db.get_all(
        "Employee Checkin",
        filters={"name": name},
        fields=[
            "name",
            "employee",
            "employee_name",
            "time",
            "log_type",
            "device_id",
            "skip_auto_attendance",
            "longitude",
            "latitude",
            "skip_auto_attendance",
            "docstatus",
        ],
    )
    if not doc_data:
        return "لا يوجد"
    response["name"] = doc_data[0].name
    response["employee"] = doc_data[0].employee
    response["employee_name"] = doc_data[0].employee_name
    response["time"] = doc_data[0].time
    response["log_type"] = doc_data[0].log_type
    response["device_id"] = doc_data[0].device_id
    response["skip_auto_attendance"] = doc_data[0].skip_auto_attendance
    response["longitude"] = doc_data[0].longitude
    response["latitude"] = doc_data[0].latitude
    response["docstatus"] = doc_data[0].docstatus

    attachments = frappe.db.sql(
        """ Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                        from `tabFile`  where `tabFile`.attached_to_doctype = "Employee Checkin"
                                        and `tabFile`.attached_to_name = "{name}"
                                        order by `tabFile`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )
    response["attachments"] = attachments

    comments = frappe.db.sql(
        """ Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Employee Checkin"
                                        and `tabComment`.reference_name = "{name}"
                                        and `tabComment`.comment_type = "Comment"
                                        order by `tabComment`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )
    # dssss
    response["comments"] = comments

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Employee Checkin" and disabled = 0 """,
        as_dict=1,
    )
    response["print_formats"] = print_formats
    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)

    if doc_data:
        return response
    else:
        return "لا يوجد"


@frappe.whitelist(allow_guest=True)
def employee(name):
    response = {}
    doc_data = frappe.db.get_all(
        "Employee",
        filters={"name": name},
        fields=[
            "name",
            "docstatus",
            "employee_name",
            "first_name",
            "last_name",
            "company",
            "employment_type",
            "status",
            "gender",
            "date_of_birth",
            "date_of_joining",
            "department",
            "designation",
            "branch",
            "expense_approver",
            "leave_approver",
            "attendance_device_id",
            "cell_number",
            "personal_email",
            "prefered_contact_email",
            "company_email",
            "prefered_email",
            "permanent_accommodation_type",
            "permanent_address",
            "current_accommodation_type",
            "current_address",
            "passport_number",
            "marital_status",
            "user_id",
            "holiday_list",
            "default_shift",
            "employee_number",
        ],
    )
    if not doc_data:
        return "لا يوجد"
    response["name"] = doc_data[0].name
    response["docstatus"] = doc_data[0].docstatus
    response["employee_name"] = doc_data[0].employee_name
    response["first_name"] = doc_data[0].first_name
    response["last_name"] = doc_data[0].last_name
    response["gender"] = doc_data[0].gender
    response["date_of_birth"] = doc_data[0].date_of_birth

    response["status"] = doc_data[0].status
    response["department"] = doc_data[0].department
    response["designation"] = doc_data[0].designation
    response["branch"] = doc_data[0].branch
    response["employment_type"] = doc_data[0].employment_type
    response["date_of_joining"] = doc_data[0].date_of_joining
    response["leave_approver"] = doc_data[0].leave_approver
    response["leave_approver_name"] = frappe.db.get_value(
        "User", doc_data[0].leave_approver, "full_name"
    )
    response["expense_approver"] = doc_data[0].expense_approver
    response["user_id"] = doc_data[0].user_id
    response["attendance_device_id"] = doc_data[0].attendance_device_id
    response["employee_number"] = doc_data[0].employee_number
    response["cell_number"] = doc_data[0].cell_number

    response["emails"] = {
        "personal_email": doc_data[0].get("personal_email", None),
        "prefered_email": doc_data[0].get("prefered_email", None),
        "company_email": doc_data[0].get("company_email", None),
    }

    response["address"] = {
        "current_address": doc_data[0].get("current_address", None),
        "permanent_address": doc_data[0].get("permanent_address", None),
    }
    response["holiday_list"] = doc_data[0].holiday_list
    response["default_shift"] = doc_data[0].default_shift

    attachments = frappe.db.sql(
        """ Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                        from `tabFile`  where `tabFile`.attached_to_doctype = "Employee"
                                        and `tabFile`.attached_to_name = "{name}"
                                        order by `tabFile`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )
    response["attachments"] = attachments

    comments = frappe.db.sql(
        """ Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Employee"
                                        and `tabComment`.reference_name = "{name}"
                                        and `tabComment`.comment_type = "Comment"
                                        order by `tabComment`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )
    # dssss
    response["comments"] = comments

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Employee" and disabled = 0 """,
        as_dict=1,
    )
    response["print_formats"] = print_formats
    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)

    con_attendance_request = frappe.db.get_all(
        "Attendance Request",
        filters={"employee": name},
    )
    count_con_attendance = len(con_attendance_request)
    attendance_request = {}

    connections = []

    if count_con_attendance > 0 and doc_data:
        attendance_request["name"] = "Attendance Request"
        attendance_request["count"] = count_con_attendance
        attendance_request[
            "icon"
        ] = "https://erpcloud.systems/files/attendance_request.png"
        connections.append(attendance_request)

    con_leave_application = frappe.db.get_all(
        "Leave Application",
        filters={"employee": name},
    )
    count_con_leave_application = len(con_leave_application)
    leave_application = {}

    if count_con_leave_application > 0 and doc_data:
        leave_application["name"] = "Leave Application"
        leave_application["count"] = count_con_leave_application
        leave_application[
            "icon"
        ] = "https://erpcloud.systems/files/leave_application.png"
        connections.append(leave_application)

    con_employee_advance = frappe.db.get_all(
        "Employee Advance",
        filters={"employee": name},
    )
    count_con_employee_advance = len(con_employee_advance)
    employee_advance = {}

    if count_con_employee_advance > 0 and doc_data:
        employee_advance["name"] = "Employee Advance"
        employee_advance["count"] = count_con_employee_advance
        employee_advance["icon"] = "https://erpcloud.systems/files/employee_advance.png"
        connections.append(employee_advance)

    con_expense_claim = frappe.db.get_all("Expense Claim", filters={"employee": name})
    count_con_expense_claim = len(con_expense_claim)
    expense_claim = {}

    if count_con_expense_claim > 0 and doc_data:
        expense_claim["name"] = "Expense Claim"
        expense_claim["count"] = count_con_expense_claim
        expense_claim["icon"] = "https://erpcloud.systems/files/expense_claim.png"
        connections.append(expense_claim)

    con_employee_grievance = frappe.db.get_all(
        "Employee Grievance", filters={"raised_by": name}
    )
    count_con_employee_grievance = len(con_employee_grievance)
    employee_grievance = {}

    if count_con_employee_grievance > 0 and doc_data:
        employee_grievance["name"] = "Employee Grievance"
        employee_grievance["count"] = count_con_employee_grievance
        employee_grievance[
            "icon"
        ] = "https://erpcloud.systems/files/employee_grievance.png"
        connections.append(employee_grievance)

    response["conn"] = connections

    if doc_data:
        return response
    else:
        return "لا يوجد"


@frappe.whitelist(allow_guest=True)
def attendance_request(name):
    response = {}
    doc_data = frappe.db.get_all(
        "Attendance Request",
        filters={"name": name},
        fields=[
            "name",
            "docstatus",
            "employee",
            "employee_name",
            "department",
            "company",
            "from_date",
            "to_date",
            "half_day",
            "half_day_date",
            "reason",
            "explanation",
            "longitude",
            "latitude",
            "location",
            "from_time",
            "to_time"
        ],
    )
    amended_to = frappe.db.get_value("Attendance Request", {"amended_from": name}, ["name"])
    if not doc_data:
        return "لا يوجد"
    response["name"] = doc_data[0].name
    response["amended_to"] = amended_to
    response["docstatus"] = doc_data[0].docstatus
    response["employee"] = doc_data[0].employee
    response["employee_name"] = doc_data[0].employee_name
    response["department"] = doc_data[0].department
    response["company"] = doc_data[0].company
    response["from_date"] = doc_data[0].from_date
    response["to_date"] = doc_data[0].to_date
    response["half_day"] = doc_data[0].half_day
    response["half_day_date"] = doc_data[0].half_day_date
    response["reason"] = doc_data[0].reason
    response["explanation"] = doc_data[0].explanation
    response["longitude"] = doc_data[0].longitude
    response["latitude"] = doc_data[0].latitude
    response["location"] = doc_data[0].location
    response["from_time"] = doc_data[0].from_time
    response["to_time"] = doc_data[0].to_time
    attachments = frappe.db.sql(
        """ Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                        from `tabFile`  where `tabFile`.attached_to_doctype = "Attendance Request"
                                        and `tabFile`.attached_to_name = "{name}"
                                        order by `tabFile`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )
    response["attachments"] = attachments

    comments = frappe.db.sql(
        """ Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Attendance Request"
                                        and `tabComment`.reference_name = "{name}"
                                        and `tabComment`.comment_type = "Comment"
                                        order by `tabComment`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )
    # dssss
    response["comments"] = comments

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Attendance Request" and disabled = 0 """,
        as_dict=1,
    )
    response["print_formats"] = print_formats
    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)

    if doc_data:
        return response
    else:
        return "لا يوجد"


@frappe.whitelist(allow_guest=True)
def employee_advance(name):
    response = {}
    doc_data = frappe.db.get_all(
        "Employee Advance",
        filters={"name": name},
        fields=[
            "name",
            "docstatus",
            "employee",
            "employee_name",
            "department",
            "posting_date",
            "currency",
            "exchange_rate",
            "repay_unclaimed_amount_from_salary",
            "purpose",
            "advance_amount",
            "paid_amount",
            "pending_amount",
            "claimed_amount",
            "return_amount",
            "status",
            "company",
            "advance_account",
            "mode_of_payment",
        ],
    )
    if not doc_data:
        return "لا يوجد"
    response["name"] = doc_data[0].name
    response["docstatus"] = doc_data[0].docstatus
    response["employee"] = doc_data[0].employee
    response["employee_name"] = doc_data[0].employee_name
    response["department"] = doc_data[0].department
    response["posting_date"] = doc_data[0].posting_date
    response["currency"] = doc_data[0].currency
    response["exchange_rate"] = doc_data[0].exchange_rate
    response["repay_unclaimed_amount_from_salary"] = doc_data[
        0
    ].repay_unclaimed_amount_from_salary
    response["purpose"] = doc_data[0].purpose
    response["advance_amount"] = doc_data[0].advance_amount
    response["paid_amount"] = doc_data[0].paid_amount
    response["pending_amount"] = doc_data[0].pending_amount
    response["claimed_amount"] = doc_data[0].claimed_amount
    response["return_amount"] = doc_data[0].return_amount
    response["status"] = doc_data[0].status
    response["company"] = doc_data[0].company
    response["advance_account"] = doc_data[0].advance_account
    response["mode_of_payment"] = doc_data[0].mode_of_payment

    attachments = frappe.db.sql(
        """ Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                        from `tabFile`  where `tabFile`.attached_to_doctype = "Employee Advance"
                                        and `tabFile`.attached_to_name = "{name}"
                                        order by `tabFile`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )
    response["attachments"] = attachments

    comments = frappe.db.sql(
        """ Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Employee Advance"
                                        and `tabComment`.reference_name = "{name}"
                                        and `tabComment`.comment_type = "Comment"
                                        order by `tabComment`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )
    # dssss
    response["comments"] = comments

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Employee Advance" and disabled = 0 """,
        as_dict=1,
    )
    response["print_formats"] = print_formats
    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)

    connections = []
    payment_entry_reference = frappe.db.get_all(
        "Payment Entry Reference", filters={"reference_name": name}
    )
    count_payment_entry_reference = len(payment_entry_reference)
    entry_reference = {}

    if count_payment_entry_reference > 0 and doc_data:
        entry_reference["name"] = "Payment Entry"
        entry_reference["count"] = count_payment_entry_reference
        entry_reference["icon"] = "https://erpcloud.systems/files/payment_entry.png"
        connections.append(entry_reference)

    con_expense_claim = frappe.db.get_all(
        "Expense Claim Advance", filters={"employee_advance": name}
    )
    count_con_expense_claim = len(con_expense_claim)
    expense_claim = {}

    if count_con_expense_claim > 0 and doc_data:
        expense_claim["name"] = "Expense Claim"
        expense_claim["count"] = count_con_expense_claim
        expense_claim["icon"] = "https://erpcloud.systems/files/expense_claim.png"
        connections.append(expense_claim)

    response["conn"] = connections
    if doc_data:
        return response
    else:
        return "لا يوجد"


@frappe.whitelist()
def get_pending_amount(employee, posting_date):
    employee_due_amount = frappe.get_all(
        "Employee Advance",
        filters={
            "employee": employee,
            "docstatus": 1,
            "posting_date": ("<=", posting_date),
        },
        fields=["advance_amount", "paid_amount"],
    )
    return sum([(emp.advance_amount - emp.paid_amount) for emp in employee_due_amount])


@frappe.whitelist(allow_guest=True)
def expense_claim(name):
    response = {}
    doc_data = frappe.db.get_all(
        "Expense Claim",
        filters={"name": name},
        fields=[
            "name",
            "docstatus",
            "employee",
            "employee_name",
            "department",
            "expense_approver",
            "approval_status",
            "is_paid",
            "total_sanctioned_amount",
            "total_taxes_and_charges",
            "total_advance_amount",
            "grand_total",
            "total_claimed_amount",
            "total_amount_reimbursed",
            "posting_date",
            "payable_account",
            "cost_center",
            "project",
            "status",
        ],
    )
    if not doc_data:
        return "لا يوجد"
    response["name"] = doc_data[0].name
    response["docstatus"] = doc_data[0].docstatus
    response["employee"] = doc_data[0].employee
    response["employee_name"] = doc_data[0].employee_name
    response["department"] = doc_data[0].department
    response["expense_approver"] = doc_data[0].expense_approver
    response["approval_status"] = doc_data[0].approval_status
    response["is_paid"] = doc_data[0].is_paid
    response["total_sanctioned_amount"] = doc_data[0].total_sanctioned_amount
    response["total_taxes_and_charges"] = doc_data[0].total_taxes_and_charges
    response["total_advance_amount"] = doc_data[0].total_advance_amount
    response["grand_total"] = doc_data[0].grand_total
    response["total_claimed_amount"] = doc_data[0].total_claimed_amount
    response["total_amount_reimbursed"] = doc_data[0].total_amount_reimbursed
    response["posting_date"] = doc_data[0].posting_date
    response["payable_account"] = doc_data[0].payable_account
    response["cost_center"] = doc_data[0].cost_center
    response["project"] = doc_data[0].project
    response["status"] = doc_data[0].status

    attachments = frappe.db.sql(
        """ Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                        from `tabFile`  where `tabFile`.attached_to_doctype = "Expense Claim"
                                        and `tabFile`.attached_to_name = "{name}"
                                        order by `tabFile`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )
    response["attachments"] = attachments

    comments = frappe.db.sql(
        """ Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Expense Claim"
                                        and `tabComment`.reference_name = "{name}"
                                        and `tabComment`.comment_type = "Comment"
                                        order by `tabComment`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )
    # dssss
    response["comments"] = comments

    expense_taxes_and_charges = frappe.db.sql(
        """
    SELECT idx, name, account_head, description, rate, tax_amount, total, cost_center
    FROM `tabExpense Taxes and Charges` expense_taxes_and_charges
    WHERE expense_taxes_and_charges.parent = "{name}"
    ORDER BY idx 
        """.format(
            name=name
        ),
        as_dict=1,
    )
    # expense_taxes_and_charges = frappe.db.get_all(
    #     "Expense Taxes And Charges",
    #     filters={"parent": name},
    #     order_by="idx",
    #     fields=[
    #         "idx",
    #         "name",
    #         "account_head",
    #         "description",
    #         "rate",
    #         "tax_amount",
    #         "total",
    #         "cost_center",
    #     ],
    # )

    if expense_taxes_and_charges and doc_data:
        response["taxes"] = expense_taxes_and_charges
    expense_claim_detail = frappe.db.get_all(
        "Expense Claim Detail",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "expense_date",
            "expense_type",
            "amount",
            "sanctioned_amount",
            "cost_center",
            "description",
            "default_account",
        ],
    )

    if expense_claim_detail and doc_data:
        response["expenses"] = expense_claim_detail

        # expense_taxes_and_charges = frappe.db.get_all(
        #     "Expense Taxes And Charges",
        #     filters={"parent": name},
        #     order_by="idx",
        #     fields=[
        #         "idx",
        #         "name",
        #         "account_head",
        #         "description",
        #         "rate",
        #         "tax_amount",
        #         "total",
        #         "cost_center",
        #     ],
        # )

        # if expense_taxes_and_charges and doc_data:
        #     response["taxes"] = expense_taxes_and_charges

        expense_claim_advance = frappe.db.get_all(
            "Expense Claim Advance",
            filters={"parent": name},
            order_by="idx",
            fields=[
                "idx",
                "name",
                "employee_advance",
                "posting_date",
                "advance_paid",
                "unclaimed_amount",
                "allocated_amount",
            ],
        )

    if expense_claim_advance and doc_data:
        response["claim_advance"] = expense_claim_advance

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Expense Claim" and disabled = 0 """,
        as_dict=1,
    )
    response["print_formats"] = print_formats
    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)

    connections = []
    payment_entry_reference = frappe.db.get_all(
        "Payment Entry Reference", filters={"reference_name": name}
    )
    count_payment_entry_reference = len(payment_entry_reference)
    entry_reference = {}

    if count_payment_entry_reference > 0 and doc_data:
        entry_reference["name"] = "Payment Entry"
        entry_reference["count"] = count_payment_entry_reference
        entry_reference["icon"] = "https://erpcloud.systems/files/payment_entry.png"
        connections.append(entry_reference)

    con_employee_advance = frappe.db.get_all(
        "Expense Claim Advance",
        filters={"employee_advance": ["!=", "null"], "parent": name},
    )
    count_con_employee_advance = len(con_employee_advance)
    employee_advance = {}

    if count_con_employee_advance > 0 and doc_data:
        employee_advance["name"] = "Employee Advance"
        employee_advance["count"] = count_con_employee_advance
        employee_advance["icon"] = "https://erpcloud.systems/files/employee_advance.png"
        connections.append(employee_advance)

    response["conn"] = connections
    if doc_data:
        return response
    else:
        return "لا يوجد"


@frappe.whitelist(allow_guest=True)
def loan_application(name):
    response = {}
    doc_data = frappe.db.get_all(
        "Loan Application",
        filters={"name": name},
        fields=[
            "name",
            "docstatus",
            "applicant_type",
            "applicant",
            "applicant_name",
            "posting_date",
            "loan_type",
            "posting_date",
            "is_term_loan",
            "loan_amount",
            "is_secured_loan",
            "rate_of_interest",
            "maximum_loan_amount",
            "repayment_method",
            "total_payable_amount",
            "repayment_periods",
            "repayment_amount",
            "total_payable_interest",
            "status",
        ],
    )
    if not doc_data:
        return "لا يوجد"
    response["name"] = doc_data[0].name
    response["docstatus"] = doc_data[0].docstatus
    response["applicant_type"] = doc_data[0].applicant_type
    response["applicant"] = doc_data[0].applicant
    response["applicant_name"] = doc_data[0].applicant_name
    response["posting_date"] = doc_data[0].posting_date
    response["loan_type"] = doc_data[0].loan_type
    response["is_term_loan"] = doc_data[0].is_term_loan
    response["loan_amount"] = doc_data[0].loan_amount
    response["is_secured_loan"] = doc_data[0].is_secured_loan
    response["rate_of_interest"] = doc_data[0].rate_of_interest
    response["maximum_loan_amount"] = doc_data[0].maximum_loan_amount
    response["repayment_method"] = doc_data[0].repayment_method
    response["total_payable_amount"] = doc_data[0].total_payable_amount
    response["repayment_periods"] = doc_data[0].repayment_periods
    response["repayment_amount"] = doc_data[0].repayment_amount
    response["total_payable_interest"] = doc_data[0].total_payable_interest
    response["status"] = doc_data[0].status

    attachments = frappe.db.sql(
        """ Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                        from `tabFile`  where `tabFile`.attached_to_doctype = "Loan Application"
                                        and `tabFile`.attached_to_name = "{name}"
                                        order by `tabFile`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )
    response["attachments"] = attachments

    comments = frappe.db.sql(
        """ Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Loan Application"
                                        and `tabComment`.reference_name = "{name}"
                                        and `tabComment`.comment_type = "Comment"
                                        order by `tabComment`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )
    # dssss
    response["comments"] = comments
    proposed_pledge = frappe.db.get_all(
        "Proposed Pledge",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "loan_security",
            "loan_security_name",
            "qty",
            "loan_security_price",
            "haircut",
            "amount",
            "post_haircut_amount",
        ],
    )

    if proposed_pledge and doc_data:
        response["expenses"] = proposed_pledge

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Loan Application" and disabled = 0 """,
        as_dict=1,
    )
    response["print_formats"] = print_formats
    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)
    if doc_data:
        return response
    else:
        return "لا يوجد"


@frappe.whitelist()
def address_query(link_doctype, link_name):
    link_doctype = link_doctype
    link_name = link_name

    condition = ""
    meta = frappe.get_meta("Address")
    searchfields = meta.get_search_fields()
    search_condition = ""

    return frappe.db.sql(
        """select
			`tabAddress`.name, `tabAddress`.city, `tabAddress`.country
		from
			`tabAddress`, `tabDynamic Link`
		where
			`tabDynamic Link`.parent = `tabAddress`.name and
			`tabDynamic Link`.parenttype = 'Address' and
			`tabDynamic Link`.link_doctype = "{link_doctype}" and
			`tabDynamic Link`.link_name = "{link_name}"
	 """.format(
            link_name=link_name, link_doctype=link_doctype
        ),
        as_dict=1,
    )


@frappe.whitelist()
def address(name):
    response = {}
    doc_data = frappe.db.get_all(
        "Address",
        filters={"name": name},
        fields=[
            "name",
            "address_title",
            "address_type",
            "address_line1",
            "city",
            "country",
            "is_shipping_address",
            "is_primary_address",
            "longitude",
            "latitude",
        ],
    )
    if not doc_data:
        return "لا يوجد"
    response["name"] = doc_data[0].name
    response["address_title"] = doc_data[0].address_title
    response["address_type"] = doc_data[0].address_type
    response["address_line1"] = doc_data[0].address_line1
    response["city"] = doc_data[0].city
    response["country"] = doc_data[0].country
    response["is_shipping_address"] = doc_data[0].is_shipping_address
    response["is_primary_address"] = doc_data[0].is_primary_address
    response["longitude"] = doc_data[0].longitude
    response["latitude"] = doc_data[0].latitude
    response["docstatus"] = 0

    attachments = frappe.db.sql(
        """ Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                        from `tabFile`  where `tabFile`.attached_to_doctype = "Address"
                                        and `tabFile`.attached_to_name = "{name}"
                                        order by `tabFile`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )
    response["attachments"] = attachments

    comments = frappe.db.sql(
        """ Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Address"
                                        and `tabComment`.reference_name = "{name}"
                                        and `tabComment`.comment_type = "Comment"
                                        order by `tabComment`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )
    # dssss
    response["comments"] = comments
    dynamic_link = frappe.db.get_all(
        "Dynamic Link",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "link_doctype",
            "link_name",
            "link_title",
        ],
    )

    if dynamic_link and doc_data:
        response["reference"] = dynamic_link

    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Address" and disabled = 0 """,
        as_dict=1,
    )
    response["print_formats"] = print_formats
    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)
    if doc_data:
        return response
    else:
        return "لا يوجد"


@frappe.whitelist()
def contact(name):
    response = {}
    doc_data = frappe.db.get_all(
        "Contact",
        filters={"name": name},
        fields=[
            "name",
            "first_name",
            "user",
            "mobile_no",
            "phone",
            "email_id",
            "is_primary_contact",
        ],
    )
    if not doc_data:
        return "لا يوجد"
    response["name"] = doc_data[0].name
    response["first_name"] = doc_data[0].first_name
    response["user"] = doc_data[0].user
    response["mobile_no"] = doc_data[0].mobile_no
    response["phone"] = doc_data[0].phone
    response["email_id"] = doc_data[0].email_id
    response["is_primary_contact"] = doc_data[0].is_primary_contact
    response["docstatus"] = 0

    attachments = frappe.db.sql(
        """ Select file_name, file_url,
                                        Date_Format(creation,'%d/%m/%Y') as date_added
                                        from `tabFile`  where `tabFile`.attached_to_doctype = "Contact"
                                        and `tabFile`.attached_to_name = "{name}"
                                        order by `tabFile`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )
    response["attachments"] = attachments

    comments = frappe.db.sql(
        """ Select creation, (Select `tabUser`.full_name from `tabUser` where `tabUser`.name = `tabComment`.owner) as owner, content
                                        from `tabComment`  where `tabComment`.reference_doctype = "Contact"
                                        and `tabComment`.reference_name = "{name}"
                                        and `tabComment`.comment_type = "Comment"
                                        order by `tabComment`.creation
                                    """.format(
            name=name
        ),
        as_dict=1,
    )
    # dssss
    response["comments"] = comments

    email_ids = frappe.db.get_all(
        "Contact Email",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "email_id",
            "is_primary",
        ],
    )

    if email_ids and doc_data:
        response["email_ids"] = email_ids

    phone_nos = frappe.db.get_all(
        "Contact Phone",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "phone",
            "is_primary_phone",
            "is_primary_mobile_no",
        ],
    )

    if phone_nos and doc_data:
        response["phone_nos"] = phone_nos

    links = frappe.db.get_all(
        "Dynamic Link",
        filters={"parent": name},
        order_by="idx",
        fields=[
            "idx",
            "name",
            "link_doctype",
            "link_name",
            "link_title",
        ],
    )

    if links and doc_data:
        response["links"] = links
    print_formats = frappe.db.sql(
        """ Select name from `tabPrint Format` where doc_type = "Contact" and disabled = 0 """,
        as_dict=1,
    )
    response["print_formats"] = print_formats
    pf_standard = {}
    pf_standard["name"] = "Standard"
    print_formats.append(pf_standard)
    if doc_data:
        return response
    else:
        return "لا يوجد"


@frappe.whitelist(methods=["GET"])
def workflow(name):
    workflow = frappe.get_doc("Workflow", name)
    # workflow.creation = humanize_datetime(str(workflow.creation))
    # workflow.modified = humanize_datetime(str(workflow.modified))
    return workflow

