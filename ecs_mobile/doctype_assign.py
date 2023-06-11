import frappe

def todo_create(assign_to: list, completed_by: str, priority: str, description: str, reference_type: str, reference_name: str) -> None:
    for user in assign_to:
        data = {
            "doctype": "ToDo",
            "status": "Open",
            "priority": priority,
            "date": completed_by,
            "description": description,
            "allocated_to": user,
            "reference_type": reference_type,
            "reference_name": reference_name,
            "assigned_by": frappe.session.user,
        }
        todo = frappe.get_doc(data)
        todo.insert()


@frappe.whitelist(methods=["POST"])
def assign(**kwargs):
    data = kwargs["data"]
    todo_create(data["assign_to"], data["date"], data["priority"], data["description"], data["reference_type"], data["reference_name"])
    response = {
                "success_key": True,
                "doctype": data["reference_type"],
                "document_name": data["reference_name"]
            }
    return response


@frappe.whitelist(methods=["PATCH"])
def cancel(**kwargs)-> None:
    query = frappe.db.get_list(
            "ToDo", 
            filters={
                    "reference_name": kwargs["document_name"],
                    "allocated_to":kwargs["user"]
                },
            )
    if query:
        todo_doc = frappe.get_doc("ToDo", query[0].name)
        todo_doc.status = "Cancelled"
        todo_doc.save()
        return {"todo": query[0].name}
    return {"error": "There is no todo found."}


@frappe.whitelist(methods=["GET"])
def assigned_list(doctype, document_name):
    users = frappe.db.get_all("ToDo", filters={
        "reference_type": doctype,
        "reference_name": document_name,
        },
        fields=["allocated_to"]
    )
    assigned_users_list = []
    for user in users:
        assigned_users_list.append(user["allocated_to"])
    return assigned_users_list
    










