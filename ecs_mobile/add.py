from __future__ import unicode_literals
import frappe
import traceback
import unicodedata
from frappe import auth
import datetime
import json, ast
from frappe import _
import requests


@frappe.whitelist(allow_guest=True)
def lead(**kwargs):
    lead = frappe.get_doc(kwargs["data"])
    lead.insert()
    lead_name = lead.name
    frappe.db.commit()
    if lead_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "lead": lead_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist(allow_guest=True)
def opportunity(**kwargs):
    opportunity = frappe.get_doc(kwargs["data"])

    opportunity.insert()
    opportunity_name = opportunity.name
    frappe.db.commit()
    if opportunity_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "opportunity": opportunity_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist(allow_guest=True)
def quotation(**kwargs):
    quotation = frappe.get_doc(kwargs["data"])
    quotation.insert()
    quotation_name = quotation.name
    frappe.db.commit()
    if quotation_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "quotation": quotation_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist(allow_guest=True)
def customer(**kwargs):
    customer = frappe.new_doc("Customer")
    customer.customer_name = kwargs["data"].get("customer_name", None)
    customer.mobile_no = kwargs["data"].get("mobile_no", None)
    customer.mobile2 = kwargs["data"].get("mobile2", None)
    customer.lead_name = kwargs["data"].get("lead_name", None)
    customer.customer_type = kwargs["data"].get("customer_type", None)
    customer.customer_group = kwargs["data"].get("customer_group", None)
    customer.territory = kwargs["data"].get("territory", None)
    customer.market_segment = kwargs["data"].get("market_segment", None)
    customer.industry = kwargs["data"].get("industry", None)
    customer.tax_id = kwargs["data"].get("tax_id", None)    
    customer.default_currency = kwargs["data"].get("default_currency", None)
    customer.default_price_list = kwargs["data"].get("default_price_list", None)
    customer.default_sales_partner = kwargs["data"].get("default_sales_partner", None)
    customer.payment_terms = kwargs["data"].get("payment_terms", None)
    customer.longitude = kwargs["data"].get("longitude", None)
    customer.latitude = kwargs["data"].get("latitude", None)
    customer.append("credit_limits", kwargs["data"].get("credit_limits")[0])
    customer.new_governorate = kwargs["data"].get("new_governorate", None)

    # START CODE THAT ONLY FROM EGUE AND ITS SIMILAR
    # only for egeu and company that like it, because each customer has exactly one sales_person
    # also the key is 'sales_person' not 'sales_team'
    kwargs["data"]["sales_team"] = [{"sales_person": kwargs["sales_person"]}]
    # END CODE THAT FOR ONLY EGUE AND ITS SIMILAR

    sales_team = kwargs["data"]["sales_team"]
    if len(sales_team) == 1:
        sales_team[0]["allocated_percentage"] = 100
        sales_team[0]["commission_rate"] = 2

    for x in sales_team:
        customer.append("sales_team", x)

    customer.insert()
    customer_name = customer.name
    # credit_limit = [
    #     {
    #         "doctype": "Customer Credit Limit",
    #         "credit_limit": kwargs["data"]["credit_limits"]["credit_limit"],
    #         "bypass_credit_limit_check": kwargs["data"]["credit_limits"][
    #             "bypass_credit_limit_check"
    #         ],
    #     }
    # ]

    # customer.credit_limits = credit_limit

    # contact = frappe.new_doc("Contact")
    # contact_link = [
    #     {
    #         "link_doctype": "Customer",
    #         "link_name": customer_name,
    #         "link_title": customer_name,
    #     }
    # ]
    # contact.first_name = kwargs["data"].get("customer_name", None)
    # contact.email_id = kwargs["data"].get("email_id", None)
    # contact.mobile_no = kwargs["data"].get("mobile_no", None)
    # contact.is_primary_contact = 1
    # contact.is_billing_contact = 1
    # contact.links = contact_link
    links = [
        {
            "link_doctype": "Customer",
            "link_name": customer_name,
            "link_title": customer_name,
        }
    ]
    emails = [{"email_id": kwargs["data"].get("email_id"), "is_primary": 1}]
    contacts = [
        {
            "phone": kwargs["data"].get("mobile_no"),
            "is_primary_phone": 1,
            "is_primary_mobile_no": 1,
        }
    ]

    contact_name = kwargs["data"]["customer_name"] + str(frappe.generate_hash(length=5))
    if not frappe.db.exists('Contact', contact_name):
        contact = frappe.get_doc(
            {
                "doctype": "Contact",
                "first_name": contact_name,
                "links": links,
                "email_ids": emails,
                "phone_nos": contacts,
                "is_primary_contact": 1,
                "is_billing_contact": 1,
            }
        )
        if (
                kwargs["data"].get("customer_name")
                and kwargs["data"].get("email_id")
                and kwargs["data"].get("mobile_no")
        ):
            contact.insert()
            customer.customer_primary_contact = contact.name
    address_link = [
        {
            "parenttype": "Address",
            "doctype": "Dynamic Link",
            "link_doctype": "Customer",
            "link_name": customer_name,
        }
    ]
    # Create a new address document
    address = frappe.get_doc(
        {
            "doctype": "Address",
            "address_title":kwargs["data"]["customer_name"],
            "address_type": "Billing",
            "address_line1": kwargs["data"]["address_line1"],
            "city": kwargs["data"]["new_governorate"],
            "country": kwargs["data"]["country"],
            "is_primary_address": 1,
            "links": address_link
        }
    )

    # Set flags to ignore permissions and password policy
    address.flags.ignore_permissions = True
    address.flags.ignore_password_policy = True

    # Insert the new address
    address.insert()
    customer.customer_primary_address = address.name
    customer.save()

    frappe.db.commit()
    if customer_name:
        message = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "customer": customer_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"

