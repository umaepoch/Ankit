# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, getdate

def execute(filters=None):
	if not filters: filters = {}

	validate_filters(filters)

	columns = get_columns()
	item_map = get_item_details(filters)
	iwb_map = get_item_warehouse_map(filters)

	data = []
	summ_data = [] 
        item_group_prev = []
        item_group_work = []
        item_count = 0
        tot_open_qty = 0
        tot_in_qty = 0
        tot_out_qty = 0
        tot_bal_qty = 0
	tot_bal_val = 0   
   
	for (company, item_group, item, warehouse) in sorted(iwb_map):
		qty_dict = iwb_map[(company, item_group, item, warehouse)]
		data.append([item_group, item, 
			warehouse,
			qty_dict.opening_qty,
			qty_dict.in_qty,
			qty_dict.out_qty,
			qty_dict.bal_qty,
			qty_dict.bal_val, qty_dict.val_rate
		
		])

	for rows in data:
       		if item_count == 0:
       			item_group_prev = rows[0]
			tot_open_qty = tot_open_qty + rows[3]
			tot_in_qty = tot_in_qty + rows[4]
			tot_out_qty = tot_out_qty + rows[5]
			tot_bal_qty = tot_bal_qty + rows[6]
			tot_bal_val = tot_bal_val + rows[7]
                        summ_data.append([item_group_prev, rows[1], 
			 	rows[2], rows[3],
				rows[4], rows[5],
				rows[6], rows[7],0				
 				])
                else:
			item_group_work = rows[0]			
			if item_group_prev == item_group_work:
				tot_open_qty = tot_open_qty + rows[3]
				tot_in_qty = tot_in_qty + rows[4]
				tot_out_qty = tot_out_qty + rows[5]
				tot_bal_qty = tot_bal_qty + rows[6]
				tot_bal_val = tot_bal_val + rows[7]
                                summ_data.append([item_group_prev, rows[1], 
			 	rows[2], rows[3],
				rows[4], rows[5],
				rows[6], rows[7],0				
 				])
			else:
				summ_data.append([item_group_work, rows[1], 
			 	rows[2], rows[3],
				rows[4], rows[5],
				rows[6], rows[7],0				
 				])
                                
				summ_data.append([item_group_prev, " ", 
			 	" ", tot_open_qty,
				tot_in_qty, tot_out_qty,
				tot_bal_qty, tot_bal_val,0				
 				])

                                tot_open_qty = 0
				tot_in_qty = 0
				tot_out_qty = 0
				tot_bal_qty = 0
				tot_bal_val = 0
				item_group_prev = item_group_work
		item_count = item_count + 1
		
		
		
						
	return columns, summ_data



                   


def get_columns():
	"""return columns"""

	columns = [
		_("Item Group")+"::100",
                _("Item")+":Link/Item:100",
		_("Warehouse")+":Link/Warehouse:100",
		_("Opening Qty")+":Float:100",
		_("In Qty")+":Float:80",
		_("Out Qty")+":Float:80",
		_("Balance Qty")+":Float:100",
		_("Valuation Rate")+":Float:90",
			]

	return columns

def get_conditions(filters):
	conditions = ""
	if not filters.get("from_date"):
		frappe.throw(_("'From Date' is required"))

	if filters.get("to_date"):
		conditions += " and posting_date <= '%s'" % frappe.db.escape(filters["to_date"])
	else:
		frappe.throw(_("'To Date' is required"))

	if filters.get("item_code"):
		conditions += " and item_code = '%s'" % frappe.db.escape(filters.get("item_code"), percent=False)

	if filters.get("warehouse"):
		warehouse_details = frappe.db.get_value("Warehouse", filters.get("warehouse"), ["lft", "rgt"], as_dict=1)
		if warehouse_details:
			conditions += " and exists (select name from `tabWarehouse` wh \
				where wh.lft >= %s and wh.rgt <= %s and sle.warehouse = wh.name)"%(warehouse_details.lft,
				warehouse_details.rgt)

	return conditions

def get_stock_ledger_entries(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""select item.item_group, sle.item_code, sle.warehouse, sle.posting_date, sle.actual_qty, sle.valuation_rate,
			sle.company, sle.voucher_type, sle.qty_after_transaction, sle.stock_value_difference
		from `tabStock Ledger Entry` sle, `tabItem` item where sle.item_code = item.name order by sle.posting_date, sle.posting_time, item.item_group, item.name""")

def get_item_warehouse_map(filters):
	iwb_map = {}
	from_date = getdate(filters["from_date"])
	to_date = getdate(filters["to_date"])

	sle = get_stock_ledger_entries(filters)

	for d in sle:
                print d
		key = (d[6], d[0], d[1], d[2])
		if key not in iwb_map:
			iwb_map[key] = frappe._dict({
				"opening_qty": 0.0, "opening_val": 0.0,
				"in_qty": 0.0, "in_val": 0.0,
				"out_qty": 0.0, "out_val": 0.0,
				"bal_qty": 0.0, "bal_val": 0.0,
				"val_rate": 0.0, "uom": None
			})

		qty_dict = iwb_map[(d[6], d[0], d[1], d[2])]

		if d[6] == "Stock Reconciliation":
			qty_diff = flt(d[8]) - qty_dict.bal_qty
		else:
			qty_diff = flt(d[4])

		value_diff = flt(d[9])

		if d[3] < from_date:
			qty_dict.opening_qty += qty_diff
			qty_dict.opening_val += value_diff

		elif d[3] >= from_date and d[3] <= to_date:
			if qty_diff > 0:
				qty_dict.in_qty += qty_diff
				qty_dict.in_val += value_diff
			else:
				qty_dict.out_qty += abs(qty_diff)
				qty_dict.out_val += abs(value_diff)

		qty_dict.val_rate = d[5]
		qty_dict.bal_qty += qty_diff
		qty_dict.bal_val += value_diff

	return iwb_map

def get_item_details(filters):
	condition = ''
	value = ()
	if filters.get("item_code"):
		condition = "where item_code=%s"
		value = (filters["item_code"],)

	items = frappe.db.sql("""select name, item_name, stock_uom, item_group, brand, description
		from tabItem {condition}""".format(condition=condition), value, as_dict=1)

	return dict((d.name, d) for d in items)

def validate_filters(filters):
	if not (filters.get("item_code") or filters.get("warehouse")):
		sle_count = flt(frappe.db.sql("""select count(name) from `tabStock Ledger Entry`""")[0][0])
		if sle_count > 500000:
			frappe.throw(_("Please set filter based on Item or Warehouse"))
