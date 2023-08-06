from __future__ import unicode_literals
import frappe
from frappe import auth
import datetime
import json, ast
import urllib.request
import requests
from frappe.defaults import get_user_permissions


current_date = datetime.datetime.today().strftime("%Y-%m-%d")
current_user = frappe.session.user


@frappe.whitelist(allow_guest=True)
def login(usr, pwd):

    try:
        login_manager = frappe.auth.LoginManager()
        login_manager.authenticate(user=usr, pwd=pwd)
        login_manager.post_login()


        api_generate = generate_keys(frappe.session.user)
        user = frappe.get_doc("User", frappe.session.user)

        allowed_modules = frappe.db.sql(
            """ select `tabMobile user Modules`.modules as modq 
        from `tabMobile user Modules` join `tabMobile User` on `tabMobile user Modules`.parent = `tabMobile User`.name 
        where `tabMobile User`.user = '{user}' or `tabMobile User`.username = '{user}' or `tabMobile User`.mobile_no = '{user}' order by `tabMobile user Modules`.idx """.format(
                user=usr
            ),
            as_dict=1,
        )

        modules = []

        for module in allowed_modules:
            
                
            if module.modq == "Accounts":
                Accounts = {}

                Accounts["Accounts"] = "https://erpcloud.systems/files/accounts.png"
                allowed_documents = frappe.db.sql(
                    """ select `tabMobile User Documents`.document_name as docq 
                                            from `tabMobile User Documents` join `tabMobile User` on `tabMobile User Documents`.parent = `tabMobile User`.name 
                                            where `tabMobile User`.user = '{user}'  or `tabMobile User`.username = '{user}' or `tabMobile User`.mobile_no = '{user}' and `tabMobile User Documents`.modules ='selling' order by `tabMobile User Documents`.idx  """.format(
                        user=usr
                    ),
                    as_dict=1,
                )
                docs = {}
                for x in allowed_documents:
                    if x.docq == "Payment Entry":
                        docs["Payment Entry"] = "https://erpcloud.systems/files/payment_entry.png"
                    if x.docq == "Journal Entry":
                        docs["Journal Entry"] = "https://erpcloud.systems/files/journal_entry.png"
                    if x.docq == "Sales Invoice":
                        docs["Sales Invoice"] = "https://erpcloud.systems/files/sales_invoice.png"
                    if x.docq == "Purchase Invoice":
                        docs["Purchase Invoice"] = "https://erpcloud.systems/files/purchase_invoice.png"

                Accounts["docs"] = docs
                modules.append(Accounts)
            if module.modq == "Selling":
                Selling = {}
                Selling["Selling"] = "https://erpcloud.systems/files/selling.png"
                allowed_documents = frappe.db.sql(
                    """ select `tabMobile User Documents`.document_name as docq 
                                            from `tabMobile User Documents` join `tabMobile User` on `tabMobile User Documents`.parent = `tabMobile User`.name 
                                            where `tabMobile User`.user = '{user}'  or `tabMobile User`.username = '{user}' or `tabMobile User`.mobile_no = '{user}' and `tabMobile User Documents`.modules ='selling' order by `tabMobile User Documents`.idx  """.format(
                        user=usr
                    ),
                    as_dict=1,
                )
                docs = {}
                for x in allowed_documents:
                    if x.docq == "Lead":
                        docs["Lead"] = "https://erpcloud.systems/files/lead.png"
                    if x.docq == "Opportunity":
                        docs["Opportunity"] = "https://erpcloud.systems/files/opportunity.png"
                    if x.docq == "Customer":
                        docs["Customer"] = "https://erpcloud.systems/files/customer.png"
                    if x.docq == "Customer Visit":
                        docs["Customer Visit"] = "https://erpcloud.systems/files/customer_visit.png"
                    if x.docq == "Address":
                        docs["Address"] = "https://erpcloud.systems/files/address.png"
                    if x.docq == "Contact":
                        docs["Contact"] = "https://erpcloud.systems/files/contact.png"
                    if x.docq == "Quotation":
                        docs["Quotation"] = "https://erpcloud.systems/files/quotation.png"
                    if x.docq == "Sales Order":
                        docs["Sales Order"] = "https://erpcloud.systems/files/sales_order.png"
                    if x.docq == "Sales Invoice":
                        docs["Sales Invoice"] = "https://erpcloud.systems/files/sales_invoice.png"
                    if x.docq == "Payment Entry":
                        docs["Payment Entry"] = "https://erpcloud.systems/files/payment_entry.png"

                Selling["docs"] = docs
                modules.append(Selling)

            if module.modq == "Buying":
                Buying = {}
                Buying["Buying"] = "https://erpcloud.systems/files/buying.png"
                allowed_documents = frappe.db.sql(
                    """ select `tabMobile User Documents`.document_name as docq 
                                            from `tabMobile User Documents` join `tabMobile User` on `tabMobile User Documents`.parent = `tabMobile User`.name 
                                            where `tabMobile User`.user = '{user}'  or `tabMobile User`.username = '{user}' or `tabMobile User`.mobile_no = '{user}' and `tabMobile User Documents`.modules ='buying' order by `tabMobile User Documents`.idx  """.format(
                        user=usr
                    ),
                    as_dict=1,
                )
                docs = {}
                for x in allowed_documents:
                    if x.docq == "Supplier":
                        docs["Supplier"] = "https://erpcloud.systems/files/supplier.png"
                    if x.docq == "Supplier Quotation":
                        docs["Supplier Quotation"] = "https://erpcloud.systems/files/supplier_quotation.png"
                    if x.docq == "Purchase Order":
                        docs["Purchase Order"] = "https://erpcloud.systems/files/purchase_order.png"
                    if x.docq == "Purchase Invoice":
                        docs["Purchase Invoice"] = "https://erpcloud.systems/files/purchase_invoice.png"
                    if x.docq == "Payment Entry":
                        docs["Payment Entry"] = "https://erpcloud.systems/files/payment_entry.png"

                Buying["docs"] = docs
                modules.append(Buying)

            if module.modq == "Stock":
                Stock = {}
                Stock["Stock"] = "https://erpcloud.systems/files/stock.png"
                allowed_documents = frappe.db.sql(
                    """ select `tabMobile User Documents`.document_name as docq 
                                            from `tabMobile User Documents` join `tabMobile User` on `tabMobile User Documents`.parent = `tabMobile User`.name 
                                            where `tabMobile User`.user = '{user}'  or `tabMobile User`.username = '{user}' or `tabMobile User`.mobile_no = '{user}' and `tabMobile User Documents`.modules ='stock' order by `tabMobile User Documents`.idx  """.format(
                        user=usr
                    ),
                    as_dict=1,
                )
                docs = {}
                for x in allowed_documents:
                    if x.docq == "Item":
                        docs["Item"] = "https://erpcloud.systems/files/item.png"
                    if x.docq == "Material Request":
                        docs["Material Request"] = "https://erpcloud.systems/files/material_request.png"
                    if x.docq == "Purchase Order":
                        docs["Purchase Receipt"] = "https://erpcloud.systems/files/purchase_receipt.png"
                    if x.docq == "Stock Entry":
                        docs["Stock Entry"] = "https://erpcloud.systems/files/stock_entry.png"
                    if x.docq == "Delivery Note":
                        docs["Delivery Note"] = "https://erpcloud.systems/files/delivery_note.png"

                Stock["docs"] = docs
                modules.append(Stock)

            if module.modq == "HR":
                HR = {}
                HR["HR"] = "https://erpcloud.systems/files/hr.png"
                allowed_documents = frappe.db.sql(
                    """ select `tabMobile User Documents`.document_name as docq 
                                            from `tabMobile User Documents` join `tabMobile User` on `tabMobile User Documents`.parent = `tabMobile User`.name 
                                            where `tabMobile User`.user = '{user}'  or `tabMobile User`.username = '{user}' or `tabMobile User`.mobile_no = '{user}' and `tabMobile User Documents`.modules ='hr' order by `tabMobile User Documents`.idx  """.format(
                        user=usr
                    ),
                    as_dict=1,
                )
                docs = {}
                for x in allowed_documents:
                    if x.docq == "Employee":
                        docs["Employee"] = "https://erpcloud.systems/files/hr.png"
                    if x.docq == "Leave Application":
                        docs["Leave Application"] = "https://erpcloud.systems/files/leave_application.png"
                    if x.docq == "Employee Checkin":
                        docs["Employee Checkin"] = "https://erpcloud.systems/files/employee_checkin.png"
                    if x.docq == "Attendance Request":
                        docs["Attendance Request"] = "https://erpcloud.systems/files/attendance_request.png"
                    if x.docq == "Employee Advance":
                        docs["Employee Advance"] = "https://erpcloud.systems/files/employee_advance.png"
                    if x.docq == "Expense Claim":
                        docs["Expense Claim"] = "https://erpcloud.systems/files/expense_claim.png"
                    if x.docq == "Loan Application":
                        docs["Loan Application"] = "https://erpcloud.systems/files/loan_application.png"

                HR["docs"] = docs
                modules.append(HR)

                
        default_tax = frappe.db.get_all(
            "Sales Taxes and Charges Template",
            filters={
                "is_default": 1,
            },
            fields=[
                "name",
            ],
        )

        taxes = frappe.db.get_all(
            "Sales Taxes and Charges",
            filters={
                "parent": default_tax[0]["name"],
            },
            fields=[
                "charge_type",
                "description",
                "account_head",
            ],
        )
        company = frappe.db.get_all(
            "Company",
            fields=[
                "name",
                "default_currency",
                "country",
                "default_selling_terms",
                "default_buying_terms",
            ],
        )
        doc_perm = frappe.db.get_all("Custom DocPerm")
        user_role = frappe.get_roles(frappe.session.user)
        user_permissions = frappe.defaults.get_user_permissions(str(frappe.session.user))
        mobile_settings = frappe.get_doc("Mobile Settings")
        frappe.response["message"] = {
            "success_key": True,
            "message": "Authentication Success",
            "sid": frappe.session.sid,
            "api_key": user.api_key,
            "api_secret": api_generate,
            "email": user.email,
            "modules": modules,
            "user_type": user.role_profile_name,
            "user_role": user_role,
            "mobile_settings": mobile_settings,
            "user_permissions": doc_perm,
            "default_tax_template": taxes,
            "company_defaults": company,
        }

    except frappe.exceptions.AuthenticationError:
        frappe.clear_messages()
        frappe.local.response["message"] = {
            "success_key": False,
            "message": "اسم المستخدم او كلمة المرور غير صحيحة !",
        }
    return


