
from __future__ import unicode_literals
import frappe
from frappe.utils import cint, flt, cstr, comma_or
from frappe import _, throw

def get_company_currency(company):
        currency = frappe.db.get_value("Company", company, "default_currency", cache=True)
        if not currency:
                currency = frappe.db.get_default("currency")
        if not currency:
                throw(_('Please specify Default Currency in Company Master and Global Defaults'))

        return currency

@frappe.whitelist()

def set_total_in_words(doc, method):
    from frappe.utils import money_in_words
    company_currency = get_company_currency(doc.company)

    disable_rounded_total = cint(frappe.db.get_value("Global Defaults", None, "disable_rounded_total"))

    if doc.meta.get_field("base_in_words"):
        doc.base_in_words = money_in_words(disable_rounded_total and
            abs(doc.base_grand_total) or abs(doc.base_rounded_total), company_currency)
    if doc.meta.get_field("in_words"):
        doc.in_words = money_in_words(disable_rounded_total and
          abs(doc.grand_total) or abs(doc.rounded_total), doc.currency)
    if doc.meta.get_field("amount_of_duty_in_words"):
        doc.amount_of_duty_in_words = money_in_words(disable_rounded_total and
            abs(doc.excise_amount) or abs(doc.excise_amount), doc.currency)
    if doc.meta.get_field("vat_in_words"):
        doc.vat_in_words = money_in_words(disable_rounded_total and
            abs(doc.vat_amount) or abs(doc.vat_amount), doc.currency)

