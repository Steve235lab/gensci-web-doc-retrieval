<template>

    <el-table
      :data="tableData"
      style="width: 100%">
      <el-table-column
        prop="username"
        label="用户"
        width="180">
      </el-table-column>
      <el-table-column
        prop="email"
        label="邮箱"
        width="180">
      </el-table-column>
      <el-table-column
        prop="password"
        label="密码"
        width="180">
      </el-table-column>
       <el-table-column
        prop="keywords"
        label="关键词">
      </el-table-column>
      <el-table-column
        label="操作">
      <el-button class="btn" @click="add" type="primary">添加</el-button>
      <el-button class="btn" @click="decline" type="primary">删除</el-button>
      </el-table-column>
    </el-table>
    
  </template>

  <script>

    export default {
      data() {
        return {
          tableData: [{
            username: 'username',
            email: 'email',
            password: 'password',
            keywords:'keywords'
          }, 
          ]
        }
      },
      methods:{
        add(){

        },
        decline(){

        },
      }
    }
  </script>