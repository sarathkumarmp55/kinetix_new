# Copyright (c) 2026, sarath and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class StudentService(Document):
	# def before_submit(self):
	# 	if self.student:
	# 		student_values = {
	# 			"custom_program_total_amount": self.program_total_amount,
	# 			"custom_hostel_total_amount": self.hostel_total_amount_new,
	# 			"custom_vehicle_total_amount": self.vehicle_total_amount_new,
	# 			"custom_hostel": self.hostel,
	# 			"custom_vehicle": self.vehicle
	# 		}

	# 		# If selected_hosted has no value
	# 		if not self.selected_hosted:
	# 			student_values.update({
	# 				"custom_hostel_total_amount": self.hostel_total_amount,
	# 				"custom_hostel_total_received_amount": self.hostel_received_amount,
	# 				"custom_hostel_balance_amount": self.hostel_total_amount - self.hostel_received_amount
	# 			})

	# 		if self.selected_hosted:
	# 			student_values.update({
					
	# 				"custom_hostel_total_received_amount": self.hostel_total_amount_new - self.outstanding_amount_1,
	# 				"custom_hostel_balance_amount": self.self.outstanding_amount_1
	# 			})

	# 		if not self.selected_vehicle:
	# 			student_values.update({
	# 				"custom_vehicle_total_amount": self.vehicle_total_amount,
	# 				"custom_vehicle_total_received_amount": self.vehicle_received_amount,
	# 				"custom_vehicle_balance_amount": self.vehicle_total_amount - self.vehicle_received_amount
	# 			})

	# 		if self.selected_vehicle:
	# 			student_values.update({
					
	# 				"custom_vehicle_total_received_amount": self.vehicle_total_amount_new - self.outstanding_amount_2,
	# 				"custom_vehicle_balance_amount": self.vehicle_total_amount_new - self.outstanding_amount_2
	# 			})
	# 		if self.selected_program:
	# 			student_values.update({
	# 				"custom_program_total_received_amount": self.program_total_amount - self.outstanding_amount,
	# 				"custom_program_balance_amount": self.outstanding_amount
	# 			})


	# 		frappe.db.set_value(
	# 			"Student",
	# 			self.student,
	# 			student_values
	# 		)



	def before_submit(self):
		if self.add_discount and not self.approved:
			frappe.throw(
				"Cannot submit Student Service. Discount approval is pending."
			)

		if not self.student:
			return

		student_values = {
			"custom_program_total_amount": self.program_total_amount,
			"custom_hostel_total_amount": self.hostel_total_amount_new,
			"custom_vehicle_total_amount": self.vehicle_total_amount_new,
			"custom_hostel": self.hostel,
			"custom_vehicle": self.vehicle,
		}

		# -------------------------
		# HOSTEL
		# -------------------------
		if not self.selected_hosted:
			hostel_total = self.hostel_total_amount or 0
			hostel_received = self.hostel_received_amount or 0
			hostel_balance = hostel_total - hostel_received

			student_values.update({
				"custom_hostel_total_amount": hostel_total,
				"custom_hostel_total_received_amount": hostel_received,
				"custom_hostel_balance_amount": hostel_balance,
			})

		else:
      
			if self.hostel_required == 1:
      
		
				hostel_total = self.hostel_total_amount_new or 0
				hostel_balance = self.outstanding_amount_1 or 0
				hostel_received = hostel_total - hostel_balance

				student_values.update({
					"custom_hostel_total_amount": hostel_total,
					"custom_hostel_total_received_amount": hostel_received,
					"custom_hostel_balance_amount": hostel_balance,
					"custom_vehicle": self.selected_vehicle
				})

		# -------------------------
		# VEHICLE
		# -------------------------
		if not self.selected_vehicle:
			vehicle_total = self.vehicle_total_amount or 0
			vehicle_received = self.vehicle_received_amount or 0
			vehicle_balance = vehicle_total - vehicle_received

			student_values.update({
				"custom_vehicle_total_amount": vehicle_total,
				"custom_vehicle_total_received_amount": vehicle_received,
				"custom_vehicle_balance_amount": vehicle_balance,
			})

		else:
			if self.vehicle_required == 1:
      
		
				vehicle_total = self.vehicle_total_amount_new or 0
				vehicle_balance = self.outstanding_amount_2 or 0
				vehicle_received = vehicle_total - vehicle_balance

				student_values.update({
					"custom_vehicle_total_amount": vehicle_total,
					"custom_vehicle_total_received_amount": vehicle_received,
					"custom_vehicle_balance_amount": vehicle_balance,
					"custom_hostel": self.selected_hosted,

				})

		# -------------------------
		# PROGRAM
		# -------------------------
		if self.fees == 1:
			program_total = self.program_total_amount or 0
			program_balance = self.outstanding_amount or 0
			program_received = program_total - program_balance

			student_values.update({
				"custom_program_total_received_amount": program_received,
				"custom_program_balance_amount": program_balance,
				"custom_hostel": self.selected_hosted,
				"custom_vehicle": self.selected_vehicle
    
			})

		# -------------------------
		# UPDATE STUDENT
		# -------------------------
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
