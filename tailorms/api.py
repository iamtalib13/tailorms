import frappe
from frappe import _


@frappe.whitelist()
def get_pos_data():
	"""Get lightweight POS bootstrap data without POS Profile."""
	company = frappe.db.get_single_value("Global Defaults", "default_company")
	if not company:
		companies = frappe.get_all("Company", pluck="name", limit=1)
		company = companies[0] if companies else None

	customers = frappe.get_all(
		"Customer",
		filters={"disabled": 0},
		fields=["name", "customer_name", "mobile_no"],
		order_by="modified desc",
		limit=100,
	)

	default_customer = customers[0]["name"] if customers else None

	templates = frappe.get_all(
		"Item",
		filters={"disabled": 0, "has_variants": 1},
		fields=["item_code", "item_name"],
		order_by="item_name asc",
	)

	items = frappe.get_all(
		"Item",
		filters={"disabled": 0, "is_sales_item": 1, "has_variants": 0},
		fields=["item_code", "item_name", "standard_rate", "stock_uom", "item_group", "variant_of", "is_stock_item"],
		order_by="modified desc",
		limit=200,
	)

	# Fetch actual item selling price and stock actual_qty
	for itm in items:
		price = frappe.db.get_value(
			"Item Price",
			{"item_code": itm["item_code"], "selling": 1},
			"price_list_rate",
		)
		itm["selling_price"] = price if price is not None else (itm.get("standard_rate") or None)

		if itm.get("is_stock_item"):
			actual_qty = frappe.db.sql(
				"""SELECT COALESCE(SUM(actual_qty), 0) FROM tabBin WHERE item_code = %s""",
				(itm["item_code"],),
			)[0][0]
			itm["actual_qty"] = float(actual_qty)
		else:
			itm["actual_qty"] = None

	modes_of_payment = frappe.get_all(
		"Mode of Payment",
		filters={"enabled": 1},
		pluck="name",
		limit=10,
	)

	return {
		"company": company,
		"default_customer": default_customer,
		"customers": customers,
		"templates": templates,
		"items": items,
		"modes_of_payment": ["Cash", "UPI"],
	}


@frappe.whitelist()
def create_customer(customer_name, mobile_no=None, email_id=None):
	"""Quick create customer from POS interface."""
	doc = frappe.new_doc("Customer")
	doc.customer_name = customer_name
	doc.customer_type = "Individual"
	if mobile_no:
		doc.mobile_no = mobile_no
	if email_id:
		doc.email_id = email_id
	doc.insert(ignore_permissions=True)
	return {
		"name": doc.name,
		"customer_name": doc.customer_name,
		"mobile_no": getattr(doc, "mobile_no", ""),
		"email_id": getattr(doc, "email_id", ""),
	}


@frappe.whitelist()
def search_customers(query=""):
	"""Search customers by name or mobile_no like ERPNext POS."""
	filters = {"disabled": 0}
	or_filters = []
	if query:
		or_filters = [
			["customer_name", "like", f"%{query}%"],
			["name", "like", f"%{query}%"],
			["mobile_no", "like", f"%{query}%"],
		]

	return frappe.get_all(
		"Customer",
		filters=filters,
		or_filters=or_filters if or_filters else None,
		fields=["name", "customer_name", "mobile_no", "email_id"],
		order_by="modified desc",
		limit=20,
	)


