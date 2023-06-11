import frappe

@frappe.whitelist()
def warehouse_balance(warehouse_filter="%%", item_filter="%%", start=0, page_length=20):
    conditions = ""
    if item_filter != '%%':
        conditions += " and `tabBin`.item_code = '{item_filter}' ".format(item_filter=item_filter)

    query = frappe.db.sql(
        f""" SELECT 
                `tabBin`.item_code, 
                `tabItem`.item_name, 
                `tabItem`.item_group, 
                `tabBin`.actual_qty, 
                `tabBin`.stock_uom
            FROM 
                `tabBin` join `tabItem` on `tabBin`.item_code = `tabItem`.item_code
            WHERE 
                `tabBin`.warehouse = '{warehouse_filter}'
                and `tabBin`.actual_qty > 0
                {conditions}
            ORDER BY
                `tabBin`.item_code
            LIMIT {start},{page_length}
        """, as_dict=1)
    if query:
        return query
    else:
        response = frappe.local.response['http_status_code'] = 404
        return response