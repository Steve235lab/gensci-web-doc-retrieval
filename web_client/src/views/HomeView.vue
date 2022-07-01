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
              @keyup.enter.native="handleSearch"
              style="height:40px;"
              autocomplete="on">
            <el-button slot="append" icon="el-icon-search" @click="handleSearch"></el-button>
          </el-input>
        </div>
      </el-col>
    </el-row>
    <p></p>
<!--    筛选条件折叠面板-->

    <!--        文章类型-->
    <el-row :gutter="20" style="height:45px;">
      <el-col :span="3" :offset="2"
      >
        <div style="float:left;font-weight :bold;">ARTICLE TYPE</div>
      </el-col>
      <el-col :span="19" :offset="0"
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
    <!--        发表时间-->
    <el-row :gutter="20" style="height:40px;">
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
    <el-collapse style="display:inline;width: 1500px" v-model="activeState" >
      <el-collapse-item >
        <template slot="title">
          <div style="font-weight :bold;font-size: 16px;float: left">More Filters</div>
        </template>
        <!--        年龄-->
        <el-row :gutter="20" type="flex" style="height:45px;">
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
        <!--        语言-->
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
        <!--        物种-->
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

          <el-row :gutter="5">
            <el-col :span="6" >
              <div style="margin-top: 15px">
                <el-radio-group v-model="tabselect" @change="TabSelect" size="small">
                  <el-radio-button label="Paper Info"></el-radio-button>
                  <el-radio-button label="Clue Info"></el-radio-button>
                  <el-radio-button label="Network"></el-radio-button>
                </el-radio-group>
              </div>
            </el-col>
            <el-col :span="6">
              <div style="margin-top: 15px;">
                <el-input
                    placeholder="请输入Pmid"
                    v-model="Pmid"
                    class="input-with-select"
                    clearable
                    size="small"
                    @keyup.enter.native="Search_Pmid"
                    autocomplete="on">
                  <el-button slot="append" icon="el-icon-search" @click="Search_Pmid"></el-button>
                </el-input>
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
</template>

<script>
import network_result from "../../../test_data/network_test.json"
import qs from "qs";
import G6 from '@antv/g6';
import insertCss from 'insert-css';
import Paper_info from "@/components/paper_info";
import Clue_info from "@/components/clue_info";
import Network from "@/components/network";
import Paper_details from "@/components/paper_details";
insertCss(`
  .g6-component-tooltip {
    border: 1px solid #e2e2e2;
    border-radius: 4px;
    font-size: 16px;
    color: #000;
    background-color: rgba(255, 255, 255, 0.9);
    padding: 10px 8px;
    box-shadow: rgb(174, 174, 174) 0px 0px 10px;
  }
`);

let graph ;