@frappe.whitelist()
def create_sales_invoice(customer, items, payments=None, update_stock=0):
	"""Create and submit a simple Sales Invoice directly without POS Profile/Shift complexity."""
	if isinstance(items, str):
		items = frappe.parse_json(items)
	if isinstance(payments, str):
		payments = frappe.parse_json(payments)

	company = frappe.db.get_single_value("Global Defaults", "default_company")
	if not company:
		companies = frappe.get_all("Company", pluck="name", limit=1)
		company = companies[0] if companies else None

	si = frappe.new_doc("Sales Invoice")
	si.company = company
	si.customer = customer
	si.is_pos = 1
	si.update_stock = 1 if int(update_stock) == 1 else 0
	si.set_posting_time = 1

	for row in items:
		si.append(
			"items",
			{
				"item_code": row.get("item_code"),
				"qty": float(row.get("qty") or 1),
				"rate": float(row.get("rate") or 0),
			},
		)

	si.set_missing_values()
	si.update_stock = 1 if int(update_stock) == 1 else 0
	si.calculate_taxes_and_totals()

	# Payments
	total_amount = si.rounded_total or si.grand_total
	if payments:
		for p in payments:
			si.append(
				"payments",
				{
					"mode_of_payment": p.get("mode_of_payment"),
					"amount": float(p.get("amount") or 0),
				},
			)
	else:
		default_mop = frappe.db.get_value("Mode of Payment", {"type": "Cash"}, "name") or "Cash"
		si.append(
			"payments",
			{
				"mode_of_payment": default_mop,
				"amount": total_amount,
			},
		)

	si.insert(ignore_permissions=True)
	si.submit()

	return {
		"name": si.name,
		"grand_total": si.grand_total,
		"rounded_total": si.rounded_total,
		"status": si.status,
	}


@frappe.whitelist()
def get_invoices(limit=50):
	"""Get recent sales invoices with customer mobile."""
	return frappe.db.sql(
		"""
		SELECT
			si.name, si.customer, si.customer_name,
			si.posting_date, si.grand_total, si.status,
			si.modified, c.mobile_no
		FROM `tabSales Invoice` si
		LEFT JOIN `tabCustomer` c ON c.name = si.customer
		ORDER BY si.creation DESC
		LIMIT %s
		""",
		(int(limit),),
		as_dict=True,
	)


@frappe.whitelist()
def get_invoice_detail(invoice_name):
	"""Get invoice with items and payments for popup view."""
	inv = frappe.get_doc("Sales Invoice", invoice_name)
	mobile = frappe.db.get_value("Customer", inv.customer, "mobile_no") or ""
	return {
		"name": inv.name,
		"customer": inv.customer,
		"customer_name": inv.customer_name,
		"mobile_no": mobile,
		"posting_date": str(inv.posting_date),
		"grand_total": inv.grand_total,
		"status": inv.status,
		"items": [
			{
				"item_code": r.item_code,
				"item_name": r.item_name,
				"qty": r.qty,
				"rate": r.rate,
				"amount": r.amount,
				"uom": r.uom or r.stock_uom,
			}
			for r in inv.items
		],
		"payments": [
			{"mode_of_payment": p.mode_of_payment, "amount": p.amount}
			for p in (inv.payments or [])
		],
	}


@frappe.whitelist()
def get_stock_entries(limit=50):
	"""Get recent purchase/stock entries with supplier."""
	return frappe.db.sql(
		"""
		SELECT name, stock_entry_type, purpose, posting_date,
		       total_amount, docstatus, supplier, supplier_name
		FROM `tabStock Entry`
		ORDER BY creation DESC
		LIMIT %s
		""",
		(int(limit),),
		as_dict=True,
	)


@frappe.whitelist()
def get_purchase_entry_detail(entry_name):
	"""Get stock entry with items for popup view."""
	se = frappe.get_doc("Stock Entry", entry_name)
	return {
		"name": se.name,
		"supplier": se.supplier,
		"supplier_name": se.supplier_name,
		"stock_entry_type": se.stock_entry_type,
		"posting_date": str(se.posting_date),
		"total_amount": float(se.total_amount or 0),
		"docstatus": se.docstatus,
		"items": [
			{
				"item_code": r.item_code,
				"item_name": r.item_name,
				"qty": r.qty,
				"basic_rate": float(r.basic_rate or 0),
				"amount": float(r.amount or 0),
				"uom": r.uom or r.stock_uom,
				"t_warehouse": r.t_warehouse,
			}
			for r in se.items
		],
	}


@frappe.whitelist()
def get_suppliers(query=""):
	"""Search suppliers by name."""
	filters = {"disabled": 0}
	or_filters = (
		[["supplier_name", "like", f"%{query}%"], ["name", "like", f"%{query}%"]]
		if query
		else None
	)
	return frappe.get_all(
		"Supplier",
		filters=filters,
		or_filters=or_filters,
		fields=["name", "supplier_name", "supplier_type"],
		order_by="modified desc",
		limit=50,
	)


