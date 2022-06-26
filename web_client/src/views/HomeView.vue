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
              v-model="keywords"
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
            <el-checkbox-group v-model="article_type" style="float:left;">

              <el-checkbox label="Books and Documents"/>
              <el-checkbox label="Clinical Trial"/>
              <el-checkbox label="Meta-Analysis"/>
              <el-checkbox label="Randomized Controlled Trial"/>
              <el-checkbox label="Review"/>
              <el-checkbox label="Systematic Review"/>

            </el-checkbox-group>
          </el-col>

        </el-row>
        <el-row :gutter="20" style="height:45px;">
          <el-col :span="3" :offset="2"
          >
            <div style="float:left;font-weight :bold;">AGE</div>
          </el-col>
          <el-col :span="17" :offset="0"
          >
            <el-checkbox-group v-model="age" style="float:left;">
              <el-checkbox label="Child: birth-18 years"/>
              <el-checkbox label="Newborn: birth-1 month"/>
              <el-checkbox label="Infant: birth-23 months"/>
              <el-checkbox label="Infant: 1-23 months"/>
              <el-checkbox label="Preschool Child: 2-5 years"/>


            </el-checkbox-group>
          </el-col>
        </el-row>
        <el-row :gutter="20" style="height:40px;">
          <el-col :span="3" :offset="2"
          >&emsp;</el-col>
          <el-col :span="17" :offset="0"
          >
            <el-checkbox-group v-model="age" style="float:left;">
              <el-checkbox label="Child: 6-12 years"/>
              <el-checkbox label="Adolescent: 13-18 years" />
              <el-checkbox label="Adult: 19+ years" />
              <el-checkbox label="Young Adult: 19-24 years" />
              <el-checkbox label="Adult: 19-44 years" />
            </el-checkbox-group>
          </el-col>
        </el-row>
        <el-row :gutter="20" style="height:40px;">
          <el-col :span="3" :offset="2"
          >&emsp;</el-col>
          <el-col :span="17" :offset="0"
          >
            <el-checkbox-group v-model="age" style="float:left;">
              <el-checkbox label="Middle Aged + Aged: 45+ years"/>
              <el-checkbox label="Middle Aged: 45-64 years" />
              <el-checkbox label="Aged: 65+ years" />
              <el-checkbox label="80 and over: 80+ years" />
            </el-checkbox-group>
          </el-col>
        </el-row>
        <el-row :gutter="20" style="height:45px;">
          <el-col :span="3" :offset="2"
          >
            <div style="float:left;font-weight :bold;">LANGUAGE</div>
          </el-col>
          <el-col :span="6" :offset="0"
          >
            <el-checkbox-group v-model="language" style="float:left;">

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
            <el-checkbox-group v-model="species" style="float:left;">

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
            <el-checkbox-group v-model="sex" style="float:left;">

              <el-checkbox label="Female"/>
              <el-checkbox label="Male"/>

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
        <el-button @click="test">test</el-button>
        <!--        <div v-for="history in history_list" style="height:30px;">{{history}}</div>-->
      </el-col>
      <el-col :span="16" :offset="2">
        <div>

          <el-tabs type="border-card">
            <el-tab-pane label="Paple_info">
              <el-table
                  :data="result"
                  style="width: 100%"
                  height=600>
                <el-table-column type="expand">
                  <template slot-scope="props">
                    <div v-for="(row,item) in props.row" :key="row" v-show="row!==''">
                      <p>
                        <el-row :gutter="10">
                          <el-col :span="5" >
                            <span class="table-expand-label" v-if="item==='Chinese_Title'">&emsp;中文标题 : </span>
                            <span class="table-expand-label" v-else-if="item==='Chinese_Abstract'">&emsp;中文摘要 : </span>
                            <span class="table-expand-label" v-else>&emsp;{{item}} : </span>
                          </el-col>
                          <el-col :span="19" >
                            <b  v-if="item==='Title'||item ==='Chinese_Title'">{{ row }}</b>
                            <i  v-else-if="item==='Authors'||item==='First_Author'||item==='Corresponding_Author'"
                                style="font-family: 'Times New Roman'">{{ row }}</i>
                            <span  v-else>{{ row }}</span>
                          </el-col>
                        </el-row>


                      </p>

                    </div>

