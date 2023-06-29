<template>
  <div class="customization content">
    <nav-status/>
    <!-- Process -->
    <div  class="add-product-process">
      <div @click="goToAddProduct">
          Cancel
      </div>

      <div @click="saveBundle">
          Save
      </div>
    </div>
    <!-- Setting -->
    <div class="customize-setting">
        <div class="title">
          <div class="title-name">
            Settings
          </div>
          <img src="/bought_together/static/images/widgets/ask.png" class="product-list-ask" alt="">
        </div>
        <div class="setting-content">
          <div class="setting-config">
            <div class="config">
              <div class="config-title">
                <img src="/bought_together/static/images/widgets/ask.png" class="product-list-ask" alt="">
                General Configuration
              </div>
              <div class="config-content">
                <!--        Title        -->
                <div class="config-text">
                  <div>Widget Title</div>
                  <input type="text" v-model="bundle.title">
                </div>
                <div class="flex">
                  <div class="choose">
                    <div class="choose-title">
                      Title Color
                    </div>
                    <div class="choose-input">
                      <div class="choose-color">
                        <input type="color" v-model="bundle.title_color">
                      </div>
                      <input type="text" v-model="bundle.title_color">
                    </div>
                  </div>
                  <div class="choose">
                    <div class="choose-title">
                      Font Size
                    </div>
                    <div class="choose-input">
                      <select v-model="bundle.title_font">
                        <option value="11">Extra small</option>
                        <option value="14">Small</option>
                        <option value="17">Medium</option>
                        <option value="20">Large</option>
                        <option value="24">Extra large</option>
                      </select>
                    </div>
                  </div>
                </div>

                <!--        Description        -->
                <div class="config-text">
                  <div>Widget Description</div>
                  <input type="text" name="" id="" v-model="bundle.description">
                </div>
                <div class="flex">
                  <div class="choose">
                    <div class="choose-title">
                      Title Color
                    </div>
                    <div class="choose-input">
                      <div class="choose-color">
                        <input type="color" v-model="bundle.description_color">
                      </div>
                      <input type="text" v-model="bundle.description_color">
                    </div>
                  </div>
                  <div class="choose">
                    <div class="choose-title">
                      Font Size
                    </div>
                    <div class="choose-input">
                      <select v-model="bundle.description_font">
                        <option value="11">Extra small</option>
                        <option value="14">Small</option>
                        <option value="17">Medium</option>
                        <option value="20">Large</option>
                        <option value="24">Extra large</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="config">
              <div class="config-title">
                <img src="/bought_together/static/images/widgets/ask.png" class="product-list-ask" alt="">
                <div>
                  Button Configuration
                </div>
              </div>
              <div class="config-content">
                <div class="config-text">
                  <div>Button Text</div>
                  <input type="text" name="" id="" v-model="bundle.button_text">
                </div>

                <div class="flex">
                <div class="choose">
                  <div class="choose-title">
                    Text Color
                  </div>
                  <div class="choose-input">
                    <div class="choose-color">
                      <input type="color" v-model="bundle.button_text_color">
                    </div>
                    <input type="text" v-model="bundle.button_text_color">
                  </div>
                </div>
              </div>

              <div class="flex">
                <div class="choose">
                  <div class="choose-title">
                    Background Color
                  </div>
                  <div class="choose-input">
                    <div class="choose-color">
                      <input type="color" v-model="bundle.button_background_color">
                    </div>
                    <input type="text" v-model="bundle.button_background_color">
                  </div>
                </div>
                <div class="choose">
                  <div class="choose-title">
                    Border Color
                  </div>
                  <div class="choose-input">
                    <div class="choose-color">
                      <input type="color" v-model="bundle.button_border_color">
                    </div>
                    <input type="text" v-model="bundle.button_border_color">
                  </div>
                </div>
              </div>
              </div>
            </div>
          </div>
          <!-- Preview -->
          <div>
            <div class="preview">
              <img src="/bought_together/static/images/widgets/ask.png" class="product-list-ask" alt="">
              <div>
                Preview
              </div>
            </div>
            <div class="bundle-preview">
              <Bundle :bundle="bundle"/>
            </div>
          </div>

        </div>
    </div>
  </div>
</template>

<script>
import NavStatus from '../components/NavStatus.vue'
import Bundle from "../components/Bundle.vue";
import axios from "axios";
export default {
  components: {Bundle, NavStatus },
  data(){
    return{
      bundle:{
        excluded_products_bundle: this.$store.state.excluded_products_bundle,
        products_bundle: this.$store.state.products_bundle,
        title:'YOU MAY ALSO LIKE...',
        title_color:'#000000',
        title_font: 20,
        description:'Good deals only for you!',
        description_color:'#000000',
        description_font:14,
        button_text:'Add bundle',
        button_text_color:'#ffffff',
        button_background_color:'#E1E3E5',
        button_border_color:'#E1E3E5',
      }
    }
  },
  methods:{
    goToAddProduct(){
      this.$store.state.activity = 'AddProduct'
      localStorage.setItem('activity','AddProduct')
      localStorage.removeItem('products_bundle')
      localStorage.removeItem('excluded_products_bundle')
      this.$router.push({name:'AddProduct'})
    },
    saveBundle(){
      axios.post('/bundle/save',{
        jsonrpc:'2.0',
        params:{
          bundle:this.bundle
        }
      })
      .then(res => {
        this.$store.state.activity = 'Installation'
        localStorage.setItem('activity','Installation')
        localStorage.removeItem('products_bundle')
        localStorage.removeItem('excluded_products_bundle')
        this.$router.push({name:'Installation'})
      })
      .catch(e => {
        console.log(e)
      })
    }
  }
}
</script>

<style scoped>
  .add-product-process div:nth-child(2){
    font-weight: 700;
  }

  .customize-setting{
    width: 100%;
  }
  /* title */
  .customize-setting .title{
    margin: 28px 0 0 35px;
    display: flex;
    align-items: center;
  }
  .customize-setting .title .title-name{
    margin-right: 69px;
    font-weight: 600;
    font-size: 20px;
  }

  .setting-content{
    display: flex;
  }
  .setting-content>div{
    width: 50%;
    margin: 29px;
  }
  .config-title, .preview{
    display: flex;
  }
  .config-title img, .preview img{
    margin-right: 10px;
  }

  .config-content{
    padding: 26px;
  }

  .config-text>div{
    margin-bottom: 9px;
    font-weight: 600;
    font-size: 16px;
    line-height: 22px;
  }
  .config-text>input{
    width: 80%;
    margin-bottom: 18px;
  }

  .product-list-ask{
    width: 12px;
    height: 12px;
  }

  .choose{
    width: 50%;
    margin-bottom: 9px;
  }

  .choose .choose-title{
    margin-bottom: 20px;
  }

  .choose-input{
    padding-right: 41px;
    display: flex;
  }

  .choose-color{
    margin-right: 20px;
  }
  .choose-color input{
    padding: 0;
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;
    width: 30px;
    height: 30px;
    background-color: transparent;
    border: none;
    cursor: pointer;
  }

  .choose-color input::-webkit-color-swatch {
    border-radius: 50%;
    border: 1px solid black;
  }

  .choose-color input::-moz-color-swatch {
    border-radius: 50%;
    border: 1px solid black;
  }

  .choose-input input[type='text']{
    max-width: 190px;
  }

  .bundle-preview{
    margin:24px 20px;
    border-radius: 5px;
    border: 1px solid #BFBFBF;
  }
</style>