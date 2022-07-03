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
          <div class="tips"  style="float:left;" >              
      <el-link type="white" color="blue" @click="zhaohui">忘记密码?</el-link>
    </div>
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
    zhaohui(){
      this.$router.push({ path: 'retrieve' })
    },
    tiaozhuan(){
      this.$router.push('register')
    },
    commitBtn(){
      var that=this;
      that.axios({
        method:"post",
        url:"http://42.192.44.52:8000/sign_in/",
        data:qs.stringify({
          message_type: "sign_in",
          email:this.loginForm.email,
          password:md5(this.loginForm.password)
          // password:this.loginForm.password
        })
      })
          .then(function(res){
            console.log(res)
            console.log(res.data);
            var token=res.data.token;
            console.log(token);

          if(res.data.result==='success'){
            that.$message({message:'登录成功',type:'success'})
            window.localStorage.setItem('token', res.data.token)
            let userName = 'test'
            window.localStorage.setItem('userName', userName)
            that.$router.push('home')
          }
          else{
            that.$message({message:'密码与邮箱不匹配',type:'warning'})
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
  background-image:url('../assets/beijing.png');
  background-size: 100% 100%;
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