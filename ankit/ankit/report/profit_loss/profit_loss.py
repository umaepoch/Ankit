# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt
from ankit.ankit.report.financial_statement_test import (get_period_list_test, get_columns_test, get_data_test)
from erpnext.accounts.report.financial_statements import (get_period_list, get_columns, get_data)

def execute(filters=None):
	period_list = get_period_list(filters.from_fiscal_year, filters.to_fiscal_year,
		filters.periodicity, filters.accumulated_values, filters.company)
	period_list_test = get_period_list_test(filters.from_fiscal_year, filters.to_fiscal_year,
		filters.periodicity, filters.accumulated_values, filters.company)
	income = get_data(filters.company, "Income", "Credit", period_list, filters = filters,
		accumulated_values=filters.accumulated_values,
		ignore_closing_entries=True, ignore_accumulated_values_for_fy= True)
	income_test = get_data_test(filters.company, "Income", "Credit", period_list_test, filters = filters,
		accumulated_values=filters.accumulated_values,
		ignore_closing_entries=True, ignore_accumulated_values_for_fy= True)
	expense = get_data(filters.company, "Expense", "Debit", period_list, filters=filters,
		accumulated_values=filters.accumulated_values,
		ignore_closing_entries=True, ignore_accumulated_values_for_fy= True)
	expense_test = get_data_test(filters.company, "Expense", "Debit", period_list_test, filters=filters,
		accumulated_values=filters.accumulated_values,
		ignore_closing_entries=True, ignore_accumulated_values_for_fy= True)
	net_profit_loss = get_net_profit_loss(income, expense, period_list, filters.company, filters.presentation_currency)
	net_profit_loss_test = get_net_profit_loss_test(income_test, expense_test, period_list_test, filters.company, filters.presentation_currency)
	data = []
	sum_data=[]
	data.extend(income or [])
	data.extend(expense or [])
	sum_data.extend(income_test or [])
	sum_data.extend(expense_test or [])
	if net_profit_loss:
		data.append(net_profit_loss)
	if net_profit_loss_test:
		sum_data.append(net_profit_loss_test)
	columns = get_columns(filters.periodicity, period_list, filters.accumulated_values, filters.company)

	chart = get_chart_data(filters, columns, income, expense, net_profit_loss)
	print("data-----------",data)
	print("sum_data",sum_data)
	print("filters.periodicity",filters.periodicity)
	for x in range(len(data)):
		if data[x].get('account_name') == 'Closing Stocks' and filters.periodicity=="Quarterly":
			print('quaterly data ----', data[x])
			print('monthly data ----', sum_data[x])
			data[x]['sep_2022'] = sum_data[x]['sep_2022']
			data[x]['jun_2022'] = sum_data[x]['jun_2022']
			data[x]['dec_2022'] = sum_data[x]['dec_2022']
			data[x]['mar_2023'] = sum_data[x]['mar_2023']
			data[x]['total']=sum_data[x]['jun_2022']+sum_data[x]['sep_2022']+sum_data[x]['dec_2022']+sum_data[x]['mar_2023']
		if data[x].get('account_name') == 'Opening Stock' and filters.periodicity=="Quarterly":
			print('quaterly data ----', data[x])
			print('monthly data ----', sum_data[x])
			data[x]['sep_2022'] = sum_data[x]['jul_2022']
			data[x]['jun_2022'] = sum_data[x]['apr_2022']
			data[x]['dec_2022'] = sum_data[x]['oct_2022']
			data[x]['mar_2023'] = sum_data[x]['jan_2023']
			data[x]['total']=sum_data[x]['apr_2022']+sum_data[x]['jul_2022']+sum_data[x]['oct_2022']+sum_data[x]['jan_2023']
	june_sum=0
	sep_sum=0
	dec_sum=0
	mar_sum=0
	june_sum_ex=0
	sep_sum_ex=0
	dec_sum_ex=0
	mar_sum_ex=0
	array_index=0
	flag = 0
	for x in data:
		if x.get('is_group') == 0 and "Income" in x.get('parent_account','None'):
			print('adding')
			june_sum += x.get('jun_2022', 0)
			sep_sum += x.get('sep_2022', 0)
			dec_sum += x.get('dec_2022', 0)
			mar_sum += x.get('mar_2023', 0)
		if x.get('is_group') == 0 and "Expenses" in x.get('parent_account','None'):
			print('adding')
			june_sum_ex += x.get('jun_2022', 0)
			sep_sum_ex += x.get('sep_2022', 0)
			dec_sum_ex += x.get('dec_2022', 0)
			mar_sum_ex += x.get('mar_2023', 0)
		if x.get('account', '') == 'Total Income (Credit)':
			x['jun_2022'] = june_sum
			x['sep_2022'] = sep_sum
			x['dec_2022'] = dec_sum
			x['mar_2023'] = mar_sum
			x['total']=june_sum+sep_sum+dec_sum+mar_sum
		if x.get('account', '') == 'Total Expense (Debit)':
			x['jun_2022'] = june_sum_ex
			x['sep_2022'] = sep_sum_ex
			x['dec_2022'] = dec_sum_ex
			x['mar_2023'] = mar_sum_ex
			x['total']=june_sum_ex+sep_sum_ex+dec_sum_ex+mar_sum_ex
		if x.get('account', '') == "'Profit for the year'":
			x['jun_2022'] = june_sum-june_sum_ex
			x['sep_2022'] = sep_sum-sep_sum_ex
			x['dec_2022'] = dec_sum-dec_sum_ex
			x['mar_2023'] = mar_sum-mar_sum_ex
			x['total']=(june_sum+sep_sum+dec_sum+mar_sum)-(june_sum_ex+sep_sum_ex+dec_sum_ex+mar_sum_ex)
	for x in data:
		print("filters.company",filters.company)
		abbr = frappe.db.get_value("Company",{"name":filters.company},"abbr")
		print("company abbr",abbr)
		company="Expenses - "+str(abbr)+""
		print("--",company)
		if(flag):
			break
		for keys, values in x.items():
			if "account" == keys:
				if "Expenses - "+str(abbr)+""== values:
					x[keys] = values
					flag=1
					break
		array_index = array_index+ 1
			
		
	#sum_data[0]['jun_2022'] = june_sum
	data[0]['jun_2022'] = june_sum
	data[0]['sep_2022'] = sep_sum
	data[0]['dec_2022'] = dec_sum
	data[0]['mar_2023'] = mar_sum
	data[array_index-1]["jun_2022"]=june_sum_ex
	data[array_index-1]["sep_2022"]=sep_sum_ex
	data[array_index-1]["dec_2022"]=dec_sum_ex
	data[array_index-1]["mar_2023"]=mar_sum_ex
	#print("---",data[array_index-1]["account"])
	#print("data",data)
	return columns, data, None, chart

