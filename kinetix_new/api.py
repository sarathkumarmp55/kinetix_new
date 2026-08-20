# pyrefly: ignore [missing-import]
import frappe

@frappe.whitelist()
def create_payment_approval_log(opportunity_name, party_name):

    opportunity = frappe.get_doc("Opportunity", opportunity_name)
    lead_name = frappe.db.get_value("Lead", party_name, "lead_name")
    lead_age = frappe.db.get_value("Lead", party_name, "custom_age")
    lead_custom_course_categories = frappe.db.get_value("Lead", party_name, "custom_course_categories")
    lead_custom_board = frappe.db.get_value("Lead", party_name, "custom_board")
    lead_gender = frappe.db.get_value("Lead", party_name, "gender")
    lead_email_id = frappe.db.get_value("Lead", party_name, "email_id")
    lead_class = frappe.db.get_value("Lead", party_name, "custom_class")
    lead_mobile_no = frappe.db.get_value("Lead", party_name, "mobile_no")

    log = frappe.get_doc({
        "doctype": "Payment Approval Log",
        "lead_reference": party_name,
        "opportunity_reference": opportunity.name,
        "student_name": lead_name,
        "age": lead_age,
        "course_category": lead_custom_course_categories,
        "board": lead_custom_board,
        "gender": lead_gender,
        "email_id": lead_email_id,
        "location": opportunity.custom_location,
        # "transaction_date": opportunity.custom_payment_date,
        "transaction_id": opportunity.custom_transaction_id,
        "academic_year": opportunity.custom_academic_year,
        "mode_of_payment": opportunity.custom_mode_of_payment,
        "account_paid_to": opportunity.custom_account_paid_to,
        "class": lead_class,
        "mobile_number": lead_mobile_no,
        "date": frappe.utils.today(),
        "from_opportunity": 1,
    })

    if opportunity.custom_fees == 1:
        log.fees = 1
        log.program = opportunity.custom_program
        log.fees_received_amount = opportunity.custom_program_received_amount
        log.total_amount = opportunity.custom_program_total_amount
        for row in opportunity.custom_fees_details:
            log.append("fee_details", {
                "components": row.components,
                "amount": row.amount,
                "received_amount": row.received_amount
            })

    if opportunity.custom_hostel_required == 1:
        log.hostel_required = 1
        log.hostel = opportunity.custom_hostel
        log.hostel_total_amount = opportunity.custom_hostel_total_amount
        log.hostel_received_amount = opportunity.custom_hostel_received_amount
        for row in opportunity.custom_hostel_components:
            log.append("hostel_components", {
                "components": row.components,
                "amount": row.amount,
                "received_amount": row.received_amount
            })

    if opportunity.custom_vehicle_required == 1:
        log.vehicle_required = 1
        log.vehicle = opportunity.custom_vehicle
        log.vehicle_total_amount = opportunity.custom_vehicle_total_amount
        log.vehicle_received_amount = opportunity.custom_vehicle_received_amount
        for row in opportunity.custom_vehicle_components:
            log.append("vehicle_components", {
                "components": row.components,
                "amount": row.amount,
                "received_amount": row.received_amount
            })

    log.insert(ignore_permissions=True)

    frappe.db.set_value(
        "Opportunity",
        opportunity.name,
        "status",
        "Payment Approval Pending"
    )

    frappe.db.commit()

    return log.name