<!--                    <el-form label-position="left" inline class="demo-table-expand">-->
<!--                      <el-form-item label="Title">-->
<!--                        <b>{{ props.row.Title }}</b>-->
<!--                      </el-form-item>-->
<!--                      <el-form-item label="PMID">-->
<!--                        <span>{{ props.row.Pmid }}</span>-->
<!--                      </el-form-item>-->
<!--                      <el-form-item label="Journal">-->
<!--                        <span>{{ props.row.Journal }}</span>-->
<!--                      </el-form-item>-->
<!--                      <el-form-item label="Publication_Type">-->
<!--                        <span>{{ props.row.Publication_Type }}</span>-->
<!--                      </el-form-item>-->
<!--                      <el-form-item label="Publication_Year">-->
<!--                        <span>{{ props.row.Publication_Year }}</span>-->
<!--                      </el-form-item>-->
<!--                      <el-form-item label="Publication_Date">-->
<!--                        <span>{{ props.row.Publication_Date }}</span>-->
<!--                      </el-form-item>-->
<!--                      <el-form-item label="First_Author">-->
<!--                        <i>{{ props.row.First_Author }}</i>-->
<!--                      </el-form-item>-->
<!--                      <el-form-item label="Corresponding_Author">-->
<!--                        <i>{{ props.row.Corresponding_Author }}</i>-->
<!--                      </el-form-item>-->
<!--                      <el-form-item label="Authors">-->
<!--                        <i>{{ props.row.Authors }}</i>-->
<!--                      </el-form-item>-->
<!--                      <el-form-item label="Affiliations">-->
<!--                        <span>{{ props.row.Affiliations }}</span>-->
<!--                      </el-form-item>-->
<!--                      <el-form-item label="Abstract">-->
<!--                        <span>{{ props.row.Abstract }}</span>-->
<!--                      </el-form-item>-->
<!--                      <el-form-item label="Keywords">-->
<!--                        <span>{{ props.row.Keywords }}</span>-->
<!--                      </el-form-item>-->
<!--                      <el-form-item label="Doi">-->
<!--                        <span>{{ props.row.Doi }}</span>-->
<!--                      </el-form-item>-->
<!--                      <el-form-item label="Conclusion">-->
<!--                        <span>{{ props.row.Conclusion }}</span>-->
<!--                      </el-form-item>-->
<!--                      <el-form-item label="Journal_If">-->
<!--                        <span>{{ props.row.Journal_If }}</span>-->
<!--                      </el-form-item>-->
<!--                      <el-form-item label="中文标题">-->
<!--                        <span>{{ props.row.Chinese_Title }}</span>-->
<!--                      </el-form-item>-->
<!--                      <el-form-item label="中文摘要">-->
<!--                        <span>{{ props.row.Chinese_Abstract }}</span>-->
<!--                      </el-form-item>-->
<!--                      <el-form-item label="Sample_Size">-->
<!--                        <span>{{ props.row.Sample_Size }}</span>-->
<!--                      </el-form-item>-->
<!--                      <el-form-item label="Location">-->
<!--                        <span>{{ props.row.Location }}</span>-->
<!--                      </el-form-item>-->
<!--                      <el-form-item label="Organization">-->
<!--                        <span>{{ props.row.Organization }}</span>-->
<!--                      </el-form-item>-->
<!--                    </el-form>-->
                  </template>
                </el-table-column>
                <el-table-column label="Title" prop="Title" sortable width="400">
                </el-table-column>
                <el-table-column label="Date" prop="Publication_Date" sortable>
                </el-table-column>
                <el-table-column label="Pmid" prop="Pmid" sortable>
                </el-table-column>
                <el-table-column label="Journal" prop="Journal" sortable>
                </el-table-column>
                <el-table-column label="Journal_If" prop="Journal_If" sortable>
                </el-table-column>

              </el-table>

              <el-row :gutter="20">
                <el-col :span="12" :offset="6" justify="center">
                  <el-pagination @current-change="handleCurrentChange"
                                 :current-page="currentInfo.currentNumber" :page-size="20" :hide-on-single-page="true"
                                 layout="total, prev, pager, next ,jumper" :total="currentInfo.total">
                  </el-pagination>


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
import axios from "axios";
import example from "../../../docs/example.json"