@frappe.whitelist(allow_guest=True)
def sales_order(**kwargs):
    sales_order = frappe.get_doc(kwargs['data'])
    sales_order.customer_address_2 = sales_order.customer_address
    customer = frappe.get_doc("Customer", kwargs['data']['customer'])

    sales_team = frappe.get_all("Sales Team", filters={"parent": sales_order.customer},
                                fields=["sales_person", "allocated_percentage", "allocated_amount", "commission_rate",
                                        "incentives"])
    if not sales_team:
        frappe.response["http_status_code"] = 404
        frappe.response["success_key"] = False
        frappe.response["message"] = "this Customer does not have a Sales Person"
        return

    for x in sales_team:
        sales_order.append("sales_team", x)

    # if customer.tax_type == "Taxable":

    sales_order.insert()
    # sales_order.save()
    frappe.db.commit()
    if (sales_order.name):
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "sales_order": sales_order.name
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"

    # elif customer.tax_type == "Commercial":
    #     sales_order = frappe.get_doc({
    #         "doctype": "Sales Order",
    #         "customer": kwargs['data']['customer'],
    #         "customer_name": kwargs['data']['customer_name'],
    #         "transaction_date": kwargs['data']['transaction_date'],
    #         "delivery_date": kwargs['data']['delivery_date'],
    #         "customer_group": kwargs['data']['customer_group'],
    #         "territory": kwargs['data']['territory'],
    #         "customer_address": kwargs['data']['customer_address'],
    #         "customer_address_2": kwargs['data']['customer_address'],
    #         "project": kwargs['data']['project'],
    #         "order_type": kwargs['data']['order_type'],
    #         "currency": kwargs['data']['currency'],
    #         "conversion_rate": kwargs['data']['conversion_rate'],
    #         "selling_price_list": kwargs['data']['selling_price_list'],
    #         "price_list_currency": kwargs['data']['price_list_currency'],
    #         "plc_conversion_rate": kwargs['data']['plc_conversion_rate'],
    #         "set_warehouse": kwargs['data']['set_warehouse'],
    #         "tc_name": kwargs['data']['tc_name'],
    #         # "terms": kwargs['data']['terms'],
    #         "payment_terms_template": kwargs['data']['payment_terms_template'],
    #         # "apply_discount_on": "On Net Total" ,
    #         # "additional_discount_percentage": 0 ,
    #         # "discount_amount": 0,
    #         "sales_partner": "ahmed",
    #         "select": kwargs["data"]["select"],
    #         # "driver": kwargs["data"]["driver"],
    #         # "vehicle": kwargs["data"]["vehicle"],
    #         "items": kwargs['data']['items']
    #     })
    #
    #     sales_order.insert()
    #     sales_order.save()
    #     sales_order_name = sales_order.name
    #     frappe.db.commit()
    #     if (sales_order_name):
    #         message = frappe.response["message"] = {
    #             "success_key": True,
    #             "message": "تم اضافة المعاملة بنجاح!",
    #             "sales_order": sales_order_name
    #         }
    #         return message
    #     else:
    #         return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist(allow_guest=True)
def sales_invoice(**kwargs):
    if "select" not in kwargs["data"] or not kwargs["data"]["select"]:
        frappe.response['http_status_code'] = 400
        return "برجاء اختيار نوع الخصم!"

    sales_invoice = frappe.get_doc(kwargs["data"])

    sales_team = frappe.get_all("Sales Team", filters={"parent": sales_invoice.customer},
                                fields=["sales_person", "allocated_percentage", "allocated_amount", "commission_rate",
                                        "incentives"])
    if not sales_team:
        frappe.response["http_status_code"] = 404
        frappe.response["success_key"] = False
        frappe.response["message"] = "this Customer does not have a Sales Person"
        return

    # calling this endpoint to get customer details that contains sales_person property
    # yes, we can fetch the sales_person from database directly, but don't repeat yourself
    # customer = frappe.local.request(method="GET", url="/api/method/ecs_mobile.pages.customer",
    #                                 params={"name": kwargs["data"]["customer"]})
    #
    # sales_team = frappe.new_doc("Sales Team")
    # sales_team.sales_person = customer.sales_person

    # customer = frappe.get_doc("Customer", kwargs['data']['customer'])
    # if customer.tax_type == "Taxable":
    #     sales_invoice.naming_series = "INV-"
    # elif customer.tax_type == "Commercial":
    #     sales_invoice.naming_series = "SINV-"
    #
    # for key, value in kwargs["data"]:
    #     sales_invoice[key] = value

    for x in sales_team:
        sales_invoice.append("sales_team", x)

    response = {"status": 200, "success_key": True}

    sales_invoice.insert()
    frappe.db.commit()
    if (sales_invoice.name):
        response["message"] = "تم اضافة المعاملة بنجاح!"
        response["sales_invoice"] = sales_invoice.name

    else:
        response["status"] = frappe.response["http_status_code"] = 404
        response["success_key"] = False
        response["message"] = "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"

    return response


