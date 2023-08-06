import frappe
from .helpers import is_field_exists, get_current_user_roles


class Workflow:
    def __init__(self, doctype: str, document_name: str, action: str = None) -> None:
        self.doctype = doctype
        self.document_name = document_name
        self.action = action

    def get_current_state(self):
        wf_state = frappe.db.get_value(
            self.doctype, {"name": self.document_name}, ["workflow_state"]
        )
        return wf_state

    def get_workflow(self) -> dict:
        workflow_name = frappe.db.get_value(
            "Workflow", {"document_type": self.doctype}, ["name"]
        )
        workflow = frappe.get_doc("Workflow", workflow_name)
        return workflow

    def get_next_valid_state(self) -> str:
        """Get the next valid workflow state for the document."""

        # Check if the workflow_state field exists in the provided doctype
        if not (is_field_exists(doctype=self.doctype, fieldname="workflow_state")):
            frappe.throw(
                "There is no workflow set for this doctype",
                frappe.exceptions.DoesNotExistError,
            )

        # Get the work flow associated to this doctype
        workflow = self.get_workflow()

        current_workflow_state = self.get_current_state()

        # This expression return a list of a single dict
        next_transition = list(
            d
            for d in workflow.transitions
            if d.state == current_workflow_state and d.action == self.action
        )

        # Check if the transitions list has dicts if so get the next state else return None
        next_state = None
        if len(next_transition):
            next_state = next_transition[0].get("next_state")

        return next_state

    def get_next_state_docstatus(self) -> str:
        """Get the docstatus associated with a workflow state for the document."""

        workflow = self.get_workflow()
        next_wf_state = self.get_next_valid_state()
        next_state = list(d for d in workflow.states if d.get("state") == next_wf_state)

        next_docstatus = None
        if len(next_state):
            next_docstatus = next_state[0].get("doc_status")

        return next_docstatus

    def get_allowed_actions(self):
        workflow = self.get_workflow()
        current_workflow_state = self.get_current_state()

        user_roles = get_current_user_roles()
        actions = list(
            transition.action
            for transition in workflow.transitions
            if transition.state == current_workflow_state
            and transition.allowed in user_roles
            or transition.allowed == "All"
        )
        return actions


@frappe.whitelist(methods=["PATCH"])
def update_workflow(**kwargs: dict) -> dict:
    """Update the workflow state of the document."""

    doctype = kwargs.get("doctype")
    document_name = kwargs.get("document_name")
    action = kwargs.get("action")

    wf_obj = Workflow(doctype=doctype, document_name=document_name, action=action)
    doc = frappe.get_doc(doctype, document_name)

    next_state = wf_obj.get_next_valid_state() # status as str
    next_state_docstatus = wf_obj.get_next_state_docstatus() # status as number but of datatype str

    doc.workflow_state = next_state
    doc.docstatus = next_state_docstatus
    doc.save(ignore_permissions=True) # remove in the production
    return doc


@frappe.whitelist(methods=["POST"])
def has_workflow(**kwargs) -> bool:
    """Check if a doctype has a workflow_state field

    Returns:
        _bool_: _False_ if the field does not exist, _True_ if the field exists
    """
    return is_field_exists(doctype=kwargs.get("doctype"), fieldname="workflow_state")


@frappe.whitelist(methods=["GET"])
def get_workflow_actions(doctype: str, docname: str) -> list[str]:
    """retrieve the workflow actions allowed for the logged in user:

    Args:
        doctype (str)
        docname (str)

    Returns:
        list[str]: list of actions allowed to the user
    """

    wf = Workflow(doctype=doctype, document_name=docname)
    actions = wf.get_allowed_actions()
    return actions


@frappe.whitelist(methods=["GET"])
def get_workflow_status(doctype: str, docname: str) -> str:
    return frappe.db.get_value(doctype, {"name": docname}, ["workflow_state"])