def generate_keys(user):
    user_details = frappe.get_doc("User", user)
    api_secret = frappe.generate_hash(length=15)

    if not user_details.api_key:
        api_key = frappe.generate_hash(length=15)
        user_details.api_key = api_key

    user_details.api_secret = api_secret
    user_details.save()
    return api_secret


# ------------------------------------------------------------------------------------
@frappe.whitelist(allow_guest=True)
def search(doctype, search_text="%%"):
    if doctype == "Lead":
        query = frappe.db.get_list(
            "Lead",
            or_filters=[
                {"name": ["like", search_text]},
                {"lead_name": ["like", search_text]},
                {"company_name": ["like", search_text]},
                {"mobile_no": ["like", search_text]},
            ],
            fields=[
                "name",
                "lead_name",
                "company_name",
                "territory",
                "source",
                "market_segment",
                "status",
            ],
        )
        return query

    if doctype == "Opportunity":
        query = frappe.db.get_list(
            "Opportunity",
            or_filters=[
                {"name": ["like", search_text]},
                {"customer_name": ["like", search_text]},
                {"party_name": ["like", search_text]},
            ],
            fields=[
                "name",
                "opportunity_from",
                "customer_name",
                "transaction_date",
                "opportunity_type",
                "sales_stage",
                "status",
            ],
        )
        return query

    if doctype == "Customer":
        query = frappe.db.get_list(
            "Customer",
            filters=[{"disabled": ["=", 0]}],
            or_filters=[
                {"name": ["like", search_text]},
                {"customer_name": ["like", search_text]},
                {"mobile_no": ["like", search_text]},
            ],
            fields=[
                "name",
                "customer_name",
                "customer_group",
                "territory",
                "mobile_no",
            ],
        )
        return query

    if doctype == "Quotation":
        query = frappe.db.get_list(
            "Quotation",
            or_filters=[
                {"name": ["like", search_text]},
                {"customer_name": ["like", search_text]},
                {"party_name": ["like", search_text]},
            ],
            fields=[
                "name",
                "quotation_to",
                "customer_name",
                "transaction_date",
                "grand_total",
                "status",
            ],
        )
        return query

    if doctype == "Sales Order":
        query = frappe.db.get_list(
            "Sales Order",
            or_filters=[
                {"name": ["like", search_text]},
                {"customer_name": ["like", search_text]},
                {"customer": ["like", search_text]},
            ],
            fields=[
                "name",
                "customer_name",
                "customer_address",
                "transaction_date",
                "grand_total",
                "status",
            ],
        )
        return query

    if doctype == "Sales Invoice":
        query = frappe.db.get_list(
            "Sales Invoice",
            or_filters=[
                {"name": ["like", search_text]},
                {"customer_name": ["like", search_text]},
                {"customer": ["like", search_text]},
            ],
            fields=[
                "name",
                "customer_name",
                "customer_address",
                "posting_date",
                "grand_total",
                "status",
            ],
        )
        return query

    if doctype == "Payment Entry":
        query = frappe.db.get_list(
            "Payment Entry",
            or_filters=[
                {"name": ["like", search_text]},
                {"party_name": ["like", search_text]},
                {"mode_of_payment": ["like", search_text]},
                {"party": ["like", search_text]},
            ],
            fields=[
                "name",
                "party_name",
                "payment_type",
                "mode_of_payment",
                "posting_date",
                "paid_amount",
                "status",
            ],
        )
        return query

    if doctype == "Lead Source":
        query = frappe.db.get_list(
            "Lead Source",
            or_filters=[
                {"name": ["like", search_text]},
                {"source_name": ["like", search_text]},
            ],
            fields=["name"],
        )
        return query

    if doctype == "Market Segment":
        query = frappe.db.get_list(
            "Market Segment",
            or_filters=[
                {"name": ["like", search_text]},
                {"market_segment": ["like", search_text]},
            ],
            fields=["name"],
        )
        return query

    if doctype == "Industry Type":
        query = frappe.db.get_list(
            "Industry Type",
            or_filters=[
                {"name": ["like", search_text]},
                {"industry": ["like", search_text]},
            ],
            fields=["name"],
        )
        return query

    if doctype == "Territory":
        query = frappe.db.get_list(
            "Territory",
            filters=[{"is_group": ["=", 0]}],
            or_filters=[
                {"name": ["like", search_text]},
                {"territory_name": ["like", search_text]},
            ],
            fields=["name", "parent_territory"],
        )
        return query

    if doctype == "Warehouse":
        query = frappe.db.get_list(
            "Warehouse",
            filters=[{"is_group": ["=", 0]}],
            or_filters=[
                {"name": ["like", search_text]},
                {"warehouse_name": ["like", search_text]},
            ],
            fields=["warehouse_name", "warehouse_type", "parent_warehouse"],
        )
        return query

    if doctype == "Country":
        query = frappe.db.get_list(
            "Country",
            or_filters=[
                {"name": ["like", search_text]},
                {"country_name": ["like", search_text]},
            ],
            fields=["name"],
        )
        return query

    if doctype == "Opportunity Type":
        query = frappe.db.get_list(
            "Opportunity Type",
            or_filters=[{"name": ["like", search_text]}],
            fields=["name"],
        )
        return query

    if doctype == "Customer Group":
        query = frappe.db.get_list(
            "Customer Group",
            filters=[{"is_group": ["=", 0]}],
            or_filters=[
                {"name": ["like", search_text]},
                {"customer_group_name": ["like", search_text]},
            ],
            fields=["name"],
        )
        return query

    if doctype == "Address":
        query = frappe.db.get_list(
            "Address",
            filters=[["Dynamic Link", "link_name", "=", "كارفور"]],
            or_filters=[
                {"name": ["like", search_text]},
                {"address_title": ["like", search_text]},
                {"address_line1": ["like", search_text]},
                {"city": ["like", search_text]},
                {"phone": ["like", search_text]},
            ],
            fields=["address_title", "address_line1", "city", "phone"],
        )
        return query

    if doctype == "Contact":
        query = frappe.db.get_list(
            "Contacts",
            or_filters=[
                {"name": ["like", search_text]},
                {"email_id": ["like", search_text]},
                {"mobile_no": ["like", search_text]},
                {"phone": ["like", search_text]},
                {"company_name": ["like", search_text]},
            ],
            fields=["name", "email_id", "phone", "mobile_no", "company_name"],
        )
        return query

    if doctype == "Campaign":
        query = frappe.db.get_list(
            "Campaign",
            or_filters=[
                {"name": ["like", search_text]},
                {"campaign_name": ["like", search_text]},
            ],
            fields=["name"],
        )
        return query

    if doctype == "Currency":
        query = frappe.db.get_list(
            "Currency",
            or_filters=[
                {"name": ["like", search_text]},
                {"currency_name": ["like", search_text]},
            ],
            fields=["name"],
        )
        return query

    if doctype == "Sales Partner":
        query = frappe.db.get_list(
            "Sales Partner",
            or_filters=[
                {"name": ["like", search_text]},
                {"partner_name": ["like", search_text]},
            ],
            fields=["name"],
        )
        return query

    if doctype == "Terms and Conditions":
        query = frappe.db.get_list(
            "Terms and Conditions",
            or_filters=[
                {"name": ["like", search_text]},
                {"title": ["like", search_text]},
            ],
            fields=["name"],
        )
        return query

    if doctype == "Mode of Payment":
        query = frappe.db.get_list(
            "Mode of Payment",
            or_filters=[
                {"name": ["like", search_text]},
                {"mode_of_payment": ["like", search_text]},
            ],
            fields=["name", "type"],
        )
        return query

    if doctype == "Price List":
        query = frappe.db.get_list(
            "Price List",
            or_filters=[
                {"name": ["like", search_text]},
                {"price_list_name": ["like", search_text]},
            ],
            fields=["name", "currency"],
        )
        return query

    if doctype == "Payment Terms Template":
        query = frappe.db.get_list(
            "Payment Terms Template",
            or_filters=[
                {"name": ["like", search_text]},
                {"template_name": ["like", search_text]},
            ],
            fields=["name"],
        )
        return query

    if doctype == "Cost Center":
        query = frappe.db.get_list(
            "Cost Center",
            filters=[{"is_group": ["=", 0]}],
            or_filters=[
                {"name": ["like", search_text]},
                {"cost_center_name": ["like", search_text]},
            ],
            fields=["name", "cost_center_name", "parent_cost_center"],
        )
        return query

    if doctype == "Project":
        query = frappe.db.get_list(
            "Project",
            filters=[{"is_active": ["=", "Yes"]}],
            or_filters=[
                {"name": ["like", search_text]},
                {"project_name": ["like", search_text]},
            ],
            fields=["name", "project_name", "status"],
        )
        return query

    if doctype == "Account":
        query = frappe.db.get_list(
            "Account",
            filters=[{"is_group": ["=", 0]}],
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
        )
        return query

    if doctype == "Item":
        query = frappe.db.get_list(
            "Item",
            or_filters=[
                {"name": ["like", search_text]},
                {"item_name": ["like", search_text]},
                {"item_code": ["like", search_text]},
            ],
            fields=["name", "item_name", "item_group", "stock_uom"],
        )
        return query

    if doctype == "Material Request":
        query = frappe.db.get_list(
            "Material Request",
            or_filters=[
                {"name": ["like", search_text]},
                {"title": ["like", search_text]},
            ],
            fields=[
                "name",
                "material_request_type",
                "transaction_date",
                "set_warehouse",
                "status",
            ],
        )
        return query

    if doctype == "Stock Entry":
        query = frappe.db.get_list(
            "Stock Entry",
            or_filters=[
                {"name": ["like", search_text]},
                {"title": ["like", search_text]},
            ],
            fields=[
                "name",
                "stock_entry_type",
                "posting_date",
                "from_warehouse",
                "to_warehouse",
                "docstatus",
            ],
        )
        return query

    if doctype == "Purchase Receipt":
        query = frappe.db.get_list(
            "Purchase Receipt",
            or_filters=[
                {"name": ["like", search_text]},
                {"title": ["like", search_text]},
                {"supplier": ["like", search_text]},
                {"supplier_name": ["like", search_text]},
            ],
            fields=["name", "supplier", "posting_date", "set_warehouse", "status"],
        )
        return query

    if doctype == "Delivery Note":
        query = frappe.db.get_list(
            "Delivery Note",
            or_filters=[
                {"name": ["like", search_text]},
                {"title": ["like", search_text]},
                {"customer": ["like", search_text]},
                {"customer_name": ["like", search_text]},
            ],
            fields=[
                "name",
                "customer",
                "territory",
                "posting_date",
                "set_warehouse",
                "status",
            ],
        )
        return query

    if doctype == "Supplier":
        query = frappe.db.get_list(
            "Supplier",
            or_filters=[
                {"name": ["like", search_text]},
                {"supplier_name": ["like", search_text]},
                {"mobile_no": ["like", search_text]},
            ],
            fields=[
                "name",
                "supplier_name",
                "supplier_group",
                "supplier_type",
                "country",
                "mobile_no",
            ],
        )
        return query

    if doctype == "Supplier Quotation":
        query = frappe.db.get_list(
            "Supplier Quotation",
            or_filters=[
                {"name": ["like", search_text]},
                {"supplier": ["like", search_text]},
            ],
            fields=[
                "name",
                "supplier",
                "transaction_date",
                "valid_till",
                "grand_total",
                "status",
            ],
        )
        return query

    if doctype == "Purchase Order":
        query = frappe.db.get_list(
            "Purchase Order",
            or_filters=[
                {"name": ["like", search_text]},
                {"supplier": ["like", search_text]},
            ],
            fields=[
                "name",
                "supplier",
                "transaction_date",
                "set_warehouse",
                "grand_total",
                "status",
            ],
        )
        return query

    if doctype == "Purchase Invoice":
        query = frappe.db.get_list(
            "Purchase Invoice",
            or_filters=[
                {"name": ["like", search_text]},
                {"supplier": ["like", search_text]},
            ],
            fields=["name", "supplier", "posting_date", "grand_total", "status"],
        )
        return query