export default {
  components: {
    Paper_info,
    Clue_info,
    Network,
    Paper_details
  },

  data() {

    let token = window.localStorage.getItem('token');
    let timestamp = 114514;
    return {
      token,
      timestamp,
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
      tabName:'',
      editableTabsValue: '',
      editableTabs: [],

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

    };
  },
  mounted() {
    // this.keyDown()
    this.getHistory();
    const tooltip = new G6.Tooltip({
      offsetX: 10,
      offsetY: 10,
      // v4.2.1 起支持配置 trigger，click 代表点击后出现 tooltip。默认为 mouseenter
      trigger: 'click',
      fixToNode: [1, 0.5],
      // the types of items that allow the tooltip show up
      // 允许出现 tooltip 的 item 类型
      itemTypes: ['node', 'edge'],
      // custom the tooltip's content
      // 自定义 tooltip 内容
      getContent: (e) => {
        const outDiv = document.createElement('div');
        outDiv.style.width = 'fit-content';
        outDiv.style.height = 'fit-content';
        const model = e.item.getModel();
        if (e.item.getType() === 'node') {
          outDiv.innerHTML = `${model.id}`;
        } else {
          // const source = e.item.getSource();
          // const target = e.item.getTarget();
          // outDiv.innerHTML = `来源：${source.getModel().name}<br/>去向：${target.getModel().name}`;
          outDiv.innerHTML = `Paper_List：${model.paper}<br/>Original_Text：${model.origin_text}`;
        }
        return outDiv;
      },
    });
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
          // opacity:'100%',
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
          fill: 'lightsteelblue',
          stroke: 'red',
          lineWidth: 2,
        },
      },
      // 边在各状态下的样式
      edgeStateStyles: {
        // click 状态为 true 时的样式
        click: {
          stroke: 'red',
          lineAppendWidth: 5,
        },
      },
      // 布局
      layout: {
        type: 'fruchterman',
        center: [200, 200], // 可选，默认为图的中心
        gravity: 0, // 可选
        speed: 2, // 可选
        clustering: true, // 可选
        clusterGravity: 5, // 可选
        maxIteration: 3000, // 可选，迭代次数
        workerEnabled: true, // 可选，开启 web-worker
        gpuEnabled: true, // 可选，开启 GPU 并行计算，G6 4.0 支持
        // linkDistance: 1000,
        preventOverlap: true,
        nodeStrength: -30,
        edgeStrength: 0.1,
      },
      // 内置交互
      modes: {
        default: ['drag-canvas', 'zoom-canvas', 'drag-node'],
      },
      // plugins: [minimap,legend],
      plugins: [tooltip],
    });
  },
  computed: {
    // 计算属性的 getter
    Pmid_separated: function (){
      return function (pmid){
        return Array.from(new Set(pmid.split('|')))
      }
    },
  },
  methods: {
    // 监听键盘
    // keyDown() {
    //   document.onkeydown =  (e) => {
    //     if (e && e.keyCode === 13) {
    //       this.handleSearch()
    //     }
    //   }
    // },

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
            if(res.data.message_type==="token_expired"){
              that.$message({
                showClose: true,
                message: '登录已过期，请重新登录！',
                type: 'error'
              });
            }else if(res.data.message_type==="history_list"){
              console.log(res.data)
              that.history = res.data.history
              that.token = res.data.token
            }
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
      // if(tab.name==='paper'){
      //   console.log('请求paper数据')
      //   this.paper_page_Info.currentNumber=1
      //   this.paperInfo()
      // }
      // if(tab.name==='clue'){
      //   console.log('请求clue数据')
      //   this.clue_page_Info.currentNumber=1
      //   this.clueInfo()
      // }
      // if(tab.name==='network'){
      //   console.log('请求network数据')
      //   this.clue_page_Info.currentNumber=0
      //   this.clueInfo()  //向后台请求数据并开始绘图
        // this.network_data = network_result //本地数据
        // this.draw_network()  //测试用
      // }
    },

    TabSelect(tab){
      console.log('tab：',tab);
      console.log(this.tabselect)
      if(tab==='Paper Info'){
        console.log('test')
        this.addTab('paper')
      }
      else if(tab==='Clue Info'){
        console.log('test')
        this.addTab('clue')
      }
      else if(tab==='Network'){
        console.log('test')
        this.addTab('network')
      }
    },

    //增加标签页
    addTab(newTabName) {
      if(newTabName==='paper'){
        this.paper_page_Info.currentNumber=1
        this.paperInfo()
        this.editableTabs.push({
          title: 'Paper Info',
          name: newTabName,
          content: Paper_info
        });
      }
      else if(newTabName==='clue'){
        this.clue_page_Info.currentNumber=1
        this.clueInfo()
        this.editableTabs.push({
          title: 'Clue Info',
          name: newTabName,
          content: Clue_info
        });
      }
      else if(newTabName==='network'){
        this.clue_page_Info.currentNumber = 0;
        this.clueInfo()
        this.editableTabs.push({
          title: 'Network',
          name: newTabName,
          content: Network
        });
      }
      else{
        this.editableTabs.push({
          title: newTabName,
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
      let tabs = this.editableTabs;
      let activeName = this.editableTabsValue;
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
    // 选择绘制的网络图
    select_network() {
      console.log(this.drawSelect)
      // this.draw_network()
      var nodeType_selector = this.drawSelect.split('_')
      if(nodeType_selector.length===1){
        this.draw_network(nodeType_selector[0],nodeType_selector[0])
      }else{
        this.draw_network(nodeType_selector[0],nodeType_selector[2])
      }
      console.log(nodeType_selector.length)
      console.log(nodeType_selector[0])
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
                that.token = res.data.token
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
          "page_num": this.paper_page_Info.currentNumber,
          "column": "Journal_If",
          "order": "reverse"
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
            }else if(res.data.message_type==="paper_info"){
              that.paper_result=res.data.paper_info
              that.paper_page_Info.total=res.data.total
              that.token = res.data.token
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
          "page_num": this.clue_page_Info.currentNumber,
          'column': "Weight",
          'order': "reverse"
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
            else if (res.data.message_type=== "clue_info"){
              that.clue_result=res.data.clue_info
              that.clue_page_Info.total=res.data.total
              that.token = res.data.token
            }
            else if(res.data.message_type==="network"){
              that.network_data = res.data.clue_info
              that.drawOptions = res.data.edge_type_list
              that.token = res.data.token
              that.draw_network()
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

    },

    // 搜索文章详情
    Search_Pmid(){
      this.getpaperdetails(this.Pmid)
      this.Pmid = ''
    },

    //获取单篇文章详情
    getpaperdetails(pmid){
      console.log("pmid:",pmid)
      console.log('请求单篇paper数据')
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
            if(res.data.message_type==="token_expired"){
              that.$message({
                showClose: true,
                message: '登录已过期，请重新登录！',
                type: 'error'
              });
            }else if(res.data.message_type==="paper_details"){
              that.paper_details.push(res.data.paper_info)
              console.log(that.paper_details)
              that.Pmid = res.data.Pmid
              that.token = res.data.token
              that.addTab(that.Pmid)
            }
            // console.log(res.data)



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
    //绘图数据预处理
    getdrawInfo(class1,class2) {
      this.selected_network = {nodes: [], edges: []};
      if(this.drawSelect==="BFS"){
        this.network_data.forEach((data) => {
          // console.log(data.is_BFS_edge)
          if(data.is_BFS_edge){
            var nodeType_selector = data.Edge_Type.split('_')
            if(nodeType_selector.length===1){
              var node1_type = nodeType_selector[0];
              var node2_type = nodeType_selector[0];
            }else{
              node1_type = nodeType_selector[0];
              node2_type = nodeType_selector[2];
            }
            this.selected_network.nodes.push({
              id: data.Node1,
              label: data.Node1,
              class: node1_type
            })
            this.selected_network.nodes.push({
              id: data.Node2,
              label: data.Node2,
              class: node2_type
            })
            this.selected_network.edges.push({
              source: data.Node1,
              target: data.Node2,
              weight: data.Weight,
              paper: data.Paper_List,
              origin_text: data.Original_Text
            })
          }
        });
      }else{
        this.network_data.forEach((data) => {
          // console.log(data.is_BFS_edge)
          if(data.Edge_Type===this.drawSelect&&data.is_BFS_edge){
            this.selected_network.nodes.push({
              id: data.Node1,
              label: data.Node1,
              class: class1
            })
            this.selected_network.nodes.push({
              id: data.Node2,
              label: data.Node2,
              class: class2
            })
            this.selected_network.edges.push({
              source: data.Node1,
              target: data.Node2,
              weight: data.Weight,
              paper: data.Paper_List,
              origin_text: data.Original_Text
            })
          }


        });
      }

      // if(this.selected_network.edges.length===0){
      //   this.$message({
      //     showClose: true,
      //     message: '无数据，请重新选择！',
      //     type: 'warning'
      //   });
      // }
    },
    //绘制network网络图
    draw_network(class1,class2) {

      this.getdrawInfo(class1,class2);

      const nodes = this.selected_network.nodes;
      const edges = this.selected_network.edges;
      if(edges.length===0) {
        this.$message({
          showClose: true,
          message: '无数据，请重新选择！',
          type: 'warning'
        });
      }

      nodes.forEach((node) => {
        if (!node.style) {
          node.style = {};
        }
        console.log(node.class)
        // node.style.lineWidth = 1;
        node.type = 'rect';
        node.size = [30, 30];
        node.style.radius = 8;
        node.style.stroke = '#fff';
        switch (node.class) {
          case "disease": {
            node.style.fill = '#c63225';
            break;
          }
          case "bacteria": {
            node.style.fill = '#fbeca0';
            break;
          }
          case "chemical": {
            node.style.fill = '#534eff';
            break;
          }
          case "mechanism": {
            node.style.fill = '#bdbddc';
            break;
          }
          case "anatomy": {
            node.style.fill = '#8c0412';
            break;
          }
          case "antibody": {
            node.style.fill = '#737373';
            break;
          }
          case "nutrient": {
            node.style.fill = '#85c375';
            break;
          }
          case class2: {
            node.style.fill = '#9ad0f5';
            break;
          }
          case class1: {
            node.style.fill = '#f5b89a';
            break;
          }
        }
      });
      edges.forEach((edge) => {
        if (!edge.style) {
          edge.style = {};
        }
        edge.style.lineWidth = edge.weight;
        edge.style.stroke = 'grey';
        if (edge.weight === '1') {
          edge.style.opacity = 0.1;
        } else {
          edge.style.opacity = 0.8;
        }

      });
      // graph.clear();
      graph.data(this.selected_network);
      graph.render();
      console.log("完成绘制")

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
        console.log(e.item);
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
        console.log(e.item._cfg);
      });
    }
  }
}

</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /*text-align: center;*/
  color: #2c3e50;
  margin-top: 0;
}

.input-with-select {
  background-color: #fff;
}



.el-collapse-item__arrow{
  float : left;
  margin-left:5px;
  margin-right:15px;
}
.el-collapse-item__header{
  margin-left:130px;
}


</style>
