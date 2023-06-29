<template>
  <div class="add-product-nav">
    <router-link :to="{name:'AddProduct'}" class="add-product-nav-item">
        Add Product
    </router-link>
    <router-link  :to="{name:'Customization'}" class="add-product-nav-item">
        Customization
    </router-link>
    <router-link :to="{name:'Installation'}" class="add-product-nav-item">
        Installation
    </router-link>
</div>
</template>

<script>
export default {

}
</script>

<style scoped>
    /* Nav */
  a{
    pointer-events: none;
  }
  .add-product-nav{
    width: 560px;
    height: 42px;
    background: #c8c8c8;
    margin: 14px auto 0;
    border-radius: 4px;
    padding: 3px;
    display: flex;
  }
  .add-product-nav-item{
    width: 33.3%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-weight: 500;
    color: white;
  }
  .add-product-nav-item.router-link-active{
    box-shadow: -1px 1px 4px rgba(0, 0, 0, 0.25);
    border-radius: 4px;
    color: black;
    background: white;
  }
</style>