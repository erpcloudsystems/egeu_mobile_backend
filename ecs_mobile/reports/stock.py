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


@frappe.whitelist(methods=["GET"])
def stock_ledger(from_date=None, to_date=None, warehouse=None, item_code=None, item_group=None, start=0, page_length=20):
    response = []
    response_dict = {}
    conditions = ""
    if (from_date is not None) and (to_date is not None):
        conditions += f" AND `tabStock Ledger Entry`.posting_date BETWEEN '{from_date}' AND '{to_date}'"
    
    if warehouse is not None:
        conditions += f" AND `tabStock Ledger Entry`.warehouse = '{warehouse}'"


    if item_code is not None:
        conditions += f" AND `tabItem`.item_code = '{item_code}'"

    if item_group is not None:
        conditions += f" AND `tabItem`.item_group = '{item_group}'"


    data = frappe.db.sql(f"""
        SELECT 
            `tabStock Ledger Entry`.name as name,
            `tabStock Ledger Entry`.posting_date as posting_date,
            `tabStock Ledger Entry`.item_code as item_code,
            `tabStock Ledger Entry`.stock_uom as stock_uom,
            `tabStock Ledger Entry`.qty_after_transaction as qty_after_transaction,
            `tabStock Ledger Entry`.actual_qty as actual_qty,
            `tabStock Ledger Entry`.voucher_no as voucher_no,
            `tabStock Ledger Entry`.warehouse as warehouse,
            `tabItem`.item_name as item_name,
            `tabItem`.item_group as item_group

        FROM `tabStock Ledger Entry`
        JOIN `tabItem`
            ON `tabItem`.name = `tabStock Ledger Entry`.item_code
        WHERE 1=1
        {conditions}
        LIMIT {start}, {page_length}

    """, as_dict=True)
    for i in data:
        in_qty = 0
        out_qty = 0
        if i.actual_qty > 0:in_qty = i.actual_qty
        if i.actual_qty < 0:out_qty = -1 * abs(i.actual_qty)
        response_dict = {
            'name': i.name,
            'date' : i.posting_date,
            'item_code' :i.item_code,
            'item_name' :i.item_name,
            'item_group' :i.item_group,
            'stock_uom' :i.stock_uom,
            'in_qty' :in_qty,
            'out_qty' : out_qty,
            'qty_after_transaction' :i.qty_after_transaction,
            'voucher_no' :i.voucher_no,
            'warehouse' :i.warehouse,
        }
        response.append(response_dict)
    if response:
        return response
    frappe.throw("No Data.", frappe.exceptions.DoesNotExistError)


@frappe.whitelist(methods=["GET"])
def item_price(item_code=None, price_list=None, item_group=None, start=0, page_length=20):
    conditions = ""
    if item_code is not None:
        conditions += f" AND `tabItem Price`.item_code = '{item_code}'"
        
    if price_list is not None:
        conditions += f" AND `tabItem Price`.price_list = '{price_list}'"

    if item_group is not None:
        conditions += f" AND `tabItem`.item_group = '{item_group}'"

    data = frappe.db.sql( 
        f"""
            SELECT
              `tabItem Price`.price_list, 
              `tabItem Price`.currency, 
              `tabItem Price`.item_code, 
              `tabItem Price`.item_name, 
              `tabItem`.item_group,
              `tabItem Price`.price_list_rate 
            FROM `tabItem Price` 
            JOIN `tabItem` 
                ON `tabItem Price`.item_code = `tabItem`.name
            WHERE 1=1
            {conditions}
            LIMIT {start}, {page_length}
        """,as_dict = True
    )
    if data:
        return data
    frappe.throw("No Data.", frappe.exceptions.DoesNotExistError)