import shopify

from odoo import fields, models, api


class ShopifyShop(models.Model):
    _name = 'shopify.shop'

    user_id = fields.Many2one('res.user')
    shop_url = fields.Char()
    currency_code = fields.Char()
    country = fields.Char()
    email = fields.Char()
    token = fields.Char()

    # Todo: Bổ xung thêm trường is_update_script_tag để phục vụ việc script tag

    def fetch_products(self):
        products = shopify.Product.find()
        for product in products:
            product_created = self.env['shopify.product'].sudo().create({
                'shop_id': self.id,
                'title': product.title,
                'image': product.attributes['image'].attributes['src']
            })
            for variant in product.variants:
                self.env['shopify.variant'].sudo().create({
                    'shopify_id': variant.id,
                    'product': product_created.id,
                    'title': variant.title,
                    'price': variant.price,
                    'compare_at_price': variant.compare_at_price,
                    'inventory': variant.inventory_quantity
                })

    def fetch_orders(self):
        orders = shopify.Order.find()
        for order in orders:
            self.env['shopify.product'].sudo().create({
                'shopify_id': self.id,
                'id': orders.id
            })

    # Todo: Viết method init session ở đây. Khi nào cần tạo shopify session thì chỉ cần gọi store.init_shopify_session()
    # Todo: Viết hàm tạo webhook và script tag vào trong model store
    # Todo: Tạo method để chạy cron job. Cứ 5 phút chạy một lần, mỗi lần cập nhật từ 50 đến 100 store.
    #  Sẽ search các store có trạng thái is_update_script_tag, sau đó xóa scrip tag cũ, cài scrip tag mới, và đánh lại trạng thái is_update_script_tag = True
    # Todo: Nhớ đặt try catch cho các hàm liên quan đén Shopify.