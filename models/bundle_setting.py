from odoo import models,fields

class BundleSetting(models.Model):
    _name = 'bundle.setting'

    bundle_id = fields.Many2one('shopify.bundle')
    title_font = fields.Integer()
    title_color = fields.Char()
    description_color = fields.Char()
    description_font = fields.Integer()
    button_text = fields.Char()
    button_text_color = fields.Char()
    button_background_color = fields.Char()
    button_border_color = fields.Char()

