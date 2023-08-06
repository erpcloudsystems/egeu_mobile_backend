import frappe
import requests
from .helpers import upload_image


@frappe.whitelist(methods=["GET"])
def user_profile(name):
    user = frappe.get_doc("User", name)
    roles = list(map(lambda obj: obj.role, user.roles))
    response = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "gender": user.gender,
        "birth_date": user.birth_date,
        "user_type": user.user_type,
        "last_active": user.last_active,
        "last_login": user.last_login,
        "roles": roles,
        "user_image": user.user_image,
    }

    return response


@frappe.whitelist(methods=["PATCH"])
def update_user_profile(**kwargs):
    user = frappe.get_doc("User", frappe.session.user)

    if "first_name" in kwargs.keys():
        user.first_name = kwargs["first_name"]

    if "last_name" in kwargs.keys():
        user.last_name = kwargs["last_name"]

    if "gender" in kwargs.keys():
        user.gender = kwargs["gender"]

    if "birth_date" in kwargs.keys():
        user.birth_date = kwargs["birth_date"]

    if "image_content" in kwargs.keys():
        image_url = upload_image(
            filename=kwargs["filename"],
            image_content=kwargs["image_content"],
        )
        user.user_image = image_url

    user.save()
    roles = list(map(lambda obj: obj.role, user.roles))
    response = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "gender": user.gender,
        "birth_date": user.birth_date,
        "user_type": user.user_type,
        "last_active": user.last_active,
        "last_login": user.last_login,
        "roles": roles,
        "user_image": user.user_image,
    }
    return response
