<template>
  <div id="app" style="overflow-x: hidden">
<!--    导航栏-->
   <el-menu
        :default-active="activeIndex"
        class="el-menu-demo"
        mode="horizontal"
        background-color="#20558a"
        text-color="#fff"
        active-text-color="#b4c8e0">
      <el-menu-item style="font-size: 16px" index="0">HOME</el-menu-item>
     <template v-if="userName">
       <el-menu-item  style="float: right;font-size: 16px" @click="dialogVisible = true">退出</el-menu-item>
       <el-menu-item  style="float: right;font-size: 16px" >欢迎登录！{{ userName }}</el-menu-item>

       <el-dialog
           :visible.sync="dialogVisible"
           width="30%">
         <span>确定退出登录吗？</span>
         <span slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible = false">取 消</el-button>
            <el-button type="danger" @click="gotoLogin">确 定</el-button>
          </span>
       </el-dialog>

     </template>
     <template v-else>
       <el-menu-item  style="float: right" @click="gotoLogin">登录</el-menu-item>
       <el-menu-item  style="float: right" @click="gotoRegister">注册</el-menu-item>
     </template>

    </el-menu>
    <div id="body">
      <!--    搜索框-->
      <el-row :gutter="20">
        <el-col :span="14" :offset="5">
          <div style="margin-top: 15px;">
            <el-input
                placeholder="请输入搜索关键词"
                v-model="keywords"
                class="input-with-select"
                clearable
                @keyup.enter.native="handleSearch"
                style="height:40px;"
                autocomplete="on">
              <el-button slot="append"  @click="handleSearch">
                <i class="el-icon-search" style="color:cornflowerblue" />
              </el-button>
            </el-input>
          </div>
        </el-col>
      </el-row>
      <p></p>
  <!--    筛选条件-->
      <!--        文章类型-->
      <el-row :gutter="20" type="flex" justify="space-around" style="flex-wrap: wrap;flex-direction: row">
        <el-col :sm="24" :md="4" :lg="3" >
          <div style="float:left;font-weight :bold;">ARTICLE TYPE</div>
        </el-col>
        <el-col  :sm="24" :md="20" :lg="21" >
          <el-checkbox-group v-model="article_type" style="float:left;" >

            <el-checkbox label="Books and Documents"/>
            <el-checkbox label="Clinical Trial"/>
            <el-checkbox label="Meta-Analysis"/>
            <el-checkbox label="Randomized Controlled Trial"/>
            <el-checkbox label="Review"/>
            <el-checkbox label="Systematic Review"/>

          </el-checkbox-group>
        </el-col>
      </el-row>
      <p></p>
      <!--        发表时间-->
      <el-row :gutter="20" type="flex" justify="space-around" style="flex-wrap: wrap;flex-direction: row">
        <el-col :xs="24" :sm="24" :md="4" :lg="3" >
          <div style="float:left;font-weight :bold;">PUBLICATION DATE</div>
        </el-col>
        <el-col :xs="23" :sm="23" :md="19" :lg="20" >
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
        <el-col :xs="1" :sm="1" :md="1" :lg="1">
          <el-link v-show="!hidden_flag" class="el-icon-arrow-down" @click="handleHidden" :underline="false"></el-link>
          <el-link v-show="hidden_flag" class="el-icon-arrow-up" @click="handleHidden" :underline="false"></el-link>
        </el-col>

      </el-row>

      <!--    筛选条件折叠-->
          <!--        年龄-->
      <p></p>
      <div v-show="hidden_flag">
          <el-row :gutter="20" type="flex" justify="space-around" style="flex-wrap: wrap;flex-direction: row">
            <el-col :sm="24" :md="4" :lg="3">
              <div style="float:left;font-weight :bold;">AGE</div>
            </el-col>
            <el-col :sm="24" :md="20" :lg="21">
              <el-checkbox-group v-model="age" style="float:left;">
                <el-checkbox label="0-18y" >Child: birth-18 years</el-checkbox>
                <el-checkbox label="0-1m">Newborn: birth-1 month</el-checkbox>
                <el-checkbox label="0-23m">Infant: birth-23 months</el-checkbox>
                <el-checkbox label="1-23m">Infant: 1-23 months</el-checkbox>
                <el-checkbox label="2-5y">Preschool Child: 2-5 years</el-checkbox>
                <el-checkbox label="6-12y">Child: 6-12 years</el-checkbox>
                <el-checkbox label="13-18y" >Adolescent: 13-18 years</el-checkbox>
                <el-checkbox label="19+y" >Adult: 19+ years</el-checkbox>
                <el-checkbox label="19-24y">Young Adult: 19-24 years</el-checkbox>
                <el-checkbox label="19-44y" >Adult: 19-44 years</el-checkbox>
                <el-checkbox label="45+y">Middle Aged + Aged: 45+ years</el-checkbox>
                <el-checkbox label="45-64y" >Middle Aged: 45-64 years</el-checkbox>
                <el-checkbox label="65+y" >Aged: 65+ years</el-checkbox>
                <el-checkbox label="80+y" >80 and over: 80+ years</el-checkbox>
              </el-checkbox-group>
            </el-col>
          </el-row>
          <p></p>
          <!--        语言-->
          <el-row :gutter="20" type="flex" justify="space-around" style="flex-wrap: wrap;flex-direction: row">
            <el-col :sm="24" :md="4" :lg="3">
              <div style="float:left;font-weight :bold;">LANGUAGE</div>
            </el-col>
            <el-col :sm="24" :md="20" :lg="21">
              <el-checkbox-group v-model="language" style="float:left;">

                <el-checkbox label="English"/>
                <el-checkbox label="Others"/>

              </el-checkbox-group>
            </el-col>
          </el-row>
          <p></p>
          <!--        物种-->
          <el-row :gutter="20" type="flex" justify="space-around" style="flex-wrap: wrap;flex-direction: row">
            <el-col :sm="24" :md="4" :lg="3">
              <div style="float:left;font-weight :bold;">SPECIES</div>
            </el-col>
            <el-col :sm="24" :md="20" :lg="21">
              <el-checkbox-group v-model="species" style="float:left;">

                <el-checkbox label="Humans"/>
                <el-checkbox label="Other Animals"/>

              </el-checkbox-group>
            </el-col>
          </el-row>
          <p></p>
          <!--        性别-->
          <el-row :gutter="20" type="flex" justify="space-around" style="flex-wrap: wrap;flex-direction: row">
            <el-col :sm="24" :md="4" :lg="3">
              <div style="float:left;font-weight :bold;">SEX</div>
            </el-col>
            <el-col :sm="24" :md="20" :lg="21">
              <el-checkbox-group v-model="sex" style="float:left;">

                <el-checkbox label="Female"/>
                <el-checkbox label="Male"/>

              </el-checkbox-group>
            </el-col>
          </el-row>
      </div>
      <p></p>
  <!--    历史记录及结果显示-->
      <el-row :gutter="20" type="flex" justify="space-around" style="flex-wrap: wrap;flex-direction: row">
  <!--      历史记录-->
        <el-col :sm="24" :md="history_lg+1" :lg="history_lg" >
          <el-card :body-style="{ padding: '0px' }" class="box-card" style="max-height: 650px">
            <div slot="header" class="clearfix" style="text-align:center;">
              <span >当前可查看</span>
              <el-link :underline="false"
                       @click="getHistory"
                       icon="el-icon-refresh"
                       style="font-size: 17px;float: right; padding: 3px 0"
              ></el-link>
            </div>
            <div style="max-height: 650px;min-height: 300px;word-break:break-all; white-space: pre-line;padding-left: 10px;padding-right: 10px">
              <div v-for="(row,item) in history" :key="item" style="text-align:left;">
                <el-tooltip effect="dark" placement="right">
                  <div slot="content" class="tips" style="word-wrap:break-word;width: 400px;line-height: 20px" >
                    <b>{{row.robust_keywords}}</b>
                  </div>
                  <el-link :underline="false" :disabled="paper_disable" @click="gettimestamp(row.timestamp)" style="font-size: 16px;line-height: 18px;padding-top: 10px">
                      {{row.raw_keywords}}

                  </el-link>
                </el-tooltip>
              </div>
            </div>
          </el-card>

        </el-col>

  <!--      结果显示-->
        <el-col :sm="24" :md="result_lg-1" :lg="result_lg">
  <!--        paper_info/clue_info/network标签页-->
          <div>

            <el-row :gutter="5" type="flex" justify="space-around" style="flex-wrap: wrap;flex-direction: row">
              <el-col :xs="22" :sm="15" :md="12" :lg="12">
                <div style="margin-top: 15px;float: left">
                  <el-radio-group v-model="tabselect" @change="TabSelect" size="small" >
                    <el-radio-button label="Paper Info" :disabled=paper_disable></el-radio-button>
                    <el-radio-button label="Clue Info" :disabled=clue_disable></el-radio-button>
                    <el-radio-button label="Network" :disabled=network_disable></el-radio-button>
                  </el-radio-group>
                  &emsp;
                  <el-link class="el-icon-download" :underline="false" style="font-size: 25px" @click="downloadVisible=true"></el-link>
                  <el-dialog
                      title="请选择需要下载的文件"
                      :visible.sync="downloadVisible"
                      width="30%">
                      <el-radio v-model="downloadList" label="paper_info.xlsx">Paper Info</el-radio>
                      <el-radio v-model="downloadList" label="clue_info.xlsx">Clue Info</el-radio>
                      <el-radio v-model="downloadList" label="web_session.zip">Network</el-radio>
                    <span slot="footer" class="dialog-footer">
                      <el-button @click="downloadVisible = false">取 消</el-button>
                      <el-button type="primary" @click="download">确 定</el-button>
                    </span>
                  </el-dialog>
                </div>
              </el-col>
              <el-col :span="2">

              </el-col>
              <el-col :xs="24" :sm="7" :md="10" :lg="10">
                <div style="margin-top: 15px;float: right">
                  <el-input
                      placeholder="请输入Pmid"
                      v-model="Pmid_input"
                      class="input-with-select"
                      clearable
                      size="small"
                      @keyup.enter.native="Search_Pmid"
                      autocomplete="on">
                    <el-button slot="append" icon="el-icon-search" @click="Search_Pmid"></el-button>
                  </el-input>