# except Exception as e:
#     return e


@frappe.whitelist(allow_guest=True)
def payment_entry(**kwargs):
    payment_entry = frappe.get_doc(kwargs["data"])

    payment_entry.insert()
    payment_entry_name = payment_entry.name
    frappe.db.commit()
    if payment_entry_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "payment_entry": payment_entry_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist(allow_guest=True)
def loan_application(**kwargs):
    loan_application_data = frappe.get_doc(kwargs["data"])
    loan_application_data.insert()
    loan_application_data_name = loan_application_data.name
    frappe.db.commit()
    if loan_application_data_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "loan_application_data_name": loan_application_data_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist(allow_guest=True)
def journal_entry(**kwargs):
    journal_entry_data = frappe.get_doc(kwargs["data"])
    journal_entry_data.insert()
    ejournal_entry_data_name = journal_entry_data.name
    frappe.db.commit()
    if ejournal_entry_data_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "ejournal_entry_data_name": ejournal_entry_data_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist(allow_guest=True)
def item(**kwargs):
    item = frappe.get_doc(kwargs["data"])

    item.insert()
    item_name = item.name
    frappe.db.commit()
    if item_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة الصنف بنجاح!",
            "item": item_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة الصنف . برجاء المحاولة مرة اخري!"


@frappe.whitelist(allow_guest=True)
def stock_entry(**kwargs):
    stock_entry = frappe.get_doc(kwargs["data"])
    stock_entry.insert()
    frappe.db.commit()
    
    stock_entry_name = stock_entry.name
    if stock_entry_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "stock_entry": stock_entry_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist(allow_guest=True)
def delivery_note(**kwargs):
    delivery_note = frappe.get_doc(kwargs["data"])
    for item in delivery_note.items:
        so_name=item.against_sales_order
        get_previous_delivery_note=frappe.db.sql("""
            SELECT DISTINCT(DN.name) 
            FROM `tabDelivery Note` DN 
            JOIN `tabDelivery Note Item` DNI ON DN.name = DNI.parent
            WHERE DNI.against_sales_order = '{so_name}'
            AND DN.status = 'To Bill'
            """.format(so_name=so_name), as_dict=1)
        get_sales_order_qty=frappe.get_all("Sales Order Item",{"parent":item.against_sales_order,"item_code":item.item_code},['qty'])
        total_qty_previous_delivery_note=0.0
        if get_previous_delivery_note:
            for row in get_previous_delivery_note:
                previous_qty=frappe.get_all("Delivery Note Item",{"parent":row['name'],"item_code":item.item_code},["qty"])
                total_qty_previous_delivery_note += previous_qty[0]['qty']

        if item.qty +  total_qty_previous_delivery_note > get_sales_order_qty[0]['qty']:
            return "لا يمكن اضافة المعاملة"
    delivery_note.insert()
    delivery_note_name = delivery_note.name
    frappe.db.commit()
    if delivery_note_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "delivery_note": delivery_note_name
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist(allow_guest=True)
def purchase_receipt(**kwargs):
    purchase_receipt = frappe.get_doc(kwargs["data"])
    purchase_receipt.insert()
    purchase_receipt_name = purchase_receipt.name
    frappe.db.commit()
    if purchase_receipt_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "purchase_receipt": purchase_receipt_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist(allow_guest=True)
def comment(**kwargs):
    comment = frappe.get_doc(kwargs["data"])

    comment.insert()
    comment_name = comment.name
    frappe.db.commit()
    if comment_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة التعليق بنجاح!",
            "comment": comment_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة التعليق . برجاء المحاولة مرة اخري!"


