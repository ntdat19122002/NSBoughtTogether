import werkzeug

import odoo
from odoo import http
import json
import logging
from odoo.addons.portal.controllers.portal import  CustomerPortal
class CustomerPortal(CustomerPortal):

    @odoo.http.route()
    def home(self):
        return werkzeug.utils.redirect('/app/bought_together')