<!--                  <el-dropdown>-->
<!--                    <el-button type="success" size="small" @command="download">-->
<!--                      <b>download</b><i class="el-icon-arrow-down el-icon&#45;&#45;right"></i>-->
<!--                    </el-button>-->
<!--                    <el-dropdown-menu slot="dropdown">-->
<!--                      <el-dropdown-item command="paper_info.xlsx">Paper Info</el-dropdown-item>-->
<!--                      <el-dropdown-item command="clue_info.xlsx">Clue Info</el-dropdown-item>-->
<!--                      <el-dropdown-item command="web_session.zip">Network</el-dropdown-item>-->
<!--                    </el-dropdown-menu>-->
<!--                  </el-dropdown>-->
                </div>
              </el-col>
            </el-row>
            <p></p>
            <el-tabs  v-model="editableTabsValue"  @tab-click="handleClick" type="border-card" closable @tab-remove="removeTab">
              <el-tab-pane

                  v-for="(item, index) in editableTabs"
                  :key="index"
                  :label="item.title"
                  :name="item.name"
              >
                <component
                    :is=item.content
                    :loading.sync="loading"
                    :paper_result="paper_result"
                    :clue_result="clue_result"
                    :network_data="network_data"
                    :paper_details="paper_details[item.index]"
                    :drawSelect="drawSelect"
                    :drawOptions="drawOptions"
                    :paper_page="paper_page_Info.currentNumber"
                    :paper_total="paper_page_Info.total"
                    :clue_page="clue_page_Info.currentNumber"
                    :clue_total="clue_page_Info.total"
                    @changesort_paper="changeSort_paper"
                    @changesort_clue="changeSort_clue"
                    @update_paper="handleCurrentChange1"
                    @update_clue="handleCurrentChange2"
                    @paper_details="getpaperdetails"
                ></component>
              </el-tab-pane>
            </el-tabs>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import network_result from "../../../test_data/asd.bfs.json"
