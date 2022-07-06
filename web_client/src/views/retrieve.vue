<template>
  <div class="logincontiner">
    <el-form class="loginForm" :model="loginForm" ref="loginForm" :inline="false" size="medium" :rules="loginrules">
      <el-form-item>
        <div class="loginTitle" >重置密码</div>
      </el-form-item>
      <el-form-item prop="email" label="用户"  style="letter-spacing: 4px">
        <el-col :span="18">
          <el-input placeholder="请输⼊邮箱" v-model="loginForm.email"></el-input>
        </el-col>
      </el-form-item>
      <el-form-item prop="code" label="验证码">
        <el-col :span="13">
            <el-input placeholder="请输⼊验证码"  v-model="loginForm.code" ></el-input>
        </el-col>
        <el-col :span="6">
            <el-button v-show="show" type="success" style="width: 100%;padding: 12px 0;font-size: 13px;" @click="send">发送验证码</el-button>
            <el-button v-show="!show" type="warning" style="width: 100%;padding: 12px 0;font-size: 13px;" disabled>{{count}} s</el-button>
        </el-col>
      </el-form-item>
      <el-form-item prop="password" label="新密码"  style="letter-spacing: 4px">
        <el-col :span="18">
          <el-input placeholder="请输⼊密码" show-password="show-password" v-model="loginForm.password"></el-input>
        </el-col>
      </el-form-item>
      

      <el-form-item>
        <el-col :span="12">
          <el-button class="btn" @click="commit" type="primary" >身份认证</el-button>
        </el-col>
        <el-col :span="12">
          <el-button class="btn" @click="tiaozhuan" type="primary" >返回登录</el-button>
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
      show:true,
      count:'',
      timer:null,
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
        code:[
          {
            required:true,
            trigger:'change',
            message:'请输入验证码'
          }
        ],
      }
    }
  },
  methods:{
    send(){
       var that=this;
      const TIME_COUNT = 60;
        if (!that.timer) {
          that.count = TIME_COUNT;
          that.show = false;
          that.timer = setInterval(() => {
          if (that.count > 0 && that.count <= TIME_COUNT) {
            that.count--;
          } else {
            that.show = true;
            clearInterval(that.timer);
            that.timer = null;
          }
        }, 1000)
      }
      that.axios({
        method:"post",
        url:"http://42.192.44.52:8000/sign_in/email_confirm/",
        data:qs.stringify({
          message_type: "email_confirm",
          email:this.loginForm.email,
        }),
      })
          .then(function(res){
            console.log(res)
            if(res.data.result==='success'){
              that.$message({message:'已发送验证码',type:'success'})
              //console.log('已发送验证码')
            }
            else{
              that.$message({message:'邮箱未注册！',type:'warning'})
            }
          })
          .catch(function(err){
            console.log(err)
          })
    },
    tiaozhuan(){
      this.$router.push('login')
    },
    commit(){
      var that=this;
      that.axios({
        method:"post",
        url:"http://42.192.44.52:8000/sign_in/reset_password/",
        data:qs.stringify({
          code:that.loginForm.code,
          email:that.loginForm.email,
          password:md5(that.loginForm.password),
        })
      })
          .then(function(res){
            console.log(res)
            console.log(res.data);
            console.log(res.data.result);
          if(res.data.result==='success'){
            that.$router.push('login')
            that.$message({message:'身份验证成功,密码已重置',type:'success'})
            //console.log('身份验证成功,密码已重置')
          }
          else{
            that.$message({message:'身份验证失败，请确认验证码输入是否正确',type:'warning'})
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
  background-image:url('/src/assets/beijing.png');
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