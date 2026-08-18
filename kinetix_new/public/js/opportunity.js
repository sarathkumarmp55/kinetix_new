
frappe.ui.form.on("Opportunity", {
    refresh(frm) {
        
        calculate_total_amount(frm);
        calculate_total_received_amount(frm);
        calculate_total_amount_vehicle(frm);
        calculate_total_received_amount_vehicle(frm);
        calculate_total_received_amount_pgm(frm)
        calculate_program_total_amount(frm)
    

        // Hide "Customer" from the "Create" group button
        setTimeout(() => {
            frm.remove_custom_button(__("Supplier Quotation"), __("Create"));
            frm.remove_custom_button(__("Request For Quotation"), __("Create"));
            frm.remove_custom_button(__("Quotation"), __("Create"));
            frm.remove_custom_button(__("Customer"), __("Create"));
            // frm.remove_custom_button(__("Add to Prospect"), __("Action"));
        }, 200);




        // Only show the button if a Payment Approval Log hasn't been created yet
        if (!frm.is_new()) {
            if (frm.doc.status !== "Payment Approval Pending") {
                frm.add_custom_button(__("Payment Approval"), function () {
                    frappe.call({
                        method: "kinetix_new.api.create_payment_approval_log",
                        args: {
                            opportunity_name: frm.doc.name,
                            party_name: frm.doc.party_name
                        },
                        callback: function (r) {
                            if (!r.exc) {
                                // Remove the button immediately so it can't be clicked again
                                frm.remove_custom_button(__("Payment Approval"));

                                // Reflect DB status on the form without making it dirty
                                frm.doc.status = "Payment Approval Pending";
                                frm.refresh_field("status");

                                frappe.msgprint({
                                    title: __("Success"),
                                    message: __("Payment Approval Log created successfully"),
                                    indicator: "green"
                                });
                            }
                        }
                    });
                });
            }
        }
    },
    custom_mode_of_payment: function (frm) {
        if (frm.doc.custom_mode_of_payment) {
            frappe.db.get_doc("Mode of Payment", frm.doc.custom_mode_of_payment)
                .then((doc) => {
                    if (doc.accounts && doc.accounts.length > 0) {
                        frm.set_value(
                            "custom_account_paid_to",
                            doc.accounts[0].default_account
                        );
                    }
                });
        }
    },
    custom_program: function (frm) {
        if (!frm.doc.custom_program) {
            frm.set_value("custom_fees_details", []);
            return;
        }

        frappe.db.get_doc("Program", frm.doc.custom_program)
            .then((doc) => {
                const components = (doc.custom_fees_details || []).map((row) => ({
                    components: row.component,
                    amount: row.amount
                }));
                frm.set_value("custom_fees_details", components);
                calculate_program_total_amount(frm);
            });
    },


    custom_hostel: function (frm) {
        if (!frm.doc.custom_hostel) {
            frm.set_value("custom_hostel_components", []);
            return;
        }

        frappe.db.get_doc("Hostel", frm.doc.custom_hostel)
            .then((doc) => {
                const components = (doc.details || []).map((row) => ({
                    components: row.components,
                    amount: row.amount
                }));
                frm.set_value("custom_hostel_components", components);
                calculate_total_amount(frm);
            });
    },
    custom_vehicle: function(frm){
        if (!frm.doc.custom_vehicle) {
            frm.set_value("custom_vehicle_components", []);
            return;
        }

        frappe.db.get_doc("Vehicle Fee", frm.doc.custom_vehicle)
            .then((doc) => {
                const components = (doc.details || []).map((row) => ({
                    components: row.components,
                    amount: row.amount
                }));
                frm.set_value("custom_vehicle_components", components);
                calculate_total_amount_vehicle(frm);
            });


    },
    custom_received_amount: function (frm) {
        if (frm.doc.custom_received_amount) {

            frm.set_value(
                "custom_balance",
                frm.doc.custom_total_amount - frm.doc.custom_received_amount
            );
        }
    },
    custom_fee_structure: function(frm) {
        if (!frm.doc.custom_fee_structure) {
            frm.set_value("custom_fee_schedule", "");
            return;
        }
    
        frappe.db.get_list("Fee Schedule", {
            filters: {
                fee_structure: frm.doc.custom_fee_structure
            },
            fields: ["name"],
            order_by: "modified desc",
            limit: 1
        }).then((r) => {
            if (r.length) {
                frm.set_value("custom_fee_schedule", r[0].name);
            } else {
                frm.set_value("custom_fee_schedule", "");
                frappe.msgprint(__("No Fee Schedule found for the selected Fee Structure."));
            }
        });
    }
});



frappe.ui.form.on("Hostel Fee Details", {
    amount(frm) {
        calculate_total_amount(frm);
        calculate_total_amount_vehicle(frm);
    },
    custom_hostel_components_remove(frm) {

        calculate_total_amount(frm);
        
        calculate_total_received_amount(frm);
       
        

    },
    custom_fees_details_remove(frm) {
        
        calculate_total_received_amount_pgm(frm)
        calculate_program_total_amount(frm)
    },

    custom_vehicle_components_remove(frm){
            calculate_total_amount_vehicle(frm);
             calculate_total_received_amount_vehicle(frm);
    },


    received_amount: function (frm) {
        calculate_total_received_amount(frm);
        calculate_total_received_amount_vehicle(frm);
        calculate_total_received_amount_pgm(frm)
    }
});

function calculate_total_amount(frm) {
    let total = 0;
    (frm.doc.custom_hostel_components || []).forEach((row) => {
        total += flt(row.amount);
    });
    frm.set_value("custom_hostel_total_amount", total);
}

function calculate_total_received_amount(frm) {
    let total_2 = 0;
    (frm.doc.custom_hostel_components || []).forEach((row) => {
        total_2 += flt(row.received_amount);
    });
    frm.set_value("custom_hostel_received_amount", total_2);
}


function calculate_total_amount_vehicle(frm) {
    let total = 0;
    (frm.doc.custom_vehicle_components || []).forEach((row) => {
        total += flt(row.amount);
    });
    frm.set_value("custom_vehicle_total_amount", total);
}

function calculate_total_received_amount_vehicle(frm) {
    let total_2 = 0;
    (frm.doc.custom_vehicle_components || []).forEach((row) => {
        total_2 += flt(row.received_amount);
    });
    frm.set_value("custom_vehicle_received_amount", total_2);
}

function calculate_program_total_amount(frm) {
    let total = 0;
    (frm.doc.custom_fees_details || []).forEach((row) => {
        total += flt(row.amount);
    });
    frm.set_value("custom_program_total_amount", total);
}



function calculate_total_received_amount_pgm(frm) {
    let total_2 = 0;
    (frm.doc.custom_fees_details || []).forEach((row) => {
        total_2 += flt(row.received_amount);
    });
    frm.set_value("custom_program_received_amount", total_2);
}


