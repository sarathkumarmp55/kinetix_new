
frappe.ui.form.on("Lead", {
    refresh(frm) {
        // Hide "Customer" from the "Create" group button
        setTimeout(() => {
            frm.remove_custom_button(__("Customer"), __("Create"));
            frm.remove_custom_button(__("Prospect"), __("Create"));
            frm.remove_custom_button(__("Quotation"), __("Create"));
            frm.remove_custom_button(__("Add to Prospect"), __("Action"));
        }, 200);

    },
    custom_connected_status(frm) {
        if (frm.doc.custom_connected_status === "Interested") {
            frm.set_value("status", "Qualified");
            frm.save();

        }
        if (frm.doc.custom_connected_status === "Call Back Requested") {
            frm.set_value("status", "Schedule Callback");
            frm.save();

        }
        if (frm.doc.custom_connected_status === "Follow-up Scheduled") {
            frm.set_value("status", "Set Reminder");
            frm.save();

        }
        if (frm.doc.custom_connected_status === "Parent Not Available") {
            frm.set_value("status", "Follow-up");
            frm.save();

        }
        if (frm.doc.custom_connected_status === "Student Not Available") {
            frm.set_value("status", "Follow-up");
            frm.save();

        }
        if (frm.doc.custom_connected_status === "Course Details Shared") {
            frm.set_value("status", "Follow-up");
            frm.save();

        }
        if (frm.doc.custom_connected_status === "Fee Details Shared") {
            frm.set_value("status", "Follow-up");
            frm.save();

        }
        if (frm.doc.custom_connected_status === "Scholarship Discussion") {
            frm.set_value("status", "Manager Approval");
            frm.save();

        }
        if (frm.doc.custom_connected_status === "Demo Class Scheduled") {
            frm.set_value("status", "Opportunity");
            frm.save();

        }
        if (frm.doc.custom_connected_status === "Branch Visit Scheduled") {
            frm.set_value("status", "Opportunity");
            frm.save();

        }
        if (frm.doc.custom_connected_status === "Payment Pending") {
            frm.set_value("status", "Opportunity");
            frm.save();

        }
        if (frm.doc.custom_connected_status === "Admission Confirmed") {
            frm.set_value("status", "Payment Done");
            frm.save();

        }
        if (frm.doc.custom_connected_status === "Not Interested") {
            frm.set_value("status", "Disqualified");
            frm.save();

        }
        if (frm.doc.custom_connected_status === "") {
            frm.set_value("status", "Lead");
            frm.save();

        }
    },
    custom_call_status(frm) {
        if (frm.doc.custom_call_status === "Wrong Number") {
            frm.set_value("status", "Invalid");
            frm.save();

        }
        if (frm.doc.custom_call_status === "Language Barrier") {
            frm.set_value("status", "Reassign");
            frm.save();

        }
        if (frm.doc.custom_call_status === "Job Enquiry") {
            frm.set_value("status", "Close Lead");
            frm.save();

        }
        if (frm.doc.custom_call_status === "Charity Enquiry") {
            frm.set_value("status", "Close Lead");
            frm.save();

        }
        if (frm.doc.custom_call_status === "Marketing Call") {
            frm.set_value("status", "Close Lead");
            frm.save();

        }
        if (frm.doc.custom_call_status === "Did Not Pick") {
            frm.set_value("status", "Did Not Pick");
            frm.save();

        }
        if (frm.doc.custom_call_status === "Lead Ownership") {
            frm.set_value("status", "Lead");
            frm.save();

        }
        if (frm.doc.custom_call_status === "Disqualified") {
            frm.set_value("status", "Disqualified");
            frm.save();

        }
    }
});

