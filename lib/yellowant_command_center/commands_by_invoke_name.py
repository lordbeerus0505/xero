"""Mapping for command invoke name to logic"""
from .commands import list_contacts,search_contact,update_contact,list_invoices,search_invoice,update_invoice,list_purchase_orders,search_purchase_orders,update_purchase_orders,reauthenticate

commands_by_invoke_name = {
    "list_contacts": list_contacts,
    "search_contact":search_contact,
    "update_contact":update_contact,
    "list_invoices":list_invoices,
    "search_invoice":search_invoice,
    "update_invoice":update_invoice,
    "list_purchase_orders":list_purchase_orders,
    "search_purchase_orders":search_purchase_orders,
    "update_purchase_orders":update_purchase_orders,
    "reauthenticate":reauthenticate,
}