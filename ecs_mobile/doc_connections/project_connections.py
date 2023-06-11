import frappe
from ecs_mobile.helpers import remove_html_tags

def purchase_invoice(cur_nam, search_text, filter1, filter2, filter3, filter4, filter5, start, page_length):
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

    connections = frappe.db.get_list(
        "Purchase Invoice",
        or_filters=or_conditions,
        filters=conditions|{"project": cur_nam},
        fields=[
            "name",
            "supplier",
            "posting_date",
            "grand_total",
            "status",
            "currency",
        ],
        order_by="`tabPurchase Invoice`.modified desc",
        start=start,
        page_length=page_length,
    )
    

    if connections:
        for pr_invoice in connections:
            items = frappe.db.get_all(
                "Purchase Invoice Item",
                filters={"parent": pr_invoice["name"]},
                fields=["item_code", "item_name", "item_group", "qty", "rate", "amount", "uom"],
            )
            pr_invoice["items"] = items
            
        return connections
    else:
        return "لا يوجد روابط !"

def task(cur_nam, search_text, filter2, filter3, filter4, filter5, filter6, filter7, start, page_length):
    conditions = {}
    conditions1 = {}
    if search_text != "%%":
        conditions1["name"] = ["like", search_text]
        conditions1["subject"] = ["like", search_text]

    
    if filter2 != "%%":
        conditions["status"] = filter2
    if filter3 != "%%":
        conditions["priority"] = filter3

    if filter4 != "%%" and filter5 == "%%":
        conditions["creation"] = [">=", filter4]
    if filter5 != "%%" and filter4 == "%%":
        conditions["creation"] = ["<=", filter5]
    if filter4 != "%%" and filter5 != "%%":
        conditions["creation"] = ["between", [filter4, filter5]]

    if filter6 != "%%":
        conditions["type"] = filter6
    if filter7 != "%%":
        conditions["color"] = filter7

    connections = frappe.db.get_list(
        "Task",
        or_filters=conditions1,
        filters=conditions|{"project": cur_nam},
        fields=[
            "name",
            "subject",
            "project",
            "priority",
            "status",
            "type",
            "color",
            "exp_start_date",
            "exp_end_date",
            "progress",
            "expected_time",
            "description",
            "department",
            "company",
        ],
        order_by="modified desc",
        start=start,
        page_length=page_length,
    )
    if connections:

        for task in connections:
            task["description"] = remove_html_tags(str(task["description"]))
            depends_on = frappe.db.get_all(
                "Task Depends On",
                filters={"parent": task["name"]},
                fields=["task", "project", "subject"],
            )
            task["depends_on"] = depends_on

        
        return connections
    else:
        return "لا يوجد !"

def timesheet(cur_nam, search_text, filter2, filter3, filter4, filter5, start, page_length):
    conditions = {}
    conditions1 = {}

    if search_text != "%%":
        conditions1["title"] = ["like", search_text]

    if filter2 != "%%":
        conditions["customer"] = filter2

    if filter3 != "%%":
        conditions["status"] = filter3

    if filter4 != "%%" and filter5 == "%%":
        conditions["start_date"] = [">=", filter4]

    if filter5 != "%%" and filter4 == "%%":
        conditions["end_date"] = ["<=", filter5]

    connections = frappe.db.get_list(
        "Timesheet",
        or_filters=conditions1,
        filters=conditions|{"parent_project": cur_nam},
        fields=[
            "name",
            "docstatus",
            "title",
            "customer",
            "currency",
            "exchange_rate",
            "status",
            "parent_project",
            "employee",
            "employee_name",
            "department",
            "start_date",
            "end_date",
            "total_hours",
            "total_billable_hours",
            "base_total_billable_amount",
            "base_total_billed_amount",
            "base_total_costing_amount",
            "total_billed_hours",
            "total_billable_amount",
            "total_billed_amount",
            "total_costing_amount",
            "per_billed",
            "note",
        ],
        order_by="`tabTimesheet`.modified desc",
        start=start,
        page_length=page_length,
    )
    if connections:
        for timesheet in connections:
            timesheet["note"] = remove_html_tags(str(timesheet["note"]))
            time_logs = frappe.db.get_all(
                "Timesheet Detail",
                filters={"parent": timesheet["name"]},
                fields=[
                    "activity_type",
                    "from_time",
                    "to_time",
                    "project",
                    "project_name",
                ],
            )
            timesheet["time_logs"] = time_logs
        
        return connections
    else:
        return "لا يوجد روابط !"

