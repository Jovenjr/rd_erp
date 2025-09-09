// Sales Invoice JavaScript overrides for DGII integration
frappe.ui.form.on('Sales Invoice', {
    refresh: function(frm) {
        // Add custom buttons for DGII operations
        if (frm.doc.docstatus === 1 && frm.doc.tax_id) { // Submitted and has RNC
            frm.add_custom_button(__('Send to DGII'), function() {
                send_invoice_to_dgii(frm);
            }, __('DGII'));
            
            frm.add_custom_button(__('Check DGII Status'), function() {
                check_dgii_status(frm);
            }, __('DGII'));
            
            frm.add_custom_button(__('Generate QR Code'), function() {
                generate_qr_code(frm);
            }, __('DGII'));
        }
    },
    
    tax_id: function(frm) {
        // Auto-format RNC when typing
        if (frm.doc.tax_id) {
            let rnc = frm.doc.tax_id.replace(/-/g, '');
            if (/^\d{9}$|^\d{11}$/.test(rnc)) {
                frm.set_value('tax_id', rnc);
            }
        }
    }
});

function send_invoice_to_dgii(frm) {
    frappe.call({
        method: 'csf_rd.csf_rd.doctype.ecf_document.ecf_document.send_invoice_to_dgii',
        args: {
            sales_invoice: frm.doc.name
        },
        callback: function(r) {
            if (r.message && r.message.success) {
                frappe.msgprint(__('Invoice sent to DGII successfully'));
                frm.reload_doc();
            } else {
                frappe.msgprint(__('Error sending to DGII: ' + (r.message.error || 'Unknown error')));
            }
        }
    });
}

function check_dgii_status(frm) {
    frappe.call({
        method: 'csf_rd.csf_rd.doctype.ecf_document.ecf_document.check_invoice_dgii_status',
        args: {
            sales_invoice: frm.doc.name
        },
        callback: function(r) {
            if (r.message && r.message.success) {
                frappe.msgprint(__('DGII Status: ' + r.message.status));
                frm.reload_doc();
            } else {
                frappe.msgprint(__('Error checking DGII status: ' + (r.message.error || 'Unknown error')));
            }
        }
    });
}

function generate_qr_code(frm) {
    frappe.call({
        method: 'csf_rd.csf_rd.doctype.ecf_document.ecf_document.generate_invoice_qr_code',
        args: {
            sales_invoice: frm.doc.name
        },
        callback: function(r) {
            if (r.message && r.message.success) {
                frappe.msgprint(__('QR Code generated successfully'));
                if (r.message.qr_url) {
                    // Show QR code in a dialog
                    show_qr_code_dialog(r.message.qr_url);
                }
            } else {
                frappe.msgprint(__('Error generating QR code: ' + (r.message.error || 'Unknown error')));
            }
        }
    });
}

function show_qr_code_dialog(qr_url) {
    let d = new frappe.ui.Dialog({
        title: __('QR Code'),
        fields: [
            {
                fieldtype: 'HTML',
                fieldname: 'qr_code_html',
                options: `<div style="text-align: center;"><img src="${qr_url}" style="max-width: 300px; max-height: 300px;"></div>`
            }
        ],
        primary_action_label: __('Close'),
        primary_action: function() {
            d.hide();
        }
    });
    d.show();
}
