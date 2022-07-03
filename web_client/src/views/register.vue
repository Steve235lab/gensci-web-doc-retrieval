<template>
  <div class="logincontiner">
    <el-form
        class="loginForm"
        :model="loginForm"
        ref="loginForm"
        :inline="false"
        size="medium"
        :rules="loginrules"
    >
      <el-form-item>
        <div class="loginTitle">注册</div>
      </el-form-item>
      <el-form-item prop="username" label="用户名" style="letter-spacing: 4px">
        <el-col :span="18">
          <el-input placeholder="请输⼊用户名" v-model="loginForm.username"></el-input>
        </el-col>
      </el-form-item>
      <el-form-item prop="email" label="邮箱" style="letter-spacing: 10px">
        <el-col :span="18">
          <el-input placeholder="请输⼊邮箱" v-model="loginForm.email"></el-input>
        </el-col>
      </el-form-item>
      <el-form-item prop="password" label="密码" style="letter-spacing: 10px">
        <el-col :span="18">
          <el-input placeholder="请设定密码" show-password="show-password" v-model="loginForm.password"></el-input>
        </el-col>
      </el-form-item>
      <el-form-item prop="epassword" label="密码确认">
        <el-col :span="18">
          <el-input placeholder="再输一次密码" show-password="show-password" v-model="loginForm.epassword"></el-input>
        </el-col>
      </el-form-item>
      <el-form-item prop="code" label="验证码 " style="letter-spacing: 4px">
        <el-col :span="12">
          <el-input placeholder="请输⼊验证码" v-model="loginForm.code"></el-input>
        </el-col>
        <el-col :span="6">
          <el-button  @click="sendemail" type="success">获取</el-button>
        </el-col>
      </el-form-item>

      <el-form-item>
        <el-col :span="12">
          <el-button class="btn" @click="commitbtn" type="primary">确认注册</el-button>
        </el-col>
        <el-col :span="12">
          <el-button class="btn" @click="back" type="primary">返回登录</el-button>
        </el-col>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import axios from 'axios';
import md5 from 'js-md5';
import qs from 'qs';
export default {
  data() {
    const validateNameLength = (loginrules, value, callback) => {
      const str = value.trim();
      const length = str.length;
      const reStr = /^[a-zA-Z]{1}/;
      const reEn = /^[a-zA-Z0-9/_)]{3,16}$/;
      if (!reStr.test(value)) {
        callback(new Error("用户名必须以字母开头"));
      } else if (length < 6 || length > 16) {
        callback(new Error("用户名的长度是6到16个字符"));
      } else if (!reEn.test(value)) {
        callback(new Error("用户名只能包含字母、数字和下划线"));
      } else {
        callback();
      }
      this.formData.username = str;
    };

    var checkEmail = (loginrules, value, callback) => {
      const reg = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
      if (!reg.test(value)) {
        callback(new Error("请输入有效的邮箱"));
      }
      callback();
    };

    var validatePass = (loginrules, value, callback) => {
      if (value === "") {
        callback(new Error("请输入密码"));
      } else {
        if (this.loginForm.epassword !== "") {
          this.$refs.loginForm.validateField("epassword");
        }
        callback();
      }
    };

    var validatePass2 = (loginrules, value, callback) => {
      if (value === "") {
        callback(new Error("请再次输入密码"));
      } else if (value !== this.loginForm.password) {
        callback(new Error("两次输入密码不一致!"));
      } else {
        callback();
      }
    };
    return {
      token:'',
      loginForm: {
        username: "",
        email: "",
        password: "",
        epassword: "",
        code: "",

      },
      loginrules: {
        username: [
          { required: true, message: "用户名不能为空", trigger: "blur" },
          { min: 6, max: 16, message: "长度在 6 到 16 个字符", trigger: "blur" },
          { validator: validateNameLength, trigger: "blur", required: true },
        ],
        email: [
          {
            required: true,
            trigger: "blur",
            message: "邮箱不能为空",
          },
          {
            validator: checkEmail,
            trigger: "blur",
          },
        ],
        password: [
          { required: true, message: "密码不能为空", trigger: "blur" },
          { min: 6, max: 16, message: "长度在 6 到 16 个字符", trigger: "blur" },
          { validator: validatePass, trigger: "blur", required: true },
        ],
        epassword: [
          { required: true, message: "请确认密码", trigger: "blur" },
          { min: 6, max: 16, message: "长度在 6 到 16 个字符", trigger: "blur" },
          { validator: validatePass2, trigger: "blur" },
        ],
        code: [
          {
            required: true,
            trigger: "change",
            message: "验证码未填写",
          },
        ],
        msg: "",
      },
    };
  },
  methods: {
    commitbtn() {
      var that=this;
      that.axios({
        method:"post",
        url:"http://42.192.44.52:8000/sign_up/email_confirm/",
        data:qs.stringify({
          message_type: "email_confirm",
          token: this.token,
          confirm_code: this.loginForm.code
        })
      })
          .then(function(res){
            console.log(res)
            console.log(res.data);
            var yanzhengma=res.data.confirmed;
            if(yanzhengma==='True'){
            that.$message({message:'注册成功',type:'success'})
            that.router.push('login')
            }
            else{
              that.$message({message:'验证码错误',type:'warning'})
            }
          })
          .catch(function(err){
            console.log(err)
          })
      this.$refs.loginForm.validate((valid) => {
        if (valid) {
          console.log(valid);
        }
      });
    },
    back(){
      this.$router.push('login')
    },
    sendemail(){
      var that=this;
      that.axios({
        method:"post",
        url:"http://42.192.44.52:8000/sign_up/",
        data:qs.stringify({
          message_type: "sign_up",
          username:this.loginForm.username,
          email:this.loginForm.email,
          password:md5(this.loginForm.password)
        }),
      })
          .then(function(res){
            console.log(res)
            if(res.data.result==='success'){
              that.$message({message:'已发送验证码',type:'success'})
              that.token=res.data.token;
            }
            else{
              that.$message({message:'邮箱已被注册',type:'warning'})
            }
          })
          .catch(function(err){
            console.log(err)
          })
    }
  }
  
}
</script>

<style lang="scss" scoped>
.logincontiner {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-image:url('/src/assets/beijing.png');
  background-size: 100% 100%;
  .loginForm {
    height: 450px;
    width: 350px;
    box-shadow: 0 0 25px #cac6c6;
    border-radius: 10px;
    padding: 20px 35px;
    .loginTitle {
      display: flex;
      justify-content: center;
      align-items: center;
      font-weight: 600;
      font-size: 24px;
    }
    .btn {
      width: 90%;
    }
  }
}
</style>
