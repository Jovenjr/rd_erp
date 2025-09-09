from . import __version__ as app_version

app_name = "csf_rd"
app_title = "República Dominicana ERPNext Customization"
app_publisher = "CSF RD Team"
app_description = (
    "ERPNext Country Specific Customizations for República Dominicana - DGII Integration"
)
app_icon = "drag"
app_color = "blue"
app_email = "support@csf-rd.com"
app_license = "GNU General Public License (v3)"
required_apps = ["erpnext"]

fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [               
            ["is_system_generated", "=", 0],
            ["module", "=", "CSF RD"],
        ],
    },
    {
        "doctype": "DocType Link",
        "filters": [
            [
                "link_doctype",
                "in",
                ("DGII Customer", "eCF Document"),
            ]
        ],
    },
]

# DocType JavaScript overrides
doctype_js = {
    "Customer": "csf_rd/overrides/customer.js",
    "Sales Invoice": "csf_rd/overrides/sales_invoice.js"
}

# Document Events
doc_events = {
    "Sales Invoice": {
        "on_submit": "csf_rd.doctype.ecf_document.ecf_document.send_to_dgii",
        "before_save": "csf_rd.overrides.sales_invoice.validate_rnc_format"
    },
    "Customer": {
        "before_save": "csf_rd.overrides.customer.validate_rnc_format"
    },
    "Supplier": {
        "before_save": "csf_rd.overrides.supplier.validate_rnc_format"
    },
}

# Jinja methods
jinja = {
    "methods": [
        "csf_rd.utils.qr_code_generator.generate_ecf_qr_code",
        "csf_rd.utils.dgii_utils.format_rnc"
    ]
}

# NO override_doctype_class - Usar controladores estándar de Frappe