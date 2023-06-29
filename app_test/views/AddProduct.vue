<template>
  <div class="content add-product">
    <!-- Nav -->
    <NavStatus/>

    <!-- Process -->
    <div class="add-product-process">
      <div>
        <div v-if="isLoading">
          Cancel
        </div>
      </div>
      <div>
        <div @click="goToCustomization" v-if="isLoading">
          Save
        </div>
      </div>
    </div>
    <!-- Enable Widget -->
    <div class="enable-widget">
      Enable Widget
      <Switch v-model:checked="checked" checked-children="ON" un-checked-children="OFF"/>
    </div>

    <!-- Product List -->
    <div class="product-list-wrapper">
      <div class="product-list-table">
        <div class="big-title">
          Manual Recommendation
          <img src="/bought_together/static/images/widgets/ask.png" class="product-list-ask" alt="">
        </div>
        <div class="title">
          <img src="/bought_together/static/images/widgets/ask.png" class="product-list-ask" alt=""> Choose recommendation product(s)
        </div>
        <div class="search-product">
          <input type="text" placeholder="Search product by name " v-model="products_search">
        </div>
        <div class="product-choosen-list">
          <div v-for="product in products">
            <div  class="product-choosen"  v-if="product.check == true">{{product.title}} <img @click="product.check = false" src="/bought_together/static/images/widgets/uncheck.png"></div>
          </div>
        </div>
        <!-- Product list content -->
        <div class="product-list">
          <!-- Header -->
          <div class="product-list-header product-list-row">
            <div class="check-box">
              <input @change="toggleCheckbox" v-model="check_all" type="checkbox">
            </div>
            <div class="image">
              Image
            </div>
            <div class="name">
              Product Name
            </div>
            <div class="price">
              Price
            </div>
            <div class="compare">
              Compare At Price
            </div>
            <div class="stock">
              In Stock
            </div>
          </div>
          <!-- item -->
          <div class="product-list-item-wrapper">
            <div v-for="product in products">
              <div :class="{'product-list-item-disable':!checked}" class="product-list-row" v-if="products_search=='' || product.title.includes(products_search)">
                <div class="check-box">
                  <input class="checkbox-item" type="checkbox" v-model="product.check">
                </div>
                <div class="image">
                  <img :src="product.image" alt="Product image">
                </div>
                <div class="name">
                  {{ product.title }}
                </div>
                <div class="price">
                  {{ product.price }}
                </div>
                <div class="compare">
                  {{ product.compare_at_price }}
                </div>
                <div class="stock">
                  {{ product.inventory }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Product List exclude -->
    <div class="product-list-wrapper">
      <div class="product-list-table">
        <div class="title">
          <img src="/bought_together/static/images/widgets/ask.png" class="product-list-ask" alt=""> Choose excluded product(s)
        </div>
        <div class="search-product">
          <input type="text" placeholder="Search product by name " v-model="excluded_products_search">
        </div>
        <div class="product-choosen-list">
          <div v-for="product in excluded_products">
            <div  class="product-choosen"  v-if="product.check == true">{{product.title}} <img @click="product.check = false" src="/bought_together/static/images/widgets/uncheck.png"></div>
          </div>
        </div>

        <!-- Product list content -->
        <div class="product-list">
          <!-- Header -->
          <div class="product-list-header product-list-row">
            <div class="check-box">
              <input type="checkbox">
            </div>
            <div class="image">
              Image
            </div>
            <div class="name">
              Product Name
            </div>
            <div class="price">
              Price
            </div>
            <div class="compare">
              Compare At Price
            </div>
            <div class="stock">
              In Stock
            </div>
          </div>

          <!-- Item -->
          <div class="product-list-item-wrapper">
            <div v-for="product in excluded_products">
              <div :class="{'product-list-item-disable':!checked}" class="product-list-row" v-if="excluded_products_search=='' || product.title.includes(excluded_products_search)">
                <div class="check-box">
                  <input class="checkbox-item" type="checkbox" v-model="product.check">
                </div>
                <div class="image">
                  <img :src="product.image" alt="Product image">
                </div>
                <div class="name">
                  {{ product.title }}
                </div>
                <div class="price">
                  {{ product.price }}
                </div>
                <div class="compare">
                  {{ product.compare_at_price }}
                </div>
                <div class="stock">
                  {{ product.inventory }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { notification } from 'ant-design-vue';
import NavStatus from '../components/NavStatus.vue';
import { Switch } from 'ant-design-vue'
import axios from "axios";
export default {
  components: { NavStatus, Switch },
  data(){
    return{
      isLoading: true,
      check_all: false,
      excluded_check_all:false,
      checked: true,
      excluded_products:[],
      excluded_products_search: '',
      products:[],
      products_search: ''
    }
  },
  methods:{
    toggleCheckbox(){
      for(let product of this.products){
        product.check = this.check_all
      }
    },
    openNotification() {
      notification.open({
        message: 'You have reach the product limitation.',
        description: 'Please untick any products from the list to continue selecting',
        onClick: () => {
          console.log('Notification Clicked!');
        },
        duration:2
      });
    },
    goToCustomization(){
      let products = this.products.filter(product => product.check == true)
      let excluded_products = this.excluded_products.filter(products => products.check == true)

      localStorage.setItem('products_bundle',JSON.stringify(products))
      localStorage.setItem('excluded_products_bundle',JSON.stringify(excluded_products))
      localStorage.setItem('activity','Customization')

      this.$store.state.excluded_products_bundle = excluded_products
      this.$store.state.products_bundle = products
      this.$store.state.activity = 'Customization'

      this.$router.push({name:'Customization'})
    }
  },
  watch: {
    products:{
      handler(newProducts){
        let count = 0
        for(let product of newProducts){
          if (product.check == true) count++
        }
        if (count>5){
          this.openNotification()
        }
      },
      deep:true
    }
  },
  mounted(){
    axios.post('/product/list',{
      jsonrpc:'2.0',
      params: {}
    }).then(res => {
      this.products = JSON.parse(res.data.result)
      this.excluded_products = JSON.parse(res.data.result)
      for(let product of this.products){
        product.check = false
      }
      for(let product of this.excluded_products){
        product.check = false
      }
    })
    .catch(e => {
      console.log(e)
    })
  }
}
</script>

<style scoped>
  /* Enable widget */
  .enable-widget{
    margin: 46px 34px 0;
    font-style: normal;
    font-weight: 600;
    font-size: 18px;
    line-height: 22px;
    display: flex;
  }

  .product-list-wrapper{
    margin: 14px 20px;
  }
  .product-list-table{
    border: 1px solid #E2E2E2;
  }
  .product-list-wrapper .big-title{
    font-weight: 600;
    font-size: 20px;
    line-height: 22px;
  }

  .product-list-ask{
    width: 12px;
    height: 12px;
  }

  .product-list-wrapper .title{
    margin: 16px 0 4px 15px;
  }

  /* Search */
  .search-product{
    margin: 0 23px 20px 10px;
  }

  .product-choosen-list{
    margin:3px 21px 1px;
    display: flex;
  }

  .product-choosen{
    margin-right: 16px;
    border-radius: 6px;
    border: 1px solid #E2E2E2;
    padding: 3px 10px;
  }

  .product-choosen img{
    width: 15px;
    height: 15px;
    border-radius: 100%;
    margin-left: 8px;
    cursor: pointer;
  }

  .search-product input{
    width: 100%;
    height: 40px;
    padding-left: 38px;
  }

  /* Product List */
  .product-list{
    margin: 10px 20px 10px;
    line-height: 34px;
    border-bottom: 1px solid #E2E2E2;
  }

  .product-list-row{
    width: 100%;
    display: flex;
    border-top: 1px solid #E2E2E2;
  }

  .product-list-header{
    font-weight: 700;
    border-bottom: 1px solid #E2E2E2;
  }
  .product-list-item-wrapper{
    height: 174px;
    overflow-y: scroll;
  }
  .product-list-item-disable div{
    font-weight: 400;
    color: #D9D9D9;
  }
  .product-list .check-box{
    width: 5%;
  }
  .product-list .image{
    width: 10%;
  }
  .product-list .image img{
    width: 20px;
    height: 20px;
    border-radius: 90%;
  }
  .product-list .name{
    width: 40%;
  }
  .product-list .price{
    width: 15%;
  }
  .product-list .compare{
    width: 15%;
  }
  .product-list .stock{
    width: 15%;
  }

  button[role='switch']{
    margin-left: 28px;
  }

</style>