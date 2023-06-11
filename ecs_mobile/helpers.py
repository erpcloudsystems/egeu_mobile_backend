import frappe


def remove_html_tags(text):
    """Remove html tags from a string"""
    
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def order_by(sort_field, sort_type):
    """
        Order the get_list query with sort field and sort type
        provided by the user
    """
    order_by = ""
    if (sort_field is not None) and (sort_type is not None):
        order_by = f"{sort_field} {sort_type}"
    return order_by