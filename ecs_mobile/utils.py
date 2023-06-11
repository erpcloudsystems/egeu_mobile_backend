import frappe


def inject_price_list_rate_free_items(free_items:list, selling_price_list:str) -> list:
    """
    Add `price_list_rate` for each item in the `free_items` list
    """

    for item in free_items:
        price_list_rate = frappe.db.get_value(
                "Item Price", 
                {"item_code": item["item_code"], "price_list": selling_price_list},
                ["price_list_rate"]
            )
        item["price_list_rate"] = price_list_rate
    
    return free_items


def inject_sales_team(data:dict) -> dict:
    """
    Add sales team information from the customer infromation
    to the sales invoice before creation.
    """
    if data["customer"]:
        sales_team = frappe.db.get_all(
                    "Sales Team",
                    filters={"parent": data["customer"]},
                    fields=
                        [
                            "name", 
                            "sales_person", 
                            "allocated_percentage", 
                            "commission_rate"
                        ]
                    )
        data["sales_team"] = sales_team
    return data

def inject_item_actual_qty_free_items(free_items:list) -> list:
    """
    Add `actual_qty` value from `Bin`
    to each item in `Free Item` table before creation.
    """
    for item in free_items:
        actual_qty = frappe.db.get_value("Bin", {"item_code": item["item_code"]}, ["actual_qty"])
        item["actual_qty"] = actual_qty
    
    return free_items

def inject_item_uom_conversion_factor(free_items:list) -> list:
    """
    Add `conversion_factor` for each item in the `Free Item` table
    """
    for item in free_items:
        conversion_factor = frappe.db.get_value(
            "UOM Conversion Detail", 
            {"parent": item["item_code"]},
            ["conversion_factor"]
        )
        item["conversion_factor"] = conversion_factor

    return free_items

def inject_item_group_free_item(free_items):
    """
    Add `item_group`,`description`, `stock_uom` of each item in `Free Item` table.
    """
    for item in free_items:
        item["item_group"] = frappe.db.get_value("Item", {"item_code": item["item_code"]}, ["item_group"])
        item["stock_uom"] = frappe.db.get_value("Item", {"item_code": item["item_code"]}, ["stock_uom"])
    return free_items