def sales_invoice(cur_nam, search_text, filter2, filter3, filter4, filter5, start, page_length):
    conditions = {}
    conditions1 = {}

    if search_text != "%%":
        conditions1["name"] = ["like", search_text]

    if filter2 != "%%":
        conditions["customer"] = filter2

    if filter3 != "%%":
        conditions["status"] = filter3

    if filter4 != "%%" and filter5 == "%%":
        conditions["posting_date"] = [">=", filter4]

    if filter5 != "%%" and filter4 == "%%":
        conditions["posting_date"] = ["<=", filter5]

    connections = frappe.db.get_list(
        "Sales Invoice",
        or_filters=conditions1,
        filters=conditions|{"project": cur_nam},
        fields=[
            "name",
            "posting_date",
            "posting_time",
            "customer",
            "due_date",
            "cost_center",
            "project",
            "tax_id",
            "status",
            "grand_total",
            "territory",
        ],
        order_by="`tabSales Invoice`.modified desc",
        start=0,
        page_length=20,
    )
    if connections:
        for invoice in connections:
            items = frappe.db.get_all(
                "Sales Invoice Item",
                filters={"parent": invoice["name"]},
                fields=["item_code", "item_name", "item_group","brand","qty","rate","amount","uom"],
            )
            invoice["items"] = items
            
        
        return connections
    else:
        return "لا يوجد روابط !"

def stock_entry(cur_nam, search_text, filter1, filter2, filter3, filter4, filter5, filter6, start, page_length):

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

    connections = frappe.db.get_list(
        "Stock Entry",
        or_filters=conditions1,
        filters=conditions|{"project": cur_nam},
        fields=[
            "name",
            "stock_entry_type",
            "posting_date",
            "from_warehouse",
            "to_warehouse",
            "docstatus",
        ],
        order_by="modified desc",
        start=start,
        page_length=page_length,
    )
    if connections:
        return connections
    else:
        return "لا يوجد !"

def material_request(cur_nam, search_text, filter1, filter2, filter3, filter4, filter5, start, page_length):
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
    connections = frappe.get_list(
        "Material Request",
        or_filters=or_conditions,
        filters=conditions|{"project": cur_nam},
        fields=[
            "name",
            "material_request_type",
            "transaction_date",
            "set_warehouse",
            "status",
        ],
        order_by="modified desc",
        start=start,
        page_length=page_length,
    )
    if connections:
        return connections
    else:
        return "لا يوجد !"

def sales_order(cur_nam, search_text, filter1, filter2, filter3, filter4, filter5, filter6, filter7, filter8, start, page_length):
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

    connections = frappe.db.get_list(
        "Sales Order",
        or_filters=conditions1,
        filters=conditions|{"project": cur_nam},
        fields=[
            "name",
            "customer_name",
            "customer_address",
            "transaction_date",
            "grand_total",
            "status",
            "currency",
        ],
        order_by="modified desc",
        start=start,
        page_length=page_length,
    )
    if connections:
        return connections
    else:
        return "لا يوجد !"

def delivery_note(cur_nam, search_text, filter1, filter2, filter3, filter4, filter5, start, page_length):

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

    connections = frappe.db.get_list(
        "Delivery Note",
        or_filters=conditions1,
        filters=conditions|{"project": cur_nam},
        fields=[
            "name",
            "customer",
            "territory",
            "posting_date",
            "set_warehouse",
            "status",
            "currency",
        ],
        order_by="modified desc",
        start=start,
        page_length=page_length,
    )
    if connections:
        return connections
    else:
        return "لا يوجد !"