@frappe.whitelist(allow_guest=True)
def party_search(doctype=0, search_text=0, party=0):
    if party == 0:
        return "Check Data"
    else:
        if doctype == "Address":
            addresses = frappe.db.get_list(
                "Dynamic Link", filters={"link_name": party}, fields=["parent"]
            )
            result = []
            for d in addresses:
                query = frappe.db.sql(
                    """ select name as name ,
                                                address_title as address_title,
                                                 address_line1 as address_line1,
                                                 city as city,
                                                 phone as phone
                                         from tabAddress where name = '{filtered}'
                                         and address_title like '{search_text}'
                                         """.format(
                        filtered=d.parent, search_text=search_text
                    ),
                    as_dict=1,
                )
                for x in query:
                    data = {
                        "name": x.name,
                        "address_title": x.address_title,
                        "address_line1": x.address_line1,
                        "city": x.city,
                        "phone": x.phone,
                    }
                    result.append(data)

            if result:
                return result
            else:
                return "no result"

        if doctype == "Contact":
            contacts = frappe.db.get_list(
                "Dynamic Link", filters={"link_name": party}, fields=["parent"]
            )
            result = []
            for d in contacts:
                query = frappe.db.sql(
                    """ select name as name ,
                                                email_id as email_id,
                                                 mobile_no as mobile_no,
                                                 phone as phone,
                                                 company_name as company_name
                                         from tabContact where name = '{filtered}'
                                         and name like '{search_text}'
                                         """.format(
                        filtered=d.parent, search_text=search_text
                    ),
                    as_dict=1,
                )
                for x in query:
                    data = {
                        "name": x.name,
                        "email_id": x.email_id,
                        "mobile_no": x.mobile_no,
                        "company_name": x.company_name,
                        "phone": x.phone,
                    }
                    result.append(data)

            if result:
                return result
            else:
                return "no result"


@frappe.whitelist(allow_guest=True)
def submit(doctype, name):
    doc = frappe.get_doc(doctype, name)
    doc.save()
    doc.submit()
    if doc.docstatus == 1:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم " " المعاملة بنجاح!" "",
            "name": doc.name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من اضافة المعاملة . برجاء المحاولة مرة اخري!"


@frappe.whitelist()
def cancel(doctype, name):
    doc = frappe.get_doc(doctype, name)
    doc.save()
    doc.cancel()
    if doc.docstatus == 2:
        message = frappe.response["message"] = {
            "success_key": True,
            "message": "تم " " المعاملة بنجاح!" "",
            "name": doc.name,
        }
        return message
    else:
        return "حدث خطأ ولم نتمكن من الغاء المعاملة . برجاء المحاولة مرة اخري!"

