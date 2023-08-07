from frappe.utils import flt, getdate
from erpnext.accounts.utils import get_balance_on
import frappe
from frappe import _
from frappe.utils import getdate, nowdate



@frappe.whitelist(methods=["GET"])
def general_ledger(from_date=None, to_date=None, account=None, party_type=None ,party=None, start=0, page_length=20):
    conditions = ""

    if (from_date is not None) and (to_date is not None):
        conditions += f" AND `tabGL Entry`.posting_date BETWEEN '{from_date}' AND '{to_date}'"
    
    if account is not None:
        conditions += f" AND `tabGL Entry`.account = '{account}'"
    
    if party_type is not None:
        conditions += f" AND `tabGL Entry`.party_type = '{party_type}'"
    
    if party is not None:
        conditions += f" AND `tabGL Entry`.party = '{party}'"
    
    query = frappe.db.sql(
        f"""
            SELECT
                name,
                posting_date,
                account,
                party_type,
                party,
                cost_center,
                debit,
                credit,
                against,
                against_voucher_type,
                against_voucher,
                voucher_type,
                voucher_no,
                project,
                remarks,
                account_currency,
                company
            FROM `tabGL Entry`
            WHERE 1=1
            {conditions}
            LIMIT {start}, {page_length}
        """, as_dict=True
    )
    total_credit = 0
    total_debit = 0
    total_balance = 0
    if query:
        for q in query:

            total_credit += q["credit"]
            total_debit += q["debit"]
            balance = flt(get_balance_on(
                account=q["account"],
                date=getdate(["posting_date"]),
                party_type=q["party_type"],
                party=q["party"],
                company=q["company"],
                in_account_currency=q["account_currency"],
                cost_center=q["cost_center"],
                ignore_account_permission=False
            ), 2)

            q["balance"] = balance
            total_balance += balance
       
        response = {
            "data":query,
            "total_debit": flt(total_debit, 2),
            "total_credit": flt(total_credit, 2),
            "total_balance": flt(total_balance, 2)
        }
        return response
    else:
        frappe.throw("No Data", frappe.exceptions.DoesNotExistError)




@frappe.whitelist(methods=["GET"])
def accounts_receivable(from_date=None, to_date=None, customer_name=None, customer_code=None, sales_person_name=None, start=0, page_length=20):
    conditions = ""
    if from_date and to_date:
        conditions += f" AND sales_invoice.posting_date BETWEEN '{from_date}' AND '{to_date}'"
    if customer_name:
        conditions += f" AND customer.name = '{customer_name}'"
    if customer_code:
        conditions += f" AND customer.code = '{customer_code}'"
    if sales_person_name:
        conditions += f" AND sales_person.sales_person = '{sales_person_name}'"

    query = frappe.db.sql(f"""
        SELECT
            customer.name AS customer_name,
            customer.code AS customer_code,
            sales_person.sales_person AS sales_person,
            sales_invoice.posting_date AS date
        FROM
            `tabCustomer` customer
        JOIN
            `tabSales Team` sales_person ON customer.name = sales_person.parent
        LEFT JOIN
            `tabSales Invoice` sales_invoice ON sales_invoice.customer = customer.name
        WHERE  
            sales_invoice.docStatus = 1
            {conditions}
        GROUP BY
            customer.name
        ORDER BY
            sales_person.sales_person
        LIMIT {start}, {page_length}
        """, as_dict=True)

    data_with_balance = []

    if query:
        for customer_data in query:
            # Calculating outstanding_balance for each customer
            outstanding_balance = get_balance_on(
                account=None,
                date=to_date,
                party_type="Customer",
                party=customer_data["customer_name"],
                company=None,
                in_account_currency=True,
                cost_center=None,
                ignore_account_permission=False
            )
            # Adding outstanding_balance to the customer_data dictionary
            customer_data["outstanding_balance"] = outstanding_balance
            data_with_balance.append(customer_data)

        return data_with_balance
    else:
        frappe.local.response.http_status_code = 404
        return "لا توجد بيانات"