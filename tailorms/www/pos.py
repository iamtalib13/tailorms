import frappe


def get_context(context):
	if frappe.session.user == "Guest":
		frappe.local.flags.redirect_location = "/login?redirect-to=/pos"
		raise frappe.Redirect

	context.csrf_token = frappe.sessions.get_csrf_token()
	return context
