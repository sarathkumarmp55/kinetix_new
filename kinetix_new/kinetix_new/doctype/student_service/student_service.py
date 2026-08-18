# Copyright (c) 2026, sarath and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class StudentService(Document):
	def before_submit(self):
		if self.student:
			student_values = {
				"custom_program_total_amount": self.program_total_amount,
				"custom_hostel_total_amount": self.hostel_total_amount_new,
				"custom_vehicle_total_amount": self.vehicle_total_amount_new,
				"custom_hostel": self.hostel,
				"custom_vehicle": self.vehicle
			}

			# If selected_hosted has no value
			if not self.selected_hosted:
				student_values.update({
					"custom_hostel_total_amount": self.hostel_total_amount,
					"custom_hostel_total_received_amount": self.hostel_received_amount,
					"custom_hostel_balance_amount": self.hostel_total_amount - self.hostel_received_amount
				})

			if self.selected_hosted:
				student_values.update({
					
					"custom_hostel_total_received_amount": self.hostel_total_amount_new - self.outstanding_amount_1,
					"custom_hostel_balance_amount": self.self.outstanding_amount_1
				})

			if not self.selected_vehicle:
				student_values.update({
					"custom_vehicle_total_amount": self.vehicle_total_amount,
					"custom_vehicle_total_received_amount": self.vehicle_received_amount,
					"custom_vehicle_balance_amount": self.vehicle_total_amount - self.vehicle_received_amount
				})

			if self.selected_vehicle:
				student_values.update({
					
					"custom_vehicle_total_received_amount": self.vehicle_total_amount_new - self.outstanding_amount_2,
					"custom_vehicle_balance_amount": self.vehicle_total_amount_new - self.outstanding_amount_2
				})
			if self.selected_program:
				student_values.update({
					"custom_program_total_received_amount": self.program_total_amount - self.outstanding_amount,
					"custom_program_balance_amount": self.outstanding_amount
				})


			frappe.db.set_value(
				"Student",
				self.student,
				student_values
			)

	def on_submit(self):
		log = frappe.new_doc("Payment Approval Log")
		log.from_student_service = 1
		log.student_id = self.student
		log.date = frappe.utils.today()
		log.transaction_id = self.transaction_id
		log.transaction_date = self.transaction_date
		log.mode_of_payment = self.mode_of_payement
		log.attach = self.attach
		log.account_paid_to = self.account_paid_to
		log.student_service_id = self.name

		if self.fees == 1:
			log.fees = 1
			log.program = self.program
			log.fees_received_amount = self.received_amount
			log.total_amount = self.total_amount
			for row in self.fees_components:
				log.append("fee_details", {
					"components": row.components,
					"amount": row.amount,
					"received_amount": row.received_amount
				})

		if self.hostel_required == 1:
			log.hostel_required = 1
			log.hostel = self.hostel
			log.hostel_total_amount = self.hostel_total_amount
			log.hostel_received_amount = self.hostel_received_amount
			for row in self.hostel_components:
				log.append("hostel_components", {
					"components": row.components,
					"amount": row.amount,
					"received_amount": row.received_amount
				})

		if self.vehicle_required == 1:
			log.vehicle_required = 1
			log.vehicle = self.vehicle
			log.vehicle_total_amount = self.vehicle_total_amount
			log.vehicle_received_amount = self.vehicle_received_amount
			for row in self.vehicle_components:
				log.append("vehicle_components", {
					"components": row.components,
					"amount": row.amount,
					"received_amount": row.received_amount
				})	

		log.insert(ignore_permissions=True)
