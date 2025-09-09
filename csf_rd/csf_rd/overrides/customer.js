// Customer JavaScript overrides for DGII integration
frappe.ui.form.on('Customer', {
    refresh: function(frm) {
        // Add custom button for DGII validation
        if (frm.doc.tax_id) {
            frm.add_custom_button(__('Validate RNC'), function() {
                validate_rnc_with_dgii(frm);
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

function validate_rnc_with_dgii(frm) {
    if (!frm.doc.tax_id) {
        frappe.msgprint(__('Please enter Tax ID first'));
        return;
    }
    
    frappe.call({
        method: 'csf_rd.csf_rd.utils.dgii_utils.validate_rnc_with_dgii',
        args: {
            rnc: frm.doc.tax_id
        },
        callback: function(r) {
            if (r.message && r.message.success) {
                frappe.msgprint(__('RNC is valid'));
            } else {
                frappe.msgprint(__('RNC validation failed: ' + (r.message.error || 'Unknown error')));
            }
        }
    });
}