def get_net_profit_loss(income, expense, period_list, company, currency=None, consolidated=False):
	total = 0
	net_profit_loss = {
	"account_name": "'" + _("Profit for the year") + "'",
	"account": "'" + _("Profit for the year") + "'",
	"warn_if_negative": True,
	"currency": currency or frappe.get_cached_value('Company',  company,  "default_currency")
	}

	has_value = False

	for period in period_list:
		key = period if consolidated else period.key
		total_income = flt(income[-2][key], 3) if income else 0
		total_expense = flt(expense[-2][key], 3) if expense else 0

		net_profit_loss[key] = total_income - total_expense

		if net_profit_loss[key]:
			has_value=True

		total += flt(net_profit_loss[key])
		net_profit_loss["total"] = total
	print("total-------",total)
	if has_value:
		return net_profit_loss

def get_net_profit_loss_test(income_test, expense_test, period_list_test, company, currency=None, consolidated=False):
	total = 0
	net_profit_loss = {
	"account_name": "'" + _("Profit for the year") + "'",
	"account": "'" + _("Profit for the year") + "'",
	"warn_if_negative": True,
	"currency": currency or frappe.get_cached_value('Company',  company,  "default_currency")
	}

	has_value = False

	for period in period_list_test:
		key = period if consolidated else period.key
		total_income = flt(income_test[-2][key], 3) if income_test else 0
		total_expense = flt(expense_test[-2][key], 3) if expense_test else 0

		net_profit_loss[key] = total_income - total_expense

		if net_profit_loss[key]:
			has_value=True

		total += flt(net_profit_loss[key])
		net_profit_loss["total"] = total

	if has_value:
		return net_profit_loss

def get_chart_data(filters, columns, income, expense, net_profit_loss):
	labels = [d.get("label") for d in columns[2:]]

	income_data, expense_data, net_profit = [], [], []

	for p in columns[2:]:
		if income:
			income_data.append(income[-2].get(p.get("fieldname")))
		if expense:
			expense_data.append(expense[-2].get(p.get("fieldname")))
		if net_profit_loss:
			net_profit.append(net_profit_loss.get(p.get("fieldname")))

	datasets = []
	if income_data:
		datasets.append({'name': _('Income'), 'values': income_data})
	if expense_data:
		datasets.append({'name': _('Expense'), 'values': expense_data})
	if net_profit:
		datasets.append({'name': _('Net Profit/Loss'), 'values': net_profit})

	chart = {
		"data": {
			'labels': labels,
			'datasets': datasets
		}
	}

	if not filters.accumulated_values:
		chart["type"] = "bar"
	else:
		chart["type"] = "line"

	chart["fieldtype"] = "Currency"

	return chart