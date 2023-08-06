// Copyright (c) 2022, ERPCloud.Systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Customer Visit', {
	location: (frm) => {
        // console.log(JSON.parse(frm.doc.location))
        let coordinates = JSON.parse(cur_frm.doc.location).features.at(-1)
        if (coordinates && coordinates.geometry.type == "Point"){
            let long = coordinates.geometry.coordinates[0]
            let lat = coordinates.geometry.coordinates[1]
            console.log(long, lat)
            frm.set_value("longitude", long)
            frm.set_value("latitude", lat)
        }
    },
    onload: function(frm) {
		var posting_date = frm.doc.posting_date;
		var time = frm.doc.time;
        if(!frm.doc.amended_from) frm.set_value('posting_date', posting_date || frappe.datetime.get_today());
        if(!frm.doc.amended_from) frm.set_value('time', time || frappe.datetime.now_time());
	},
   
});

frappe.ui.form.on("Customer Visit", {
    setup: function(frm) {
        frm.set_query('customer_address', function(doc) {
			return {
				query: 'frappe.contacts.doctype.address.address.address_query',
				filters: {
					link_doctype: 'Customer',
					link_name: doc.customer
				}
			};
		});
	}
});
