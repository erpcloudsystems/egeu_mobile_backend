import frappe
from datetime import datetime
# import humanize
import base64

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


def encode_image(image_content):
    endcoded_str = base64.b64encode(image_content).decode("utf-8")
    return endcoded_str


def upload_image(filename, image_content):
    file_doc = frappe.get_doc(
        {
            "doctype": "File",
            "file_name": filename,
            "is_private": False,
            "content": image_content,
            "decode": True,
        }
    )
    file_doc.save(ignore_permissions=True)
    return file_doc.file_url


# def humanize_datetime(datetime_str):
#     dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f")
#     humanized_str = humanize.naturaltime(dt)
#     return humanized_str


def get_connections(doc_list, fileds, filters, con_filed, con_doc):
    result = {}
    for doc in doc_list:
        data = frappe.db.get_all(doc, fileds[doc], filters[doc])
        result[doc] = data
    return result


def get_timesheet_task_count(task):
    """
    Get the count of the timesheet connected to a certain task
    """
    c = 0
    tss = frappe.db.get_all("Timesheet")
    for i in tss:
        ts = frappe.get_doc("Timesheet", i.name)
        for log in ts.time_logs:
            if log.task == task:
                c += 1
    return c


def is_field_exists(doctype, fieldname):
    meta = frappe.get_meta(doctype)
    field_exists = fieldname in [field.fieldname for field in meta.fields]

    if field_exists:
        return True
    else:
        return False


def get_current_user_roles():
    roles = frappe.get_doc("User", frappe.session.user).roles
    return list(role.role for role in roles)

