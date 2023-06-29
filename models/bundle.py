from odoo import fields,models,api
from odoo.exceptions import ValidationError


class ShopifyProduct(models.Model):
    _name = 'shopify.bundle'

    shop_id = fields.Many2one('shopify.shop')
    title = fields.Char()
    description = fields.Char()
    enable = fields.Boolean(default=True)
    excluded_variant_ids = fields.Many2many('shopify.variant','excluded_bundle_variant_res')
    variant_ids = fields.Many2many('shopify.variant','bundle_variant_res')
    total_price = fields.Float(compute='_compute_total_price')

    setting_id = fields.Many2one('bundle.setting')

    @api.depends("variant_ids")
    def _compute_total_price(self):
        for record in self:
            total = 0
            for variant in record.variant_ids:
                total += variant.price
            record.total_price = total