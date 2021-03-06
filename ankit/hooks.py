# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "ankit"
app_title = "Ankit"
app_publisher = "Epoch"
app_description = "Ankit customization"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "umag@epochconsulting.in"
app_license = "MIT"
fixtures = ["Custom Field",
"Property Setter",
"Custom Script",
"Report",
"Print Format"]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ankit/css/ankit.css"
# app_include_js = "/assets/ankit/js/ankit.js"

# include js, css files in header of web template
# web_include_css = "/assets/ankit/css/ankit.css"
# web_include_js = "/assets/ankit/js/ankit.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "ankit.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "ankit.install.before_install"
# after_install = "ankit.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ankit.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

doc_events = {
       "Sales Invoice": {
                "validate": "ankit.api.set_total_in_words"
             }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"ankit.tasks.all"
# 	],
# 	"daily": [
# 		"ankit.tasks.daily"
# 	],
# 	"hourly": [
# 		"ankit.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ankit.tasks.weekly"
# 	]
# 	"monthly": [
# 		"ankit.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "ankit.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ankit.event.get_events"
# }