export default {
  // name: 'HomeView',
  // components: {
  //
  // },
  data() {
    let token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1dWlkIjoiMCIsImV4cCI6MTY1NjIyODY0MS42NzkwNjg2LCJzYWx0IjoiU3RldmUyMzVMYWIifQ.ZG08WrLQNMliQwMx4LSRhNyjn05IOS3U7e9HzM1Ys8E";
    let timestamp = 114514;
    return {
      token,
      timestamp,
      activeIndex: '0',
      keywords: '',
      article_type: [],
      species: [],
      language: [],
      sex: [],
      age: [],
      publication_date: [],
      activeNames: ['1'],

      pickerOptions: {
        disabledDate(time) {
          return time.getTime() > Date.now() - 8.64e6
        },
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
      history:[],
      result:[],
      example,
      currentInfo: {
        total: 100,
        // 当前页数
        currentNumber: 1,
      }

    };
  },
  mounted() {
    this.newpageInfo()
  },
  methods: {
    test(){
      var that = this;
      that.axios({
        method:"get",
        url:"http://42.192.44.52:8000/search/history/",
        params:{
          message_type: "get_history",
          token: this.token
        }
      })
          .then(function (res){
            console.log(res)
            console.log('连接成功')
            that.result = res.data.data
            that.token = res.data.token
            console.log(that.result)
            console.log(that.token)
            console.log(res.data)
          })
          .catch(function(err){
            console.log(err)
            console.log('连接失败')
          })
    },
    // 监听 页码值 改变的事件
    handleCurrentChange(newPage) {
      console.log(newPage)
      //把最新的页码（newPage）赋值给 动态的 pagenum
      this.currentInfo.currentNumber = newPage
      //获取到最新显示的页码值  重新发送axios请求 这里是封装好的请求方法
      this.newpageInfo()
    },



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
      if (this.keywords === ''){
        this.$message('输入不能为空');
      }
      else {

        var that=this;
        that.axios({
          method:"post",
          url:"http://42.192.44.52:8000/search/",
          data:qs.stringify({
            "token": this.token,
            "message_type": "search",
            "keywords": this.keywords,
            "start_time": this.publication_date[0],
            "end_time": this.publication_date[1],
            "article_type": this.article_type,
            "language": this.language,
            "species": this.species,
            "sex": this.sex,
            "age": this.age

          })
        })
            .then(function(res){
              console.log(res);
              console.log(res.data)
            })
            .catch(function(err){
              console.log(err)
            })
        this.keywords = '';
        this.species = [];
        this.age = [];
        this.sex = [];
        this.publication_date = [];
      }

    },

    // newpageInfo() {
    //   var that=this;
    //   that.axios({
    //     method:"post",
    //     url:"http://42.192.44.52:8000/search/",
    //     data:qs.stringify({
    //       "token": this.token,
    //       "message_type": 'get_result',
    //       "timestamp": this.timestamp,
    //       "page_num": this.currentInfo.currentNumber
    //     })
    //   })
    //       .then(function(res){
    //         console.log(res);
    //         console.log(res.data)
    //       })
    //       .catch(function(err){
    //         console.log(err)
    //       })
    //
    // }
    newpageInfo(){
      if(this.currentInfo.currentNumber===1){
        this.result = example.paper_info_1
      }
      if(this.currentInfo.currentNumber===2){
        this.result = example.paper_info_2
      }
      if(this.currentInfo.currentNumber===3){
        this.result = example.paper_info_3
      }
      if(this.currentInfo.currentNumber===4){
        this.result = example.paper_info_4
      }
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

.table-expand-label {
  width: 180px;
  display:-moz-inline-box;
  display:inline-block;
  color: #A9A9A9;
}
</style>
