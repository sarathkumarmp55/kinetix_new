frappe.ui.form.on("Payment Entry", {
	refresh: function (frm) {
		frm.add_custom_button(
			__("Get Datas from Payment Approval log"),
			function () {
				if (!frm.doc.custom_payment_approval_log) {
					frappe.msgprint(__("Please select a Payment Approval Log first."));
					return;
				}
				frappe.call({
					method: "frappe.client.get",
					args: {
						doctype: "Payment Approval Log",
						name: frm.doc.custom_payment_approval_log,
					},
					callback: function (r) {
						if (!r.message) {
							frappe.msgprint(__("Could not fetch the Payment Approval Log data."));
							return;
						}
						frm.set_value(
							"paid_amount",
							parseFloat(r.message.received_amount) || 0
						);
						frm.set_value("mode_of_payment", r.message.mode_of_payment);
						frm.set_value("reference_date", r.message.transaction_date);
						frm.set_value("reference_no", r.message.transaction_id);

						frappe.msgprint(__("Data fetched successfully from Payment Approval Log."));

						frm.page.remove_inner_button(
							__("Get Datas from Payment Approval log")
						);
					},
				});
			}
		);
	},
});
