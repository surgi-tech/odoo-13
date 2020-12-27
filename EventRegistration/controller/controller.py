import sys

from odoo import http,models
from odoo.http import request
from odoo.addons.website_event.controllers import main as main

class websiteventregistration(main.WebsiteEventController):


    @http.route(['/event/<model("event.event"):event>/registration/new'], type='json', auth="public", methods=['POST'], website=True)
    def registration_new(self, event, **post):
        contact=request.env['res.partner'].sudo().search([])
        hello="hellos"
        tickets = self._process_tickets_details(post)

        if not tickets:
            return False
        return request.env['ir.ui.view'].render_template("website_event.registration_attendee_details",{'contact': contact, 'tickets': tickets, 'event': event})

