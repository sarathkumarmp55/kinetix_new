# kinetix_new app

- Site: `kinetix_new.com` (bench at `/home/user/frappe-benchA15`, apps install via `sites/apps.txt`; kinetix_new not yet in apps.txt, list via `bench --site kinetix_new.com list-apps` shows it installed).
- Wire Program doctype JS via `doctype_js` in `kinetix_new/hooks.py` -> `public/js/program.js`.
- Program doctype custom fields: child table `custom_fees_details` (Table -> "Fees Details") with `component`+`amount`, and Currency `custom_total_amount`. Sum of child `amount` is written to `custom_total_amount` from `public/js/program.js`.
- Child table removal event name is `<child_field>_remove`, i.e. `custom_fees_details_remove`.
