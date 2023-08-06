from __future__ import unicode_literals
import frappe
import erpnext
from frappe import auth
import random
import datetime
import json, ast
from erpnext.accounts.utils import get_balance_on
from frappe.utils import (flt, getdate, get_url, now,
                          nowtime, get_time, today, get_datetime, add_days)
from frappe.utils import add_to_date, now, nowdate
from frappe.utils import cstr
from frappe.utils.make_random import get_random


@frappe.whitelist()
def filtered_connections(cur_doc, cur_nam, con_doc, search_text=0):
    if cur_doc == "Lead" and con_doc == "Quotation":
        connections = frappe.db.sql(
            """ select name, quotation_to, customer_name, transaction_date, grand_total, status
                from `tabQuotation` where `party_name` = '{cur_nam}'
                and (name like '%{search_text}%' or customer_name like '%{search_text}%')
            """.format(cur_nam=cur_nam, search_text=search_text), as_dict=1)
        result = []
        for item_dict in connections:
            data = {
                'name': item_dict.name,
                'quotation_to': item_dict.quotation_to,
                'customer_name': item_dict.customer_name,
                'transaction_date': item_dict.transaction_date,
                'grand_total': item_dict.grand_total,
                'status': item_dict.status
            }
            result.append(data)

        if connections:
            return result

        else:
            return "لا يوجد روابط !"


    elif cur_doc == "Lead" and con_doc == "Opportunity":
        connections = frappe.db.sql(
            """ select name,opportunity_from,customer_name,transaction_date,opportunity_type,sales_stage,status 
                from `tabOpportunity` where `party_name` = '{cur_nam}'
                and (name like '%{search_text}%' or customer_name like '%{search_text}%' or party_name like '%{search_text}%')
            """.format(cur_nam=cur_nam, search_text=search_text), as_dict=1)
        result = []
        for item_dict in connections:
            data = {
                'name': item_dict.name,
                'opportunity_from': item_dict.opportunity_from,
                'customer_name': item_dict.customer_name,
                'transaction_date': item_dict.transaction_date,
                'opportunity_type': item_dict.opportunity_type,
                'sales_stage': item_dict.sales_stage,
                'status': item_dict.status
            }
            result.append(data)
        if connections:
            return result
        else:
            return "لا يوجد روابط !"

    elif cur_doc == "Opportunity" and con_doc == "Quotation":
        connections = frappe.db.sql(
            """ select name, quotation_to, customer_name, transaction_date, grand_total, status 
                from `tabQuotation` where `opportunity` = '{cur_nam}'
                and (name like '%{search_text}%' or customer_name like '%{search_text}%')
            """.format(cur_nam=cur_nam, search_text=search_text), as_dict=1)
        result = []
        for item_dict in connections:
            data = {
                'name': item_dict.name,
                'quotation_to': item_dict.quotation_to,
                'customer_name': item_dict.customer_name,
                'transaction_date': item_dict.transaction_date,
                'grand_total': item_dict.grand_total,
                'status': item_dict.status
            }
            result.append(data)
        if connections:
            return result
        else:
            return "لا يوجد روابط !"

    elif cur_doc == "Opportunity" and con_doc == "Supplier Quotation":
        connections = frappe.db.sql(
            """ select name,supplier,transaction_date,valid_till,grand_total,status from `tabSupplier Quotation` where `opportunity` = '{cur_nam}' """.format(
                cur_nam=cur_nam), as_dict=1)
        result = []
        for item_dict in connections:
            data = {
                'name': item_dict.name,
                'supplier': item_dict.supplier,
                'transaction_date': item_dict.transaction_date,
                'valid_till': item_dict.valid_till,
                'grand_total': item_dict.grand_total,
                'status': item_dict.status
            }
            result.append(data)
        if connections:
            return result
        else:
            return "لا يوجد روابط !"

    elif cur_doc == "Quotation" and con_doc == "Sales Order":
        connections = frappe.db.sql(""" select distinct `tabSales Order`.name as name,`tabSales Order`.customer_name as customer_name,`tabSales Order`.customer_address as customer_address,
                                               `tabSales Order`.transaction_date as transaction_date,`tabSales Order`.grand_total as grand_total,`tabSales Order`.status as status
                                        from `tabSales Order` join `tabSales Order Item` on `tabSales Order`.name = `tabSales Order Item`.parent
                                        where `tabSales Order Item`.prevdoc_docname = '{cur_nam}'
                                    """.format(cur_nam=cur_nam), as_dict=1)
        result = []
        for item_dict in connections:
            data = {
                'name': item_dict.name,
                'customer_name': item_dict.customer_name,
                'customer_address': item_dict.customer_address,
                'transaction_date': item_dict.transaction_date,
                'grand_total': item_dict.grand_total,
                'status': item_dict.status
            }
            result.append(data)
        if connections:
            return result
        else:
            return "لا يوجد روابط !"

    elif cur_doc == "Customer" and con_doc == "Quotation":
        connections = frappe.db.sql(
            """ select name, quotation_to, customer_name, transaction_date, grand_total, status
                from `tabQuotation` where `party_name` = '{cur_nam}'
                and (name like '%{search_text}%' or customer_name like '%{search_text}%')
            """.format(cur_nam=cur_nam, search_text=search_text), as_dict=1)
        result = []
        for item_dict in connections:
            data = {
                'name': item_dict.name,
                'quotation_to': item_dict.quotation_to,
                'customer_name': item_dict.customer_name,
                'transaction_date': item_dict.transaction_date,
                'grand_total': item_dict.grand_total,
                'status': item_dict.status
            }
            result.append(data)
        if connections:
            return result
        else:
            return "لا يوجد روابط !"

    elif cur_doc == "Customer" and con_doc == "Opportunity":
        connections = frappe.db.sql(
            """ select name,opportunity_from,customer_name,transaction_date,opportunity_type,sales_stage,status 
                from `tabOpportunity` where `party_name` = '{cur_nam}'
                and (name like '%{search_text}%' or customer_name like '%{search_text}%' or party_name like '%{search_text}%')
            """.format(cur_nam=cur_nam, search_text=search_text), as_dict=1)
        result = []
        for item_dict in connections:
            data = {
                'name': item_dict.name,
                'opportunity_from': item_dict.opportunity_from,
                'customer_name': item_dict.customer_name,
                'transaction_date': item_dict.transaction_date,
                'opportunity_type': item_dict.opportunity_type,
                'sales_stage': item_dict.sales_stage,
                'status': item_dict.status
            }
            result.append(data)
        if connections:
            return result
        else:
            return "لا يوجد روابط !"

    elif cur_doc == "Customer" and con_doc == "Sales Order":
        connections = frappe.db.sql(
            """ select name,customer_name,customer_address,transaction_date,grand_total,status from `tabSales Order` where `customer` = '{cur_nam}' """.format(
                cur_nam=cur_nam), as_dict=1)
        result = []
        for item_dict in connections:
            data = {
                'name': item_dict.name,
                'customer_name': item_dict.customer_name,
                'customer_address': item_dict.customer_address,
                'transaction_date': item_dict.transaction_date,
                'grand_total': item_dict.grand_total,
                'status': item_dict.status
            }
            result.append(data)
        if connections:
            return result
        else:
            return "لا يوجد روابط !"

    elif cur_doc == "Customer" and con_doc == "Delivery Note":
        connections = frappe.db.sql(
            """ select name,customer,territory,posting_date,set_warehouse,status from `tabDelivery Note` where `customer` = '{cur_nam}' """.format(
                cur_nam=cur_nam), as_dict=1)
        result = []
        for item_dict in connections:
            data = {
                'name': item_dict.name,
                'customer': item_dict.customer,
                'territory': item_dict.territory,
                'posting_date': item_dict.posting_date,
                'set_warehouse': item_dict.set_warehouse,
                'status': item_dict.status
            }
            result.append(data)
        if connections:
            return result
        else:
            return "لا يوجد روابط !"

    elif cur_doc == "Customer" and con_doc == "Sales Invoice":
        connections = frappe.db.sql(
            """ select name,customer_name,customer_address,posting_date,grand_total,status from `tabSales Invoice` where `customer` = '{cur_nam}' """.format(
                cur_nam=cur_nam), as_dict=1)
        result = []
        for item_dict in connections:
            data = {
                'name': item_dict.name,
                'customer_name': item_dict.customer_name,
                'customer_address': item_dict.customer_address,
                'posting_date': item_dict.posting_date,
                'grand_total': item_dict.grand_total,
                'status': item_dict.status
            }
            result.append(data)
        if connections:
            return result
        else:
            return "لا يوجد روابط !"

    elif cur_doc == "Customer" and con_doc == "Payment Entry":
        connections = frappe.db.sql(
            """ select name,party_name,payment_type,mode_of_payment,posting_date,paid_amount,status from `tabPayment Entry` where `party` = '{cur_nam}' """.format(
                cur_nam=cur_nam), as_dict=1)
        result = []
        for item_dict in connections:
            data = {
                'name': item_dict.name,
                'party_name': item_dict.party_name,
                'payment_type': item_dict.payment_type,
                'mode_of_payment': item_dict.mode_of_payment,
                'posting_date': item_dict.posting_date,
                'paid_amount': item_dict.paid_amount,
                'status': item_dict.status
            }
            result.append(data)
        if connections:
            return result
        else:
            return "لا يوجد روابط !"

    elif cur_doc == "Sales Order" and con_doc == "Sales Invoice":
        connections = frappe.db.sql(""" select distinct `tabSales Invoice`.name as name,`tabSales Invoice`.customer_name as customer_name,`tabSales Invoice`.customer_address as customer_address,
                                               `tabSales Invoice`.posting_date as posting_date,`tabSales Invoice`.grand_total as grand_total,`tabSales Invoice`.status as status
                                        from `tabSales Invoice` join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent
                                        where `sales_order` = '{cur_nam}' """.format(cur_nam=cur_nam), as_dict=1)
        result = []
        for item_dict in connections:
            data = {
                'name': item_dict.name,
                'customer_name': item_dict.customer_name,
                'customer_address': item_dict.customer_address,
                'posting_date': item_dict.posting_date,
                'grand_total': item_dict.grand_total,
                'status': item_dict.status
            }
            result.append(data)
        if connections:
            return result
        else:
            return "لا يوجد روابط !"

    elif cur_doc == "Sales Order" and con_doc == "Delivery Note":
        connections = frappe.db.sql(""" select distinct `tabDelivery Note`.name as name,`tabDelivery Note`.customer as customer,`tabDelivery Note`.territory as territory,
                                               `tabDelivery Note`.posting_date as posting_date,`tabDelivery Note`.set_warehouse as set_warehouse,`tabDelivery Note`.status as status
                                        from `tabDelivery Note` join `tabDelivery Note Item` on `tabDelivery Note`.name = `tabDelivery Note Item`.parent
                                        where `against_sales_order` = '{cur_nam}' """.format(cur_nam=cur_nam),
                                    as_dict=1)
        result = []
        for item_dict in connections:
            data = {
                'name': item_dict.name,
                'customer': item_dict.customer,
                'territory': item_dict.territory,
                'posting_date': item_dict.posting_date,
                'set_warehouse': item_dict.set_warehouse,
                'status': item_dict.status
            }
            result.append(data)
        if connections:
            return result
        else:
            return "لا يوجد روابط !"

    elif cur_doc == "Sales Order" and con_doc == "Material Request":
        connections = frappe.db.sql(""" select distinct `tabMaterial Request`.name as name,`tabMaterial Request`.material_request_type as material_request_type,
                                              `tabMaterial Request`.transaction_date as transaction_date,`tabMaterial Request`.set_warehouse as set_warehouse,`tabMaterial Request`.status as status
                                        from `tabMaterial Request` join `tabMaterial Request Item` on `tabMaterial Request`.name = `tabMaterial Request Item`.parent
                                        where `sales_order` = '{cur_nam}' """.format(cur_nam=cur_nam), as_dict=1)
        result = []
        for item_dict in connections:
            data = {
                'name': item_dict.name,
                'material_request_type': item_dict.material_request_type,
                'transaction_date': item_dict.transaction_date,
                'set_warehouse': item_dict.set_warehouse,
                'status': item_dict.status
            }
            result.append(data)
        if connections:
            return result
        else:
            return "لا يوجد روابط !"

    elif cur_doc == "Sales Order" and con_doc == "Purchase Order":
        connections = frappe.db.sql(""" select distinct `tabPurchase Order`.name as name,`tabPurchase Order`.supplier as supplier, `tabPurchase Order`.grand_total as grand_total,
                                              `tabPurchase Order`.transaction_date as transaction_date,`tabPurchase Order`.set_warehouse as set_warehouse,`tabPurchase Order`.status as status
                                        from `tabPurchase Order` join `tabPurchase Order Item` on `tabPurchase Order`.name = `tabPurchase Order Item`.parent
                                        where `sales_order` = '{cur_nam}' """.format(cur_nam=cur_nam), as_dict=1)
        result = []



        for item_dict in connections:
            data = {
                'name': item_dict.name,
                'supplier': item_dict.supplier,
                'set_warehouse': item_dict.set_warehouse,
                'transaction_date': item_dict.transaction_date,
                'grand_total': item_dict.grand_total,
                'status': item_dict.status
            }
            result.append(data)
        if connections:
            return result
        else:
            return "لا يوجد روابط !"

    elif cur_doc == "Sales Order" and con_doc == "Quotation":
        connections = frappe.db.sql(""" select distinct `tabQuotation`.name as name, `tabQuotation`.quotation_to as quotation_to, `tabQuotation`.customer_name as customer_name,
                                               `tabQuotation`.transaction_date as transaction_date, `tabQuotation`.grand_total as grand_total, `tabQuotation`.status as status
                                        from `tabQuotation` join `tabSales Order Item` on `tabQuotation`.name = `tabSales Order Item`.prevdoc_docname
                                        where `tabSales Order Item`.parent = '{cur_nam}'
                                        and (`tabQuotation`.name like '%{search_text}%' or `tabQuotation`.customer_name like '%{search_text}%')
                                    """.format(cur_nam=cur_nam, search_text=search_text), as_dict=1)
        result = []
        for item_dict in connections:
            data = {
                'name': item_dict.name,
                'quotation_to': item_dict.quotation_to,
                'customer_name': item_dict.customer_name,
                'transaction_date': item_dict.transaction_date,
                'grand_total': item_dict.grand_total,
                'status': item_dict.status
            }
            result.append(data)
        if connections:
            return result
        else:
            return "لا يوجد روابط !"

    elif cur_doc == "Sales Order" and con_doc == "Payment Entry":
        connections = frappe.db.sql(""" select distinct `tabPayment Entry`.name as name,`tabPayment Entry`.party_name as party_name,
                                               `tabPayment Entry`.payment_type as payment_type,`tabPayment Entry`.mode_of_payment as mode_of_payment,
                                               `tabPayment Entry`.posting_date as posting_date,`tabPayment Entry`.paid_amount as paid_amount,`tabPayment Entry`.status as status
                                        from `tabPayment Entry` join `tabPayment Entry Reference` on `tabPayment Entry`.name = `tabPayment Entry Reference`.parent
                                        where `reference_name` = '{cur_nam}' """.format(cur_nam=cur_nam), as_dict=1)
        result = []
        for item_dict in connections:
            data = {
                'name': item_dict.name,
                'party_name': item_dict.party_name,
                'payment_type': item_dict.payment_type,
                'mode_of_payment': item_dict.mode_of_payment,
                'posting_date': item_dict.posting_date,
                'paid_amount': item_dict.paid_amount,
                'status': item_dict.status
            }
            result.append(data)
        if connections:
            return result
        else:
            return "لا يوجد روابط !"

    elif cur_doc == "Sales Invoice" and con_doc == "Sales Order":
        connections = frappe.db.sql(""" select distinct `tabSales Order`.name as name,`tabSales Order`.customer_name as customer_name,`tabSales Order`.customer_address as customer_address,
                                               `tabSales Order`.transaction_date as transaction_date,`tabSales Order`.grand_total as grand_total,`tabSales Order`.status as status
                                        from `tabSales Order` join `tabSales Invoice Item` on `tabSales Order`.name = `tabSales Invoice Item`.sales_order
                                        where `tabSales Invoice Item`.parent = '{cur_nam}'
                                    """.format(cur_nam=cur_nam), as_dict=1)
        result = []
        for item_dict in connections:
            data = {
                'name': item_dict.name,
                'customer_name': item_dict.customer_name,
                'customer_address': item_dict.customer_address,
                'transaction_date': item_dict.transaction_date,
                'grand_total': item_dict.grand_total,
                'status': item_dict.status
            }
            result.append(data)
        if connections:
            return result
        else:
            return "لا يوجد روابط !"

    elif cur_doc == "Sales Invoice" and con_doc == "Delivery Note":
        connections = frappe.db.sql(""" select distinct `tabDelivery Note`.name as name,`tabDelivery Note`.customer as customer,`tabDelivery Note`.territory as territory,
                                               `tabDelivery Note`.posting_date as posting_date,`tabDelivery Note`.set_warehouse as set_warehouse,`tabDelivery Note`.status as status
                                        from `tabDelivery Note` join `tabDelivery Note Item` on `tabDelivery Note`.name = `tabDelivery Note Item`.parent
                                        where `against_sales_invoice` = '{cur_nam}' """.format(cur_nam=cur_nam),
                                    as_dict=1)
        result = []
        for item_dict in connections:
            data = {
                'name': item_dict.name,
                'customer': item_dict.customer,
                'territory': item_dict.territory,
                'posting_date': item_dict.posting_date,
                'set_warehouse': item_dict.set_warehouse,
                'status': item_dict.status
            }
            result.append(data)
        if connections:
            return result
        else:
            return "لا يوجد روابط !"

    elif cur_doc == "Sales Invoice" and con_doc == "Payment Entry":
        connections = frappe.db.sql(""" select distinct `tabPayment Entry`.name as name,`tabPayment Entry`.party_name as party_name,
                                               `tabPayment Entry`.payment_type as payment_type,`tabPayment Entry`.mode_of_payment as mode_of_payment,
                                               `tabPayment Entry`.posting_date as posting_date,`tabPayment Entry`.paid_amount as paid_amount,`tabPayment Entry`.status as status
                                        from `tabPayment Entry` join `tabPayment Entry Reference` on `tabPayment Entry`.name = `tabPayment Entry Reference`.parent
                                        where `reference_name` = '{cur_nam}' """.format(cur_nam=cur_nam), as_dict=1)
        result = []
        for item_dict in connections:
            data = {
                'name': item_dict.name,
                'party_name': item_dict.party_name,
                'payment_type': item_dict.payment_type,
                'mode_of_payment': item_dict.mode_of_payment,
                'posting_date': item_dict.posting_date,
                'paid_amount': item_dict.paid_amount,
                'status': item_dict.status
            }
            result.append(data)
        if connections:
            return result
        else:
            return "لا يوجد روابط !"
