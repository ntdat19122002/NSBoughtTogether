<template>
  <header>
    <div class="logo">
      <img src="" alt="Logo">
      NestScale
    </div>
    <div class="header-right">
      <div class="ask">
        <img @click="check" src="/bought_together/static/images/widgets/ask.png" alt="">
      </div>
      <div class="notification">
        <img src="/bought_together/static/images/widgets/notification.png" alt="">
        <div class="have-notification"></div>
      </div>
      <div class="logout">
        <img @click="logout" src="/bought_together/static/images/widgets/ava.png" alt="">
      </div>
    </div>
  </header>
</template>

<script>
import axios from "axios";

export default {
  methods:{
      logout(){
          window.location.href = '/web/session/logout'
      },
      check(){
        axios.post('/check/scrip_tag',{
          jsonrpc:'2.0',
          params:{}
        })
      }
  }
}
</script>

<style>
  header{
    background: #EFEFEF;
    height: 83px;
    display: flex;
    justify-content: space-between;
  }
  .logo{
    padding: 24px 0 0 20px;
    display: flex;
    align-items: center;
    font-weight: 600;
    font-size: 27px;
    color: #17181A;
  }
  .logo img{
    font-family: 'Kanit';
    height: 46px;
    width: 46px;
    margin-right: 12px;
    border-radius: 50%;
    background: black;
  }
  .have-notification{
    /* width: 6px;
    height: 6px;
    border-radius: 50%;
    background: red; */
  }
  .header-right{
    display: flex;
    align-items: center;
    margin-right: 25px;
  }
  .header-right div{
    margin-left: 29px;
  }

  .logout{
    cursor: pointer;
  }
</style>