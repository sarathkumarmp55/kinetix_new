frappe.ui.form.on("Student", {
	refresh(frm) {
		render_student_dashboard(frm);
	}
});

function render_student_dashboard(frm) {
	const control = frm.fields_dict.custom_student_dashboard;
	if (!control) {
		return;
	}

	const d = frm.doc;
	const esc = (v) => frappe.utils.escape_html(v || "");
	const currency = frappe.defaults.get_default("currency") || "INR";
	const sections = [
		{
			label: "Program",
			value: d.custom_program,
			total: flt(d.custom_program_total_amount),
			received: flt(d.custom_program_total_received_amount),
			balance: flt(d.custom_program_balance_amount),
			letter: "P",
			color: "#2563eb"
		},
		{
			label: "Hostel",
			value: d.custom_hostel,
			total: flt(d.custom_hostel_total_amount),
			received: flt(d.custom_hostel_total_received_amount),
			balance: flt(d.custom_hostel_balance_amount),
			letter: "H",
			color: "#ed3a3a"
		},
		{
			label: "Vehicle",
			value: d.custom_vehicle,
			total: flt(d.custom_vehicle_total_amount),
			received: flt(d.custom_vehicle_total_received_amount),
			balance: flt(d.custom_vehicle_balance_amount),
			letter: "V",
			color: "#1bd906"
		}
	];

	const cards = sections
		.map((s) => {
			const pct = Math.max(0, Math.min(100, s.total > 0 ? (s.received / s.total) * 100 : 0));
			return `
			<div style="background:#fff;border:1px solid #e5e7eb;border-radius:14px;overflow:hidden;box-shadow:0 1px 2px rgba(17,24,39,.06);">
				<div style="height:5px;background:${s.color};"></div>
				<div style="padding:18px 20px 20px;">
					<div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;">
						<div style="width:40px;height:40px;border-radius:10px;background:${s.color}1a;color:${s.color};display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:800;">${s.letter}</div>
						<div style="min-width:0;">
							<div style="font-size:11px;letter-spacing:.6px;text-transform:uppercase;color:#6b7280;font-weight:700;">${s.label}</div>
							<div style="font-size:14px;color:#111827;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${s.value ? esc(s.value) : "—"}</div>
						</div>
					</div>
					<div style="font-size:11px;color:#6b7280;margin-bottom:4px;">Total Amount</div>
					<div style="font-size:22px;font-weight:800;color:#111827;font-variant-numeric:tabular-nums;margin-bottom:12px;">${format_currency(s.total, currency)}</div>
					<div style="height:8px;background:#eef2f7;border-radius:999px;overflow:hidden;margin-bottom:6px;">
						<div style="height:100%;width:${pct}%;background:${s.color};border-radius:999px;"></div>
					</div>
					<div style="font-size:11px;color:#6b7280;margin-bottom:14px;">${pct.toFixed(0)}% received</div>
					<div style="display:flex;justify-content:space-between;gap:8px;border-top:1px solid #f1f5f9;padding-top:14px;">
						<div style="min-width:0;">
							<div style="display:flex;align-items:center;gap:6px;font-size:11px;color:#6b7280;margin-bottom:2px;">
								<span style="width:8px;height:8px;border-radius:999px;background:#059669;flex-shrink:0;"></span>Received
							</div>
							<div style="font-size:14px;font-weight:700;color:#047857;font-variant-numeric:tabular-nums;white-space:nowrap;">${format_currency(s.received, currency)}</div>
						</div>
						<div style="min-width:0;text-align:right;">
							<div style="display:flex;align-items:center;justify-content:flex-end;gap:6px;font-size:11px;color:#6b7280;margin-bottom:2px;">
								<span style="width:8px;height:8px;border-radius:999px;background:#d97706;flex-shrink:0;"></span>Balance
							</div>
							<div style="font-size:14px;font-weight:700;color:#b45309;font-variant-numeric:tabular-nums;white-space:nowrap;">${format_currency(s.balance, currency)}</div>
						</div>
					</div>
				</div>
			</div>`;
		})
		.join("");

	const html = `
	<div style="font-family:'Inter','Segoe UI',system-ui,-apple-system,sans-serif;color:#111827;line-height:1.4;">
		<div style="display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:16px;">
			<div>
				<div style="font-size:18px;font-weight:800;letter-spacing:-.2px;">Student Fee Dashboard</div>
				<div style="font-size:12px;color:#6b7280;">Fee, hostel and vehicle summary at a glance</div>
			</div>
			<div style="background:#eff6ff;color:#1d4ed8;font-size:12px;font-weight:700;padding:6px 12px;border-radius:999px;white-space:nowrap;">Academic Year: ${d.custom_academic_year ? esc(d.custom_academic_year) : "—"}</div>
		</div>
		<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:16px;">${cards}</div>
	</div>`;

	control.html(html);
}