@frappe.whitelist()
def create_supplier(supplier_name, supplier_type="Company"):
	"""Quick-create a supplier from POS purchase form."""
	doc = frappe.new_doc("Supplier")
	doc.supplier_name = supplier_name
	doc.supplier_type = supplier_type or "Company"
	doc.insert(ignore_permissions=True)
	return {"name": doc.name, "supplier_name": doc.supplier_name, "supplier_type": doc.supplier_type}


@frappe.whitelist()
def save_purchase_draft(supplier, items):
    """Create a draft Material Receipt Stock Entry without submitting."""
    if isinstance(items, str):
        items = frappe.parse_json(items)

    company = frappe.db.get_single_value("Global Defaults", "default_company")
    if not company:
        rows = frappe.get_all("Company", pluck="name", limit=1)
        company = rows[0] if rows else frappe.throw("No company configured")

    warehouse = _get_default_warehouse(company)
    if not warehouse:
        frappe.throw("No warehouse found for company.")

    se = frappe.new_doc("Stock Entry")
    se.company = company
    se.stock_entry_type = "Material Receipt"
    se.purpose = "Material Receipt"
    se.to_warehouse = warehouse
    se.supplier = supplier
    se.supplier_name = frappe.db.get_value("Supplier", supplier, "supplier_name") or supplier

    for row in items:
        se.append("items", {
            "item_code": row.get("item_code"),
            "qty": float(row.get("qty") or 1),
            "basic_rate": float(row.get("rate") or 0),
            "t_warehouse": warehouse,
        })

    se.insert(ignore_permissions=True)
    return {
        "name": se.name,
        "supplier": se.supplier,
        "supplier_name": se.supplier_name,
        "total_amount": float(se.total_amount or 0),
        "docstatus": se.docstatus,
        "posting_date": str(se.posting_date),
    }


@frappe.whitelist()
def submit_stock_entry(entry_name):
    """Submit a saved draft Stock Entry."""
    se = frappe.get_doc("Stock Entry", entry_name)
    if se.docstatus != 0:
        frappe.throw("Entry is not in Draft state.")
    se.submit()
    return {"name": se.name, "docstatus": se.docstatus}


@frappe.whitelist()
def create_purchase_entry(supplier, items):
	"""Create a Material Receipt Stock Entry with supplier for purchase tracking."""
	if isinstance(items, str):
		items = frappe.parse_json(items)

	company = frappe.db.get_single_value("Global Defaults", "default_company")
	if not company:
		rows = frappe.get_all("Company", pluck="name", limit=1)
		company = rows[0] if rows else frappe.throw("No company configured")

	warehouse = _get_default_warehouse(company)
	if not warehouse:
		frappe.throw("No warehouse found for company. Please create a warehouse first.")

	se = frappe.new_doc("Stock Entry")
	se.company = company
	se.stock_entry_type = "Material Receipt"
	se.purpose = "Material Receipt"
	se.to_warehouse = warehouse
	se.supplier = supplier
	se.supplier_name = frappe.db.get_value("Supplier", supplier, "supplier_name") or supplier

	for row in items:
		se.append(
			"items",
			{
				"item_code": row.get("item_code"),
				"qty": float(row.get("qty") or 1),
				"basic_rate": float(row.get("rate") or 0),
				"t_warehouse": warehouse,
			},
		)

	se.insert(ignore_permissions=True)
	se.submit()

	return {
		"name": se.name,
		"supplier": se.supplier,
		"supplier_name": se.supplier_name,
		"total_amount": float(se.total_amount or 0),
		"docstatus": se.docstatus,
		"posting_date": str(se.posting_date),
	}


def _get_default_warehouse(company):
	"""Return best available warehouse for the company."""
	wh = frappe.db.get_value("Company", company, "default_warehouse")
	if wh and not frappe.db.get_value("Warehouse", wh, "disabled"):
		return wh
	# fallback: first non-group, non-disabled warehouse for the company
	rows = frappe.get_all(
		"Warehouse",
		filters={"company": company, "is_group": 0, "disabled": 0},
		pluck="name",
		limit=1,
	)
	return rows[0] if rows else None


