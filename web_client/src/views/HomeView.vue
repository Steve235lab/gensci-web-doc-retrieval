<template>
  <div id="app">
<!--    导航栏-->
   <el-menu
        :default-active="activeIndex"
        class="el-menu-demo"
        mode="horizontal"
        background-color="#20558a"
        text-color="#fff"
        active-text-color="#b4c8e0">
      <el-menu-item index="0">HOME</el-menu-item>
      <el-menu-item index="1" style="float: right" @click="gotoLogin">登录</el-menu-item>
      <el-menu-item index="2" style="float: right" @click="gotoRegister">注册</el-menu-item>
    </el-menu>
<!--    搜索框-->
    <el-row :gutter="20">
      <el-col :span="12" :offset="6">
        <div style="margin-top: 15px;">
          <el-input
              placeholder="请输入搜索关键词"
              v-model="keywords"
              class="input-with-select"
              clearable
              style="height:40px;"
              autocomplete="on">
            <el-button slot="append" icon="el-icon-search" @click="handleSearch"></el-button>
          </el-input>
        </div>
      </el-col>
    </el-row>
<!--    筛选条件折叠面板-->
    <el-collapse style="display:inline;" v-model="activeState">
      <el-collapse-item >
<!--        文章类型-->
        <el-row :gutter="20" style="height:45px;">
          <el-col :span="3" :offset="2"
          >
            <div style="float:left;font-weight :bold;">ARTICLE TYPE</div>
          </el-col>
          <el-col :span="17" :offset="0"
          >
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
<!--        年龄-->
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
<!--        语言-->
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
<!--        性别-->
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
<!--        发表时间-->
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
<!--    历史记录及结果显示-->
    <el-row :gutter="5">
<!--      历史记录-->
      <el-col :span="3" :offset="2" >
        <div style="height:30px;text-align:left;">
          当前可查看
          <el-link :underline="false" @click="getHistory" icon="el-icon-refresh" style="font-size: 17px"></el-link>
        </div>
        <div style="height: 650px;overflow:auto">
          <div v-for="(row,item) in history" :key="item" style="text-align:left">
            <el-tooltip effect="dark" placement="right">
              <div slot="content" class="tips" style="word-wrap:break-word;width: 400px;line-height: 20px" >
                <b>{{row.robust_keywords}}</b>
              </div>
              <el-link :underline="false" @click="gettimestamp(row.timestamp)">
                <p class="content" style="font-size: 16px;line-height: 10px">
                  &emsp;{{row.raw_keywords}}
                </p>
              </el-link>
            </el-tooltip>
          </div>
        </div>
      </el-col>
<!--      结果显示-->
      <el-col :span="16" :offset="1">
<!--        paper_info/clue_info/network标签页-->
        <div>
          <el-tabs type="border-card" @tab-click="handleClick" v-model="tabName">
<!--            paper_info-->
            <el-tab-pane label="Paple_info" name="paper">
              <el-table
                  :data="paper_result"
                  style="width: 100%"
                  height=600>
                <el-table-column type="expand">
<!--                  折叠面板-文章详情-->
                  <template slot-scope="props">
                    <div v-for="(row,item) in props.row" :key="row" v-show="row">
                      <p>
                        <el-row :gutter="10">
<!--                          左侧标题-->
                          <el-col :span="5" >
                            <span class="table-expand-label" v-if="item==='Chinese_Title'">&emsp;中文标题 : </span>
                            <span class="table-expand-label" v-else-if="item==='Chinese_Abstract'">&emsp;中文摘要 : </span>
                            <span class="table-expand-label" v-else>&emsp;{{item}} : </span>
                          </el-col>
<!--                          右侧具体内容及格式-->
                          <el-col :span="19" >
                            <b  v-if="item==='Title'||item ==='Chinese_Title'">{{ row }}</b>
                            <i  v-else-if="item==='Authors'||item==='First_Author'||item==='Corresponding_Author'"
                                style="font-family: 'Times New Roman',serif">{{ row }}</i>
                            <span  v-else-if="item==='Abstract'" v-html="row"></span>
                            <span  v-else>{{ row }}</span>
                          </el-col>
                        </el-row>


                      </p>

                    </div>
                  </template>
<!--                  表格纵列-->
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
                  <el-pagination @current-change="handleCurrentChange1"
                                 :current-page="paper_page_Info.currentNumber" :page-size="10" :hide-on-single-page="true"
                                 layout="total, prev, pager, next ,jumper" :total="paper_page_Info.total">
                  </el-pagination>
                </el-col>
              </el-row>
            </el-tab-pane>
