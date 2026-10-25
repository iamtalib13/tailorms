import frappe


def setup_pos_desktop():
	"""Automatically configure POS single desktop icon on app install or migration."""
	# 1. Enable Desktop Icons mode
	frappe.db.set_single_value("Desktop Settings", "desktop_page", "Desktop Icons")

	# 2. Hide all other desktop icons
	frappe.db.sql(
		"""
		UPDATE `tabDesktop Icon`
		SET hidden = 1
		WHERE label != 'POS'
	"""
	)

	# 3. Create or update POS desktop icon
	if frappe.db.exists("Desktop Icon", "POS"):
		icon_doc = frappe.get_doc("Desktop Icon", "POS")
	else:
		icon_doc = frappe.new_doc("Desktop Icon")
		icon_doc.label = "POS"

	icon_doc.icon_type = "App"
	icon_doc.link_type = "External"
	icon_doc.link = "/pos"
	icon_doc.standard = 0
	icon_doc.app = "tailorms"
	icon_doc.hidden = 0
	icon_doc.parent_icon = None
	icon_doc.bg_color = "gray"
	icon_doc.save(ignore_permissions=True)

	# 4. Clean up any saved layouts so new grid layout applies
	frappe.db.delete("Desktop Layout")
	frappe.db.commit()
	frappe.clear_cache()
