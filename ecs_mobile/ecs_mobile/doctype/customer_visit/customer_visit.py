# Copyright (c) 2022, ERPCloud.Systems and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

import json
from collections import defaultdict

import frappe
from frappe import scrub
from frappe.desk.reportview import get_filters_cond, get_match_cond
from frappe.utils import nowdate, unique

import erpnext
from erpnext.stock.get_item_details import _get_item_tax_template

class CustomerVisit(Document):
    pass