import example from "../../../test_data/example_test.json"
import history_test from "../../../test_data/history_test.json"
import qs from "qs";
import G6 from '@antv/g6';

import Paper_info from "@/components/paper_info";
import Clue_info from "@/components/clue_info";
import Network from "@/components/network";
import Paper_details from "@/components/paper_details";


export default {
  components: {
    Paper_info,
    Clue_info,
    Network,
    Paper_details
  },

  data() {
    return {
      hidden_flag: false,
      token:'',
      userName:'',
      paper_disable:false,
      clue_disable:false,
      network_disable:false,
      paper_tab:'off',
      clue_tab:'off',
      network_tab:'off',
      loading:true,
      dialogVisible: false,
      downloadVisible:false,
      history_lg:24,
      result_lg:0,
      timestamp:'',
      tabselect:'',
      paper_index:-1,
      activeIndex: '0',
      activeState:'',
      keywords: '',
      article_type: [],
      articleType:[],
      species: [],
      language: [],
      sex: [],
      age: [],
      publication_date: [],
      downloadList:'',
      tabName:'',
      editableTabsValue: '',
      editableTabs: [],
      tabIndex:0,
      paper_tabIndex:0,
      clue_tabIndex:0,
      network_tabIndex:0,

      pickerOptions: {
        disabledDate(time) {
          return time.getTime() > Date.now() - 8.64e6
        },
      shortcuts: [{
          text: '近一年',
          onClick(picker) {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 365);
            picker.$emit('pick', [start, end]);
          }
        },{
        text: '近五年',
        onClick(picker) {
          const end = new Date();
          const start = new Date();
          start.setTime(start.getTime() - 3600 * 1000 * 24 * (365 * 5 + 1));
          picker.$emit('pick', [start, end]);
        }
      }, {
        text: '近十年',
        onClick(picker) {
          const end = new Date();
          const start = new Date();
          start.setTime(start.getTime() - 3600 * 1000 * 24 * (365 * 10 + 2));
          picker.$emit('pick', [start, end]);
        }
      }]
      },
      history:[],
      paper_result:[],
      clue_result:[],
      paper_details:[],
      network_data:[],
      selected_network:{nodes: [], edges: []},
      paper_column:'Publication_Date',
      paper_order:'reverse',
      clue_column:'Weight',
      clue_order:'reverse',
      paper_page_Info: {
        total: 0,
        currentNumber: 1,
      },
      clue_page_Info: {
        total: 0,
        currentNumber: 1,
      },
      drawSelect: '',
      drawOptions: [],
      Pmid:'',
      Pmid_input:'',
      message_type: '',

    };
  },
  created() {
    this.token = window.localStorage.getItem('token');
    this.userName = window.localStorage.getItem('userName');
  },
  mounted() {
    // this.keyDown()
    this.getHistory();

  },
  computed: {


  },
  watch:{
    token(newToken){
      window.localStorage.setItem('token',newToken)
    },
    message_type(new_message){
      if(new_message==="token_expired"){
        this.gotoLogin()
        this.$message({
          showClose: true,
          message: '登录已过期，请重新登录！',
          type: 'error'
        })
      }else if(new_message==="Network Error"){
        this.$message({
          showClose: true,
          message: '连接错误，请重试！',
          type: 'error'
        });
      }
    },
    age(test){
      console.log(test)
    }

  },
  methods: {
    handleHidden(){
      this.hidden_flag=!this.hidden_flag
      console.log(this.hidden_flag)
    },

    //获取历史记录
    getHistory(){
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
            that.message_type = res.data.message_type
            if(res.data.message_type==="history_list"){
              console.log(res.data)
              console.log(res)
              if(res.data.history==='[]')
              console.log('test')
            }
            that.history = res.data.history
            that.token = res.data.token
          })
          .catch(function(err){
            console.log(err)
            console.log('连接失败')
            that.message_type = err.message;
          })
    },

    //下载
    download(filename) {
      console.log(this.downloadList)
      this.downloadVisible=false
      var that=this;
      that.axios({
        method:"get",
        url:"http://42.192.44.52:8000/search/download/",
        params:{
          message_type: 'download',
          token: this.token,
          timestamp:this.timestamp,
          file_name:this.downloadList,
        }

      })

          .then(function(res){
            console.log(res)
            location.href="http://42.192.44.52:8000/search/download/"
                + "?token=" + that.token
                + "&timestamp=" + that.timestamp
                + "&file_name=" + that.downloadList
          })
          .catch(function(err){
            console.log(err)
          })
    },

    //监听结果显示标签页选择事件
    handleClick(tab, event) {
      console.log('tab：',tab);
      console.log('event',event)
      console.log(tab.name)
    },

    TabSelect(tab){
      console.log('tab：',tab);
      if(tab==='Paper Info'){
        this.addTab('paper')
        this.tabselect=''
      }
      else if(tab==='Clue Info'){
        this.addTab('clue')
        this.tabselect=''
      }
      else if(tab==='Network'){
        this.addTab('network')
        this.tabselect=''
      }

    },

    //增加标签页
    addTab(newTab) {
      let newTabName = ++this.tabIndex + '';
      if(newTab==='paper'){
        this.paper_tab='on';
        this.paper_tabIndex=newTabName
        this.paper_page_Info.currentNumber=1
        this.history_lg=0;
        this.result_lg=24;
        this.paperInfo()
        this.paper_disable = true
        this.editableTabs.push({
          title: 'Paper Info ',
          name: newTabName,
          content: Paper_info
        });
      }
      else if(newTab==='clue'){
        this.clue_tab='on';
        this.clue_tabIndex=newTabName
        this.clue_page_Info.currentNumber=1
        this.clueInfo()
        this.clue_disable = true
        this.editableTabs.push({
          title: 'Clue Info ',
          name: newTabName,
          content: Clue_info
        });
      }
      else if(newTab==='network'){
        this.network_tab='on';
        this.network_tabIndex=newTabName
        this.clue_page_Info.currentNumber = 0;
        this.clueInfo()
        this.network_disable = true
        this.editableTabs.push({
          title: 'Network ',
          name: newTabName,
          content: Network
        });
      }
      else{
        this.editableTabs.push({
          title: newTab,
          name: newTabName,
          index: ++this.paper_index,
          content: Paper_details
        });
        console.log(this.editableTabs)
      }

      this.editableTabsValue = newTabName;
    },

    //关闭标签页
    removeTab(targetName) {
      console.log(targetName)
      let tabs = this.editableTabs;
      let activeName = this.editableTabsValue;
      if(targetName===this.paper_tabIndex){
        this.paper_tab='off'
        this.paper_disable=false;
      }else if(targetName===this.clue_tabIndex){
        this.clue_tab='off'
        this.clue_disable=false;
      }else if(targetName===this.network_tabIndex){
        this.network_tab='off';
        this.network_disable=false;
      }
      if(this.paper_disable===false&&this.clue_disable===false&&this.network_disable===false){
        this.history_lg=3;
        this.result_lg=21;
      }
      if (activeName === targetName) {
        tabs.forEach((tab, index) => {
          if (tab.name === targetName) {
            let nextTab = tabs[index + 1] || tabs[index - 1];
            if (nextTab) {
              activeName = nextTab.name;
            }
          }
        });
      }
      this.editableTabsValue = activeName;
      this.editableTabs = tabs.filter(tab => tab.name !== targetName);
    },

    //获取时间戳并获取该记录的paper_info
    gettimestamp(timestamp){
      this.timestamp = timestamp
      console.log(this.timestamp)
      this.addTab('paper')
    },

    // 监听paper_info页码值改变的事件
    handleCurrentChange1(newPage) {
      console.log('当前paper_info页码为：',newPage)
      //把最新的页码（newPage）赋值给 动态的 pagenum
      this.paper_page_Info.currentNumber = newPage
      //获取到最新显示的页码值  重新发送axios请求 这里是封装好的请求方法
      this.paperInfo()
    },

    // 监听clue_info页码值改变的事件
    handleCurrentChange2(newPage) {
      console.log('当前clue_info页码为：',newPage)
      //把最新的页码（newPage）赋值给 动态的 pagenum
      this.clue_page_Info.currentNumber = newPage
      //获取到最新显示的页码值  重新发送axios请求 这里是封装好的请求方法
      this.clueInfo()
    },


    //跳转至登录页面
    gotoLogin(){
      window.localStorage.setItem('userName', '')
      this.$router.push('login')
    },

    //跳转至注册页面
    gotoRegister(){
      this.$router.push('register')
    },

    //提交搜索请求
    handleSearch() {
      if (this.keywords === ''){
        this.$message({
          showClose: true,
          message: '输入不能为空',
          type: 'error'
        });
      }
      else {
        console.log('发送搜索请求')
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
            "article_type": JSON.stringify(this.article_type),
            "language": JSON.stringify(this.language),
            "species": JSON.stringify(this.species),
            "sex": JSON.stringify(this.sex),
            "age": JSON.stringify(this.age)

          })
        })
            .then(function(res){
              that.message_type = res.data.message_type
              console.log(res)
              if(res.data.message_type==="search_received"){
                that.$message({
                  showClose: true,
                  message: '您已成功提交搜索，稍后将于邮箱通知您！',
                  type: 'success'
                });
                that.token = res.data.token
              }
            })
            .catch(function(err){
              console.log(err)
              that.message_type = err.message;
            })
        this.keywords = '';
        this.species = [];
        this.language = [];
        this.article_type = [];
        this.age = [];
        this.sex = [];
        this.publication_date = [];
        this.activeState = ''
      }

    },

    //获取当前页paper_info数据
    paperInfo() {
      this.loading=true
      console.log('请求paper数据')
      console.log(this.timestamp);
      var that=this;
      that.axios({
        method:"post",
        url:"http://42.192.44.52:8000/search/paper_info/",
        data:qs.stringify({
          "token": this.token,
          "message_type": "get_paper_info",
          "timestamp": this.timestamp,
          "page_num": this.paper_page_Info.currentNumber,
          "column": this.paper_column,
          "order": this.paper_order,
        })
      })
          .then(function(res){
            console.log(res);
            console.log('连接成功');
            console.log(res.data)
            that.message_type = res.data.message_type;
            if(res.data.message_type==="paper_info"){
              that.loading=false
              that.paper_result=res.data.paper_info
              that.paper_page_Info.total=res.data.total
              that.token = res.data.token
              if(that.paper_tab==='on'){
                that.paper_disable = true
              }
            }
          })
          .catch(function(err){
            console.log(err)
            that.paper_disable=false;
            that.message_type = err.message;
            that.paper_result = example.paper_info_4 //测试用
          })

    },

    //获取当前页clue_info数据
    clueInfo() {
      this.loading=true
      console.log('请求clue数据')
      var that=this;
      that.axios({
        method:"post",
        url:"http://42.192.44.52:8000/search/clue_info/",
        data:qs.stringify({
          "token": this.token,
          "message_type": "get_clue_info",
          "timestamp": this.timestamp,
          "page_num": this.clue_page_Info.currentNumber,
          'column': this.clue_column,
          'order': this.clue_order
          // "page_num": 1
        })
      })
          .then(function(res){
            console.log(res);
            console.log('连接成功');
            that.message_type = res.data.message_type;
            if (res.data.message_type=== "clue_info"){
              that.loading=false
              that.clue_result=res.data.clue_info
              that.clue_page_Info.total=res.data.total
              that.token = res.data.token
              if(that.clue_tab==='on'){
                that.clue_disable = true
              }
            }
            else if(res.data.message_type==="network"){
              that.loading=false
              that.network_data = res.data.clue_info
              that.drawOptions = res.data.edge_type_list
              that.token = res.data.token
              if(that.network_tab==='on'){
                that.network_disable = true
              }
            }
          })
          .catch(function(err){
            console.log(err)
            that.message_type = err.message;
            that.clue_result = network_result //测试用
            that.network_data = network_result  //测试用
            that.drawOptions = ["BFS","anatomy","antibody_to_anatomy", "bacteria","bacteria_to_anatomy","bacteria_to_antibody","bacteria_to_chemical","bacteria_to_disease","bacteria_to_mechanism","bacteria_to_nutrient","chemical","chemical_to_anatomy","chemical_to_disease","chemical_to_mechanism","disease","disease_to_anatomy","disease_to_antibody","disease_to_mechanism","mechanism","mechanism_to_anatomy","mechanism_to_antibody","nutrient_to_anatomy","nutrient_to_chemical","nutrient_to_disease","nutrient_to_mechanism"]

          })

    },

    //更改paper_info排序方式
    changeSort_paper(column){
      this.paper_page_Info.currentNumber=1;
      this.paper_column=column[0];
      this.paper_order=column[1];
      this.paperInfo()
    },

    //更改clue_info排序方式
    changeSort_clue(column){
      this.clue_page_Info.currentNumber=1;
      this.clue_column=column[0];
      this.clue_order=column[1];
      this.clueInfo()
    },


    // 搜索文章详情
    Search_Pmid(){
      this.Pmid=this.Pmid_input
      this.getpaperdetails(this.Pmid)
      this.Pmid_input = ''
    },

    //获取单篇文章详情
    getpaperdetails(pmid){
      console.log("pmid:",pmid)
      console.log('请求单篇paper数据')
      this.loading=true
      var that=this;
      that.axios({
        method:"post",
        url:"http://42.192.44.52:8000/search/paper_details/",
        data:qs.stringify({
          "token": this.token,
          "message_type": "get_paper_details",
          "timestamp": this.timestamp,
          "pmid": pmid
        })
      })
          .then(function(res){
            console.log(res);
            console.log('连接成功');
            that.message_type = res.data.message_type;
            if(res.data.message_type==="paper_details"){
              that.paper_details.push(res.data.paper_info)
              console.log(that.paper_details)
              that.Pmid = res.data.Pmid
              that.token = res.data.token
              that.addTab(that.Pmid)
              that.loading = false
            }
          })
          .catch(function(err){
            that.message_type = err.message;
            console.log(err)
          })
    },

  }
}

</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /*text-align: center;*/

  margin-top: 0;

}

#body{
  margin-left:3%;
  margin-right:3%;
  line-height:30px;
}

.input-with-select {
  background-color: #fff;
}



.el-collapse-item__arrow{
  float : left;
  margin-left:5px;
  margin-right:15px;
}

.el-table .cell {
  white-space: pre-line;
}
.el-card__header {
  padding: 10px 10px;
  border-bottom: 1px solid #EBEEF5;
  box-sizing: border-box;
}
.el-button--success {
  color: #FFF;
  background-color: #51a34d;
  border-color: #51a34d;
}
</style>
