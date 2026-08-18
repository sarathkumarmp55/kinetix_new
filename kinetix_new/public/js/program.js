
frappe.ui.form.on("Program", {
    refresh(frm) {
        calculate_total_amount(frm);
    }
});

frappe.ui.form.on("Fees Details", {
    amount(frm) {
        calculate_total_amount(frm);
    },
    custom_fees_details_remove(frm) {
        calculate_total_amount(frm);
    }
});

function calculate_total_amount(frm) {
    let total = 0;
    (frm.doc.custom_fees_details || []).forEach((row) => {
        total += flt(row.amount);
    });
    frm.set_value("custom_total_amount", total);
}