<!--            clue_info-->
            <el-tab-pane label="Clue_info" name="clue">
              <el-table
                  :data="clue_result"
                  style="width: 100%"
                  height=600>
<!--                折叠面板-->
                <el-table-column type="expand">
                  <template slot-scope="props">
                    <div v-for="(row,item) in props.row" :key="row" v-show="row">
                      <p>
                        <el-row :gutter="10">
                          <el-col :span="5" >
                            <span class="table-expand-label">&emsp;{{item}} : </span>
                          </el-col>
                          <el-col :span="19" >
                            <span>{{ row }}</span>
                          </el-col>
                        </el-row>


                      </p>

                    </div>
                  </template>
                </el-table-column>
<!--                表格纵列-->
                <el-table-column label="Node1" prop="Node1" sortable />
                <el-table-column label="Edge_Type" prop="Edge_Type"   sortable/>
                <el-table-column label="Node2" prop="Node2"   sortable/>
                <el-table-column label="Weight" prop="Weight" width="100" sortable/>
                <el-table-column label="Paper_List" prop="Paper_List" sortable/>

              </el-table>
              <el-row :gutter="20">
                <el-col :span="12" :offset="6" justify="center">
                  <el-pagination @current-change="handleCurrentChange2"
                                 :current-page="clue_page_Info.currentNumber" :page-size="20" :hide-on-single-page="true"
                                 layout="total, prev, pager, next ,jumper" :total="clue_page_Info.total">
                  </el-pagination>
                </el-col>
              </el-row>
            </el-tab-pane>
<!--            network-->
            <el-tab-pane label="Network" name="network">
              <div id="network" style="width: 100%;height: 600px"></div>
            </el-tab-pane>

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
import example from "../../../docs/example_test.json"
import G6 from '@antv/g6';
let graph ;

