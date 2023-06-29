<template>
  <div class="bundle">
    <div class="title" :style="{fontSize:bundle.title_font+'px'}">
      {{bundle.title}}
    </div>
    <div class="description" :style="{fontSize:bundle.description_font+'px'}">
      {{bundle.description}}
    </div>
    <div class="flex space-between middle">
      <div class="product-img">
        <div v-for="i in bundle.products_bundle.length">
          <img :src="bundle.products_bundle[i-1].image">
          <span v-if="i != bundle.products_bundle.length" class="nest-product">+</span>
        </div>
      </div>
      <div>
        <div class="total">Total: <span class="price">$123</span></div>
        <div @click="addToCart" class="add-bundle-btn" :style="{color:bundle.button_text_color,
                  backgroundColor:bundle.button_background_color,
                  borderColor:bundle.button_border_color}">{{bundle.button_text}}</div>
      </div>
    </div>
    <div class="flex space-between product-list" v-for="product in bundle.products_bundle">
      <div>
        <input type="checkbox" checked>
        {{product.title}}
      </div>
      <div class="price product-price">
        ${{product.price}}
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props:['bundle'],
  methods:{
    addToCart(){
        let items = []
        for(let product of this.bundle.products_bundle){
          items.push({
            id: product.shopify_id,
            quantity: 1
          })
        }
        axios.post(window.Shopify.routes.root + 'cart/add.js',{'items':items})
          .then(response => {
            window.location.href = 'https://'+window.Shopify.shop+'/cart'
          })
          .catch(err => {
              console.log(err)
          })
      }
  }
}
</script>

<style scoped>
  .bundle{
    padding: 32px 16px 10px;
  }
  .title{
    display: flex;
    justify-content: center;
    font-weight: 700;
  }
  .description{
    display: flex;
    justify-content: center;
    margin: 14px 0 51px;
  }

  .product-img{
    display: flex;
  }

  .product-img img{
    border-radius: 6px;
    width: 65px;
    height: 61px;
  }
  .nest-product{
    margin:0 9px;
  }
  .add-bundle-btn{
    cursor: pointer;
    width: 183px;
    padding: 5px;
    text-align: center;
  }

  .middle{
    margin-bottom: 30px;
  }

  .product-list{
    margin: 0 29px 12px 29px;
  }

  .total{
    display: flex;
    justify-content: center;
  }

  .price{
    color: #FF0000;
    font-weight: 600;
  }

  .product-price{
    min-width: 100px;
    display: flex;
    justify-content: center;
  }

  input[type='checkbox']{
    pointer-events: none;
  }
</style>