<template>
  <div id="app">
   <el-menu
        :default-active="activeIndex"
        class="el-menu-demo"
        mode="horizontal"
        @select="handleSelect"
        background-color="#20558a"
        text-color="#fff"
        active-text-color="#b4c8e0">
      <el-menu-item index="0">HOME</el-menu-item>
      <el-menu-item index="1" style="float: right" @click="gotoLogin">登录</el-menu-item>
      <el-menu-item index="2" style="float: right" @click="gotoRegister">注册</el-menu-item>
    </el-menu>
    <el-row :gutter="20">
      <el-col :span="12" :offset="6">
        <div style="margin-top: 15px;">
          <el-input
              placeholder="请输入搜索关键词"
              v-model="input"
              class="input-with-select"
              clearable
              style="height:40px;"
              @keyup.enter.native="handleSearch"
              autocomplete="on">
            <el-button slot="append" icon="el-icon-search" @click="handleSearch"></el-button>
          </el-input>
        </div>
      </el-col>
    </el-row>
    <el-collapse style="display:inline;">
      <el-collapse-item>
        <el-row :gutter="20" style="height:45px;">
          <el-col :span="3" :offset="2"
          >
            <div style="float:left;font-weight :bold;">ARTICLE TYPE</div>
          </el-col>
          <el-col :span="17" :offset="0"
          >
            <el-checkbox-group v-model="article_type" @change="handleFilter" style="float:left;">

              <el-checkbox label="Books and Documents"/>
              <el-checkbox label="Clinical Trial"/>
              <el-checkbox label="Meta-Analysis"/>
              <el-checkbox label="Randomized Controlled Trial"/>
              <el-checkbox label="Review"/>
              <el-checkbox label="Systematic Review"/>

            </el-checkbox-group>
          </el-col>

        </el-row>
        <!--  <el-row :gutter="20" style="height:40px;">
            <el-col :span="3" :offset="2"
            ><div style="float:left;font-weight :bold;" >ARTICLE TYPE</div>
            </el-col>
            <el-col :span="17" :offset="0"
            ><el-checkbox-group v-model="article_type" @change="filter" style="float:left;">

              <el-checkbox label="Option D" />
              <el-checkbox label="Option B" />
              <el-checkbox label="Option C" />
              <el-checkbox label="Option A" />
              <el-checkbox label="Option B" />
              <el-checkbox label="Option C" />

            </el-checkbox-group>
            </el-col>

          </el-row>-->
        <el-row :gutter="20" style="height:45px;">
          <el-col :span="3" :offset="2"
          >
            <div style="float:left;font-weight :bold;">LANGUAGE</div>
          </el-col>
          <el-col :span="6" :offset="0"
          >
            <el-checkbox-group v-model="language" @change="handleFilter" style="float:left;">

              <el-checkbox label="English"/>
              <el-checkbox label="Others"/>

            </el-checkbox-group>
          </el-col>
        </el-row>
        <el-row :gutter="20" style="height:45px;">
          <el-col :span="3" :offset="2"
          >
            <div style="float:left;font-weight :bold;">SPECIES</div>
          </el-col>
          <el-col :span="6" :offset="0"
          >
            <el-checkbox-group v-model="species" @change="handleFilter" style="float:left;">

              <el-checkbox label="Humans"/>
              <el-checkbox label="Other Animals"/>

            </el-checkbox-group>
          </el-col>
        </el-row>
        <el-row :gutter="20" style="height:45px;">
          <el-col :span="3" :offset="2"
          >
            <div style="float:left;font-weight :bold;">SEX</div>
          </el-col>
          <el-col :span="6" :offset="0"
          >
            <el-checkbox-group v-model="sex" @change="handleFilter" style="float:left;">

              <el-checkbox label="Female"/>
              <el-checkbox label="Male"/>

            </el-checkbox-group>
          </el-col>
        </el-row>
        <el-row :gutter="20" style="height:45px;">
          <el-col :span="3" :offset="2"
          >
            <div style="float:left;font-weight :bold;"><span style="color: crimson">AGE</span></div>
          </el-col>
          <el-col :span="6" :offset="0"
          >
            <el-checkbox-group v-model="age" @change="handleFilter" style="float:left;">
              <el-row>
                <el-col :span="3" >
                  <el-checkbox label="Humans"/>
                </el-col>
                <el-col :span="3" :offset="10">
                  <el-checkbox label="Other Animals"/>
                </el-col>
              </el-row>
            </el-checkbox-group>
          </el-col>
        </el-row>
        <el-row :gutter="20" style="height:45px;">
          <el-col :span="3" :offset="2"
          >
            <div style="float:left;font-weight :bold;">PUBLICATION DATE</div>
          </el-col>
          <el-col :span="6" :offset="0">
            <div class="block">
              <el-date-picker
                  v-model="publication_date"
                  type="daterange"
                  unlink-panels
                  range-separator="至"
                  start-placeholder="开始日期"
                  end-placeholder="结束日期"
                  value-format="yyyy-MM-dd"
                  size="small"
                  :picker-options="pickerOptions">
              </el-date-picker>
            </div>
          </el-col>
          <!--          <el-col :span="2" :offset="9">-->
          <!--            <el-button type="primary" round @click="handleSearch">高级检索</el-button>-->
          <!--          </el-col>-->

        </el-row>
      </el-collapse-item>
    </el-collapse>
    <p></p>
    <el-row :gutter="5">
      <el-col :span="2" :offset="2">
        <div style="height:30px;">历史搜索记录</div>
        <!--        <div v-for="history in history_list" style="height:30px;">{{history}}</div>-->
      </el-col>
      <el-col :span="16" :offset="2">
        <div>

          <el-tabs type="border-card">
            <el-tab-pane label="Paple_info">

              <!--              <el-table :data="paper_info" style="width: 100% "  height=600>-->
              <!--                <el-table-column type="expand">-->
              <!--                  <template #default="props">-->
              <!--                    <div m="4">-->
              <!--                      <p v-for="(item,key) in props.row" v-show="item">{{key }}:{{ item }}</p>-->
              <!--                    </div>-->
              <!--                  </template>-->
              <!--                </el-table-column>-->
              <!--                <el-table-column label="Title" prop="Title" width="400" />-->
              <!--                <el-table-column label="Date" prop="Publication_Date"  width="100" sortable/>-->
              <!--                <el-table-column label="First_Author" prop="First_Author"  width="200" />-->
              <!--                <el-table-column label="Keywords" prop="Keywords" />-->
              <!--              </el-table>-->
              <el-row :gutter="20">
                <el-col :span="12" :offset="6" justify="center">
                  <!--                  <el-pagination-->
                  <!--                      layout="prev, pager, next"-->
                  <!--                      :page-size="20"-->
                  <!--                      :hide-on-single-page="true"-->
                  <!--                      :total="changePage.total"-->
                  <!--                      @current-change="handleCurrentChange"-->
                  <!--                      v-model:currentPage="changePage.currentPage"-->
                  <!--                  >-->
                  <!--                  </el-pagination>-->
                </el-col>

              </el-row>
            </el-tab-pane>
            <el-tab-pane label="Clue_info">
              <!--              <el-table :data="clue_info" style="width: 100% "  height=600>-->
              <!--                <el-table-column type="expand">-->
              <!--                  <template #default="props">-->
              <!--                    <div m="4">-->
              <!--                      <p v-for="(item,key) in props.row" v-show="item">{{key }}:{{ item }}</p>-->
              <!--                    </div>-->
              <!--                  </template>-->
              <!--                </el-table-column>-->
              <!--                <el-table-column label="Node1" prop="Node1" sortable />-->
              <!--                <el-table-column label="Edge_Type" prop="Edge_Type"   sortable/>-->
              <!--                <el-table-column label="Node2" prop="Node2"   sortable/>-->
              <!--                <el-table-column label="Weight" prop="Weight" width="100" sortable/>-->
              <!--                <el-table-column label="Paper_List" prop="Paper_List" sortable/>-->
              <!--              </el-table>-->
              <el-row :gutter="20">
                <el-col :span="12" :offset="6"
                >
                  <el-pagination layout="prev, pager, next" :total="5" :hide-on-single-page="true"/>
                </el-col>
              </el-row>
            </el-tab-pane>
            <el-tab-pane label="Network">network</el-tab-pane>

          </el-tabs>
        </div>
      </el-col>

    </el-row>


  </div>