export default {

  data() {

    let token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1dWlkIjoiMCIsImV4cCI6MTY1NjM4ODUwOS41NjA4NDk0LCJzYWx0IjoiU3RldmUyMzVMYWIifQ.Bs3Sg47ULyMi-OgCYyQeRE44f9UbdyLn6njIVtQZ1Oo";
    let timestamp = 114514;
    return {
      token,
      timestamp,
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
      tabName:'',

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
      clue:{nodes:[],edges:[]},
      paper_page_Info: {
        total: 0,
        currentNumber: 1,
      },
      clue_page_Info: {
        total: 0,
        currentNumber: 1,
      }

    };
  },
  mounted() {
    this.keyDown()
    this.getHistory();
    graph = new G6.Graph({
          container: 'network',
          width: 980,
          height: 600,
          // 是否开启画布自适应。开启后图自动适配画布大小。
          fitView: true,
          //v3.5.1 后支持。开启后，图将会被平移，图的中心将对齐到画布中心，但不缩放。优先级低于 fitView
          fitCenter: true,
          // 节点默认配置
          defaultNode: {
            labelCfg: {
              position: 'bottom',
              offset: 3,
              style: {
                fill: '#000',
              },
            },
          },
          // 边默认配置
          defaultEdge: {
            labelCfg: {
              refY: 7,
              autoRotate: true,
            },
          },
          // 节点在各状态下的样式
          nodeStateStyles: {
            // hover 状态为 true 时的样式
            hover: {
              fill: 'lightsteelblue',
            },
            // click 状态为 true 时的样式
            click: {
              stroke: '#000',
              lineWidth: 3,
            },
          },
          // 边在各状态下的样式
          edgeStateStyles: {
            // click 状态为 true 时的样式
            click: {
              stroke: 'steelblue',
            },
          },
          // 布局
          layout: {
            type: 'force',
            linkDistance: 100,
            preventOverlap: true,
            nodeStrength: -30,
            edgeStrength: 0.1,
          },
          // 内置交互
          modes: {
            default: ['drag-canvas', 'zoom-canvas', 'drag-node'],
          },
        });
  },
  computed: {
    // 计算属性的 getter
    // reversedHistory: function () {
    //   // `this` 指向 vm 实例
    //   return this.history.reverse()
    // }
  },
  methods: {
    // 监听键盘
    keyDown() {
      document.onkeydown =  (e) => {
        if (e && e.keyCode === 13) {
          this.handleSearch()
        }
      }
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

            that.history = res.data.history
            that.token = res.data.token
            if(res.data.message_type==="token_expired"){
              that.$message({
                showClose: true,
                message: '登录已过期，请重新登录！',
                type: 'error'
              });
            }
            console.log(that.history)
            console.log(that.token)
            console.log(res.data)
          })
          .catch(function(err){
            console.log(err)
            console.log('连接失败')
            if(err.message==="Network Error"){
              that.$message({
                showClose: true,
                message: '连接错误，请重试！',
                type: 'error'
              });
            }
          })
    },
    //监听结果显示标签页选择事件
    handleClick(tab, event) {
      console.log('tab：',tab);
      console.log('event',event)
      console.log(tab.name)
      if(tab.name==='paper'){
        console.log('请求paper数据')
        this.paper_page_Info.currentNumber=1
        this.paperInfo()
      }
      if(tab.name==='clue'){
        console.log('请求clue数据')
        this.clue_page_Info.currentNumber=1
        this.clueInfo()
      }
      if(tab.name==='network'){
        console.log('请求network数据')
        this.clue_page_Info.currentNumber=0
        this.clueInfo()
        console.log('开始绘图')
        this.draw_network()
      }
    },
    //获取时间戳并获取该记录的paper_info
    gettimestamp(timestamp){
      this.timestamp = timestamp
      console.log(this.timestamp)
      this.tabName = 'paper'
      this.paperInfo()
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
              console.log(res);
              console.log('已成功发送搜索请求');
              console.log(res.data)
              if(res.data.message_type==="token_expired"){
                that.$message({
                  showClose: true,
                  message: '登录已过期，请重新登录！',
                  type: 'error'
                });
              }
              else if(res.data.message_type==="search_received"){
                that.$message({
                  showClose: true,
                  message: '您已成功提交搜索，稍后将于邮箱通知您！',
                  type: 'success'
                });
              }
            })
            .catch(function(err){
              console.log(err)
              if(err.message==="Network Error"){
                that.$message({
                  showClose: true,
                  message: '连接错误，请重试！',
                  type: 'error'
                });
              }
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
          "page_num": this.paper_page_Info.currentNumber
          // "page_num": 1
        })
      })
          .then(function(res){
            console.log(res);
            console.log('连接成功');
            console.log(res.data)
            if(res.data.message_type==="token_expired"){
              that.$message({
                showClose: true,
                message: '登录已过期，请重新登录！',
                type: 'error'
              });
            }
            that.paper_result=res.data.paper_info
            that.paper_page_Info.total=res.data.total
          })
          .catch(function(err){
            console.log(err)
            if(err.message==="Network Error"){
              that.$message({
                showClose: true,
                message: '连接错误，请重试！',
                type: 'error'
              });
            }
          })

    },
    //获取当前页clue_info数据
    clueInfo() {
      console.log('请求clue数据')
      var that=this;
      that.axios({
        method:"post",
        url:"http://42.192.44.52:8000/search/clue_info/",
        data:qs.stringify({
          "token": this.token,
          "message_type": "get_clue_info",
          "timestamp": this.timestamp,
          "page_num": this.clue_page_Info.currentNumber
          // "page_num": 1
        })
      })
          .then(function(res){
            console.log(res);
            console.log('连接成功');
            if(res.data.message_type==="token_expired"){
              that.$message({
                showClose: true,
                message: '登录已过期，请重新登录！',
                type: 'error'
              });
            }
            console.log(res.data)
            that.clue_result=res.data.clue_info
            that.clue_page_Info.total=res.data.total
            that.draw_network()
          })
          .catch(function(err){
            console.log(err)
            if(err.message==="Network Error"){
              that.$message({
                showClose: true,
                message: '连接错误，请重试！',
                type: 'error'
              });
            }
          })

    },
    //绘制network网络图
    getdrawInfo(){
      var index_n = 0;
      var index_e = 0;
      this.clue_result.forEach((clue_info) => {
        console.log(clue_info);
        if(!this.clue.nodes[index_n]){
          this.clue.nodes[index_n]={};
        }
        this.clue.nodes[index_n].id = clue_info.Node1;
        this.clue.nodes[index_n].label = clue_info.Node1;
        index_n++;
        if(!this.clue.nodes[index_n]){
          this.clue.nodes[index_n]={};
        }
        this.clue.nodes[index_n].id = clue_info.Node2;
        this.clue.nodes[index_n].label = clue_info.Node2;
        index_n++;
        if(!this.clue.edges[index_e]){
          this.clue.edges[index_e]={};
        }
        this.clue.edges[index_e].source = clue_info.Node1;
        this.clue.edges[index_e].target = clue_info.Node2;
        this.clue.edges[index_e].weight = clue_info.Weight;
        this.clue.edges[index_e].label = clue_info.Paper_List;
        index_e++;
      });
    },
    draw_network(){
      this.getdrawInfo();

      const nodes = this.clue.nodes;
      const edges = this.clue.edges;
      nodes.forEach((node) => {
        if (!node.style) {
          node.style = {};
        }
        node.style.lineWidth = 1;
        node.style.stroke = '#666';
        node.style.fill = 'steelblue';
      });
      edges.forEach((edge) => {
        if (!edge.style) {
          edge.style = {};
        }
        edge.style.lineWidth = edge.weight;
        edge.style.opacity = 0.6;
        edge.style.stroke = 'grey';
      });

      graph.data(this.clue);
      graph.render();

      // 监听鼠标进入节点
      graph.on('node:mouseenter', (e) => {
        const nodeItem = e.item;
        // 设置目标节点的 hover 状态 为 true
        graph.setItemState(nodeItem, 'hover', true);
      });
      // 监听鼠标离开节点
      graph.on('node:mouseleave', (e) => {
        const nodeItem = e.item;
        // 设置目标节点的 hover 状态 false
        graph.setItemState(nodeItem, 'hover', false);
      });
      // 监听鼠标点击节点
      graph.on('node:click', (e) => {
        // 先将所有当前有 click 状态的节点的 click 状态置为 false
        const clickNodes = graph.findAllByState('node', 'click');
        clickNodes.forEach((cn) => {
          graph.setItemState(cn, 'click', false);
        });
        const nodeItem = e.item;
        // 设置目标节点的 click 状态 为 true
        graph.setItemState(nodeItem, 'click', true);
      });
      // 监听鼠标点击节点
      graph.on('edge:click', (e) => {
        // 先将所有当前有 click 状态的边的 click 状态置为 false
        const clickEdges = graph.findAllByState('edge', 'click');
        clickEdges.forEach((ce) => {
          graph.setItemState(ce, 'click', false);
        });
        const edgeItem = e.item;
        // 设置目标边的 click 状态 为 true
        graph.setItemState(edgeItem, 'click', true);
      });
    }
    // draw_network(){
    //   const remoteData = {
    //
    //     "nodes": [
    //       {"id": "0", "label": "n0", "class": "c0" },
    //       {"id": "1", "label": "n1", "class": "c0" },
    //       {"id": "2", "label": "n2", "class": "c0" },
    //       {"id": "3", "label": "n3", "class": "c0" },
    //       {"id": "4", "label": "n4", "class": "c0" },
    //       {"id": "5", "label": "n5", "class": "c0" },
    //       {"id": "6", "label": "n6", "class": "c1"},
    //       {"id": "7", "label": "n7", "class": "c1"},
    //       {"id": "8", "label": "n8", "class": "c1" },
    //       {"id": "9", "label": "n9", "class": "c1" },
    //       {"id": "10", "label": "n10", "class": "c1" },
    //       {"id": "11", "label": "n11", "class": "c1" },
    //       {"id": "12", "label": "n12", "class": "c1" },
    //       {"id": "13", "label": "n13", "class": "c2" },
    //       {"id": "14", "label": "n14", "class": "c2" },
    //       {"id": "15", "label": "n15", "class": "c2" },
    //       {"id": "16", "label": "n16", "class": "c2" },
    //       {"id": "17", "label": "n17", "class": "c2" },
    //       {"id": "18", "label": "n18", "class": "c2" },
    //       {"id": "19", "label": "n19", "class": "c2" }
    //     ],
    //     "edges": [
    //       {"source": "0", "target": "1", "label": "e0-1", "weight": 1 },
    //       {"source": "0", "target": "2", "label": "e0-2", "weight": 2 },
    //       {"source": "0", "target": "3", "label": "e0-3", "weight": 3 },
    //       {"source": "0", "target": "4", "label": "e0-4", "weight": 1.4 },
    //       {"source": "0", "target": "5", "label": "e0-5", "weight": 2 },
    //       {"source": "0", "target": "7", "label": "e0-7", "weight": 2 },
    //       {"source": "0", "target": "8", "label": "e0-8", "weight": 2 },
    //       {"source": "0", "target": "9", "label": "e0-9", "weight": 1.3 },
    //       {"source": "0", "target": "10", "label": "e0-10", "weight": 1.5 },
    //       {"source": "0", "target": "11", "label": "e0-11", "weight": 1 },
    //       {"source": "0", "target": "13", "label": "e0-13", "weight": 10 },
    //       {"source": "0", "target": "14", "label": "e0-14", "weight": 2 },
    //       {"source": "0", "target": "15", "label": "e0-15", "weight": 0.5 },
    //       {"source": "0", "target": "16", "label": "e0-16", "weight": 0.8 },
    //       {"source": "2", "target": "3", "label": "e2-3", "weight": 1 },
    //       {"source": "4", "target": "5", "label": "e4-5", "weight": 1.4 },
    //       {"source": "4", "target": "6", "label": "e4-6", "weight": 2.1 },
    //       {"source": "5", "target": "6", "label": "e5-6", "weight": 1.9 },
    //       {"source": "7", "target": "13", "label": "e7-13", "weight": 0.5 },
    //       {"source": "8", "target": "14", "label": "e8-14", "weight": 0.8 },
    //       {"source": "9", "target": "10", "label": "e9-10", "weight": 0.2 },
    //       {"source": "10", "target": "14", "label": "e10-14", "weight": 1 },
    //       {"source": "10", "target": "12", "label": "e10-12", "weight": 1.2 },
    //       {"source": "11", "target": "14", "label": "e11-14", "weight": 1.2 },
    //       {"source": "12", "target": "13", "label": "e12-13", "weight": 2.1 },
    //       {"source": "16", "target": "17", "label": "e16-17", "weight": 2.5 },
    //       {"source": "16", "target": "18", "label": "e16-18", "weight": 3 },
    //       {"source": "17", "target": "18", "label": "e17-18", "weight": 2.6 },
    //       {"source": "18", "target": "19", "label": "e18-19", "weight": 1.6 }
    //     ]
    //
    //
    //   }
    //
    //   const nodes = remoteData.nodes;
    //   const edges = remoteData.edges;
    //   nodes.forEach((node) => {
    //     if (!node.style) {
    //       node.style = {};
    //     }
    //     node.style.lineWidth = 1;
    //     node.style.stroke = '#666';
    //     node.style.fill = 'steelblue';
    //     switch (node.class) {
    //       case 'c0': {
    //         node.type = 'circle';
    //         node.size = 30;
    //         break;
    //       }
    //       case 'c1': {
    //         node.type = 'rect';
    //         node.size = [35, 20];
    //         break;
    //       }
    //       case 'c2': {
    //         node.type = 'ellipse';
    //         node.size = [35, 20];
    //         break;
    //       }
    //     }
    //   });
    //   edges.forEach((edge) => {
    //     if (!edge.style) {
    //       edge.style = {};
    //     }
    //     edge.style.lineWidth = edge.weight;
    //     edge.style.opacity = 0.6;
    //     edge.style.stroke = 'grey';
    //   });
    //
    //   graph.data(remoteData);
    //   graph.render();
    //
    //   // 监听鼠标进入节点
    //   graph.on('node:mouseenter', (e) => {
    //     const nodeItem = e.item;
    //     // 设置目标节点的 hover 状态 为 true
    //     graph.setItemState(nodeItem, 'hover', true);
    //   });
    //   // 监听鼠标离开节点
    //   graph.on('node:mouseleave', (e) => {
    //     const nodeItem = e.item;
    //     // 设置目标节点的 hover 状态 false
    //     graph.setItemState(nodeItem, 'hover', false);
    //   });
    //   // 监听鼠标点击节点
    //   graph.on('node:click', (e) => {
    //     // 先将所有当前有 click 状态的节点的 click 状态置为 false
    //     const clickNodes = graph.findAllByState('node', 'click');
    //     clickNodes.forEach((cn) => {
    //       graph.setItemState(cn, 'click', false);
    //     });
    //     const nodeItem = e.item;
    //     // 设置目标节点的 click 状态 为 true
    //     graph.setItemState(nodeItem, 'click', true);
    //   });
    //   // 监听鼠标点击节点
    //   graph.on('edge:click', (e) => {
    //     // 先将所有当前有 click 状态的边的 click 状态置为 false
    //     const clickEdges = graph.findAllByState('edge', 'click');
    //     clickEdges.forEach((ce) => {
    //       graph.setItemState(ce, 'click', false);
    //     });
    //     const edgeItem = e.item;
    //     // 设置目标边的 click 状态 为 true
    //     graph.setItemState(edgeItem, 'click', true);
    //   });
    // }
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
