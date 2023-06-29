from odoo import models,fields

class ShopifyVariant(models.Model):
    _name = 'shopify.variant'

    shopify_id = fields.Char()
    product = fields.Many2one('shopify.product')
    title = fields.Char()
    price = fields.Float()
    compare_at_price = fields.Float()
    inventory = fields.Integer()
    bundle_id = fields.Many2one('shopify.bundle')