@frappe.whitelist(allow_guest=True)
def add_item_list(**kwargs):
    start = 0
    page_length = 20
    try:
        if kwargs["search_text"]:
            items = frappe.db.sql(
                """ select tabItem.name as name ,
                                                     tabItem.item_code as item_code, 
                                                     tabItem.item_name as item_name, 
                                                     tabItem.item_group as item_group, 
                                                     tabItem.stock_uom as stock_uom, 
                                                     tabItem.image as image,
                                                     tabItem.sales_uom as sales_uom,
                                                     ifnull((select max(price_list_rate)  from `tabItem Price` where item_code = tabItem.name and price_list = '{price_list}'),0) as price_list_rate,
                                                     ifnull((select distinct `tabItem Tax Template Detail`.tax_rate from `tabItem Tax Template Detail` join `tabItem Tax` 
                                                     where `tabItem Tax Template Detail`.parent = `tabItem Tax`.item_tax_template and `tabItem Tax`.parent = `tabItem`.name),0) as tax_percent
                                                     from tabItem  where tabItem.disabled = 0 and tabItem.name like '%{item}%' or tabItem.item_name like '%{item}%' LIMIT {start},{page_length}""".format(
                    start=kwargs["start"],
                    page_length=kwargs["page_length"],
                    price_list=kwargs["price_list"],
                    item=kwargs["search_text"],
                ),
                as_dict=1,
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

    except:
        items = frappe.db.sql(
            """ select tabItem.name as name,
                                         tabItem.item_code as item_code,
                                         tabItem.item_name as item_name, 
                                         tabItem.item_group as item_group, 
                                         tabItem.stock_uom as stock_uom, 
                                         tabItem.image as image,
                                         tabItem.sales_uom as sales_uom,
                                         ifnull((select max(price_list_rate) from `tabItem Price` where item_code = tabItem.name and price_list = '{price_list}'),0) as price_list_rate,
                                         ifnull((select distinct `tabItem Tax Template Detail`.tax_rate from `tabItem Tax Template Detail` join `tabItem Tax` 
                                         where `tabItem Tax Template Detail`.parent = `tabItem Tax`.item_tax_template and `tabItem Tax`.parent = `tabItem`.name),0) as tax_percent
                                         from tabItem where tabItem.disabled = 0 LIMIT {start},{page_length} """.format(
                start=kwargs["start"],
                page_length=kwargs["page_length"],
                price_list=kwargs["price_list"],
            ),
            as_dict=1,
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


'''
@frappe.whitelist(allow_guest=True)
def add_item_list(**kwargs):
    start = 0
    page_length = 20
    user = frappe.session.user
    warehouse = frappe.db.get_value("Employee", {'user_id': user}, "warehouse")
    try:
        if kwargs['search_text']:
            items = frappe.db.sql(""" select tabItem.name as name ,
                                                     tabItem.item_name as item_name, 
                                                     tabItem.item_group as item_group, 
                                                     tabItem.stock_uom as stock_uom, 
                                                     tabItem.image as image,
                                                     tabItem.sales_uom as sales_uom,
                                                     ifnull((select max(price_list_rate)  from `tabItem Price` where item_code = tabItem.name and price_list = '{price_list}'),0) as price_list_rate,
                                                     ifnull((select distinct `tabItem Tax Template Detail`.tax_rate from `tabItem Tax Template Detail` join `tabItem Tax` 
                                                     where `tabItem Tax Template Detail`.parent = `tabItem Tax`.item_tax_template and `tabItem Tax`.parent = `tabItem`.name),0) as tax_percent
                                                     from tabItem
                                                     where tabItem.disabled = 0 
                                                     and (tabItem.name like '%{item}%' or tabItem.item_name like '%{item}%') LIMIT {start},{page_length}
                                                     """.format(start=kwargs['start'], page_length=kwargs['page_length'], price_list=kwargs['price_list'], item=kwargs['search_text']), as_dict=1)
            result = []
            for item_dict in items:
                if item_dict.tax_percent > 0 and item_dict.price_list_rate > 0:
                    net_rate = item_dict.price_list_rate * (1 + (item_dict.tax_percent / 100))
                    vat_value = net_rate - item_dict.price_list_rate 
                    data = {
                        'name': item_dict.name,
                        'item_name': item_dict.item_name,
                        'item_group': item_dict.item_group,
                        'stock_uom': item_dict.stock_uom,
                        'image': item_dict.image,
                        'sales_uom': item_dict.sales_uom,
                        'price_list_rate': item_dict.price_list_rate,
                        'tax_percent': item_dict.tax_percent,
                        'net_rate': net_rate,
                        'vat_value': vat_value
                    }
                    result.append(data)
                else:
                    data = {
                        'name': item_dict.name,
                        'item_name': item_dict.item_name,
                        'item_group': item_dict.item_group,
                        'stock_uom': item_dict.stock_uom,
                        'image': item_dict.image,
                        'sales_uom': item_dict.sales_uom,
                        'price_list_rate': item_dict.price_list_rate,
                        'tax_percent': item_dict.tax_percent,
                        'net_rate': item_dict.price_list_rate
                    }
                    result.append(data)

            if items:
                return result
            else:
                return "لا يوجد منتجات !"


    except:
        items = frappe.db.sql(""" select tabItem.name as name ,
                                         tabItem.item_name as item_name, 
                                         tabItem.item_group as item_group, 
                                         tabItem.stock_uom as stock_uom, 
                                         tabItem.image as image,
                                         tabItem.sales_uom as sales_uom,
                                         ifnull((select max(price_list_rate)  from `tabItem Price` where item_code = tabItem.name and price_list = '{price_list}'),0) as price_list_rate,
                                         ifnull((select distinct `tabItem Tax Template Detail`.tax_rate from `tabItem Tax Template Detail` join `tabItem Tax` 
                                         where `tabItem Tax Template Detail`.parent = `tabItem Tax`.item_tax_template and `tabItem Tax`.parent = `tabItem`.name),0) as tax_percent
                                         from tabItem
                                         where tabItem.disabled = 0 LIMIT {start},{page_length}
                                         """.format(start=kwargs['start'],
                                                    page_length=kwargs['page_length'],
                                                    warehouse=warehouse,
                                                    price_list=kwargs['price_list']), as_dict=1)

        result = []
        for item_dict in items:
            if item_dict.tax_percent > 0 and item_dict.price_list_rate > 0:
                net_rate = item_dict.price_list_rate * (1 + (item_dict.tax_percent / 100))
                vat_value = net_rate - item_dict.price_list_rate
                data = {
                    'name': item_dict.name,
                    'item_name': item_dict.item_name,
                    'item_group': item_dict.item_group,
                    'stock_uom': item_dict.stock_uom,
                    'image': item_dict.image,
                    'sales_uom': item_dict.sales_uom,
                    'price_list_rate': item_dict.price_list_rate,
                    'tax_percent': item_dict.tax_percent,
                    'net_rate': net_rate,
                    'vat_value': vat_value
                }
                result.append(data)
            else:
                data = {
                    'name': item_dict.name,
                    'item_name': item_dict.item_name,
                    'item_group': item_dict.item_group,
                    'stock_uom': item_dict.stock_uom,
                    'image': item_dict.image,
                    'sales_uom': item_dict.sales_uom,
                    'price_list_rate': item_dict.price_list_rate,
                    'tax_percent': item_dict.tax_percent,
                    'net_rate': item_dict.price_list_rate
                }
                result.append(data)

        if items:
            return result
        else:
            return "لا يوجد منتجات !"
'''


@frappe.whitelist(allow_guest=True)
def add_item_list_warehouse_filtered(**kwargs):
    start = 0
    page_length = 20
    user = frappe.session.user
    warehouse = frappe.db.get_value("Employee", {'user_id': user}, "warehouse")
    try:
        if kwargs['search_text']:
            items = frappe.db.sql(""" select tabItem.name as name ,
                                                     tabItem.item_name as item_name, 
                                                     tabItem.item_group as item_group, 
                                                     tabItem.stock_uom as stock_uom, 
                                                     tabItem.image as image,
                                                     tabItem.sales_uom as sales_uom,
                                                     tabBin.actual_qty as actual_qty,
                                                     ifnull((select max(price_list_rate)  from `tabItem Price` where item_code = tabItem.name and price_list = '{price_list}'),0) as price_list_rate,
                                                     ifnull((select distinct `tabItem Tax Template Detail`.tax_rate from `tabItem Tax Template Detail` join `tabItem Tax` 
                                                     where `tabItem Tax Template Detail`.parent = `tabItem Tax`.item_tax_template and `tabItem Tax`.parent = `tabItem`.name),0) as tax_percent
                                                     from tabItem join tabBin on tabItem.item_code = tabBin.item_code 
                                                     where tabBin.warehouse = '{warehouse}' and tabBin.actual_qty > 0 and tabItem.disabled = 0 and (tabItem.name like '%{item}%' or tabItem.item_name like '%{item}%') LIMIT {start},{page_length}
                                                     """.format(start=kwargs['start'],
                                                                page_length=kwargs['page_length'], warehouse=warehouse,
                                                                price_list=kwargs['price_list'],
                                                                item=kwargs['search_text']), as_dict=1)
            result = []
            for item_dict in items:
                if item_dict.tax_percent > 0 and item_dict.price_list_rate > 0:
                    net_rate = item_dict.price_list_rate * (1 + (item_dict.tax_percent / 100))
                    vat_value = net_rate - item_dict.price_list_rate
                    data = {
                        'name': item_dict.name,
                        'item_name': item_dict.item_name,
                        'item_group': item_dict.item_group,
                        'stock_uom': str(item_dict.actual_qty),
                        'image': item_dict.image,
                        'sales_uom': str(item_dict.actual_qty),
                        'actual_qty': item_dict.actual_qty,
                        'price_list_rate': item_dict.price_list_rate,
                        'tax_percent': item_dict.tax_percent,
                        'net_rate': net_rate,
                        'vat_value': vat_value
                    }
                    result.append(data)
                else:
                    data = {
                        'name': item_dict.name,
                        'item_name': item_dict.item_name,
                        'item_group': item_dict.item_group,
                        'stock_uom': str(item_dict.actual_qty),
                        'image': item_dict.image,
                        'sales_uom': str(item_dict.actual_qty),
                        'actual_qty': item_dict.actual_qty,
                        'price_list_rate': item_dict.price_list_rate,
                        'tax_percent': item_dict.tax_percent,
                        'net_rate': item_dict.price_list_rate
                    }
                    result.append(data)

            if items:
                return result
            else:
                return "لا يوجد منتجات !"


    except:
        items = frappe.db.sql(""" select tabItem.name as name ,
                                         tabItem.item_name as item_name, 
                                         tabItem.item_group as item_group, 
                                         tabItem.stock_uom as stock_uom, 
                                         tabItem.image as image,
                                         tabItem.sales_uom as sales_uom,
                                         tabBin.actual_qty as actual_qty,
                                         ifnull((select max(price_list_rate)  from `tabItem Price` where item_code = tabItem.name and price_list = '{price_list}'),0) as price_list_rate,
                                         ifnull((select distinct `tabItem Tax Template Detail`.tax_rate from `tabItem Tax Template Detail` join `tabItem Tax` 
                                         where `tabItem Tax Template Detail`.parent = `tabItem Tax`.item_tax_template and `tabItem Tax`.parent = `tabItem`.name),0) as tax_percent
                                         from tabItem join tabBin on tabItem.item_code = tabBin.item_code 
                                         where tabBin.warehouse = '{warehouse}' and tabBin.actual_qty > 0 
                                         and tabItem.disabled = 0 LIMIT {start},{page_length}
                                         """.format(start=kwargs['start'],
                                                    page_length=kwargs['page_length'],
                                                    warehouse=warehouse,
                                                    price_list=kwargs['price_list']), as_dict=1)

        result = []
        for item_dict in items:
            if item_dict.tax_percent > 0 and item_dict.price_list_rate > 0:
                net_rate = item_dict.price_list_rate * (1 + (item_dict.tax_percent / 100))
                vat_value = net_rate - item_dict.price_list_rate
                data = {
                    'name': item_dict.name,
                    'item_name': item_dict.item_name,
                    'item_group': item_dict.item_group,
                    'stock_uom': str(item_dict.actual_qty),
                    'image': item_dict.image,
                    'sales_uom': str(item_dict.actual_qty),
                    'actual_qty': item_dict.actual_qty,
                    'price_list_rate': item_dict.price_list_rate,
                    'tax_percent': item_dict.tax_percent,
                    'net_rate': net_rate,
                    'vat_value': vat_value
                }
                result.append(data)
            else:
                data = {
                    'name': item_dict.name,
                    'item_name': item_dict.item_name,
                    'item_group': item_dict.item_group,
                    'stock_uom': str(item_dict.actual_qty),
                    'image': item_dict.image,
                    'sales_uom': str(item_dict.actual_qty),
                    'actual_qty': item_dict.actual_qty,
                    'price_list_rate': item_dict.price_list_rate,
                    'tax_percent': item_dict.tax_percent,
                    'net_rate': item_dict.price_list_rate
                }
                result.append(data)

        if items:
            return result
        else:
            return "لا يوجد منتجات !"


@frappe.whitelist(allow_guest=True)
def supplier_quotation(**kwargs):
    s_quotation = frappe.get_doc(kwargs["data"])

    s_quotation.insert()
    quotation_name = s_quotation.name
    frappe.db.commit()
    if s_quotation:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "supplier_quotation_name": quotation_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist(allow_guest=True)
def purchase_order(**kwargs):
    p_order = frappe.get_doc(kwargs["data"])

    p_order.insert()
    purchase_order_name = p_order.name
    frappe.db.commit()
    if purchase_order_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "purchase_order_name": purchase_order_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist(allow_guest=True)
def purchase_invoice(**kwargs):
    purchase_invoice = frappe.get_doc(kwargs["data"])

    purchase_invoice.insert()
    purchase_invoice_name = purchase_invoice.name
    frappe.db.commit()
    if purchase_invoice_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "purchase_invoice_name": purchase_invoice_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist(allow_guest=True)
def purchsae_receipt(**kwargs):
    purchsae_receipt_data = frappe.get_doc(kwargs["data"])

    purchsae_receipt_data.insert()
    purchsae_receipt_data_name = purchsae_receipt_data.name
    frappe.db.commit()
    if purchsae_receipt_data_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "purchsae_receipt_name": purchsae_receipt_data_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist(allow_guest=True)
def material_request(**kwargs):
    material_request_data = frappe.get_doc(kwargs["data"])

    material_request_data.insert()
    material_request_data_name = material_request_data.name
    frappe.db.commit()
    if material_request_data_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "material_request_name": material_request_data_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist(allow_guest=True)
def leave_application(**kwargs):
    leave_application_data = frappe.get_doc(kwargs["data"])

    leave_application_data.insert()
    leave_application_data_name = leave_application_data.name
    frappe.db.commit()
    if leave_application_data_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "leave_application_name": leave_application_data_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist(allow_guest=True)
def supplier(**kwargs):
    supplier = frappe.new_doc("Supplier")
    supplier.supplier_name = kwargs["data"]["supplier_name"]
    supplier.supplier_type = kwargs["data"]["supplier_type"]
    supplier.supplier_group = kwargs["data"]["supplier_group"]
    if kwargs["data"].get("tax_id"):
        supplier.tax_id = kwargs["data"]["tax_id"]
    if kwargs["data"].get("default_currency"):
        supplier.default_currency = kwargs["data"]["default_currency"]
    if kwargs["data"].get("default_price_list"):
        supplier.default_price_list = kwargs["data"]["default_price_list"]
    if kwargs["data"].get("payment_terms"):
        supplier.payment_terms = kwargs["data"]["payment_terms"]
    if kwargs["data"].get("country"):
        supplier.country = kwargs["data"]["country"]
    supplier.insert()
    supplier_name = supplier.name

    links = [
        {
            "link_doctype": "Supplier",
            "link_name": supplier_name,
            "link_title": supplier_name,
        }
    ]
    emails = [{"email_id": kwargs["data"].get("email_id"), "is_primary": 1}]

    contacts = [
        {
            "phone": kwargs["data"].get("mobile_no"),
            "is_primary_phone": 1,
            "is_primary_mobile_no": 1,
        }
    ]

    contact = frappe.get_doc(
        {
            "doctype": "Contact",
            "first_name": kwargs["data"]["supplier_name"],
            "links": links,
            "email_ids": emails,
            "phone_nos": contacts,
            "is_primary_contact": 1,
            "is_billing_contact": 1,
        }
    )
    if (
            kwargs["data"].get("supplier_name")
            and kwargs["data"].get("email_id")
            and kwargs["data"].get("mobile_no")
    ):
        contact.insert()
        supplier.supplier_primary_contact = contact.name

    if (
            kwargs["data"].get("supplier_name")
            and kwargs["data"].get("address_line1")
            and kwargs["data"].get("city")
            and kwargs["data"].get("address_type", "Billing")
    ):
        address = frappe.get_doc(
            {
                "doctype": "Address",
                "address_title": kwargs["data"]["supplier_name"],
                "address_line1": kwargs["data"]["address_line1"],
                "city": kwargs["data"]["city"],
                "country": kwargs["data"].get("country", None),
                "address_type": kwargs["data"].get("address_type", "Billing"),
                "links": links,
                "is_primary_address_type": 1,
                "is_shipping_address_type": 1,
            }
        )
        address.insert()
        supplier.supplier_primary_address = address.name

    supplier.save()

    frappe.db.commit()
    if supplier_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "name": supplier_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist(allow_guest=True)
def employee_checkin(**kwargs):
    employee_checkin_data = frappe.get_doc(kwargs["data"])

    employee_checkin_data.insert()
    employee_checkin_data_name = employee_checkin_data.name
    frappe.db.commit()
    if employee_checkin_data_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "employee_checkin_data_name": employee_checkin_data_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist(allow_guest=True)
def employee(**kwargs):
    employee_data = frappe.new_doc("Employee")
    employee_data.first_name = kwargs["data"].get("first_name", None)
    employee_data.last_name = kwargs["data"].get("last_name", None)
    employee_data.gender = kwargs["data"].get("gender", None)
    employee_data.date_of_birth = kwargs["data"].get("date_of_birth", None)
    employee_data.company = kwargs["data"].get("company", None)
    employee_data.status = kwargs["data"].get("status", None)
    employee_data.department = kwargs["data"].get("department", None)
    employee_data.designation = kwargs["data"].get("designation", None)
    employee_data.branch = kwargs["data"].get("branch", None)
    employee_data.employment_type = kwargs["data"].get("employment_type", None)
    employee_data.date_of_joining = kwargs["data"].get("date_of_joining", None)
    employee_data.leave_approver = kwargs["data"].get("leave_approver", None)
    employee_data.expense_approver = kwargs["data"].get("expense_approver", None)
    employee_data.cell_number = kwargs["data"].get("cell_number", None)
    employee_data.company_email = kwargs["data"].get("company_email", None)
    employee_data.personal_email = kwargs["data"].get("personal_email", None)
    employee_data.prefered_email = kwargs["data"].get("prefered_email", None)
    employee_data.current_address = kwargs["data"].get("current_address", None)
    employee_data.permanent_address = kwargs["data"].get("permanent_address", None)
    employee_data.holiday_list = kwargs["data"].get("holiday_list", None)
    employee_data.default_shift = kwargs["data"].get("default_shift", None)
    if kwargs["data"].get("user_id"):
        employee_data.user_id = kwargs["data"].get("user_id")
        employee_data.create_user_permission = 1
    if kwargs["data"].get("attendance_device_id"):
        employee_data.attendance_device_id = kwargs["data"].get("attendance_device_id")
        employee_data.employee_number = kwargs["data"].get("attendance_device_id")
    employee_data.insert()
    employee_data_name = employee_data.name
    frappe.db.commit()
    if employee_data_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "employee_data_name": employee_data_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist(allow_guest=True)
def attendance_request(**kwargs):
    attendance_request_data = frappe.get_doc(kwargs["data"])

    attendance_request_data.insert()
    attendance_request_data_name = attendance_request_data.name
    frappe.db.commit()
    if attendance_request_data_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "attendance_request_data_name": attendance_request_data_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist(allow_guest=True)
def employee_advance(**kwargs):
    employee_advance_data = frappe.get_doc(kwargs["data"])

    employee_advance_data.insert()
    employee_advance_data_name = employee_advance_data.name
    frappe.db.commit()
    if employee_advance_data_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "employee_advance_data_name": employee_advance_data_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist(allow_guest=True)
def expense_claim(**kwargs):
    expense_claim_data = frappe.get_doc(kwargs["data"])
    expense_claim_data.insert()
    expense_claim_data_name = expense_claim_data.name
    frappe.db.commit()
    if expense_claim_data_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "expense_claim_data_name": expense_claim_data_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist(allow_guest=True)
def customer_visit(**kwargs):
    customer_visit_data = frappe.get_doc(kwargs["data"])
    customer_visit_data.insert()
    customer_visit_data_name = customer_visit_data.name
    frappe.db.commit()
    if customer_visit_data_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "customer_visit_data_name": customer_visit_data_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def address(**kwargs):
    if kwargs["data"].get("is_primary_address", 0):
        addresses = frappe.db.get_list(
            "Address",
            filters={
                "link_doctype": kwargs["data"]["link_doctype"],
                "link_name": kwargs["data"]["link_name"],
            },
        )
        for row in addresses:
            cur_address = frappe.get_doc("Address", row.name)
            if cur_address.is_primary_address == 1:
                cur_address.is_primary_address = 0
                cur_address.save()

    links = [
        {
            "doctype": "Dynamic Link",
            "link_doctype": kwargs["data"]["link_doctype"],
            "link_name": kwargs["data"]["link_name"],
        }
    ]

    address = frappe.get_doc(
        {
            "doctype": "Address",
            "is_primary_address": kwargs["data"].get("is_primary_address", 0),
            "address_title": kwargs["data"].get("address_title", None),
            "address_type": kwargs["data"].get("address_type", None),
            "address_line1": kwargs["data"].get("address_line1", None),
            "city": kwargs["data"].get("city", None),
            "country": kwargs["data"].get("country", None),
            "longitude": kwargs["data"].get("longitude", None),
            "latitude": kwargs["data"].get("latitude", None),
            "links": links,
        }
    )
    address.insert()
    if (
            kwargs["data"].get("is_primary_address", 0)
            and kwargs["data"]["link_doctype"] == "Customer"
    ):
        customer = frappe.get_doc("Customer", kwargs["data"]["link_name"])
        customer.customer_primary_address = address.name
        customer.save()

    if (
            kwargs["data"].get("is_primary_address", 0)
            and kwargs["data"]["link_doctype"] == "Supplier"
    ):
        customer = frappe.get_doc("Supplier", kwargs["data"]["link_name"])
        customer.supplier_primary_address = address.name
        customer.save()
    address.links = links
    frappe.db.commit()
    address_name = address.name
    if address_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "address_name": address_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist(allow_guest=True)
def make_primary_address(**kwargs):
    if kwargs["data"].get("is_primary_address", 0):
        addresses = frappe.db.get_list(
            "Address",
            filters={
                "link_doctype": kwargs["data"]["link_doctype"],
                "link_name": kwargs["data"]["link_name"],
            },
        )
        for row in addresses:
            cur_address = frappe.get_doc("Address", row.name)
            if cur_address.is_primary_address == 1:
                cur_address.is_primary_address = 0
                cur_address.save()

    if kwargs["data"]["link_doctype"] == "Customer":
        customer = frappe.get_doc("Customer", kwargs["data"]["link_name"])
        customer.customer_primary_address = kwargs["data"]["name"]
        customer.save()
        customer_name = customer.name
        if customer_name:
            message = frappe.response["message"] = {
                "success_key": True,
                "message": "تم اضافة المعاملة بنجاح!",
                "customer_name": customer_name,
            }
            return message

    if kwargs["data"]["link_doctype"] == "Supplier":
        customer = frappe.get_doc("Supplier", kwargs["data"]["link_name"])
        customer.supplier_primary_address = kwargs["data"]["name"]
        customer.save()
        customer_name = customer.name
        if customer_name:
            message = frappe.response["message"] = {
                "success_key": True,
                "message": "تم اضافة المعاملة بنجاح!",
                "customer_name": customer_name,
            }
            return message
    frappe.db.commit()

    return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def contact(**kwargs):
    contact_data = frappe.get_doc(kwargs["data"])
    contact_data.insert()
    contact_data_name = contact_data.name
    frappe.db.commit()
    if contact_data_name:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم اضافة المعاملة بنجاح!",
            "contact_data_name": contact_data_name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist(methods=["POST"])
def workflow(**kwargs):
    if "data" not in kwargs:
        frappe.throw("data key must be in the body.", frappe.exceptions.ValidationError)

    data = kwargs["data"]
    workflow = frappe.get_doc(data)
    workflow.insert()

    response = {"succss_key": True, "workflow": workflow.name}
    return response

