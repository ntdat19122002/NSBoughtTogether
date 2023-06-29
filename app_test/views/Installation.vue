<template>
    <div class="content installation">
        <NavStatus/>

        <!-- Process -->
        <div class="add-product-process">
          <div>
            <div @click="goToAddProduct">
              Cancel
            </div>
          </div>
          <div>
            <div @click="goToTheme">
              Go to Themes Customization
            </div>
          </div>
        </div>

        <!--   Content   -->
        <div class="main">
          <div class="congration">CONGRATULATION! YOU HAVE CREATED WIDGET SUCCESSFULLY! </div>
          <div class="follow">Now please follow these steps below to display it on your product pages</div>
          <ol>
            <li>Lorem ipsum is placeholder text commonly used in the graphic, print </li>
            <li>and publishing industries for previewing layouts and visual mockups. </li>
            <li>Lorem ipsum is placeholder text commonly used in the graphic, print, and publishing industries for previewing layouts and visual mockups.</li>
          </ol>

          <video width="671px" height="256px" controls>
            <source src="/bought_together/static/videos/bundle.mp4" type="video/mp4">
          </video>
        </div>
    </div>
</template>

<script>
import NavStatus from '../components/NavStatus.vue'
import axios from "axios";
export default {
  components: { NavStatus },
  data(){
    return{}
  },
  methods:{
    goToAddProduct(){
      this.$store.state.activity = 'AddProduct'
      localStorage.setItem('activity','AddProduct')
      this.$router.push({name:'AddProduct'})
    },
    async goToTheme(){
      axios.post('/go-to-theme',{
        jsonrpc:'2.0',
        params:{}
      })
      .then(res => {
        let data = JSON.parse(res.data.result)
        window.location.href = `https://admin.shopify.com/store/${data.shop}/themes/${data.theme_id}/editor`
      })
      .catch(e => {
        console.log(e)
      })
    }
  }
}
</script>

<style>
  .main{
    width: 80%;
    margin: 164px auto 0;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .congration{
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 22px;
  }

  .follow{
    font-weight: 700;
    margin-bottom: 62px;
  }
  video{
    margin-top: 71px;
  }
</style>