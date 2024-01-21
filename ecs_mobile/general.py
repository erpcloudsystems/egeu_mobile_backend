from frappe.query_builder.functions import Convert
import frappe
import erpnext
from frappe import auth
import random
import datetime
import json, ast
from erpnext.accounts.utils import get_balance_on
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
import time


# this endpoint is trash
@frappe.whitelist()
def general_service(
        doctype,
        filter1="%%",
        filter2="%%",
        filter3="%%",
        filter4="%%",
        filter5="%%",
        filter6="%%",
        filter7="%%",
        filter8="%%",
        search_text="%%",
        cur_nam="%%",
        con_doc="%%",
        start=0,
        page_length=20,
        sort_field=None,
        sort_type=None,
):
    from .helpers import order_by, remove_html_tags

    ############################################ LEAD ############################################

    ########################### Lead Full List & Search ############################
    if doctype == "Sales Person" and con_doc == "%%":
        print("oj")
        conditions = {}
        if search_text != "%%":
            conditions["name"] = ["like", search_text]

        query = frappe.db.get_list(
            "Sales Person",
            or_filters=conditions,
            fields=["name", "commission_rate"],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Lead" and con_doc == "%%":
        conditions = {}
        conditions1 = {}
        if search_text != "%%":
            conditions1["name"] = ["like", search_text]
            conditions1["lead_name"] = ["like", search_text]
            conditions1["company_name"] = ["like", search_text]
            conditions1["mobile_no"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["lead_owner"] = filter2
        if filter3 != "%%":
            conditions["organization_lead"] = filter3

        if filter4 != "%%" and filter5 == "%%":
            conditions["creation"] = [">=", filter4]
        if filter5 != "%%" and filter4 == "%%":
            conditions["creation"] = ["<=", filter5]
        if filter4 != "%%" and filter5 != "%%":
            conditions["creation"] = ["between", [filter4, filter5]]

        query = frappe.db.get_list(
            "Lead",
            or_filters=conditions1,
            filters=conditions,
            fields=[
                "name",
                "lead_name",
                "company_name",
                "territory",
                "source",
                "market_segment",
                "status",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Quotations Connected With Lead & Search ############################
    if doctype == "Quotation" and con_doc == "Lead":
        connections = frappe.db.sql(
            """ select name, quotation_to, customer_name, transaction_date, currency, grand_total, status
                from `tabQuotation` where `party_name` = '{cur_nam}'
                and (`tabQuotation`.name like '%{search_text}%' or `tabQuotation`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Opportunities Connected With Lead & Search ############################
    if doctype == "Opportunity" and con_doc == "Lead":
        connections = frappe.db.sql(
            """ select name,opportunity_from,customer_name,transaction_date,opportunity_type,sales_stage,status
                from `tabOpportunity` where `party_name` = '{cur_nam}'
                and (`tabOpportunity`.name like '%{search_text}%' or `tabOpportunity`.customer_name like '%{search_text}%' or `tabOpportunity`.party_name like '%{search_text}%' or `tabOpportunity`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ############################################ OPPORTUNITY ############################################

    ########################### Opportunity Full List & Search ############################

    if doctype == "Opportunity" and con_doc == "%%":
        conditions = {}
        conditions1 = {}
        if search_text != "%%":
            conditions1["name"] = ["like", search_text]
            conditions1["customer_name"] = ["like", search_text]
            conditions1["party_name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["opportunity_from"] = filter2
        if filter3 != "%%":
            conditions["party_name"] = filter3
        if filter4 != "%%":
            conditions["opportunity_type"] = filter4

        if filter5 != "%%" and filter6 == "%%":
            conditions["transaction_date"] = [">=", filter5]
        if filter6 != "%%" and filter5 == "%%":
            conditions["transaction_date"] = ["<=", filter6]
        if filter5 != "%%" and filter6 != "%%":
            conditions["transaction_date"] = ["between", [filter5, filter6]]

        query = frappe.db.get_list(
            "Opportunity",
            or_filters=conditions1,
            filters=conditions,
            fields=[
                "name",
                "opportunity_from",
                "customer_name",
                "transaction_date",
                "opportunity_type",
                "sales_stage",
                "status",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Quotations Connected With Opportunity & Search ############################
    if doctype == "Quotation" and con_doc == "Opportunity":
        connections = frappe.db.sql(
            """ select name, quotation_to, customer_name, transaction_date, currency, grand_total, status
                from `tabQuotation` where `opportunity` = '{cur_nam}'
                and (`tabQuotation`.name like '%{search_text}%' or `tabQuotation`.customer_name like '%{search_text}%' or `tabQuotation`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Supplier Quotations Connected With Opportunity & Search ############################
    if doctype == "Supplier Quotation" and con_doc == "Opportunity":
        connections = frappe.db.sql(
            """ select name,supplier,transaction_date,valid_till,currency,grand_total,status
                from `tabSupplier Quotation` where `opportunity` = '{cur_nam}'
                and (`tabSupplier Quotation`.name like '%{search_text}%' or `tabSupplier Quotation`.supplier like '%{search_text}%' or `tabSupplier Quotation`.supplier_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ############################################ QUOTATION ############################################

    ########################### Quotation Full List & Search ############################

    if doctype == "Quotation" and con_doc == "%%":
        conditions = {}
        conditions1 = {}
        if search_text != "%%":
            conditions1["name"] = ["like", search_text]
            conditions1["customer_name"] = ["like", search_text]
            conditions1["party_name"] = ["like", search_text]
            conditions1["customer_address"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["quotation_to"] = filter2
        if filter3 != "%%":
            conditions["customer_name"] = filter3
        if filter4 != "%%":
            conditions["order_type"] = filter4

        if filter5 != "%%" and filter6 == "%%":
            conditions["transaction_date"] = [">=", filter5]
        if filter6 != "%%" and filter5 == "%%":
            conditions["transaction_date"] = ["<=", filter6]
        if filter5 != "%%" and filter6 != "%%":
            conditions["transaction_date"] = ["between", [filter5, filter6]]

        query = frappe.db.get_list(
            "Quotation",
            or_filters=conditions1,
            filters=conditions,
            fields=[
                "name",
                "quotation_to",
                "customer_name",
                "transaction_date",
                "grand_total",
                "status",
                "currency",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    '''
    if doctype == "Quotation" and con_doc == '%%':
        conditions = ""
        if search_text != '%%':
            conditions += " and (`tabQuotation`.name like '%{search_text}%' or `tabQuotation`.customer_name like '%{search_text}%' or `tabQuotation`.party_name like '%{search_text}%') ".format(
                search_text=search_text)
        if filter1 != '%%':
            conditions += " and `tabQuotation`.status = '{filter1}' ".format(filter1=filter1)
        if filter2 != '%%':
            conditions += " and `tabQuotation`.quotation_to = '{filter2}' ".format(filter2=filter2)
        if filter3 != '%%':
            conditions += " and `tabQuotation`.customer_name = '{filter3}' ".format(filter3=filter3)
        if filter4 != '%%':
            conditions += " and `tabQuotation`.order_type = '{filter4}' ".format(filter4=filter4)
        if filter5 != '%%':
            conditions += " and `tabQuotation`.transaction_date >= '{filter5}' ".format(filter5=filter5)
        if filter6 != '%%':
            conditions += " and `tabQuotation`.transaction_date <= '{filter6}' ".format(filter6=filter6)

        query = frappe.db.sql(
            """ select name, quotation_to, customer_name, transaction_date, grand_total,
                   status
                from `tabQuotation`
                where `tabQuotation`.docstatus in (0, 1, 2)
                {conditions}
                order by modified desc
                LIMIT {start},{page_length}
            """.format(conditions=conditions, start=start, page_length=page_length), as_dict=1)
        if query:
            return query
        else:
            return "لا يوجد !"
    '''

    ########################### Sales Orders Connected With Quotation & Search ############################
    if doctype == "Sales Order" and con_doc == "Quotation":
        connections = frappe.db.sql(
            """ select distinct `tabSales Order`.name as name,`tabSales Order`.customer_name as customer_name,`tabSales Order`.customer_address as customer_address,
                       `tabSales Order`.transaction_date as transaction_date,`tabSales Order`.currency as currency,`tabSales Order`.grand_total as grand_total,`tabSales Order`.status as status
                from `tabSales Order` join `tabSales Order Item` on `tabSales Order`.name = `tabSales Order Item`.parent
                where `tabSales Order Item`.prevdoc_docname = '{cur_nam}'
                and (`tabSales Order`.name like '%{search_text}%' or `tabSales Order`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ############################################ CUSTOMER ############################################

    ########################### Customer Full List & Search ############################

    if doctype == "Customer" and con_doc == "%%":
        conditions1 = {}
        conditions = {"disabled": ["=", 0]}
        if search_text != "%%":
            conditions1["name"] = ["like", search_text]
            conditions1["customer_name"] = ["like", search_text]
            conditions1["code"] = ["like", search_text]
        if filter1 != "%%":
            conditions["customer_group"] = filter1
        if filter2 != "%%":
            conditions["territory"] = filter2
        if filter3 != "%%":
            conditions["customer_type"] = filter3

        if filter4 != "%%" and filter5 == "%%":
            conditions["creation"] = [">=", filter4]
        if filter5 != "%%" and filter4 == "%%":
            conditions["creation"] = ["<=", filter5]
        if filter4 != "%%" and filter5 != "%%":
            conditions["creation"] = ["between", [filter4, filter5]]

        query = frappe.db.get_list(
            "Customer",
            or_filters=conditions1,
            filters=conditions,
            fields=[
                "name",
                "code",
                "customer_name",
                "customer_group",
                "customer_type",
                "territory",
                "mobile2",
                "tax_id",
                "customer_primary_address",
                "customer_primary_contact",
                "default_currency",
                "default_price_list",
                "payment_terms",
                "default_sales_partner",
                "default_currency",
                "new_governorate"
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            for customer in query:
                sales_team = frappe.get_doc("Customer", customer["name"]).sales_team
                if sales_team:
                    customer["sales_person"] = sales_team[0].sales_person
                customer.governorate = customer.pop("new_governorate", None)
            return query
        else:
            return "لا يوجد !"

    ########################### Quotations Connected With Customer & Search ############################
    if doctype == "Quotation" and con_doc == "Customer":
        connections = frappe.db.sql(
            """ select name, quotation_to, customer_name, transaction_date, currency, grand_total, status
                from `tabQuotation` where `party_name` = '{cur_nam}'
                and (`tabQuotation`.name like '%{search_text}%' or `tabQuotation`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Opportunities Connected With Customer & Search ############################
    if doctype == "Opportunity" and con_doc == "Customer":
        connections = frappe.db.sql(
            """ select name,opportunity_from,customer_name,transaction_date,opportunity_type,sales_stage,status
                 from `tabOpportunity` where `party_name` = '{cur_nam}'
                and (`tabOpportunity`.name like '%{search_text}%' or `tabOpportunity`.customer_name like '%{search_text}%' or `tabOpportunity`.party_name like '%{search_text}%' or `tabOpportunity`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Sales Orders Connected With Customer & Search ############################
    if doctype == "Sales Order" and con_doc == "Customer":
        connections = frappe.db.sql(
            """ select name,customer_name,customer_address,transaction_date,currency,grand_total,status
                from `tabSales Order` where `customer` = '{cur_nam}'
                and (`tabSales Order`.name like '%{search_text}%' or `tabSales Order`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Delivery Notes Connected With Customer & Search ############################
    if doctype == "Delivery Note" and con_doc == "Customer":
        connections = frappe.db.sql(
            """ select name,customer,territory,posting_date,set_warehouse,currency,status
                from `tabDelivery Note` where `customer` = '{cur_nam}'
                and (`tabDelivery Note`.name like '%{search_text}%' or `tabDelivery Note`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Sales Invoices Connected With Customer & Search ############################
    if doctype == "Sales Invoice" and con_doc == "Customer":
        connections = frappe.db.sql(
            """ select name,customer_name,customer_address,posting_date,currency,grand_total,status
                from `tabSales Invoice` where `customer` = '{cur_nam}'
                and (`tabSales Invoice`.name like '%{search_text}%' or `tabSales Invoice`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Payment Entries Connected With Customer & Search ############################
    if doctype == "Payment Entry" and con_doc == "Customer":
        connections = frappe.db.sql(
            """ select name,party_name,payment_type,mode_of_payment,posting_date,paid_from_account_currency as currency,paid_amount as base_paid_amount,status
                from `tabPayment Entry` where `party` = '{cur_nam}'
                and (`tabPayment Entry`.name like '%{search_text}%' or `tabPayment Entry`.mode_of_payment like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Payment Entries Connected With Supplier & Search ############################
    if doctype == "Payment Entry" and con_doc == "Supplier":
        connections = frappe.db.sql(
            """ select name,party_name,payment_type,mode_of_payment,posting_date,paid_amount as base_paid_amount, paid_from_account_currency as currency,status
                 from `tabPayment Entry` where `party` = '{cur_nam}'
                 and (`tabPayment Entry`.name like '%{search_text}%' or `tabPayment Entry`.mode_of_payment like '%{search_text}%') LIMIT {start},{page_length}
             """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ############################################ SALES ORDER ############################################

    ########################### Sales Order Full List & Search ############################

    if doctype == "Sales Order" and con_doc == "%%":
        conditions1 = {}
        conditions = {}
        if search_text != "%%":
            conditions1["name"] = ["like", search_text]
            conditions1["customer_name"] = ["like", search_text]
            conditions1["customer"] = ["like", search_text]
            conditions1["customer_address"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["customer"] = filter2
        if filter3 != "%%":
            conditions["delivery_status"] = filter3
        if filter4 != "%%":
            conditions["billing_status"] = filter4
        if filter5 != "%%" and filter6 == "%%":
            conditions["transaction_date"] = [">=", filter5]
        if filter6 != "%%" and filter5 == "%%":
            conditions["transaction_date"] = ["<=", filter6]
        if filter5 != "%%" and filter6 != "%%":
            conditions["transaction_date"] = ["between", [filter5, filter6]]
        if filter7 != "%%" and filter8 == "%%":
            conditions["delivery_date"] = [">=", filter7]
        if filter8 != "%%" and filter7 == "%%":
            conditions["delivery_date"] = ["<=", filter8]
        if filter7 != "%%" and filter8 != "%%":
            conditions["delivery_date"] = ["between", [filter7, filter8]]

        query = frappe.db.get_list(
            "Sales Order",
            or_filters=conditions1,
            filters=conditions,
            fields=[
                "name",
                "customer_name",
                "customer_address",
                "transaction_date",
                "grand_total",
                "status",
                "currency",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    '''
    if doctype == "Sales Order" and con_doc == '%%':
        conditions = ""
        if search_text != '%%':
            conditions += " and (`tabSales Order`.name like '%{search_text}%' or `tabSales Order`.customer_name like '%{search_text}%' or `tabSales Order`.customer like '%{search_text}%') ".format(
                search_text=search_text)
        if filter1 != '%%':
            conditions += " and `tabSales Order`.status = '{filter1}' ".format(filter1=filter1)
        if filter2 != '%%':
            conditions += " and `tabSales Order`.customer = '{filter2}' ".format(filter2=filter2)
        if filter3 != '%%':
            conditions += " and `tabSales Order`.delivery_status = '{filter3}' ".format(filter3=filter3)
        if filter4 != '%%':
            conditions += " and `tabSales Order`.billing_status = '{filter4}' ".format(filter4=filter4)
        if filter5 != '%%':
            conditions += " and `tabSales Order`.transaction_date >= '{filter5}' ".format(filter5=filter5)
        if filter6 != '%%':
            conditions += " and `tabSales Order`.transaction_date <= '{filter6}' ".format(filter6=filter6)

        query = frappe.db.sql(
            """ select name, customer_name, customer_address, transaction_date,
                   grand_total, status
                from `tabSales Order`
                where `tabSales Order`.docstatus in (0, 1, 2)
                {conditions}
                order by modified desc
                LIMIT {start},{page_length}
            """.format(conditions=conditions, start=start, page_length=page_length), as_dict=1)
        if query:
            return query
        else:
            return "لا يوجد !"
    '''

    ########################### Sales Invoices Connected With Sales Order & Search ############################
    if doctype == "Sales Invoice" and con_doc == "Sales Order":
        connections = frappe.db.sql(
            """ select distinct `tabSales Invoice`.name as name,`tabSales Invoice`.customer_name as customer_name,`tabSales Invoice`.customer_address as customer_address,
                       `tabSales Invoice`.posting_date as posting_date, `tabSales Invoice`.currency as currency, `tabSales Invoice`.grand_total as grand_total,`tabSales Invoice`.status as status
                from `tabSales Invoice` join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent
                where `tabSales Invoice Item`.sales_order = '{cur_nam}'
                and (`tabSales Invoice`.name like '%{search_text}%' or `tabSales Invoice`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Delivery Notes Connected With Sales Order & Search ############################
    if doctype == "Delivery Note" and con_doc == "Sales Order":
        connections = frappe.db.sql(
            """ select distinct `tabDelivery Note`.name as name,`tabDelivery Note`.customer as customer,`tabDelivery Note`.territory as territory,
                       `tabDelivery Note`.posting_date as posting_date,`tabDelivery Note`.set_warehouse as set_warehouse,`tabDelivery Note`.currency as currency,`tabDelivery Note`.status as status
                from `tabDelivery Note` join `tabDelivery Note Item` on `tabDelivery Note`.name = `tabDelivery Note Item`.parent
                where `tabDelivery Note Item`.against_sales_order = '{cur_nam}'
                and (`tabDelivery Note`.name like '%{search_text}%' or `tabDelivery Note`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Material Requests Connected With Sales Order & Search ############################
    if doctype == "Material Request" and con_doc == "Sales Order":
        connections = frappe.db.sql(
            """ select distinct `tabMaterial Request`.name as name,`tabMaterial Request`.material_request_type as material_request_type,
                      `tabMaterial Request`.transaction_date as transaction_date,`tabMaterial Request`.set_warehouse as set_warehouse,`tabMaterial Request`.status as status
                from `tabMaterial Request` join `tabMaterial Request Item` on `tabMaterial Request`.name = `tabMaterial Request Item`.parent
                where `tabMaterial Request Item`.sales_order = '{cur_nam}'
                and (`tabMaterial Request`.name like '%{search_text}%' or `tabMaterial Request`.material_request_type like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Purchase Orders Connected With Sales Order & Search ############################
    if doctype == "Purchase Order" and con_doc == "Sales Order":
        connections = frappe.db.sql(
            """ select distinct `tabPurchase Order`.name as name,`tabPurchase Order`.supplier as supplier, `tabPurchase Order`.grand_total as grand_total,
                      `tabPurchase Order`.transaction_date as transaction_date,`tabPurchase Order`.set_warehouse as set_warehouse,
                      `tabPurchase Order`.currency as currency, `tabPurchase Order`.status as status
                from `tabPurchase Order` join `tabPurchase Order Item` on `tabPurchase Order`.name = `tabPurchase Order Item`.parent
                where `tabPurchase Order Item`.sales_order = '{cur_nam}'
                and (`tabPurchase Order`.name like '%{search_text}%' or `tabPurchase Order`.supplier_address like '%{search_text}%' or `tabPurchase Order`.supplier like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Quotations Connected With Sales Order & Search ############################
    if doctype == "Quotation" and con_doc == "Sales Order":
        connections = frappe.db.sql(
            """ select distinct `tabQuotation`.name as name, `tabQuotation`.quotation_to as quotation_to, `tabQuotation`.customer_name as customer_name,
                       `tabQuotation`.transaction_date as transaction_date, `tabQuotation`.currency as currency,`tabQuotation`.grand_total as grand_total, `tabQuotation`.status as status
                from `tabQuotation` join `tabSales Order Item` on `tabQuotation`.name = `tabSales Order Item`.prevdoc_docname
                where `tabSales Order Item`.parent = '{cur_nam}'
                and (`tabQuotation`.name like '%{search_text}%' or `tabQuotation`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Payment Entries Connected With Sales Order & Search ############################
    if doctype == "Payment Entry" and con_doc == "Sales Order":
        connections = frappe.db.sql(
            """ select distinct `tabPayment Entry`.name as name,`tabPayment Entry`.party_name as party_name,
                       `tabPayment Entry`.payment_type as payment_type,`tabPayment Entry`.mode_of_payment as mode_of_payment, `tabPayment Entry`.paid_from_account_currency as currency,
                       `tabPayment Entry`.posting_date as posting_date,`tabPayment Entry`.paid_amount as base_paid_amount,`tabPayment Entry`.status as status
                from `tabPayment Entry` join `tabPayment Entry Reference` on `tabPayment Entry`.name = `tabPayment Entry Reference`.parent
                where `tabPayment Entry Reference`.reference_name = '{cur_nam}'
                and (`tabPayment Entry`.name like '%{search_text}%' or `tabPayment Entry`.mode_of_payment like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ############################################ SALES INVOICE ############################################

    ########################### Sales Invoice Full List & Search ############################

    if doctype == "Sales Invoice" and con_doc == "%%":
        conditions1 = {}
        conditions = {}
        if search_text != "%%":
            conditions1["name"] = ["like", search_text]
            conditions1["customer_name"] = ["like", search_text]
            conditions1["customer"] = ["like", search_text]
            conditions1["customer_address"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["customer"] = filter2

        if filter3 != "%%" and filter4 == "%%":
            conditions["posting_date"] = [">=", filter3]
        if filter4 != "%%" and filter3 == "%%":
            conditions["posting_date"] = ["<=", filter4]
        if filter3 != "%%" and filter4 != "%%":
            conditions["posting_date"] = ["between", [filter3, filter4]]

        query = frappe.db.get_list(
            "Sales Invoice",
            or_filters=conditions1,
            filters=conditions,
            fields=[
                "name",
                "customer_name",
                "customer_address",
                "posting_date",
                "grand_total",
                "status",
                "currency",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            if filter6 != "%%" and filter2 != "%%":
                filters = [
                    ["Sales Invoice", "customer", "=", filter2],
                    ["Sales Invoice Item", "item_code", "=", filter6],
                ]
                query = frappe.db.get_all(
                    "Sales Invoice",
                    filters=filters,
                    fields=[
                        "name",
                        "customer_name",
                        "customer_address",
                        "posting_date",
                        "grand_total",
                        "status",
                        "currency",
                    ],
                )
            return query
        else:
            return "لا يوجد !"

    '''
    if doctype == "Sales Invoice" and con_doc == '%%':
        conditions = ""
        if search_text != '%%':
            conditions += " and (`tabSales Invoice`.name like '%{search_text}%' or `tabSales Invoice`.customer_name like '%{search_text}%' or `tabSales Invoice`.customer like '%{search_text}%') ".format(
                search_text=search_text)
        if filter1 != '%%':
            conditions += " and `tabSales Invoice`.status = '{filter1}' ".format(filter1=filter1)
        if filter2 != '%%':
            conditions += " and `tabSales Invoice`.customer = '{filter2}' ".format(filter2=filter2)
        if filter3 != '%%':
            conditions += " and `tabSales Invoice`.posting_date >= '{filter3}' ".format(filter3=filter3)
        if filter4 != '%%':
            conditions += " and `tabSales Invoice`.posting_date <= '{filter4}' ".format(filter4=filter4)

        query = frappe.db.sql(
            """ select name, customer_name, customer_address, posting_date, grand_total,
                   status
                from `tabSales Invoice`
                where `tabSales Invoice`.docstatus in (0, 1, 2)
                {conditions}
                order by modified desc
                LIMIT {start},{page_length}
            """.format(conditions=conditions, start=start, page_length=page_length), as_dict=1)
        if query:
            return query
        else:
            return "لا يوجد !"
    '''

    ########################### Sales Orders Connected With Sales Invoice & Search ############################
    if doctype == "Sales Order" and con_doc == "Sales Invoice":
        connections = frappe.db.sql(
            """ select distinct `tabSales Order`.name as name,`tabSales Order`.customer_name as customer_name,`tabSales Order`.customer_address as customer_address,
                    `tabSales Order`.transaction_date as transaction_date, `tabSales Order`.currency as currency, `tabSales Order`.grand_total as grand_total,`tabSales Order`.status as status
                from `tabSales Order` join `tabSales Invoice Item` on `tabSales Order`.name = `tabSales Invoice Item`.sales_order
                where `tabSales Invoice Item`.parent = '{cur_nam}'
                and (`tabSales Order`.name like '%{search_text}%' or `tabSales Order`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Delivery Notes Connected With Sales Invoice & Search ############################
    if doctype == "Delivery Note" and con_doc == "Sales Invoice":
        connections = frappe.db.sql(
            """ select distinct `tabDelivery Note`.name as name,`tabDelivery Note`.customer as customer,`tabDelivery Note`.territory as territory,
                       `tabDelivery Note`.posting_date as posting_date,`tabDelivery Note`.set_warehouse as set_warehouse, `tabDelivery Note`.currency as currency,
                       `tabDelivery Note`.status as status
                from `tabDelivery Note` join `tabDelivery Note Item` on `tabDelivery Note`.name = `tabDelivery Note Item`.parent
                where `tabDelivery Note Item`.against_sales_invoice = '{cur_nam}'
                and (`tabDelivery Note`.name like '%{search_text}%' or `tabDelivery Note`.customer_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Payment Entries Connected With Sales Invoice & Search ############################
    if doctype == "Payment Entry" and con_doc == "Sales Invoice":
        connections = frappe.db.sql(
            """ select distinct `tabPayment Entry`.name as name,`tabPayment Entry`.party_name as party_name,
                       `tabPayment Entry`.payment_type as payment_type,`tabPayment Entry`.mode_of_payment as mode_of_payment,
                       `tabPayment Entry`.posting_date as posting_date,`tabPayment Entry`.paid_amount as base_paid_amount,
                       `tabPayment Entry`.status as status, `tabPayment Entry`.paid_from_account_currency as currency
                from `tabPayment Entry` join `tabPayment Entry Reference` on `tabPayment Entry`.name = `tabPayment Entry Reference`.parent
                where `tabPayment Entry Reference`.reference_name = '{cur_nam}'
                and (`tabPayment Entry`.name like '%{search_text}%' or `tabPayment Entry`.mode_of_payment like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )

        if connections:
            return connections

        else:
            return "لا يوجد روابط !"

    ############################################ PAYMENT ENTRY ############################################

    ########################### Payment Entry Full List & Search ############################

    if doctype == "Payment Entry" and con_doc == "%%":
        conditions1 = {}
        conditions = {}
        if search_text != "%%":
            conditions1["name"] = ["like", search_text]
            conditions1["party_name"] = ["like", search_text]
            conditions1["mode_of_payment"] = ["like", search_text]
            conditions1["party"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["payment_type"] = filter2
        if filter3 != "%%":
            conditions["mode_of_payment"] = filter3
        if filter4 != "%%":
            conditions["party_type"] = filter4
        if filter5 != "%%":
            conditions["party"] = filter5
        if filter6 != "%%" and filter7 == "%%":
            conditions["posting_date"] = [">=", filter6]
        if filter7 != "%%" and filter6 == "%%":
            conditions["posting_date"] = ["<=", filter7]
        if filter6 != "%%" and filter7 != "%%":
            conditions["posting_date"] = ["between", [filter6, filter7]]
        query = frappe.db.get_list(
            "Payment Entry",
            or_filters=conditions1,
            filters=conditions,
            fields=[
                "name",
                "party_name",
                "payment_type",
                "mode_of_payment",
                "posting_date",
                "paid_amount as base_paid_amount",
                "paid_from_account_currency as currency",
                "status",
                "company",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )

        """
        for x in range(len(query)):

            currency = frappe.db.get_value("Company", {"name": query[x].company}, "default_currency")

            query[x]["currency"] = currency
        """
        if query:
            return query
        else:
            return "لا يوجد !"

    '''
    if doctype == "Payment Entry" and con_doc == '%%':
        conditions = ""
        if search_text != '%%':
            conditions += " and (`tabPayment Entry`.name like '%{search_text}%' or `tabPayment Entry`.party_name like '%{search_text}%' or `tabPayment Entry`.party like '%{search_text}%') ".format(
                search_text=search_text)
        if filter1 != '%%':
            conditions += " and `tabPayment Entry`.status = '{filter1}' ".format(filter1=filter1)
        if filter2 != '%%':
            conditions += " and `tabPayment Entry`.payment_type = '{filter2}' ".format(filter2=filter2)
        if filter3 != '%%':
            conditions += " and `tabPayment Entry`.mode_of_payment = '{filter3}' ".format(filter3=filter3)
        if filter4 != '%%':
            conditions += " and `tabPayment Entry`.party_type = '{filter4}' ".format(filter4=filter4)
        if filter5 != '%%':
            conditions += " and `tabPayment Entry`.party = '{filter5}' ".format(filter5=filter5)
        if filter6 != '%%':
            conditions += " and `tabPayment Entry`.posting_date >= '{filter6}' ".format(filter6=filter6)
        if filter7 != '%%':
            conditions += " and `tabPayment Entry`.posting_date <= '{filter7}' ".format(filter7=filter7)

        query = frappe.db.sql(
            """ select name, party_name, payment_type, mode_of_payment, posting_date,
                   paid_amount, status
                from `tabPayment Entry`
                where `tabPayment Entry`.docstatus in (0, 1, 2)
                {conditions}
                order by modified desc
                LIMIT {start},{page_length}
            """.format(conditions=conditions, start=start, page_length=page_length), as_dict=1)
        if query:
            return query
        else:
            return "لا يوجد !"
    '''

    ########################### Journal Entry Full List & Search ############################
    if doctype == "Journal Entry" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["title"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["voucher_type"] = filter1
        if filter2 != "%%" and filter3 == "%%":
            conditions["posting_date"] = [">=", filter2]
        if filter3 != "%%" and filter2 == "%%":
            conditions["posting_date"] = ["<=", filter3]
        if filter2 != "%%" and filter3 != "%%":
            conditions["posting_date"] = ["between", [filter2, filter3]]

        query = frappe.db.get_list(
            "Journal Entry",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "docstatus",
                "voucher_type",
                "posting_date",
                "total_debit",
                "total_credit",
                "mode_of_payment",
                "cheque_no",
                "cheque_date",
                "remark",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"
    ############################################ LEAD SOURCE ############################################

    ########################### Lead Source Full List & Search ############################
    if doctype == "Lead Source" and con_doc == "%%":
        query = frappe.db.get_list(
            "Lead Source",
            or_filters=[
                {"name": ["like", search_text]},
                {"source_name": ["like", search_text]},
            ],
            fields=["name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ PROJECT ############################################

    ########################### Project Segment Full List & Search ############################
    if doctype == "Project" and con_doc == "%%":
        query = frappe.db.get_list(
            "Project",
            filters=[{"is_active": ["=", "Yes"]}],
            or_filters=[
                {"name": ["like", search_text]},
                {"project_name": ["like", search_text]},
            ],
            fields=["name", "project_name", "status"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ PAYMENT TERMS TEMPLATE ############################################

    ########################### Payment Terms Template Full List & Search ############################
    if doctype == "Payment Terms Template" and con_doc == "%%":
        query = frappe.db.get_list(
            "Payment Terms Template",
            or_filters=[
                {"name": ["like", search_text]},
                {"template_name": ["like", search_text]},
            ],
            fields=["name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ MARKET SEGEMENT ############################################

    ########################### Market Segment Full List & Search ############################
    if doctype == "Market Segment" and con_doc == "%%":
        query = frappe.db.get_list(
            "Market Segment",
            or_filters=[
                {"name": ["like", search_text]},
                {"market_segment": ["like", search_text]},
            ],
            fields=["name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ TERRITORY ############################################

    ########################### Territory Full List & Search ############################
    if doctype == "Territory" and con_doc == "%%":
        query = frappe.db.get_list(
            "Territory",
            filters=[{"is_group": ["=", 0]}],
            or_filters=[
                {"name": ["like", search_text]},
                {"territory_name": ["like", search_text]},
            ],
            fields=["name", "parent_territory"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ WAREHOUSE ############################################

    ########################### Warehouse Full List & Search ############################
    if doctype == "Warehouse" and con_doc == "%%":
        if filter1=="1":
            query = frappe.db.get_list(
            "Warehouse",
            filters={"mobile": 1,"is_group": ["=", 0]},
            fields=["name", "warehouse_name", "warehouse_type", "parent_warehouse"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        else:
            query = frappe.db.get_list(
                "Warehouse",
                filters=[{"is_group": ["=", 0]}],
                or_filters=[
                    {"name": ["like", search_text]},
                    {"warehouse_name": ["like", search_text]},
                ],
                fields=["name", "warehouse_name", "warehouse_type", "parent_warehouse"],
                order_by="name asc",
                start=start,
                page_length=page_length,
            )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ COUNTRY ############################################

    ########################### Country Full List & Search ############################
    if doctype == "Country" and con_doc == "%%":
        query = frappe.db.get_list(
            "Country",
            or_filters=[
                {"name": ["like", search_text]},
                {"country_name": ["like", search_text]},
            ],
            fields=["name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ OPPORTUNITY TYPE ############################################

    ########################### Opportunity Type Full List & Search ############################
    if doctype == "Opportunity Type" and con_doc == "%%":
        query = frappe.db.get_list(
            "Opportunity Type",
            or_filters=[{"name": ["like", search_text]}],
            fields=["name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ CUSTOMER GROUP ############################################

    ########################### Customer Group Full List & Search ############################
    if doctype == "Customer Group" and con_doc == "%%":
        query = frappe.db.get_list(
            "Customer Group",
            filters=[{"is_group": ["=", 0]}],
            or_filters=[
                {"name": ["like", search_text]},
                {"customer_group_name": ["like", search_text]},
            ],
            fields=["name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ ITEM GROUP ############################################

    ########################### Item Group Full List & Search ############################
    if doctype == "Item Group" and con_doc == "%%":
        query = frappe.db.get_list(
            "Item Group",
            or_filters=[
                {"name": ["like", search_text]},
                {"item_group_name": ["like", search_text]},
            ],
            fields=["name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ BRAND ############################################

    ########################### Brand Full List & Search ############################
    if doctype == "Brand" and con_doc == "%%":
        query = frappe.db.get_list(
            "Brand",
            or_filters=[
                {"name": ["like", search_text]},
                {"brand": ["like", search_text]},
            ],
            fields=["name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ UOM ############################################

    ########################### UOM Full List & Search ############################
    if doctype == "UOM" and con_doc == "%%":
        query = frappe.db.get_list(
            "UOM",
            filters=[{"enabled": 1}],
            or_filters=[
                {"name": ["like", search_text]},
                {"uom_name": ["like", search_text]},
            ],
            fields=["name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ User ############################################

    ########################### User Full List & Search ############################
    if doctype == "User" and con_doc == "%%":
        query = frappe.db.get_list(
            "User",
            filters=[{"enabled": 1}],
            or_filters=[
                {"name": ["like", search_text]},
                {"full_name": ["like", search_text]},
            ],
            fields=["name", "full_name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ Stock Entry Type ############################################

    ########################### Stock Entry Type Full List & Search ############################
    if doctype == "Stock Entry Type" and con_doc == "%%":
        query = frappe.db.get_list(
            "Stock Entry Type",
            or_filters=[
                {"name": ["like", search_text]},
                {"purpose": ["like", search_text]},
            ],
            fields=["name", "purpose"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ CAMPAIGN ############################################

    ########################### Campaign Full List & Search ############################
    if doctype == "Campaign" and con_doc == "%%":
        query = frappe.db.get_list(
            "Campaign",
            or_filters=[
                {"name": ["like", search_text]},
                {"campaign_name": ["like", search_text]},
            ],
            fields=["name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ INDUSTRY TYPE ############################################

    ########################### Industry Type Full List & Search ############################
    if doctype == "Industry Type" and con_doc == "%%":
        query = frappe.db.get_list(
            "Industry Type",
            or_filters=[
                {"name": ["like", search_text]},
                {"industry": ["like", search_text]},
            ],
            fields=["name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ CURRENCY ############################################

    ########################### Currency Full List & Search ############################
    if doctype == "Currency" and con_doc == "%%":
        query = frappe.db.get_list(
            "Currency",
            or_filters=[
                {"name": ["like", search_text]},
                {"currency_name": ["like", search_text]},
            ],
            fields=["name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ SALES PARTNER ############################################

    ########################### Sales Partner Full List & Search ############################
    if doctype == "Sales Partner" and con_doc == "%%":
        query = frappe.db.get_list(
            "Sales Partner",
            or_filters=[
                {"name": ["like", search_text]},
                {"partner_name": ["like", search_text]},
            ],
            fields=["name", "commission_rate"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ TERMS & CONDITIONS ############################################

    ########################### Terms and Conditions Full List & Search ############################
    if doctype == "Terms and Conditions" and con_doc == "%%":
        query = frappe.db.get_list(
            "Terms and Conditions",
            or_filters=[
                {"name": ["like", search_text]},
                {"title": ["like", search_text]},
            ],
            fields=["name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ MODE OF PAYMENT ############################################

    ########################### Mode of Payment Full List & Search ############################
    if doctype == "Mode of Payment" and con_doc == "%%":
        query = frappe.db.get_list(
            "Mode of Payment",
            or_filters=[
                {"name": ["like", search_text]},
                {"mode_of_payment": ["like", search_text]},
            ],
            fields=["name", "type"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ PRICE LIST ############################################

    ########################### Price List Full List & Search ############################
    if doctype == "Price List" and con_doc == "%%":
        query = frappe.db.get_list(
            "Price List",
            or_filters=[
                {"name": ["like", search_text]},
                {"price_list_name": ["like", search_text]},
            ],
            filters={"selling": 1},
            fields=["name", "currency"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Buying Price List Full List & Search ############################
    if doctype == "Buying Price List" and con_doc == "%%":
        query = frappe.db.get_list(
            "Price List",
            or_filters=[
                {"name": ["like", search_text]},
                {"price_list_name": ["like", search_text]},
            ],
            filters={"buying": 1},
            fields=["name", "currency"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ COST CENTER ############################################

    ########################### Cost Center Full List & Search ############################
    if doctype == "Cost Center" and con_doc == "%%":
        query = frappe.db.get_list(
            "Cost Center",
            filters=[{"is_group": ["=", 0]}],
            or_filters=[
                {"name": ["like", search_text]},
                {"cost_center_name": ["like", search_text]},
            ],
            fields=["name", "cost_center_name", "parent_cost_center"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ ACCOUNT ############################################
    ########################### Account Full List & Search ############################
    if doctype == "Account" and con_doc == "%%":
        conditions = {"is_group": ["=", 0]}
        or_conditions = {}
        if filter1 != "%%":
            conditions["account_type"] = filter1
        if filter2 != "%%":
            conditions["name"] = filter2
        query = frappe.db.get_list(
            "Account",
            filters=conditions,
            or_filters=[
                {"name": ["like", search_text]},
                {"account_name": ["like", search_text]},
                {"account_number": ["like", search_text]},
            ],
            fields=[
                "name",
                "account_type",
                "root_type",
                "account_currency",
                "parent_account",
            ],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"
    ############################################ ITEM ############################################

    ########################### Item Full List & Search ############################

    if doctype == "Item" and con_doc == "%%":
        conditions = {}
        conditions1 = {}
        if search_text != "%%":
            conditions1["name"] = ["like", search_text]
            conditions1["item_name"] = ["like", search_text]
            conditions1["item_code"] = ["like", search_text]
        if filter1 != "%%":
            conditions["item_group"] = filter1
        if filter2 != "%%":
            conditions["brand"] = filter2
        if filter3 != "%%":
            conditions["is_stock_item"] = filter3
        if filter4 != "%%":
            conditions["stock_uom"] = filter4

        query = frappe.db.get_list(
            "Item",
            or_filters=conditions1,
            filters=conditions,
            fields=[
                "name",
                "item_code",
                "item_name",
                "item_group",
                "stock_uom as uom",
                "image",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )

        if query:
            return query
        else:
            return "لا يوجد !"

    '''
    if doctype == "Item" and con_doc == '%%':
        conditions = ""
        if search_text != '%%':
            conditions += " and (`tabItem`.name like '%{search_text}%' or `tabItem`.item_name like '%{search_text}%' or `tabItem`.item_code like '%{search_text}%') ".format(search_text=search_text)
        if filter1 != '%%':
            conditions += " and `tabItem`.item_group = '{filter1}' ".format(filter1=filter1)
        if filter2 != '%%':
            conditions += " and `tabItem`.brand = '{filter2}' ".format(filter2=filter2)
        if filter3 != '%%':
            conditions += " and `tabItem`.is_stock_item = '{filter3}' ".format(filter3=filter3)
        if filter4 != '%%':
            conditions += " and `tabItem`.stock_uom = '{filter4}' ".format(filter4=filter4)
        query = frappe.db.sql(
            """ select name, item_name, item_group, stock_uom, image
                from `tabItem`
                where `tabItem`.disabled = 0
                {conditions}
                order by modified desc
                LIMIT {start},{page_length}
            """.format(conditions=conditions, start=start, page_length=page_length), as_dict=1)
        if query:
            return query
        else:
            return "لا يوجد !"
    '''
    ############################################ MATERIAL REQUEST ############################################

    ########################### Material Request Full List & Search ############################
    if doctype == "Material Request" and con_doc == "%%":
        conditions = {}
        or_conditions = {}
        if search_text != "%%":
            or_conditions["name"] = ["like", search_text]
            or_conditions["title"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["material_request_type"] = filter2
        if filter3 != "%%":
            conditions["set_warehouse"] = filter3
        if filter4 != "%%" and filter5 == "%%":
            conditions["transaction_date"] = [">=", filter4]
        if filter5 != "%%" and filter4 == "%%":
            conditions["transaction_date"] = ["<=", filter5]
        if filter4 != "%%" and filter5 != "%%":
            conditions["transaction_date"] = ["between", [filter4, filter5]]
        query = frappe.db.get_list(
            "Material Request",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "material_request_type",
                "transaction_date",
                "set_warehouse",
                "status",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ STOCK ENTRY ############################################

    if doctype == "Supplier Quotation" and con_doc == "Material Request":
        connections = frappe.db.sql(
            """ select distinct `tabSupplier Quotation`.name as name,`tabSupplier Quotation`.supplier as supplier,
                       `tabSupplier Quotation`.transaction_date as transaction_date, `tabSupplier Quotation`.valid_till as valid_till,
                       `tabSupplier Quotation`.grand_total as grand_total,`tabSupplier Quotation`.status as status,
                       `tabSupplier Quotation`.currency as currency
                    from `tabSupplier Quotation` join `tabSupplier Quotation Item` on `tabSupplier Quotation`.name = `tabSupplier Quotation Item`.parent
                where `tabSupplier Quotation Item`.material_request = '{cur_nam}'
                and (`tabSupplier Quotation`.name like '%{search_text}%' or `tabSupplier Quotation`.supplier like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    if doctype == "Purchase Order" and con_doc == "Material Request":
        connections = frappe.db.sql(
            """ select distinct `tabPurchase Order`.name as name,`tabPurchase Order`.supplier as supplier,
                       `tabPurchase Order`.transaction_date as transaction_date, `tabPurchase Order`.set_warehouse as set_warehouse,
                       `tabPurchase Order`.grand_total as grand_total,`tabPurchase Order`.status as status,
                       `tabPurchase Order`.currency as currency
                from `tabPurchase Order` join `tabPurchase Order Item` on `tabPurchase Order`.name = `tabPurchase Order Item`.parent
                where `tabPurchase Order Item`.material_request = '{cur_nam}'
                and (`tabPurchase Order`.name like '%{search_text}%' or `tabPurchase Order`.supplier like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    if doctype == "Purchase Receipt" and con_doc == "Material Request":
        connections = frappe.db.sql(
            """ select distinct `tabPurchase Receipt`.name as name,`tabPurchase Receipt`.supplier as supplier,`tabPurchase Receipt`.posting_date as posting_date		,
                `tabPurchase Receipt`.set_warehouse as set_warehouse,`tabPurchase Receipt`.status as status,
                `tabPurchase Receipt`.currency as currency, `tabPurchase Receipt`.total as total,`tabPurchase Receipt`.total_qty as total_qty,`tabPurchase Receipt`.status as status,
                `tabPurchase Receipt`.currency as currency
                from `tabPurchase Receipt` join `tabPurchase Receipt Item` on `tabPurchase Receipt`.name = `tabPurchase Receipt Item`.parent
                where `tabPurchase Receipt Item`.material_request = '{cur_nam}'
                and (`tabPurchase Receipt`.name like '%{search_text}%' or `tabPurchase Receipt`.supplier_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    if doctype == "Stock Entry" and con_doc == "Material Request":
        connections = frappe.db.sql(
            """ select distinct `tabStock Entry`.name	 as name,`tabStock Entry`.stock_entry_type as stock_entry_type,
                       `tabStock Entry`.posting_date as posting_date, `tabStock Entry`.from_warehouse as from_warehouse,
                       `tabStock Entry`.to_warehouse as to_warehouse, `tabStock Entry`.docstatus as docstatus
                from `tabStock Entry` join `tabStock Entry Detail` on `tabStock Entry`.name = `tabStock Entry Detail`.parent
                where `tabStock Entry Detail`.material_request = '{cur_nam}'
                and (`tabStock Entry`.name like '%{search_text}%' or `tabStock Entry`.stock_entry_type like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"
    ############################################ STOCK ENTRY ############################################

    ########################### Stock Entry Full List & Search ############################

    if doctype == "Stock Entry" and con_doc == "%%":
        conditions = {}
        conditions1 = {}
        if search_text != "%%":
            conditions1["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["docstatus"] = filter1
        if filter2 != "%%":
            conditions["stock_entry_type"] = filter2

        if filter3 != "%%" and filter4 == "%%":
            conditions["posting_date"] = [">=", filter3]
        if filter4 != "%%" and filter3 == "%%":
            conditions["posting_date"] = ["<=", filter4]
        if filter3 != "%%" and filter4 != "%%":
            conditions["posting_date"] = ["between", [filter3, filter4]]
        if filter5 != "%%":
            conditions["from_warehouse"] = filter5
        if filter6 != "%%":
            conditions["to_warehouse"] = filter6

        query = frappe.db.get_list(
            "Stock Entry",
            or_filters=conditions1,
            filters=conditions,
            fields=[
                "name",
                "stock_entry_type",
                "posting_date",
                "from_warehouse",
                "to_warehouse",
                "docstatus",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    '''
    if doctype == "Stock Entry" and con_doc == '%%':
        conditions = ""
        if search_text != '%%':
            conditions += " and (`tabStock Entry`.name like '%{search_text}%' or `tabStock Entry`.title like '%{search_text}%') ".format(search_text=search_text)
        if filter1 != '%%':
            conditions += " and `tabStock Entry`.docstatus = '{filter1}' ".format(filter1=filter1)
        if filter2 != '%%':
            conditions += " and `tabStock Entry`.stock_entry_type = '{filter2}' ".format(filter2=filter2)
        if filter3 != '%%':
            conditions += " and `tabStock Entry`.posting_date >= '{filter3}' ".format(filter3=filter3)
        if filter4 != '%%':
            conditions += " and `tabStock Entry`.posting_date <= '{filter4}' ".format(filter4=filter4)
        if filter5 != '%%':
            conditions += " and `tabStock Entry`.from_warehouse = '{filter5}' ".format(filter5=filter5)
        if filter6 != '%%':
            conditions += " and `tabStock Entry`.to_warehouse = '{filter6}' ".format(filter6=filter6)
        query = frappe.db.sql(
            """ select name, stock_entry_type, posting_date, from_warehouse, to_warehouse, docstatus
                from `tabStock Entry`
                where `tabStock Entry`.docstatus in (0, 1, 2)
                {conditions}
                order by modified desc
                LIMIT {start},{page_length}
            """.format(conditions=conditions, start=start, page_length=page_length), as_dict=1)
        if query:
            return query
        else:
            return "لا يوجد !"
    '''
    ############################################ PURCHASE RECEIPT ############################################

    ########################### Purchase Receipt Full List & Search ############################
    if doctype == "Purchase Receipt" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["supplier"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["supplier"] = filter2
        if filter3 != "%%":
            conditions["is_return"] = filter3
        if filter4 != "%%":
            conditions["set_warehouse"] = filter4
        if filter5 != "%%" and filter6 == "%%":
            conditions["posting_date"] = [">=", filter5]
        if filter6 != "%%" and filter5 == "%%":
            conditions["posting_date"] = ["<=", filter6]
        if filter5 != "%%" and filter6 != "%%":
            conditions["posting_date"] = ["between", [filter5, filter6]]

        query = frappe.db.get_list(
            "Purchase Receipt",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "supplier",
                "posting_date",
                "set_warehouse",
                "status",
                "currency",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ DELIVERY NOTE ############################################

    ########################### Purchase Order Connected With Purchase Receipt & Search ############################
    if doctype == "Purchase Order" and con_doc == "Purchase Receipt":
        connections = frappe.db.sql(
            """ select distinct `tabPurchase Order`.name as name,`tabPurchase Order`.supplier as supplier,
                       `tabPurchase Order`.transaction_date as transaction_date,
                       `tabPurchase Order`.set_warehouse as set_warehouse	,`tabPurchase Order`.grand_total as grand_total,
                       `tabPurchase Order`.currency as currency, `tabPurchase Order`.status as status
                from `tabPurchase Order` join `tabPurchase Receipt Item` on `tabPurchase Order`.name = `tabPurchase Receipt Item`.purchase_order
                where `tabPurchase Receipt Item`.parent = '{cur_nam}'
                and (`tabPurchase Order`.name like '%{search_text}%' or `tabPurchase Order`.supplier like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Purchase Invoice Connected With Purchase Receipt & Search ############################
    if doctype == "Purchase Invoice" and con_doc == "Purchase Receipt":
        connections = frappe.db.sql(
            """ select distinct `tabPurchase Invoice`.name as name,`tabPurchase Invoice`.supplier as supplier,
                       `tabPurchase Invoice`.posting_date as posting_date, `tabPurchase Invoice`.due_date as due_date,
                       `tabPurchase Invoice`.total as total,`tabPurchase Invoice`.grand_total as grand_total,
                       `tabPurchase Invoice`.currency as currency, `tabPurchase Invoice`.status as status
                from `tabPurchase Invoice` join `tabPurchase Invoice Item` on `tabPurchase Invoice`.name = `tabPurchase Invoice Item`.parent
                where `tabPurchase Invoice Item`.purchase_receipt = '{cur_nam}'
                and (`tabPurchase Invoice`.name like '%{search_text}%' or `tabPurchase Invoice`.supplier like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Purchase Receipt Connected With Purchase Receipt & Search ############################
    if doctype == "Purchase Receipt" and con_doc == "Purchase Receipt":
        connections = frappe.db.sql(
            """ select distinct pr1.name as name, pr1.supplier as supplier,
                       pr1.posting_date as posting_date, pr1.posting_date as posting_date,
                       pr1.set_warehouse as set_warehouse,pr1.status as status,
                       pr1.currency as currency
                from `tabPurchase Receipt` pr1 join `tabPurchase Receipt` pr2 on pr1.name = pr2.amended_from
                where pr2.amended_from = '{cur_nam}'
                and ( pr1.name like '%{search_text}%' or pr1.supplier like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ############################################ DELIVERY NOTE ############################################

    ########################### Delivery Note Full List & Search ############################

    if doctype == "Delivery Note" and con_doc == "%%":
        conditions = {}
        conditions1 = {}
        if search_text != "%%":
            conditions1["name"] = ["like", search_text]
            conditions1["title"] = ["like", search_text]
            conditions1["customer"] = ["like", search_text]
            conditions1["customer_name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["customer"] = filter2
        if filter3 != "%%" and filter4 == "%%":
            conditions["posting_date"] = [">=", filter3]
        if filter4 != "%%" and filter3 == "%%":
            conditions["posting_date"] = ["<=", filter4]
        if filter3 != "%%" and filter4 != "%%":
            conditions["posting_date"] = ["between", [filter3, filter4]]

        if filter5 != "%%":
            conditions["set_warehouse"] = filter5

        query = frappe.db.get_list(
            "Delivery Note",
            or_filters=conditions1,
            filters=conditions,
            fields=[
                "name",
                "customer",
                "territory",
                "posting_date",
                "set_warehouse",
                "status",
                "currency",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    '''
    if doctype == "Delivery Note" and con_doc == '%%':
        conditions = ""
        if search_text != '%%':
            conditions += " and (`taDelivery Note`.name like '%{search_text}%' or `taDelivery Note`.title like '%{search_text}%' or `tabDelivery Note`.customer_name like '%{search_text}%' or `tabDelivery Note`.customer like '%{search_text}%') ".format(
                search_text=search_text)
        if filter1 != '%%':
            conditions += " and `tabDelivery Note`.status = '{filter1}' ".format(filter1=filter1)
        if filter2 != '%%':
            conditions += " and `tabDelivery Note`.customer = '{filter2}' ".format(filter2=filter2)
        if filter3 != '%%':
            conditions += " and `tabDelivery Note`.posting_date >= '{filter3}' ".format(filter3=filter3)
        if filter4 != '%%':
            conditions += " and `tabDelivery Note`.posting_date <= '{filter4}' ".format(filter4=filter4)
        if filter5 != '%%':
            conditions += " and `tabDelivery Note`.set_warehouse = '{filter5}' ".format(filter5=filter5)

        query = frappe.db.sql(
            """ select name, customer, territory, posting_date, set_warehouse, status
                from `tabDelivery Note`
                where `tabDelivery Note`.docstatus in (0, 1, 2)
                {conditions}
                order by modified desc
                LIMIT {start},{page_length}
            """.format(conditions=conditions, start=start, page_length=page_length), as_dict=1)
        if query:
            return query
        else:
            return "لا يوجد !"
    '''
    ############################################ SUPPLIER ############################################

    ########################### Supplier Full List & Search ############################
    if doctype == "Supplier" and con_doc == "%%":
        conditions1 = {}
        conditions = {"disabled": ["=", 0]}
        if search_text != "%%":
            conditions1["name"] = ["like", search_text]
            conditions1["supplier_name"] = ["like", search_text]
            conditions1["mobile_no"] = ["like", search_text]
        if filter1 != "%%":
            conditions["supplier_group"] = filter1
        if filter2 != "%%":
            conditions["country"] = filter2
        if filter3 != "%%":
            conditions["supplier_type"] = filter3

        if filter4 != "%%" and filter5 == "%%":
            conditions["creation"] = [">=", filter4]
        if filter5 != "%%" and filter4 == "%%":
            conditions["creation"] = ["<=", filter5]
        if filter4 != "%%" and filter5 != "%%":
            conditions["creation"] = ["between", [filter4, filter5]]

        query = frappe.db.get_list(
            "Supplier",
            or_filters=conditions1,
            filters=conditions,
            fields=[
                "name",
                "supplier_name",
                "supplier_group",
                "supplier_type",
                "country",
                "mobile_no",
                "default_currency",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Purchase Invoice Connected With Purchase Order & Search ############################
    if doctype == "Supplier Quotation" and con_doc == "Supplier":
        connections = frappe.db.sql(
            """ select distinct `tabSupplier Quotation`.name as name,`tabSupplier Quotation`.supplier as supplier,
                       `tabSupplier Quotation`.transaction_date as transaction_date, `tabSupplier Quotation`.valid_till as valid_till,
                       `tabSupplier Quotation`.total as total,`tabSupplier Quotation`.grand_total as grand_total,
                       `tabSupplier Quotation`.currency as currency, `tabSupplier Quotation`.status as status
                from `tabSupplier Quotation` join `tabSupplier` on `tabSupplier`.name = `tabSupplier Quotation`.supplier
                where `tabSupplier Quotation`.supplier = '{cur_nam}'
                and (`tabSupplier Quotation`.name like '%{search_text}%' or `tabSupplier Quotation`.supplier like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Purchase Receipt Connected With Purchase Order & Search ############################

    if doctype == "Purchase Receipt" and con_doc == "Supplier":
        connections = frappe.db.sql(
            """ select distinct `tabPurchase Receipt`.name as name,`tabPurchase Receipt`.supplier as supplier,`tabPurchase Receipt`.set_warehouse as set_warehouse,
                `tabPurchase Receipt`.posting_date as posting_date,`tabPurchase Receipt`.grand_total as grand_total,
                `tabPurchase Receipt`.currency as currency, `tabPurchase Receipt`.total as total,`tabPurchase Receipt`.total_qty as total_qty,`tabPurchase Receipt`.status as status
                from `tabPurchase Receipt` join `tabSupplier` on `tabPurchase Receipt`.supplier = `tabSupplier`.name
                where `tabPurchase Receipt`.supplier = '{cur_nam}'
                and (`tabPurchase Receipt`.name like '%{search_text}%' or `tabPurchase Receipt`.supplier_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Purchase Invoice Connected With Purchase Order & Search ############################
    if doctype == "Purchase Invoice" and con_doc == "Supplier":
        connections = frappe.db.sql(
            """ select distinct `tabPurchase Invoice`.name as name,`tabPurchase Invoice`.supplier as supplier,`tabPurchase Invoice`.currency as currency,
                       `tabPurchase Invoice`.posting_date as posting_date, `tabPurchase Invoice`.due_date as due_date,`tabPurchase Invoice`.grand_total as grand_total,`tabPurchase Invoice`.status as status
                from `tabPurchase Invoice` join `tabSupplier` on `tabPurchase Invoice`.supplier = `tabSupplier`.name
                where `tabPurchase Invoice`.supplier = '{cur_nam}'
                and (`tabPurchase Invoice`.name like '%{search_text}%' or `tabPurchase Invoice`.supplier_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Purchase Receipt Connected With Purchase Order & Search ############################

    ########################### Payment Entry Connected With Purchase Invoice & Search ############################
    if doctype == "Purchase Order" and con_doc == "Supplier":
        connections = frappe.db.sql(
            """ select distinct `tabPurchase Order`.name as name,`tabPurchase Order`.supplier as supplier,
                `tabPurchase Order`.transaction_date as transaction_date,
                `tabPurchase Order`.set_warehouse as set_warehouse,
                `tabPurchase Order`.grand_total as grand_total,
                `tabPurchase Order`.currency as currency,
                `tabPurchase Order`.status as status
                from `tabPurchase Order` join `tabSupplier` on `tabPurchase Order`.supplier = `tabSupplier`.name
                where `tabPurchase Order`.supplier   = '{cur_nam}'
                and (`tabPurchase Order`.name like '%{search_text}%' or `tabPurchase Order`.supplier_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ############################################ SUPPLIER GROUP ############################################

    ########################### Supplier Group Full List & Search ############################
    if doctype == "Supplier Group" and con_doc == "%%":
        query = frappe.db.get_list(
            "Supplier Group",
            filters=[{"is_group": ["=", 0]}],
            or_filters=[
                {"name": ["like", search_text]},
                {"supplier_group_name": ["like", search_text]},
            ],
            fields=["name"],
            order_by="name asc",
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ############################################ SUPPLIER QUOTATION ############################################

    ########################### Supplier Quotation Full List & Search ############################
    if doctype == "Supplier Quotation" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["supplier"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
            or_conditions["supplier_name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["supplier"] = filter2
        if filter3 != "%%" and filter4 == "%%":
            conditions["transaction_date"] = [">=", filter3]
        if filter4 != "%%" and filter3 == "%%":
            conditions["transaction_date"] = ["<=", filter4]
        if filter3 != "%%" and filter4 != "%%":
            conditions["transaction_date"] = ["between", [filter3, filter4]]

        query = frappe.db.get_list(
            "Supplier Quotation",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "supplier",
                "transaction_date",
                "valid_till",
                "grand_total",
                "status",
                "currency",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Purchase Invoice Connected With Purchase Order & Search ############################
    if doctype == "Quotation" and con_doc == "Supplier Quotation":
        connections = frappe.db.sql(
            """ select distinct `tabQuotation`.name as name,`tabQuotation`.quotation_to as quotation_to,`tabQuotation`.customer_name as customer_name,
                       `tabQuotation`.transaction_date as transaction_date, `tabQuotation`.currency as currency,
                       `tabQuotation`.grand_total as grand_total,`tabQuotation`.status as status
                from `tabQuotation` join `tabSupplier Quotation` on `tabQuotation`.supplier_quotation = `tabSupplier Quotation`.name
                where `tabQuotation`.supplier_quotation = '{cur_nam}'
                and (`tabQuotation`.name like '%{search_text}%' or `tabQuotation`.quotation_to like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Purchase Orders Connected With Supplier Quotation & Search ############################
    if doctype == "Purchase Order" and con_doc == "Supplier Quotation":
        connections = frappe.db.sql(
            """ select distinct `tabPurchase Order`.name as name,`tabPurchase Order`.supplier as supplier,
                `tabPurchase Order`.currency as currency, `tabPurchase Order`.transaction_date as transaction_date,
                `tabPurchase Order`.status as status, `tabPurchase Order`.set_warehouse as set_warehouse,
                `tabPurchase Order`.grand_total as grand_total
                from `tabPurchase Order` join `tabPurchase Order Item` on `tabPurchase Order`.name = `tabPurchase Order Item`.parent
                where `tabPurchase Order Item`.supplier_quotation = '{cur_nam}'
                and (`tabPurchase Order`.name like '%{search_text}%' or `tabPurchase Order`.supplier_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Payment Request Connected With Purchase Invoice & Search ############################
    if doctype == "Material Request" and con_doc == "Supplier Quotation":
        connections = frappe.db.sql(
            """ select distinct `tabMaterial Request`.name as name,`tabMaterial Request`.material_request_type as material_request_type,`tabMaterial Request`.set_warehouse as set_warehouse,
                       `tabMaterial Request`.transaction_date as transaction_date, `tabMaterial Request`.schedule_date as schedule_date,`tabMaterial Request`.status as status
                from `tabMaterial Request` join `tabSupplier Quotation Item` on `tabMaterial Request`.name = `tabSupplier Quotation Item`.material_request
                where `tabSupplier Quotation Item`.parent = '{cur_nam}'
                and (`tabMaterial Request`.name like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ############################################ PURCHASE ORDER ############################################

    ########################### Purchase Order Full List & Search ############################
    if doctype == "Purchase Order" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["supplier"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["supplier"] = filter2

        if filter3 != "%%" and filter4 == "%%":
            conditions["transaction_date"] = [">=", filter3]
        if filter4 != "%%" and filter3 == "%%":
            conditions["transaction_date"] = ["<=", filter4]
        if filter3 != "%%" and filter4 != "%%":
            conditions["transaction_date"] = ["between", [filter3, filter4]]

        query = frappe.db.get_list(
            "Purchase Order",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "supplier",
                "transaction_date",
                "set_warehouse",
                "grand_total",
                "status",
                "currency",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Purchase Receipt" and con_doc == "Purchase Order":
        connections = frappe.db.sql(
            """ select distinct `tabPurchase Receipt`.name as name,`tabPurchase Receipt`.supplier as supplier,
                       `tabPurchase Receipt`.set_warehouse as set_warehouse, `tabPurchase Receipt`.currency as currency,
                       `tabPurchase Receipt`.posting_date as posting_date,`tabPurchase Receipt`.grand_total as grand_total,`tabPurchase Receipt`.status as status
                from `tabPurchase Receipt` join `tabPurchase Receipt Item` on `tabPurchase Receipt`.name = `tabPurchase Receipt Item`.parent
                where `tabPurchase Receipt Item`.purchase_order = '{cur_nam}'
                and (`tabPurchase Receipt`.name like '%{search_text}%' or `tabPurchase Receipt`.supplier_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Purchase Invoice Connected With Purchase Order & Search ############################
    if doctype == "Purchase Invoice" and con_doc == "Purchase Order":
        connections = frappe.db.sql(
            """ select distinct `tabPurchase Invoice`.name as name,`tabPurchase Invoice`.supplier as supplier,`tabPurchase Invoice`.currency as currency,
                       `tabPurchase Invoice`.posting_date as posting_date, `tabPurchase Invoice`.due_date as due_date,`tabPurchase Invoice`.grand_total as grand_total,`tabPurchase Invoice`.status as status
                from `tabPurchase Invoice` join `tabPurchase Invoice Item` on `tabPurchase Invoice`.name = `tabPurchase Invoice Item`.parent
                where `tabPurchase Invoice Item`.purchase_order = '{cur_nam}'
                and (`tabPurchase Invoice`.name like '%{search_text}%' or `tabPurchase Invoice`.supplier_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Payment Entry Connected With Purchase Invoice & Search ############################
    if doctype == "Material Request" and con_doc == "Purchase Order":
        connections = frappe.db.sql(
            """ select distinct `tabMaterial Request`.name as name,`tabMaterial Request`.material_request_type as material_request_type,`tabMaterial Request`.set_warehouse as set_warehouse,
                       `tabMaterial Request`.transaction_date as transaction_date, `tabMaterial Request`.schedule_date as schedule_date,`tabMaterial Request`.status as status
                from `tabMaterial Request` join `tabPurchase Order Item` on `tabMaterial Request`.name = `tabPurchase Order Item`.material_request
                where `tabPurchase Order Item`.parent = '{cur_nam}'
                and (`tabMaterial Request`.name like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Payment Request Connected With Purchase Invoice & Search ############################
    if doctype == "Supplier Quotation" and con_doc == "Purchase Order":
        connections = frappe.db.sql(
            """ select distinct `tabSupplier Quotation`.name as name,`tabSupplier Quotation`.supplier as supplier,
                       `tabSupplier Quotation`.currency as currency,
                       `tabSupplier Quotation`.grand_total as grand_total,
                       `tabSupplier Quotation`.transaction_date as transaction_date,
                       `tabSupplier Quotation`.valid_till as valid_till,
                       `tabSupplier Quotation`.status as status
                from `tabSupplier Quotation` join `tabPurchase Order Item` on `tabSupplier Quotation`.name = `tabPurchase Order Item`.supplier_quotation
                where `tabPurchase Order Item`.parent = '{cur_nam}'
                and (`tabSupplier Quotation`.name like '%{search_text}%' or `tabSupplier Quotation`.supplier_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Purchase Receipt Connected With Purchase Order & Search ############################

    if doctype == "Payment Entry" and con_doc == "Purchase Order":
        connections = frappe.db.sql(
            """ select distinct `tabPayment Entry`.name as name,`tabPayment Entry`.payment_type as payment_type,
                       `tabPayment Entry`.mode_of_payment as mode_of_payment,
                       `tabPayment Entry`.paid_from_account_currency as currency,
                       `tabPayment Entry`.paid_amount as base_paid_amount,
                       `tabPayment Entry`.posting_date as posting_date, `tabPayment Entry`.party_name as party_name,`tabPayment Entry`.status as status
                from `tabPayment Entry` join `tabPayment Entry Reference` on `tabPayment Entry`.name = `tabPayment Entry Reference`.parent
                where `tabPayment Entry Reference`.reference_name = '{cur_nam}'
                and (`tabPayment Entry`.name like '%{search_text}%' or `tabPayment Entry`.contact_email like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ############################################ PURCHASE INVOICE ############################################

    ########################### Purchase Invoice Full List & Search ############################
    if doctype == "Purchase Invoice" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["supplier"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["supplier"] = filter2
        if filter3 != "%%":
            conditions["is_return"] = filter3

        if filter4 != "%%" and filter5 == "%%":
            conditions["posting_date"] = [">=", filter4]
        if filter5 != "%%" and filter4 == "%%":
            conditions["posting_date"] = ["<=", filter5]
        if filter4 != "%%" and filter5 != "%%":
            conditions["posting_date"] = ["between", [filter4, filter5]]

        query = frappe.db.get_list(
            "Purchase Invoice",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "supplier",
                "posting_date",
                "grand_total",
                "status",
                "currency",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Purchase Order Connected With Purchase Invoice & Search ############################

    if doctype == "Purchase Order" and con_doc == "Purchase Invoice":
        connections = frappe.db.sql(
            """ select distinct `tabPurchase Order`.name as name,`tabPurchase Order`.supplier as supplier,`tabPurchase Order`.currency as currency,
                       `tabPurchase Order`.transaction_date as transaction_date,`tabPurchase Order`.grand_total as grand_total,`tabPurchase Order`.status as status
                from `tabPurchase Order` join `tabPurchase Invoice Item` on `tabPurchase Order`.name = `tabPurchase Invoice Item`.purchase_order
                where `tabPurchase Invoice Item`.parent = '{cur_nam}'
                and (`tabPurchase Order`.name like '%{search_text}%' or `tabPurchase Order`.supplier_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Purchase Invoice Connected With Purchase Invoice & Search ############################
    if doctype == con_doc == "Purchase Invoice":
        connections = frappe.db.sql(
            """ select  pi_2.name as name, pi_2.supplier as supplier,pi_2.supplier_address as supplier_address,
                       pi_2.posting_date as posting_date,pi_2.due_date as due_date,pi_2.grand_total as grand_total,pi_2.status as status
                from `tabPurchase Invoice` pi_1 join `tabPurchase Invoice` pi_2 on pi_1.name = pi_2.return_against
                where pi_2.return_against = '{cur_nam}'
                and (pi_2.name like '%{search_text}%' or pi_2.supplier_address like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Payment Entry Connected With Purchase Invoice & Search ############################
    if doctype == "Payment Entry" and con_doc == "Purchase Invoice":
        connections = frappe.db.sql(
            """ select distinct `tabPayment Entry`.name as name,`tabPayment Entry`.payment_type as payment_type,`tabPayment Entry`.mode_of_payment as mode_of_payment,
                       `tabPayment Entry`.posting_date as posting_date,`tabPayment Entry`.party as party,`tabPayment Entry`.party_name as part_name,
                       `tabPayment Entry`.status as status,
                       `tabPayment Entry`.paid_amount as base_paid_amount,`tabPayment Entry`.paid_from_account_currency as currency
                from `tabPayment Entry` join `tabPayment Entry Reference` on `tabPayment Entry`.name = `tabPayment Entry Reference`.parent
                where `tabPayment Entry Reference`.reference_name = '{cur_nam}'
                and (`tabPayment Entry`.name like '%{search_text}%' or `tabPayment Entry`.party_name like '%{search_text}%') LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Payment Request Connected With Purchase Invoice & Search ############################
    if doctype == "Payment Request" and con_doc == "Purchase Invoice":
        connections = frappe.db.sql(
            """ select distinct `tabPayment Request`.name as name,`tabPayment Request`.payment_request_type as payment_request_type, `tabPayment Request`.mode_of_payment as mode_of_payment,
                      `tabPayment Request`.transaction_date as transaction_date,`tabPayment Request`.party_type as party_type,`tabPayment Request`.party as party,`tabPayment Request`.status as status,
                      `tabPayment Request`.grand_total as grand_total,`tabPayment Request`.currency as currency
                from `tabPayment Request` join `tabPurchase Invoice` on `tabPayment Request`.reference_name = `tabPurchase Invoice`.name
                where `tabPayment Request`.reference_name = '{cur_nam}'
                and (`tabPayment Request`.name like '%{search_text}%' or `tabPayment Request`.party_type like '%{search_text}%' ) LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ############################################ ADDRESS ############################################

    ########################### Filtered Address List & Search ############################
    if doctype == "Filtered Address" and con_doc == "%%":
        addresses = frappe.db.get_all(
            "Dynamic Link", filters={"link_name": cur_nam}, fields=["parent"]
        )
        result = []
        for d in addresses:
            query = frappe.db.sql(
                """ select name as name ,
                                                 address_title as address_title,
                                                 address_line1 as address_line1,
                                                 city as city,
                                                 country as country
                                          from tabAddress where name = '{filtered}'
                                          and (address_title like '{search_text}' or address_line1 like '{search_text}'
                                               or city like '{search_text}' or country like '{search_text}') LIMIT {start},{page_length}
                                      """.format(
                    filtered=d.parent,
                    search_text=search_text,
                    start=start,
                    page_length=page_length,
                ),
                as_dict=1,
            )
            for x in query:
                data = {
                    "name": x.name,
                    "address_title": x.address_title,
                    "address_line1": x.address_line1,
                    "city": x.city,
                    "country": x.country,
                }
                result.append(data)

        if result:
            return result
        else:
            return "لا يوجد !"

    ############################################ CONTACT ############################################

    ########################### Filtered Contact List & Search ############################
    if doctype == "Filtered Contact" and con_doc == "%%":
        contacts = frappe.db.get_list(
            "Dynamic Link", filters={"link_name": cur_nam}, fields=["parent"]
        )
        result = []
        for d in contacts:
            query = frappe.db.sql(
                """ select name as name,
                                             first_name as contact_display,
                                             email_id as email_id,
                                             mobile_no as mobile_no,
                                             phone as phone
                                      from tabContact where name = '{filtered}'
                                      and (name like '{search_text}' or email_id like '{search_text}'
                                           or mobile_no like '{search_text}' or phone like '{search_text}'
                                           or company_name like '{search_text}') LIMIT {start},{page_length}
                                      """.format(
                    filtered=d.parent,
                    search_text=search_text,
                    start=start,
                    page_length=page_length,
                ),
                as_dict=1,
            )
            for x in query:
                data = {
                    "name": x.name,
                    "contact_display": str(x.contact_display),
                    "mobile_no": x.mobile_no,
                    "phone": x.phone,
                    "email_id": x.email_id,
                }
                result.append(data)

        if result:
            return result
        else:
            return "لا يوجد !"

    ########################### Leave Ap[plication Full List & Search ############################
    if doctype == "Leave Application" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        from_date = "from_date"
        to_date = "to_date"
        if search_text != "%%":
            or_conditions["employee_name"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["employee"] = filter2
        if filter3 != "%%":
            query = frappe.db.get_list(
                "Leave Application",
                fields=[
                    "name",
                    "employee_name",
                    "leave_approver_name",
                    "leave_approver",
                    "department",
                    "leave_type",
                    "from_date",
                    "to_date",
                    "total_leave_days",
                    "status",
                ],
                order_by=order_by(sort_field, sort_type),
                start=start,
                page_length=page_length,
            )
            response = []
            # return query[0].from_date
            for row in range(len(query)):
                if (
                        time.strptime(str(query[row].from_date), "%Y-%m-%d")
                        <= time.strptime(filter3.split("T")[0], "%Y-%m-%d")
                        <= time.strptime(str(query[row].to_date), "%Y-%m-%d")
                ):
                    response.append(query[row])

            return response

        if filter4 != "%%":
            conditions["department"] = filter4
        if filter5 != "%%":
            conditions["leave_type"] = filter5
        if filter6 != "%%" and filter7 == "%%":
            conditions["posting_date"] = [">=", filter6]
        if filter7 != "%%" and filter6 == "%%":
            conditions["posting_date"] = ["<=", filter7]
        if filter6 != "%%" and filter7 != "%%":
            conditions["posting_date"] = ["between", [filter6, filter7]]

        query = frappe.db.get_list(
            "Leave Application",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "employee_name",
                "leave_approver_name",
                "leave_approver",
                "department",
                "leave_type",
                "from_date",
                "to_date",
                "total_leave_days",
                "status",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"
            ########################### Attendance Connected With Leave Application & Search ############################

    # if doctype == "Attendance" and con_doc == "Leave Application":
    #     connections = frappe.db.sql(
    #         """ select distinct `tabAttendance`.name as name,`tabAttendance`.employee_name as employee_name,`tabAttendance`.department as department,
    #                    `tabAttendance`.leave_type as leave_type,`tabAttendance`.attendance_date as attendance_date, `tabAttendance`.status as status
    #             from `tabAttendance` join `tabLeave Application` on `tabLeave Application`.name = `Attendance`.leave_application
    #             where `Attendance`.leave_application = '{cur_nam}'
    #             and (`tabAttendance`.name like '%{search_text}%' or `tabAttendance`.supplier_address like '%{search_text}%') LIMIT {start},{page_length}
    #         """.format(
    #             start=start,
    #             page_length=page_length,
    #             cur_nam=cur_nam,
    #             search_text=search_text,
    #         ),
    #         as_dict=1,
    #     )
    #     if connections:
    #         return connections
    #     else:
    #         return "لا يوجد روابط !"

    ########################### Purchase Invoice Full List & Search ############################
    if doctype == "Employee" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["employee_name"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["gender"] = filter2
        if filter3 != "%%":
            conditions["department"] = filter3

        if filter4 != "%%" and filter5 == "%%":
            conditions["date_of_joining"] = [">=", filter4]
        if filter5 != "%%" and filter4 == "%%":
            conditions["date_of_joining"] = ["<=", filter5]
        if filter4 != "%%" and filter5 != "%%":
            conditions["date_of_joining"] = ["between", [filter4, filter5]]

        query = frappe.db.get_list(
            "Employee",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "employee_name",
                "attendance_device_id",
                "designation",
                "department",
                "leave_approver",
                "branch",
                "company",
                "status",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        for x in range(len(query)):
            currency = frappe.db.get_value(
                "Company", {"name": query[x].company}, "default_currency"
            )

            query[x]["currency"] = currency
            currency = frappe.db.get_value(
                "User", {"email": query[x].leave_approver}, "full_name"
            )

            query[x]["leave_approver_name"] = currency
            advance_account = frappe.db.get_value(
                "Company",
                {"name": query[x].company},
                "default_employee_advance_account",
            )

            query[x]["advance_account"] = advance_account
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Attendance Request" and con_doc == "Employee":
        connections = frappe.db.sql(
            """ select distinct `tabAttendance Request`.name as name,`tabAttendance Request`.employee_name as employee_name, `tabAttendance Request`.employee as employee,
                      `tabAttendance Request`.department as department,`tabAttendance Request`.from_date as from_date,`tabAttendance Request`.to_date as to_date,`tabAttendance Request`.reason as reason,`tabAttendance Request`.docstatus as docstatus
                from `tabAttendance Request` join `tabEmployee` on `tabAttendance Request`.employee = `tabEmployee`.name
                where `tabAttendance Request`.employee = '{cur_nam}'
                and (`tabAttendance Request`.name like '%{search_text}%' or `tabAttendance Request`.employee_name like '%{search_text}%' ) LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

            ###########################

    if doctype == "Leave Application" and con_doc == "Employee":
        connections = frappe.db.sql(
            """ select distinct `tabLeave Application`.name as name,`tabLeave Application`.employee_name as employee_name, `tabLeave Application`.employee as employee,
                      `tabLeave Application`.department as department,`tabLeave Application`.from_date as from_date,`tabLeave Application`.to_date as to_date,`tabLeave Application`.description as description,`tabLeave Application`.docstatus as docstatus
                from `tabLeave Application` join `tabEmployee` on `tabLeave Application`.employee = `tabEmployee`.name
                where `tabLeave Application`.employee = '{cur_nam}'
                and (`tabLeave Application`.name like '%{search_text}%' or `tabLeave Application`.employee_name like '%{search_text}%' ) LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################################

    if doctype == "Employee Advance" and con_doc == "Employee":
        connections = frappe.db.sql(
            """ select distinct `tabEmployee Advance`.name as name,`tabEmployee Advance`.employee_name as employee_name, `tabEmployee Advance`.employee as employee,
                      `tabEmployee Advance`.department as department,`tabEmployee Advance`.posting_date as posting_date,`tabEmployee Advance`.purpose as purpose,`tabEmployee Advance`.advance_amount as advance_amount,`tabEmployee Advance`.status as status
                from `tabEmployee Advance` join `tabEmployee` on `tabEmployee Advance`.employee = `tabEmployee`.name
                where `tabEmployee Advance`.employee = '{cur_nam}'
                and (`tabEmployee Advance`.name like '%{search_text}%' or `tabEmployee Advance`.employee_name like '%{search_text}%' ) LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################################

    if doctype == "Expense Claim" and con_doc == "Employee":
        connections = frappe.db.sql(
            """ select distinct `tabExpense Claim`.name as name,`tabExpense Claim`.employee_name as employee_name, `tabExpense Claim`.employee as employee,
                      `tabExpense Claim`.department as department,`tabExpense Claim`.posting_date as posting_date,`tabExpense Claim`.grand_total as grand_total,`tabExpense Claim`.status as status
                from `tabExpense Claim` join `tabEmployee` on `tabExpense Claim`.employee = `tabEmployee`.name
                where `tabExpense Claim`.employee = '{cur_nam}'
                and (`tabExpense Claim`.name like '%{search_text}%' or `tabExpense Claim`.employee_name like '%{search_text}%' ) LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    if doctype == "Employee Grievance" and con_doc == "Employee":
        connections = frappe.db.sql(
            """ select distinct `tabEmployee Grievance`.name as name, `tabEmployee Grievance`.raised_by as raised_by,
                      `tabEmployee Grievance`.designation as designation,`tabEmployee Grievance`.date as date,`tabEmployee Grievance`.grievance_against_party as grievance_against_party,`tabEmployee Grievance`.grievance_against as grievance_against,
                      `tabEmployee Grievance`.grievance_type as grievance_type, `tabEmployee Grievance`.status as status
                from `tabEmployee Grievance` join `tabEmployee` on `tabEmployee Grievance`.raised_by = `tabEmployee`.name
                where `tabEmployee Grievance`.raised_by = '{cur_nam}'
                and (`tabEmployee Grievance`.name like '%{search_text}%' ) LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"
    if doctype == "Leave Type" and con_doc == "%%":
        conditions = {}
        query = frappe.db.get_list(
            "Leave Type",
            filters=conditions,
            fields=["name", "leave_type_name"],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Department" and con_doc == "%%":
        conditions = {}
        query = frappe.db.get_list(
            "Department",
            filters=conditions,
            fields=[
                "name",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Employee Checkin" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["employee_name"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["log_type"] = filter1
        if filter2 != "%%":
            conditions["employee"] = filter2
        if filter3 != "%%" and filter4 == "%%":
            conditions["time"] = [">=", filter3]
        if filter4 != "%%" and filter3 == "%%":
            conditions["time"] = ["<=", filter4]
        if filter3 != "%%" and filter4 != "%%":
            conditions["time"] = ["between", [filter3, filter4]]

        query = frappe.db.get_list(
            "Employee Checkin",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "employee_name",
                "employee",
                "log_type",
                "time",
                "shift",
                "device_id",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Gender Full List & Search ############################
    if doctype == "Gender" and con_doc == "%%":
        query = frappe.db.get_list(
            "Gender",
            fields=[
                "name",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Employment Type Full List & Search ############################
    if doctype == "Employment Type" and con_doc == "%%":
        query = frappe.db.get_list(
            "Employment Type",
            fields=[
                "name",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Company Full List & Search ############################
    if doctype == "Company" and con_doc == "%%":
        query = frappe.db.get_list(
            "Company",
            fields=[
                "name",
                "round_off_cost_center",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"
    ########################### Department Full List & Search ############################
    if doctype == "Department" and con_doc == "%%":
        query = frappe.db.get_list(
            "Department",
            fields=[
                "name",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### User Full List & Search ############################
    if doctype == "User" and con_doc == "%%":
        query = frappe.db.get_list(
            "User",
            fields=[
                "name",
                "email",
                "full_name",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Designation List & Search ############################
    if doctype == "Designation" and con_doc == "%%":
        query = frappe.db.get_list(
            "Designation",
            fields=[
                "name",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Branch List & Search ############################
    if doctype == "Branch" and con_doc == "%%":
        query = frappe.db.get_list(
            "Branch",
            fields=[
                "name",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Holiday List List & Search ############################
    if doctype == "Holiday List" and con_doc == "%%":
        query = frappe.db.get_list(
            "Holiday List",
            fields=[
                "name",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Shift Type List List & Search ############################
    if doctype == "Default Shift" and con_doc == "%%":
        query = frappe.db.get_list(
            "Shift Type",
            fields=[
                "name",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Attendance Request" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["employee_name"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["employee"] = filter1
        if filter2 != "%%":
            conditions["department"] = filter2
        if filter3 != "%%" and filter4 == "%%":
            conditions["from_date"] = [">=", filter3]
        if filter4 != "%%" and filter3 == "%%":
            conditions["from_date"] = ["<=", filter4]
        if filter3 != "%%" and filter4 != "%%":
            conditions["from_date"] = ["between", [filter3, filter4]]

        query = frappe.db.get_list(
            "Attendance Request",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "employee_name",
                "employee",
                "department",
                "from_date",
                "to_date",
                "reason",
                "docstatus",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Employee Advance Full List & Search ############################
    if doctype == "Employee Advance" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["employee_name"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["employee"] = filter2
        if filter3 != "%%":
            conditions["department"] = filter3
        if filter4 != "%%" and filter5 == "%%":
            conditions["posting_date"] = [">=", filter4]
        if filter5 != "%%" and filter4 == "%%":
            conditions["posting_date"] = ["<=", filter5]
        if filter4 != "%%" and filter5 != "%%":
            conditions["posting_date"] = ["between", [filter4, filter5]]

        query = frappe.db.get_list(
            "Employee Advance",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "employee_name",
                "employee",
                "department",
                "posting_date",
                "purpose",
                "advance_amount",
                "status",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        for x in range(len(query)):
            company = frappe.db.get_value(
                "Employee", {"name": query[x].employee}, "company"
            )

            query[x]["company"] = company
            advance_account = frappe.db.get_value(
                "Company", {"name": company}, "default_employee_advance_account"
            )

            query[x]["advance_account"] = advance_account
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Payment Entry" and con_doc == "Employee Advance":
        connections = frappe.db.sql(
            """ select distinct `tabPayment Entry`.name as name, `tabPayment Entry`.party_name as party_name,
                      `tabPayment Entry`.payment_type as payment_type,`tabPayment Entry`.mode_of_payment as mode_of_payment,`tabPayment Entry`.posting_date as posting_date,`tabPayment Entry`.base_paid_amount as base_paid_amount,
                       `tabPayment Entry`.status as status
                from `tabPayment Entry` join `tabPayment Entry Reference` on `tabPayment Entry`.name = `tabPayment Entry Reference`.parent
                where  `tabPayment Entry Reference`.reference_name = '{cur_nam}'
                and (`tabPayment Entry`.name like '%{search_text}%' ) LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    if doctype == "Expense Claim" and con_doc == "Employee Advance":
        connections = frappe.db.sql(
            """ select distinct `tabExpense Claim`.name as name, `tabExpense Claim`.employee_name as employee_name,
                      `tabExpense Claim`.employee as employee,`tabExpense Claim`.department as department,`tabExpense Claim`.posting_date as posting_date,`tabExpense Claim`.grand_total as grand_total,
                       `tabExpense Claim`.status as status
                from `tabExpense Claim` join `tabExpense Claim Advance` on `tabExpense Claim`.name = `tabExpense Claim Advance`.parent
                where  `tabExpense Claim Advance`.employee_advance = '{cur_nam}'
                and (`tabExpense Claim`.name like '%{search_text}%' ) LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Branch List & Search ############################

    ########################### Expense Claim Type List & Search ############################
    if doctype == "Expense Claim Type" and con_doc == "%%":
        query = frappe.db.get_list(
            "Expense Claim Type",
            fields=[
                "name",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Expense Claim Full List & Search ############################
    if doctype == "Expense Claim" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["employee_name"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["employee"] = filter2
        if filter3 != "%%":
            conditions["department"] = filter3
        if filter4 != "%%" and filter5 == "%%":
            conditions["posting_date"] = [">=", filter4]
        if filter5 != "%%" and filter4 == "%%":
            conditions["posting_date"] = ["<=", filter5]
        if filter4 != "%%" and filter5 != "%%":
            conditions["posting_date"] = ["between", [filter4, filter5]]

        query = frappe.db.get_list(
            "Expense Claim",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "employee_name",
                "employee",
                "department",
                "posting_date",
                "grand_total",
                "status",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Payment Entry" and con_doc == "Expense Claim":
        connections = frappe.db.sql(
            """ select distinct `tabPayment Entry`.name as name, `tabPayment Entry`.party_name as party_name,
                      `tabPayment Entry`.payment_type as payment_type,`tabPayment Entry`.mode_of_payment as mode_of_payment,`tabPayment Entry`.posting_date as posting_date,`tabPayment Entry`.base_paid_amount as base_paid_amount,
                       `tabPayment Entry`.status as status
                from `tabPayment Entry` join `tabPayment Entry Reference` on `tabPayment Entry`.name = `tabPayment Entry Reference`.parent
                where  `tabPayment Entry Reference`.reference_name = '{cur_nam}'
                and (`tabPayment Entry`.name like '%{search_text}%' ) LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )
        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    if doctype == "Employee Advance" and con_doc == "Expense Claim":
        connections = frappe.db.sql(
            """ select distinct `tabEmployee Advance`.name as name, `tabEmployee Advance`.employee_name as employee_name,
                      `tabEmployee Advance`.employee as employee,`tabEmployee Advance`.department as department,`tabEmployee Advance`.posting_date as posting_date,`tabEmployee Advance`.purpose as purpose,
                       `tabEmployee Advance`.advance_amount as advance_amount, `tabEmployee Advance`.status as status
                from `tabEmployee Advance` join `tabExpense Claim Advance` on `tabEmployee Advance`.name = `tabExpense Claim Advance`.employee_advance
                where  `tabExpense Claim Advance`.parent = "{cur_nam}"
                and (`tabEmployee Advance`.name like '%{search_text}%' ) LIMIT {start},{page_length}
            """.format(
                start=start,
                page_length=page_length,
                cur_nam=cur_nam,
                search_text=search_text,
            ),
            as_dict=1,
        )

        if connections:
            return connections
        else:
            return "لا يوجد روابط !"

    ########################### Expense Claim Type List & Search ############################
    if doctype == "Loan Type" and con_doc == "%%":
        query = frappe.db.get_list(
            "Loan Type",
            fields=[
                "name",
                "rate_of_interest",
                "is_term_loan",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Loan Application Full List & Search ############################
    if doctype == "Loan Application" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["employee_name"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%":
            conditions["applicant_type"] = filter2
        if filter3 != "%%":
            conditions["applicant"] = filter3
        if filter4 != "%%":
            conditions["loan_type"] = filter4
        if filter5 != "%%" and filter6 == "%%":
            conditions["posting_date"] = [">=", filter5]
        if filter6 != "%%" and filter5 == "%%":
            conditions["posting_date"] = ["<=", filter6]
        if filter5 != "%%" and filter6 != "%%":
            conditions["posting_date"] = ["between", [filter5, filter6]]

        query = frappe.db.get_list(
            "Loan Application",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "applicant_type",
                "applicant_name",
                "applicant",
                "posting_date",
                "loan_type",
                "loan_amount",
                "status",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )

        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Bank Account List & Search ############################
    if doctype == "Bank Account" and con_doc == "%%":
        query = frappe.db.get_list(
            "Bank Account",
            fields=["name"],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Customer Visit" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["employee_name"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["customer"] = filter1
        if filter2 != "%%":
            conditions["customer_address"] = filter2
        if filter3 != "%%" and filter4 == "%%":
            conditions["posting_date"] = [">=", filter3]
        if filter4 != "%%" and filter3 == "%%":
            conditions["posting_date"] = ["<=", filter4]
        if filter3 != "%%" and filter4 != "%%":
            conditions["posting_date"] = ["between", [filter3, filter4]]
        if filter5 != "%%":
            conditions["owner"] = filter5

        query = frappe.db.get_list(
            "Customer Visit",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "customer",
                "customer_address",
                "posting_date",
                "time",
                "owner",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Address" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["address_title"] = ["like", search_text]
            or_conditions["address_line1"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["address_type"] = filter1
        if filter2 != "%%" and filter3 != "%%":
            address = frappe.qb.DocType("Address")
            dynamic_link = frappe.qb.DocType("Dynamic Link")
            q = (
                frappe.qb.from_(address)
                .join(dynamic_link)
                .on(dynamic_link.parent == address.name)
                .select(
                    address.name,
                    address.address_title,
                    address.address_type,
                    address.address_line1,
                    address.city,
                    address.country,
                )
                .where(dynamic_link.link_doctype == filter2)
                .where(dynamic_link.link_name == filter3)
            ).run(as_dict=True)
            for x in range(len(q)):
                link_doctype = frappe.db.get_value(
                    "Dynamic Link",
                    {
                        "parent": q[x].name,
                    },
                    "link_doctype",
                )
                link_name = frappe.db.get_value(
                    "Dynamic Link",
                    {
                        "parent": q[x].name,
                    },
                    "link_name",
                )
                q[x]["link_doctype"] = link_doctype
                q[x]["link_name"] = link_name
            return q
        if filter2 != "%%":
            address = frappe.qb.DocType("Address")
            dynamic_link = frappe.qb.DocType("Dynamic Link")
            q = (
                frappe.qb.from_(address)
                .inner_join(dynamic_link)
                .on(dynamic_link.parent == address.name)
                .select(
                    address.name,
                    address.address_title,
                    address.address_type,
                    address.address_line1,
                    address.city,
                    address.country,
                )
                .where(dynamic_link.link_doctype == filter2)
            ).run(as_dict=True)
            for x in range(len(q)):
                link_doctype = frappe.db.get_value(
                    "Dynamic Link",
                    {
                        "parent": q[x].name,
                    },
                    "link_doctype",
                )
                link_name = frappe.db.get_value(
                    "Dynamic Link",
                    {
                        "parent": q[x].name,
                    },
                    "link_name",
                )
                q[x]["link_doctype"] = link_doctype
                q[x]["link_name"] = link_name
            return q
        query = frappe.db.get_list(
            "Address",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "address_title",
                "address_type",
                "address_line1",
                "city",
                "country",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        # for x in range(len(query)):

        #     link_doctype = frappe.db.get_value(
        #         "Dynamic Link",
        #         {
        #             "parent": query[x].name,
        #         },
        #         "link_doctype",
        #     )
        #     link_name = frappe.db.get_value(
        #         "Dynamic Link",
        #         {
        #             "parent": query[x].name,
        #         },
        #         "link_name",
        #     )
        #     query[x]["link_doctype"] = link_doctype
        #     query[x]["link_name"] = link_name
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Contact" and con_doc == "%%":
        or_conditions = {}
        conditions = {}
        if search_text != "%%":
            or_conditions["mobile_no"] = ["like", search_text]
            or_conditions["phone"] = ["like", search_text]
            or_conditions["first_name"] = ["like", search_text]
            or_conditions["email_id"] = ["like", search_text]
            or_conditions["name"] = ["like", search_text]
        if filter1 != "%%":
            conditions["status"] = filter1
        if filter2 != "%%" and filter3 != "%%":
            address = frappe.qb.DocType("Contact")
            dynamic_link = frappe.qb.DocType("Dynamic Link")
            q = (
                frappe.qb.from_(address)
                .join(dynamic_link)
                .on(dynamic_link.parent == address.name)
                .select(
                    address.name,
                    address.first_name,
                    address.user,
                    address.mobile_no,
                    address.phone,
                    address.email_id,
                )
                .where(dynamic_link.link_doctype == filter2)
                .where(dynamic_link.link_name == filter3)
            ).run(as_dict=True)
            for x in range(len(q)):
                link_doctype = frappe.db.get_value(
                    "Dynamic Link",
                    {
                        "parent": q[x].name,
                    },
                    "link_doctype",
                )
                link_name = frappe.db.get_value(
                    "Dynamic Link",
                    {
                        "parent": q[x].name,
                    },
                    "link_name",
                )
                q[x]["link_doctype"] = link_doctype
                q[x]["link_name"] = link_name
            return q
        if filter2 != "%%":
            address = frappe.qb.DocType("Contact")
            dynamic_link = frappe.qb.DocType("Dynamic Link")
            q = (
                frappe.qb.from_(address)
                .inner_join(dynamic_link)
                .on(dynamic_link.parent == address.name)
                .select(
                    address.name,
                    address.first_name,
                    address.user,
                    address.mobile_no,
                    address.phone,
                    address.email_id,
                )
                .where(dynamic_link.link_doctype == filter2)
            ).run(as_dict=True)
            for x in range(len(q)):
                link_doctype = frappe.db.get_value(
                    "Dynamic Link",
                    {
                        "parent": q[x].name,
                    },
                    "link_doctype",
                )
                link_name = frappe.db.get_value(
                    "Dynamic Link",
                    {
                        "parent": q[x].name,
                    },
                    "link_name",
                )
                q[x]["link_doctype"] = link_doctype
                q[x]["link_name"] = link_name
            return q
        query = frappe.db.get_list(
            "Contact",
            or_filters=or_conditions,
            filters=conditions,
            fields=[
                "name",
                "first_name",
                "user",
                "mobile_no",
                "phone",
                "email_id",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        for x in range(len(query)):
            link_doctype = frappe.db.get_value(
                "Dynamic Link",
                {
                    "parent": query[x].name,
                },
                "link_doctype",
            )
            link_name = frappe.db.get_value(
                "Dynamic Link",
                {
                    "parent": query[x].name,
                },
                "link_name",
            )
            query[x]["link_doctype"] = link_doctype
            query[x]["link_name"] = link_name
        if query:
            return query
        else:
            return "لا يوجد !"

    ########################### Asset Category Type List & Search ############################
    if doctype == "Asset Category" and con_doc == "%%":
        query = frappe.db.get_list(
            "Asset Category",
            fields=[
                "name",
                "asset_category_name",
                "enable_cwip_accounting",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"
    ################################# Free Items ########################
    if doctype == "Free Items" and con_doc == "%%":
        conditions = {}
        conditions1 = {}
        if search_text != "%%":
            conditions1["name"] = ["like", search_text]
            conditions1["item_name"] = ["like", search_text]
            conditions1["item_code"] = ["like", search_text]
        if filter1 != "%%":
            conditions["item_group"] = filter1
        if filter2 != "%%":
            conditions["brand"] = filter2
        if filter3 != "%%":
            conditions["stock_uom"] = filter3
        query = frappe.db.get_list(
            "Free Items",
            or_filters=conditions1,
            filters=conditions,
            fields=[
                "name",
                "item_code",
                "item_name",
                "item_group",
                "stock_uom as uom",
                "image",
            ],
            order_by=order_by(sort_field, sort_type),
            start=start,
            page_length=page_length,
        )
        if query:
            return query
        else:
            return "لا يوجد !"

    if doctype == "Governorate":
        results = frappe.db.sql("""
                SELECT 
                    name,
                    governorate_name
                FROM `tabGovernorate`AS G
            """, as_dict=True)
        return results


@frappe.whitelist()
def get_user_default_warehouse():
    user_id = frappe.session.user
    warehouse = frappe.db.get_all(
        "User Permission",
        fields=["for_value"],
        filters={
            "user": user_id,
            "allow": "Warehouse",
            "is_default": True,
        },
    )
    if warehouse:
        warehouse = warehouse[0]
    else:
        response = frappe.response["message"] = {
            "error_message": "please set a default warehouse in the user perissions"
        }
        return response

    response = frappe.response["message"] = {
        "default_warehouse": warehouse["for_value"]
    }
    return response


@frappe.whitelist()
def get_item_uoms(item_code):
    try:
        item = frappe.get_doc("Item", item_code)
        uoms = []
        for uom in item.uoms:
            uoms.append(
                dict(
                    name=uom.name, uom=uom.uom, conversion_factor=uom.conversion_factor
                )
            )
        response = frappe.response["message"] = uoms
        return response

    except:
        response = frappe.response["message"] = {
            "success": False,
            "error": "Can't found an item with the provided item code",
        }
        return response


@frappe.whitelist()
def get_item_list(
        allow_sales=None,
        allow_purchase=None,
        search_text="%%",
        price_list="%%",
        start=0,
        page_length=5,
):
    conditions = ""
    if allow_purchase is not None:
        conditions += f" and tabItem.is_purchase_item = {allow_purchase} "

    if allow_sales is not None:
        conditions += f" and tabItem.is_sales_item = {allow_sales}"

    if search_text != "%%":
        items = frappe.db.sql(
            f""" select tabItem.name as name ,
                                                    tabItem.item_code as item_code,
                                                    tabItem.is_sales_item,
                                                    tabItem.is_purchase_item,
                                                    tabItem.item_name as item_name, 
                                                    tabItem.item_group as item_group, 
                                                    tabItem.stock_uom as stock_uom, 
                                                    tabItem.image as image,
                                                    tabItem.sales_uom as sales_uom,
                                                    ifnull((select max(price_list_rate)  from `tabItem Price` where item_code = tabItem.name and price_list = '{price_list}'),0) as price_list_rate,
                                                    ifnull((select distinct `tabItem Tax Template Detail`.tax_rate from `tabItem Tax Template Detail` join `tabItem Tax` 
                                                    where `tabItem Tax Template Detail`.parent = `tabItem Tax`.item_tax_template and `tabItem Tax`.parent = `tabItem`.name),0) as tax_percent
                                                    from tabItem
                                                    where tabItem.name like '%{search_text}%'
                                                    or tabItem.item_name like '%{search_text}%'
                                                    {conditions}
                                                    and tabItem.disabled = 0
                                                    LIMIT {start}, {page_length}""",
            as_dict=True,
        )
        result = []
        for item_dict in items:
            if item_dict.tax_percent > 0 and item_dict.price_list_rate > 0:
                net_rate = item_dict.price_list_rate * (
                        1 + (item_dict.tax_percent / 100)
                )
                vat_value = net_rate - item_dict.price_list_rate
                data = {
                    "name": item_dict.name,
                    "item_code": item_dict.item_code,
                    "item_name": item_dict.item_name,
                    "item_group": item_dict.item_group,
                    "allow_sales": item_dict.is_sales_item,
                    "allow_purchase": item_dict.is_purchase_item,
                    "uom": item_dict.stock_uom,
                    "stock_uom": item_dict.stock_uom,
                    "image": item_dict.image,
                    "sales_uom": item_dict.sales_uom,
                    "price_list_rate": item_dict.price_list_rate,
                    "tax_percent": item_dict.tax_percent,
                    "net_rate": net_rate,
                    "vat_value": vat_value,
                }
                result.append(data)
            else:
                data = {
                    "name": item_dict.name,
                    "item_code": item_dict.item_code,
                    "item_name": item_dict.item_name,
                    "item_group": item_dict.item_group,
                    "allow_sales": item_dict.is_sales_item,
                    "allow_purchase": item_dict.is_purchase_item,
                    "uom": item_dict.stock_uom,
                    "stock_uom": item_dict.stock_uom,
                    "image": item_dict.image,
                    "sales_uom": item_dict.sales_uom,
                    "price_list_rate": item_dict.price_list_rate,
                    "tax_percent": item_dict.tax_percent,
                    "net_rate": item_dict.price_list_rate,
                }
                result.append(data)

        if items:
            return result
        else:
            return "لا يوجد منتجات !"
    else:
        items = frappe.db.sql(
            f""" select tabItem.name as name,
                                        tabItem.item_code as item_code,
                                        tabItem.item_name as item_name,
                                        tabItem.is_sales_item,
                                        tabItem.is_purchase_item, 
                                        tabItem.item_group as item_group, 
                                        tabItem.stock_uom as stock_uom, 
                                        tabItem.image as image,
                                        tabItem.sales_uom as sales_uom,
                                        ifnull((select max(price_list_rate) from `tabItem Price` where item_code = tabItem.name and price_list = '{price_list}'),0) as price_list_rate,
                                        ifnull((select distinct `tabItem Tax Template Detail`.tax_rate from `tabItem Tax Template Detail` join `tabItem Tax` 
                                        where `tabItem Tax Template Detail`.parent = `tabItem Tax`.item_tax_template and `tabItem Tax`.parent = `tabItem`.name),0) as tax_percent
                                        from tabItem 
                                        where tabItem.disabled = 0 
                                        {conditions}
                                        LIMIT {start},{page_length} """,
            as_dict=True,
        )

        result = []
        for item_dict in items:
            if item_dict.tax_percent > 0 and item_dict.price_list_rate > 0:
                net_rate = item_dict.price_list_rate * (
                        1 + (item_dict.tax_percent / 100)
                )
                vat_value = net_rate - item_dict.price_list_rate
                data = {
                    "name": item_dict.name,
                    "item_code": item_dict.item_code,
                    "item_name": item_dict.item_name,
                    "allow_sales": item_dict.is_sales_item,
                    "allow_purchase": item_dict.is_purchase_item,
                    "item_group": item_dict.item_group,
                    "uom": item_dict.stock_uom,
                    "stock_uom": item_dict.stock_uom,
                    "image": item_dict.image,
                    "sales_uom": item_dict.sales_uom,
                    "price_list_rate": item_dict.price_list_rate,
                    "tax_percent": item_dict.tax_percent,
                    "net_rate": net_rate,
                    "vat_value": vat_value,
                }
                result.append(data)
            else:
                data = {
                    "name": item_dict.name,
                    "item_code": item_dict.item_code,
                    "item_name": item_dict.item_name,
                    "allow_sales": item_dict.is_sales_item,
                    "allow_purchase": item_dict.is_purchase_item,
                    "item_group": item_dict.item_group,
                    "uom": item_dict.stock_uom,
                    "stock_uom": item_dict.stock_uom,
                    "image": item_dict.image,
                    "sales_uom": item_dict.sales_uom,
                    "price_list_rate": item_dict.price_list_rate,
                    "tax_percent": item_dict.tax_percent,
                    "net_rate": item_dict.price_list_rate,
                }
                result.append(data)

        if items:
            return result
        else:
            return "لا يوجد منتجات !"


@frappe.whitelist(methods=["GET"])
def get_reports(module):
    mobile_user = frappe.db.get_all(
        "Mobile User", filters={"user": frappe.session.user}
    )
    if not mobile_user:
        frappe.throw(
            "The logged in user is not a mobile user.",
            frappe.exceptions.ValidationError,
        )

    mobile_user_id = mobile_user[0]["name"]
    mobile_reports = frappe.db.get_all(
        "Mobile Reports Table",
        filters={"parent": mobile_user_id, "module": module},
        fields=["report_name"],
    )

    if mobile_reports:
        return mobile_reports

    frappe.throw("There is no reports to show", frappe.exceptions.DoesNotExistError)


@frappe.whitelist(methods=["GET"])
def get_governorates():
    results = frappe.db.sql("""
        SELECT 
            name,
            governorate_name
        FROM `tabGovernorate`AS G
    """, as_dict=True)
    return results


@frappe.whitelist(methods=["GET"])
def get_faqs():
    filters = dict(frappe.local.request.args) or {}
    faqs = frappe.get_all("FAQ", fields=["question", "answer", "tag"], filters=filters)

    if not faqs:
        frappe.response['http_status_code'] = 404

    for faq in faqs:
        faq["answer_without_html"] = remove_html_tags(str(faq["answer"]))
    return faqs