def issue(cur_nam, search_text, filter1, filter2, filter3, filter4, start, page_length):
    conditions = {}
    conditions1 = {}
    if search_text != "%%":
        conditions1["name"] = ["like", search_text]
        conditions1["subject"] = ["like", search_text]

    if filter1 != "%%":
        conditions["status"] = filter1
    if filter2 != "%%":
        conditions["customer"] = filter2
    if filter3 != "%%" and filter4 == "%%":
        conditions["priority"] = filter3
    if filter4 != "%%":
        conditions["issue_type"] = filter4


    connections = frappe.db.get_list(
        "Issue",
        or_filters=conditions1,
        filters=conditions|{"project": cur_nam},
        fields=[
            "name",
            "subject",
            "status",
            "priority",
            "customer",
            "issue_type",
            "description"
        ],
        order_by="modified desc",
        start=start,
        page_length=page_length,
    )
    if connections:
        return connections
    else:
        return "لا يوجد !"

def purchase_reciept(cur_nam, search_text, filter1, filter2, filter3, filter4, filter5, filter6, start, page_length):
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
        filters=conditions|{"project": cur_nam},
        fields=[
            "name",
            "supplier",
            "posting_date",
            "set_warehouse",
            "status",
            "currency",
        ],
        order_by="modified desc",
        start=start,
        page_length=page_length,
    )
    if query:
        return query
    else:
        return "لا يوجد !"   

def expense_claim(cur_name, search_text, filter1, filter2, filter3, filter4, filter5, start, page_length):
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
        filters=conditions|{"project": cur_name},
        fields=[
            "name",
            "employee_name",
            "employee",
            "department",
            "posting_date",
            "grand_total",
            "status",
        ],
        order_by="modified desc",
        start=start,
        page_length=page_length,
    )
    if query:
        return query
    else:
        return "لا يوجد !"

def bom(cur_nam, start, page_length):
    results = []
    query = frappe.db.get_list(
        "BOM",
        filters={"project": cur_nam},
        fields=[
            "name",
            "item",
            "company",
            "item_name",
            "uom",
            "project",
            "quantity",
            "image",
            "currency",
            "conversion_rate",
            "operating_cost",
            "raw_material_cost",
            "scrap_material_cost",
            "total_cost",
            "base_total_cost",
            "description"
        ],
        order_by="modified desc",
        start=start,
        page_length=page_length,
    )
    for q in query:
        result_dict = {}
        result_dict["name"] = q.name
        result_dict["item"] = q.item
        result_dict["company"] = q.company
        result_dict["item_name"] = q.item_name
        result_dict["uom"] = q.uom
        result_dict["quantity"] = q.quantity
        result_dict["image"] = q.image
        result_dict["currency"] = q.currency
        result_dict["conversion_rate"] = q.conversion_rate
        result_dict["operating_cost"] = q.operating_cost
        result_dict["raw_material_cost"] = q.raw_material_cost
        result_dict["scrap_material_cost"] = q.scrap_material_cost
        result_dict["total_cost"] = q.total_cost
        result_dict["base_total_cost"] = q.base_total_cost
        result_dict["description"] = q.base_total_cost
        result_dict["items"] = frappe.db.get_all("BOM Item", filters={"parent": q["name"]}, fields=[
            "name",
            "item_code",
            "item_name",
            "bom_no",
            "operation",
            "source_warehouse",
            "allow_alternative_item",
            "description",
            "qty",
            "uom",
            "stock_qty",
            "stock_uom",
            "conversion_factor",
            "rate",
            "base_rate",
            "amount",
            "base_amount",
            "qty_consumed_per_unit",
            "has_variants",
            "include_item_in_manufacturing",
            "original_item",
            "sourced_by_supplier",
        ])
        result_dict["scrap_items"] = frappe.db.get_all("BOM Scrap Item", filters={"parent": q["name"]}, fields=[
            "name",
            "item_code",
            "item_name",
            "is_process_loss",
            "stock_qty",
            "rate",
            "amount",
            "stock_uom",
            "base_rate",
            "base_amount"

        ])
        result_dict["exploded_items"] = frappe.db.get_all("BOM Explosion Item", filters={"parent": q["name"]}, fields=[
            "name",
            "item_code",
            "item_name",
            "source_warehouse",
            "operation",
            "description",
            "image",
            "stock_qty",
            "rate",
            "qty_consumed_per_unit",
            "stock_uom",
            "amount",
            "include_item_in_manufacturing",
            "sourced_by_supplier"
        
        ])
        
        results.append(result_dict)
    if results:
        return results
    else:
        return "لا يوجد !"