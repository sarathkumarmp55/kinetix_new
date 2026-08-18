# Copyright (c) 2026, sarath and contributors
# For license information, please see license.txt

# pyrefly: ignore [missing-import]
import frappe
# pyrefly: ignore [missing-import]
from frappe.utils import flt
# pyrefly: ignore [missing-import]
from frappe.model.document import Document


class PaymentApprovalLog(Document):
	def on_submit(self):
		if self.payment_status == "Approved":
			try:
				if self.from_opportunity ==1:
					try:
			
						student = frappe.get_doc({
							"doctype": "Student",
							"first_name": self.student_name,
							"custom_age": self.age,
							"custom_payment_approval_log":self.name,
							"student_name": self.student_name,
							"student_email_id": self.email_id,
							"student_mobile_number": self.mobile_number,
							"custom_program": self.program,
							"gender":self.gender,
							"custom_hostel": self.hostel,
							"custom_academic_year": self.academic_year,
							"custom_vehicle": self.vehicle,
							"custom_program_total_amount": self.total_amount,
							"custom_program_total_received_amount": self.fees_received_amount,
							"custom_program_balance_amount": self.total_amount - self.fees_received_amount,
							"custom_hostel_total_amount": self.hostel_total_amount,
							"custom_hostel_total_received_amount" : self.hostel_received_amount,
							"custom_hostel_balance_amount" : self.hostel_total_amount - self.hostel_received_amount,
							"custom_vehicle_total_amount": self.vehicle_total_amount,
							"custom_vehicle_total_received_amount": self.vehicle_received_amount,
							"custom_vehicle_balance_amount": self.vehicle_total_amount - self.vehicle_received_amount,

						})
						# Skip Student's validate_user() hook — it tries to create a Frappe User
						# which fails when no valid system email is present
						student.flags.ignore_validate = True
						student.flags.ignore_mandatory = True
						student.insert(ignore_permissions=True)

						# Save the generated Student ID back into this log
						frappe.db.set_value("Payment Approval Log", self.name, "student", student.name)
						# frappe.db.commit()

						# ERPNext Education auto-creates a Customer on Student insert
						# (Student.on_update -> create_customer). Reload to get the linked customer.
						student.reload()
						frappe.db.set_value("Student", student.name, "custom_student_customer", student.customer)
      
						invoice = frappe.get_doc({
							"doctype": "Sales Invoice",
							"student": student.name,
							"customer": student.customer,
							# "program": self.program,
							"custom_payment_approval_log":self.name,
							# "academic_year": self.academic_year
						})
						for row in self.fee_details + self.hostel_components + self.vehicle_components:
							invoice.append("items", {
								"item_code": row.components,
								"qty": 1,
								"rate": row.received_amount,
							})

			
			
						invoice.flags.ignore_permissions = True
						invoice.flags.ignore_mandatory = True
						invoice.insert(ignore_permissions=True)
						invoice.submit()

						invoice.reload()

						received_total = (
							flt(self.fees_received_amount)
							+ flt(self.hostel_received_amount)
							+ flt(self.vehicle_received_amount)
						)

						payment_entry = frappe.get_doc({
							"doctype": "Payment Entry",
							"payment_type": "Receive",
							"party_type": "Customer",
							"party": invoice.customer,
							"posting_date": self.date,
							"mode_of_payment": self.mode_of_payment,
							"paid_amount": received_total,
							"received_amount": received_total,
							"paid_from": invoice.debit_to,
							"paid_to": self.account_paid_to,
							"company": invoice.company,
							"reference_no": self.transaction_id,
							"reference_date": self.transaction_date,
							"custom_payment_approval_log": self.name,
							"student": student.name,
						})

						payment_entry.append("references", {
							"reference_doctype": "Sales Invoice",
							"reference_name": invoice.name,
							"total_amount": invoice.grand_total,
							"outstanding_amount": invoice.outstanding_amount,
							"allocated_amount": received_total,
						})

						payment_entry.flags.ignore_permissions = True
						payment_entry.flags.ignore_mandatory = True
						payment_entry.insert(ignore_permissions=True)
						payment_entry.submit()
			
			
      
      
      
      

					except Exception as e:
						frappe.log_error(
							message=frappe.get_traceback(),
							title="Payment Approval Log"
						)
						frappe.throw(
							f"Failed to create Student or Sales Invoice: {e}",
							title="Payment Approval Log"
						)



					frappe.msgprint(
						f" Student <b>{self.student_name}</b> has been successfully Created.",
						title="Records Created",
						indicator="green"
					)




				# /////////////////////////////////////////////////////////////////////////////////

				if self.from_student_service ==1:
					try:
			
						
      
						invoice = frappe.get_doc({
							"doctype": "Sales Invoice",
							"student": self.student_id,
							"customer": self.created_customer_id,
							"custom_payment_approval_log":self.name,
							
						})
						for row in self.fee_details + self.hostel_components + self.vehicle_components:
							invoice.append("items", {
								"item_code": row.components,
								"qty": 1,
								"rate": row.received_amount,
							})

			
			
						invoice.flags.ignore_permissions = True
						invoice.flags.ignore_mandatory = True
						invoice.insert(ignore_permissions=True)
						invoice.submit()

						invoice.reload()

						received_total = (
							flt(self.fees_received_amount)
							+ flt(self.hostel_received_amount)
							+ flt(self.vehicle_received_amount)
						)

						payment_entry = frappe.get_doc({
							"doctype": "Payment Entry",
							"payment_type": "Receive",
							"party_type": "Customer",
							"party": invoice.customer,
							"posting_date": self.date,
							"mode_of_payment": self.mode_of_payment,
							"paid_amount": received_total,
							"received_amount": received_total,
							"paid_from": invoice.debit_to,
							"paid_to": self.account_paid_to,
							"company": invoice.company,
							"reference_no": self.transaction_id,
							"reference_date": self.transaction_date,
							"custom_payment_approval_log": self.name,
							"student": self.student_id,
						})

						payment_entry.append("references", {
							"reference_doctype": "Sales Invoice",
							"reference_name": invoice.name,
							"total_amount": invoice.grand_total,
							"outstanding_amount": invoice.outstanding_amount,
							"allocated_amount": received_total,
						})

						payment_entry.flags.ignore_permissions = True
						payment_entry.flags.ignore_mandatory = True
						payment_entry.insert(ignore_permissions=True)
						payment_entry.submit()
			
			
      
      
      
      

					except Exception as e:
						frappe.log_error(
							message=frappe.get_traceback(),
							title="Payment Approval Log"
						)
						frappe.throw(
							f"Failed to create Student or Sales Invoice: {e}",
							title="Payment Approval Log"
						)



				frappe.msgprint(
					f" Payment has been Received from Student <b>{self.student_id}</b> ",
					title="Records Created",
					indicator="green"
				)









			except Exception as e:
				frappe.log_error(
					message=frappe.get_traceback(),
					title="Payment Approval Log"
				)
				frappe.throw(
					f"Payment Approval Log submission failed: {e}",
					title="Payment Approval Log"
				)
