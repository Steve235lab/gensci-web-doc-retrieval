<template>
  <div class="logincontiner">
    <el-form class="loginForm" :model="loginForm" ref="loginForm" :inline="false" size="medium" :rules="loginrules">
      <el-form-item>
        <div class="loginTitle">系统登录</div>
      </el-form-item>
      <el-form-item prop="email" label="用户">
        <el-col :span="18">
          <el-input placeholder="请输⼊邮箱" v-model="loginForm.email"></el-input>
        </el-col>
      </el-form-item>
      <el-form-item prop="password" label="密码">
        <el-col :span="18">
          <el-input placeholder="请输⼊密码" show-password="show-password" v-model="loginForm.password"></el-input>
        </el-col>
      </el-form-item>

      <el-form-item>
        <el-col :span="12">
          <el-button class="btn" @click="commitBtn" type="success" >登录</el-button>
        </el-col>
        <el-col :span="12">
          <el-button class="btn" @click="tiaozhuan" type="primary" >注册</el-button>
        </el-col>
      </el-form-item>
      <el-form-item>
        <el-col :span="12">
          <el-button class="btn" @click="ceshi" type="primary" >测试</el-button>
        </el-col>
      </el-form-item>
    </el-form>

  </div>
</template>

<script>
import axios from 'axios';
import md5 from 'js-md5';
import qs from 'qs';
import setStorage from './storage.js';
export default {
  data(){
    return{
      loginForm:{
        email:'',
        password:'',
        code:'',
      },
      loginrules:{
        email:[
          {
            required:true,
            trigger:'change',
            message:'请输入邮箱'
          }
        ],
        password:[
          {
            required:true,
            trigger:'change',
            message:'请输入密码'
          }
        ],
      }
    }
  },
  methods:{
    tiaozhuan(){
      this.$router.push('register')
    },
    ceshi(){
       this.$router.push('home')
    },
    commitBtn(){
      var that=this;
      that.axios({
        method:"post",
        url:"http://42.192.44.52:8000/sign_in/",
        data:qs.stringify({
          message_type: "sign_in",
          email:this.loginForm.email,
          //password:this.loginForm.password,
           password:this.loginForm.password
        })
      })
          .then(function(res){
            console.log(res)
            console.log(res.data);
            var token=res.data.token;
            console.log(token);
            var jieguo=res.data.result;
          if(jieguo==='success'){
            console.log('登录成功')
            that.$router.push('home')
          }  
            //setStorage.getItem('token')//获取token
            //console.log(setStorage.token)
          })
          .catch(function(err){
            console.log(err)
          })

  
      this.$refs.loginForm.validate(valid=>{
        if(valid){
          console.log(valid);
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.logincontiner{
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  .loginForm{
    height: 300px;
    width: 350px;
    box-shadow: 0 0 25px #cac6c6;
    border-radius: 10px;
    padding: 20px 35px;
    .loginTitle{
      display: flex;
      justify-content: center;
      align-items: center;
      font-weight: 600;
      font-size: 24px;
    }
    .btn{
      width: 90%;
    }
  }
}
</style>