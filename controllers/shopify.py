import binascii
import os

import shopify
import werkzeug

from odoo import http
from odoo.http import request
import json


class ShopifyController(http.Controller):
    @http.route('/shopify/auth2', auth='public')
    #Todo: Sửa router thành /shopify/<tên app>/auth
    def shopify_auth2(self, **kw):
        #Todo: Viết thêm view trong setting để điền shopify api, secret, api version
        #Todo: Bổ xung view modal backend để quản lý dữ liệu với quyền admin
        #Todo: Bổ xung security
        api_version = request.env['ir.config_parameter'].sudo().get_param('shopify_api_version')
        shopify_key = request.env['ir.config_parameter'].sudo().get_param('shopify_key')
        shopify_secret = request.env['ir.config_parameter'].sudo().get_param('shopify_secret')

        shopify.Session.setup(api_key=shopify_key, secret=shopify_secret)

        shop_url = kw['shop']
        state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
        redirect_uri = request.env['ir.config_parameter'].sudo().get_param('web.base.url') + "/shopify/callback"
        scopes = [
            "read_products",
            "read_orders",
            "write_orders",
            'read_script_tags',
            'write_script_tags',
            'read_themes'
        ]

        newSession = shopify.Session(shop_url, api_version)
        auth_url = newSession.create_permission_url(scopes, redirect_uri, state)

        return werkzeug.utils.redirect(auth_url)

    @http.route('/shopify/callback', autgeth="public", type="http", cors="*")
    # Todo: Sửa router thành /shopify/<tên app>/finalize
    def shopify_callback(self,**kw):
        api_version = request.env['ir.config_parameter'].sudo().get_param('shopify_api_version')
        shopify_key = request.env['ir.config_parameter'].sudo().get_param('shopify_key')
        shopify_secret = request.env['ir.config_parameter'].sudo().get_param('shopify_secret')

        shopify.Session.setup(api_key=shopify_key, secret=shopify_secret)
        session = shopify.Session(kw['shop'], api_version)
        access_token = session.request_token(kw)

        session = shopify.Session(kw['shop'], api_version, access_token)
        shopify.ShopifyResource.activate_session(session)

        shopify_shop = shopify.Shop.current()  # Get the current shop

        shop = request.env['shopify.shop'].sudo().search([('shop_url', '=', kw['shop'])])
        if not shop:
            self.make_new_shop(shopify_shop,access_token)
            shop.fetch_products()
            # self.fetch_orders()
        else:
            shop.sudo().write({
                'token':access_token
            })

        #Todo: Check chưa có webhook mới đẩy webhook mới
        #Todo: Thiếu webhook uninstall
        self.make_webhook()
        # Todo: Check chưa có script tag mới đẩy webhook mới
        self.make_script_tag()

        return werkzeug.utils.redirect('/app/bought_together')

    def make_new_shop(self,shop,access_token):
        if request.env.user:
            request.env['shopify.shop'].sudo().create({
                'shop_url': shop.attributes['domain'],
                'currency_code': shop.attributes['currency'],
                'country': shop.attributes['country'],
                'email': shop.attributes['email'],
                'token': access_token,
                'user_id': request.env.user.id
            })
        else:
            request.env['shopify.shop'].sudo().create({
                'shop_url': shop.attributes['domain'],
                'currency_code': shop.attributes['currency'],
                'country': shop.attributes['country'],
                'email': shop.attributes['email'],
                'token': access_token
            })

    def make_webhook(self):
        print(request.env["ir.config_parameter"].sudo().get_param("ngrok_address"))
        shopify.Webhook({
            'topic': "orders/create",
            'address': request.env["ir.config_parameter"].sudo().get_param("ngrok_address") + "/webhook/orders_create",
            'format': "json"
        }).save()

        shopify.Webhook({
            'topic': "orders/update",
            'address': request.env["ir.config_parameter"].sudo().get_param("ngrok_address") + "/webhook/orders_update",
            'format': "json"
        }).save()

        shopify.Webhook({
            'topic': "products/create",
            'address': request.env["ir.config_parameter"].sudo().get_param("ngrok_address") + "/webhook/products_create",
            'format': "json"
        }).save()

        shopify.Webhook({
            'topic': "products/update",
            'address': request.env["ir.config_parameter"].sudo().get_param("ngrok_address") + "/webhook/products_update",
            'format': "json"
        }).save()

    def make_script_tag(self):
        shopify.ScriptTag.create({
            "event": "onload",
            "src": 'https://odoo.website/bought_together/static/js/script_tag.js',
            "display_scope": "all",
        })

    # FE UI
    @http.route('/app/bought_together', auth='user')
    def main(self, **kw):
        value = {
            'key': 'value'
        }
        return request.render('bought_together.app-test', {'app_setting': json.dumps(value)})

    @http.route('/app/bought_together/<string:components>', auth="user", type="http", cors="*")
    def app_shopify_xero_branch(self):
        value = {
            'key': 'value'
        }
        return request.render('bought_together.app-test', {'app_setting': json.dumps(value)})

    @http.route('/api/refresh_webhook', type="json", auth='user', cors='*', method=['POST'])
    def refresh_webhook(self, **kw):
        api_version = request.env['ir.config_parameter'].sudo().get_param('shopify_api_version')
        shop = request.env['shopify.shop'].sudo().search([('shop_url','=',kw['url'])])
        session = shopify.Session(shop['shop_url'], api_version, shop['token'])
        shopify.ShopifyResource.activate_session(session)
        webhooks = shopify.Webhook.find()
        for webhook in webhooks:
            shopify.Webhook.find(webhook.id).destroy()
        self.make_webhook()

    @http.route('/api/refresh_script_tag', type="json", auth='user', cors='*', method=['POST'])
    def refresh_script_tag(self, **kw):
        api_version = request.env['ir.config_parameter'].sudo().get_param('shopify_api_version')
        shop = request.env['shopify.shop'].sudo().search([('shop_url', '=', kw['url'])])
        session = shopify.Session(shop['shop_url'], api_version, shop['token'])
        shopify.ShopifyResource.activate_session(session)
        script_tags = shopify.ScriptTag.find()
        for script_tag in script_tags:
            shopify.ScriptTag.find(script_tag.id).destroy()
        self.make_script_tag()

    @http.route('/product/list', type="json", auth='user', cors='*', method=['POST'])
    def get_product_list(self):
        products = request.env['shopify.product'].sudo().search([])
        products_data = []
        for product in products:
            products_data.append(
                {
                    'id': product.variant[0].id,
                    'title': product.title,
                    'image': product.image,
                    'price': product.variant[0].price,
                    'compare_at_price': product.variant[0].compare_at_price,
                    'inventory': product.variant[0].inventory
                }
            )
        return json.dumps(products_data)

    @http.route('/bundle/save', type="json", auth='user', cors='*', method=['POST'])
    def create_bundle(self,**kw):
        shop = request.env['shopify.shop'].sudo().search([('user_id','=', request.env.user.id)])
        bundles = kw['bundle']
        variant_ids = []
        for product in kw['bundle']['products_bundle']:
            variant_ids.append(product['id'])
        excluded_variant_ids = []
        for product in kw['bundle']['excluded_products_bundle']:
            excluded_variant_ids.append(product['id'])
        bundle_created = request.env['shopify.bundle'].sudo().create({
            'shop_id':shop.id,
            'title':bundles['title'],
            'description' : bundles['description'],
            'variant_ids': [(6,0,variant_ids)],
            'excluded_variant_ids':[(6,0,excluded_variant_ids)]
        })

        setting_created = bundle_created.setting_id.create({
            'bundle_id' : bundle_created.id,
            'title_color' : bundles['title_color'],
            'title_font' : bundles['title_font'],
            'description_color' : bundles['description_color'],
            'description_font' : bundles['description_font'],
            'button_text' : bundles['button_text'],
            'button_text_color': bundles['button_text_color'],
            'button_background_color': bundles['button_background_color'],
            'button_border_color': bundles['button_border_color']
        })

        bundle_created.write({
            'setting_id': setting_created.id
        })

    @http.route('/ui/bundle', type="json", auth='public', cors='*', method=['POST'])
    def shopify_bundle_ui(self, **kw):
        shop = request.env['shopify.shop'].sudo().search([('shop_url','=', kw['shop'])])
        bundles = request.env['shopify.bundle'].sudo().search([('shop_id','=', shop.id),('enable','=',True)])
        bundles_data = []
        for bundle in bundles:
            if not kw['variant'] in bundle.excluded_variant_ids.shopify_id:
                product_data=[]
                for variant in bundle.variant_ids:
                    product_data.append({
                        'shopify_id':variant.shopify_id,
                        'title':variant.title,
                        'price':variant.price,
                        'image':variant.product.image
                    })
                bundles_data.append({
                    'title':bundle['title'],
                    'description' : bundle['description'],
                    'products_bundle': product_data,
                    'title_color': bundle.setting_id['title_color'],
                    'title_font': bundle.setting_id['title_font'],
                    'description_color': bundle.setting_id['description_color'],
                    'description_font': bundle.setting_id['description_font'],
                    'button_text': bundle.setting_id['button_text'],
                    'button_text_color': bundle.setting_id['button_text_color'],
                    'button_background_color': bundle.setting_id['button_background_color'],
                    'button_border_color': bundle.setting_id['button_border_color']
                })
        return json.dumps(bundles_data)

    @http.route('/widget/info', type="json", auth='public', cors='*', method=['POST'])
    def widget_info(self):
        shop = request.env['shopify.shop'].sudo().search([('user_id', '=', request.env.user.id)])
        bundles = request.env['shopify.bundle'].sudo().search([('shop_id', '=', shop.id)])
        bundles_data = []
        for bundle in bundles:
            bundles_data.append({
                'id': bundle.id,
                'title':bundle.title,
                'description':bundle.description,
                'products_num':len(bundle.variant_ids),
                'total_price': bundle.total_price,
                'status': bundle.enable
            })
        return json.dumps(bundles_data)

    @http.route('/go-to-theme', type="json", auth='user', cors='*', method=['POST'])
    def go_to_theme(self):
        api_version = request.env['ir.config_parameter'].sudo().get_param('shopify_api_version')
        shop = request.env['shopify.shop'].sudo().search([('user_id','=', request.env.user.id)])
        session = shopify.Session(shop['shop_url'], api_version, shop['token'])
        shopify.ShopifyResource.activate_session(session)
        themes = shopify.Theme.find()
        for theme in themes:
            if theme.attributes['role'] == 'main':
                print(theme.attributes['id'])
                return json.dumps({
                    'shop': shop.shop_url.split('.')[0],
                    'theme_id':theme.attributes['id']
                })

    @http.route('/check/scrip_tag', type="json", auth='user', cors='*', method=['POST'])
    def check_script_tag(self):
        api_version = request.env['ir.config_parameter'].sudo().get_param('shopify_api_version')
        shop = request.env['shopify.shop'].sudo().search([('user_id', '=', request.env.user.id)])
        session = shopify.Session(shop['shop_url'], api_version, shop['token'])
        shopify.ShopifyResource.activate_session(session)
        script_tag = shopify.ScriptTag.find()
        print(script_tag)

    @http.route('/bundle/toggle_status', type="json", auth='user', cors='*', method=['POST'])
    def toggle_status_bundle(self,**kw):
        bundle = request.env['shopify.bundle'].sudo().browse(kw['id'])
        bundle.write({
            'enable': not bundle.enable
        })