@frappe.whitelist()
def create_template_item(item_name, item_code=None, stock_uom="Meter", item_group="Products", attribute_name="Code"):
	"""Create a template parent item with has_variants=1."""
	code = item_code or item_name
	if frappe.db.exists("Item", code):
		frappe.throw(f"Item {code} already exists.")

	# Ensure Item Attribute exists
	if not frappe.db.exists("Item Attribute", attribute_name):
		attr_doc = frappe.new_doc("Item Attribute")
		attr_doc.attribute_name = attribute_name
		attr_doc.insert(ignore_permissions=True)

	doc = frappe.new_doc("Item")
	doc.item_code = code
	doc.item_name = item_name
	doc.item_group = item_group or "Products"
	doc.stock_uom = stock_uom or "Meter"
	doc.is_stock_item = 1
	doc.is_sales_item = 1
	doc.has_variants = 1
	doc.variant_based_on = "Item Attribute"
	doc.append("attributes", {"attribute": attribute_name})
	doc.insert(ignore_permissions=True)

	return {
		"item_code": doc.item_code,
		"item_name": doc.item_name,
		"stock_uom": doc.stock_uom,
	}


@frappe.whitelist()
def create_item_variant(template_item, variant_code, selling_price=None, attribute_value=None):
	"""Create a child variant item from an existing template item."""
	template = frappe.get_doc("Item", template_item)
	if not template.has_variants:
		frappe.throw(f"Item {template_item} is not a variant template.")

	full_code = f"{template.item_code}-{variant_code}"
	if frappe.db.exists("Item", full_code):
		frappe.throw(f"Variant item {full_code} already exists.")

	attr_name = template.attributes[0].attribute if template.attributes else "Code"
	val = attribute_value or variant_code

	# Ensure value exists in Item Attribute Value
	attr_doc = frappe.get_doc("Item Attribute", attr_name)
	existing_values = [v.attribute_value for v in attr_doc.item_attribute_values]
	if val not in existing_values:
		attr_doc.append("item_attribute_values", {"attribute_value": val, "abbr": val})
		attr_doc.save(ignore_permissions=True)

	variant = frappe.new_doc("Item")
	variant.item_code = full_code
	variant.item_name = full_code
	variant.item_group = template.item_group
	variant.stock_uom = template.stock_uom
	variant.is_stock_item = template.is_stock_item
	variant.is_sales_item = 1
	variant.has_variants = 0
	variant.variant_of = template.name
	variant.variant_based_on = "Item Attribute"
	variant.append("attributes", {"attribute": attr_name, "attribute_value": val})
	variant.insert(ignore_permissions=True)

	# If selling_price provided, create Item Price
	if selling_price:
		ip = frappe.new_doc("Item Price")
		ip.item_code = variant.item_code
		ip.price_list = frappe.db.get_single_value("Selling Settings", "selling_price_list") or "Standard Selling"
		ip.price_list_rate = float(selling_price)
		ip.selling = 1
		ip.insert(ignore_permissions=True)

	return {
		"item_code": variant.item_code,
		"item_name": variant.item_name,
		"variant_of": variant.variant_of,
		"stock_uom": variant.stock_uom,
		"selling_price": float(selling_price) if selling_price else None,
		"actual_qty": 0.0,
		"is_stock_item": variant.is_stock_item,
	}


@frappe.whitelist()
def update_item_price(item_code, rate):
	"""Update or create selling Item Price for a given item_code."""
	rate = float(rate)
	price_list = frappe.db.get_single_value("Selling Settings", "selling_price_list") or "Standard Selling"
	
	existing_ip = frappe.db.get_value(
		"Item Price",
		{"item_code": item_code, "price_list": price_list, "selling": 1},
		"name",
	)
	if existing_ip:
		ip = frappe.get_doc("Item Price", existing_ip)
		ip.price_list_rate = rate
		ip.save(ignore_permissions=True)
	else:
		ip = frappe.new_doc("Item Price")
		ip.item_code = item_code
		ip.price_list = price_list
		ip.price_list_rate = rate
		ip.selling = 1
		ip.insert(ignore_permissions=True)

	return {"item_code": item_code, "selling_price": rate}