</template>

<script>

import qs from "qs";
import md5 from "js-md5";

export default {
  // name: 'HomeView',
  // components: {
  //
  // },
  data() {
    return {
      activeIndex: '0',
      input: '',
      activeNames: ['1'],
      article_type: [],
      species: [],
      language: [],
      sex: [],
      age: [],
      publication_date: [],
      pickerOptions: {
        shortcuts: [{
          text: '最近一个月',
          onClick(picker) {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
            picker.$emit('pick', [start, end]);
          }
        }, {
          text: '最近三个月',
          onClick(picker) {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 91);
            picker.$emit('pick', [start, end]);
          }
        }, {
          text: '最近六个月',
          onClick(picker) {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 183);
            picker.$emit('pick', [start, end]);
          }
        }, {
          text: '最近一年',
          onClick(picker) {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 365);
            picker.$emit('pick', [start, end]);
          }
        },]
      },

    };
  },
  methods: {
    gotoLogin(){
      this.$router.push('login')
    },
    gotoRegister(){
      this.$router.push('register')
    },
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
    },
    handleSearch() {
      if (this.input === ''){
        this.$message('输入不能为空');
      }
      else {
        let token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1dWlkIjoiMDAxIiwiZXhwIjoxNjU1NDUzMzg2LjEyODI2LCJzYWx0IjoiU3RldmUyMzVMYWIifQ.vLmc5nNmJc4xBN83CMneKEYG2GmIDan-p_fP91n7WTE";
        var that=this;
        that.axios({
          method:"post",
          url:"http://42.192.44.52:8000/search/",
          data:qs.stringify({
            "token": token,
            "message_type": 'search',
            "keywords": this.input,
            "start_time": this.publication_date[0],
            "end_time": this.publication_date[1],
            "filters": [
              {
                "article_type": this.article_type,
                "language": this.language,
                "species": this.species,
                "sex": this.sex,
                "age": this.age,
              }
            ]
          })
        })
            .then(function(res){
              console.log(res);
            })
            .catch(function(err){
              console.log(err)
            })
        this.input = '';
        this.species = [];
        this.filters = [];
        this.publication_date = [];
      }

    },
    // handleChange(val) {
    //   console.log(val);
    // }
    handleFilter(val) {
      console.log(val);

    }
  }
}

</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0;
}

.input-with-select {
  background-color: #fff;
}
</style>
