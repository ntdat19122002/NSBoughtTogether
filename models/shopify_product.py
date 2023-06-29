from odoo import fields,models,api

class ShopifyProduct(models.Model):
    _name = 'shopify.product'

    shop_id = fields.Many2one('shopify.shop')
    title = fields.Char()
    image = fields.Char()
    variant = fields.One2many('shopify.variant', 'product')

