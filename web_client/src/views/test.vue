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
              @keyup.enter.native="handleSearch"
              autocomplete="on">
            <el-button slot="append" icon="el-icon-search" @click="handleSearch"></el-button>
          </el-input>
        </div>
      </el-col>
    </el-row>
    <!--    筛选条件折叠面板-->
    <el-collapse style="display:inline;" v-model="activeState">
      <el-collapse-item>
        <!--        文章类型-->
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
          >&emsp;
          </el-col>
          <el-col :span="17" :offset="0"
          >
            <el-checkbox-group v-model="age" style="float:left;">
              <el-checkbox label="Child: 6-12 years"/>
              <el-checkbox label="Adolescent: 13-18 years"/>
              <el-checkbox label="Adult: 19+ years"/>
              <el-checkbox label="Young Adult: 19-24 years"/>
              <el-checkbox label="Adult: 19-44 years"/>
            </el-checkbox-group>
          </el-col>
        </el-row>
        <el-row :gutter="20" style="height:40px;">
          <el-col :span="3" :offset="2"
          >&emsp;
          </el-col>
          <el-col :span="17" :offset="0"
          >
            <el-checkbox-group v-model="age" style="float:left;">
              <el-checkbox label="Middle Aged + Aged: 45+ years"/>
              <el-checkbox label="Middle Aged: 45-64 years"/>
              <el-checkbox label="Aged: 65+ years"/>
              <el-checkbox label="80 and over: 80+ years"/>
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
      <el-col :span="3" :offset="2">
        <div style="height:30px;text-align:left;">
          当前可查看
          <el-link :underline="false" @click="getHistory" icon="el-icon-refresh-right"
                   style="font-size: 17px"></el-link>
        </div>
        <div v-for="(row,item) in history" :key="item" style="text-align:left;">
          <el-tooltip effect="dark" placement="right">
            <div slot="content" class="tips">
              {{ row.robust_keywords }}
            </div>
            <template>
              <el-link :underline="false" @click="gettimestamp(item)">
                <p class="content" style="font-size: 16px;line-height: 10px">
                  &emsp;{{ row.raw_keywords }}
                </p>
              </el-link>
            </template>
          </el-tooltip>
        </div>
      </el-col>
      <!--      结果显示-->
      <el-col :span="16" :offset="1">
        <!--        paper_info/clue_info/network标签页-->
        <div style="margin-bottom: 20px;">
          <el-button
              size="small"
              @click="addTab(editableTabsValue)"
          >
            add tab
          </el-button>
          <el-button
              size="small"
              @click="test"
          >
            paper info
          </el-button>
        </div>
        <el-tabs v-model="editableTabsValue"  @tab-click="handleClick" type="border-card" closable @tab-remove="removeTab">
          <el-tab-pane
              v-for="(item, index) in editableTabs"
              :key="index"
              :label="item.title"
              :name="item.name"
          >
            {{item.name}}
            <component
                :is=item.content
                :paper_result="paper_result"
                :paper_page.sync="paper_page_Info.currentNumber"
                @update_paper="handleCurrentChange1"
                @updata_clue="handleCurrentChange2"
                :paper_total="paper_page_Info.total"
                :clue_result="clue_result"
            ></component>
<!--            {{item.content}}-->
          </el-tab-pane>
          <!--            paper_info-->
<!--          <el-tab-pane>-->
<!--            <Paper_info :paper_result="paper_result" v-show="paper_info_Flag"></Paper_info>-->
<!--          </el-tab-pane>-->


        </el-tabs>
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
                          <el-col :span="5">
                            <span class="table-expand-label" v-if="item==='Chinese_Title'">&emsp;中文标题 : </span>
                            <span class="table-expand-label" v-else-if="item==='Chinese_Abstract'">&emsp;中文摘要 : </span>
                            <span class="table-expand-label" v-else>&emsp;{{ item }} : </span>
                          </el-col>
                          <!--                          右侧具体内容及格式-->
                          <el-col :span="19">
                            <b v-if="item==='Title'||item ==='Chinese_Title'">{{ row }}</b>
                            <i v-else-if="item==='Authors'||item==='First_Author'||item==='Corresponding_Author'"
                               style="font-family: 'Times New Roman',serif">{{ row }}</i>
                            <span v-else-if="item==='Abstract'||item==='Publication_Type'" v-html="row"></span>
                            <span v-else>{{ row }}</span>
                          </el-col>
                        </el-row>


                      </p>

                    </div>
                  </template>
                  <!--                  表格纵列-->
                </el-table-column>
                <el-table-column label="Title" prop="Title" sortable width="400"></el-table-column>
                <el-table-column label="Date" prop="Publication_Date" sortable></el-table-column>
                <el-table-column label="Pmid" prop="Pmid" sortable></el-table-column>
                <el-table-column label="Journal" prop="Journal" sortable width="150"></el-table-column>
                <el-table-column label="Journal_If" prop="Journal_If" sortable width="100"></el-table-column>
                <el-table-column label="Sample_Size" prop="Sample_Size" sortable width="100"></el-table-column>
                <el-table-column label="Publication_Type" prop="Publication_Type" sortable width="200"></el-table-column>

              </el-table>
              <el-row :gutter="20">
                <el-col :span="12" :offset="6" justify="center">
                  <el-pagination @current-change="handleCurrentChange1"
                                 :current-page="paper_page_Info.currentNumber" :page-size="20"
                                 :hide-on-single-page="true"
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
                          <el-col :span="5">
                            <span class="table-expand-label">&emsp;{{ item }} : </span>
                          </el-col>
                          <el-col :span="19">
                            <el-link v-if="item==='Paper_List'" @click="getpaperdetails(row)">{{row}}</el-link>
                            <span v-else>{{ row }}</span>
                          </el-col>
                        </el-row>
                      </p>

                    </div>
                  </template>
                </el-table-column>
                <!--                表格纵列-->
                <el-table-column label="Node1" prop="Node1" sortable/>
                <el-table-column label="Edge_Type" prop="Edge_Type" sortable/>
                <el-table-column label="Node2" prop="Node2" sortable/>
                <el-table-column label="Weight" prop="Weight" width="100" sortable/>
                <el-table-column label="Paper_List"  sortable>

                  <template slot-scope="props">
                    <div v-for="(row,item) in props.row" :key="item">
                      <span v-if="item==='Paper_List'">
                        <span v-for="pmid in Pmid_separated(row) " :key=pmid>
                          <el-link  @click="getpaperdetails(row)">{{pmid}}</el-link>&emsp;
                        </span>
                      </span>
                    </div>
<!--                    <el-link>{{props.row}}</el-link>-->
                  </template>

                </el-table-column>

              </el-table>
              <el-row :gutter="20">
                <el-col :span="12" :offset="6" justify="center">
                  <el-pagination @current-change="handleCurrentChange2"
                                 :current-page="clue_page_Info.currentNumber" :page-size="20"
                                 :hide-on-single-page="true"
                                 layout="total, prev, pager, next ,jumper" :total="clue_page_Info.total">
                  </el-pagination>
                </el-col>
              </el-row>
            </el-tab-pane>
            <!--            network-->
            <el-tab-pane label="Network" name="network">
              <el-select v-model="drawSelect" placeholder="请选择" @change="select_network" style="float: left">
                <el-option
                    v-for="item in drawOptions"
                    :key="item.Edge_Type"
                    :label="item.Edge_Type"
                    :value="item.Edge_Type">
                </el-option>
              </el-select>
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
import example from "../../../test_data/example_test.json"
import network_result from "../../../test_data/network_test.json"
import asd_net from "../../../test_data/asd.bfs.json"
import IL6_net from "../../../test_data/IL-6.bfs.json"
import paper_info from "@/components/paper_info";
import G6 from '@antv/g6';
import insertCss from 'insert-css';
import Paper_info from "@/components/paper_info";
import Clue_info from "@/components/clue_info";
insertCss(`
  .g6-component-tooltip {
    border: 1px solid #e2e2e2;
    border-radius: 4px;
    font-size: 12px;
    color: #000;
    background-color: rgba(255, 255, 255, 0.9);
    padding: 10px 8px;
    box-shadow: rgb(174, 174, 174) 0px 0px 10px;
  }
`);

let graph;

export default {
  components: {
    Paper_info,
    Clue_info
  },
  data() {

    let token = window.localStorage.getItem('token')
    let timestamp = 114514;

    return {
      token,
      timestamp,
      activeIndex: '0',
      activeState: '',
      keywords: '',
      article_type: [],
      articleType: [],
      species: [],
      language: [],
      sex: [],
      age: [],
      publication_date: [],
      tabName: '',

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
        }, {
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
      history: [],

      paper_info_Flag: 'false',
      paper_result: [],
      clue_result: [],
      network_data: [],
      selected_network:{nodes: [], edges: []},
      paper_page_Info: {
        total: 100,
        currentNumber: 1,
      },
      clue_page_Info: {
        total: 0,
        currentNumber: 1,
      },
      drawSelect: '',
      drawOptions: [{"Edge_Type": "BFS"},{"Edge_Type": "anatomy"}, {"Edge_Type": "antibody_to_anatomy"}, {"Edge_Type": "bacteria"}, {"Edge_Type": "bacteria_to_anatomy"}, {"Edge_Type": "bacteria_to_antibody"}, {"Edge_Type": "bacteria_to_chemical"}, {"Edge_Type": "bacteria_to_disease"}, {"Edge_Type": "bacteria_to_mechanism"}, {"Edge_Type": "bacteria_to_nutrient"}, {"Edge_Type": "chemical"}, {"Edge_Type": "chemical_to_anatomy"}, {"Edge_Type": "chemical_to_disease"}, {"Edge_Type": "chemical_to_mechanism"}, {"Edge_Type": "disease"}, {"Edge_Type": "disease_to_anatomy"}, {"Edge_Type": "disease_to_antibody"}, {"Edge_Type": "disease_to_mechanism"}, {"Edge_Type": "mechanism"}, {"Edge_Type": "mechanism_to_anatomy"}, {"Edge_Type": "mechanism_to_antibody"}, {"Edge_Type": "nutrient_to_anatomy"}, {"Edge_Type": "nutrient_to_chemical"}, {"Edge_Type": "nutrient_to_disease"}, {"Edge_Type": "nutrient_to_mechanism"}],
      editableTabsValue: '2',
      editableTabs: [{
        title: 'Tab 1',
        name: '1',
        content: Paper_info
      }, {
        title: 'Tab 2',
        name: '2',
        content: Clue_info
      }],
      tabIndex: 2
    }
  },
  mounted() {
    this.getHistory()
    // const minimap = new G6.Minimap();
    // const legend = new G6.Legend();
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
        style:{
          lineAppendWidth: 50,
        },
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
        // nodeSpacing: 50,
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
    Pmid_separated: function (){
      return function (pmid){
        // Array.from(new Set(pmid.split('|')))
        return Array.from(new Set(pmid.split('|')))
      }
    },
  },
  methods: {
    test(){
      console.log(this.paper_info_Flag)
      this.paper_info_Flag = !this.paper_info_Flag
      console.log(this.paper_info_Flag)
    },
    // getpaperdetails(pmid){
    //   console.log(pmid)
    // },
    //获取单篇文章详情
    getpaperdetails(pmid){
      console.log(pmid)
      // pmid=11938636
      // console.log(pmid)
      console.log('请求单篇paper数据')
      // var that=this;
      // that.axios({
      //   method:"post",
      //   url:"http://42.192.44.52:8000/search/paper_details/",
      //   data:qs.stringify({
      //     "token": this.token,
      //     "message_type": "get_paper_details",
      //     "timestamp": this.timestamp,
      //     "pmid": pmid
      //   })
      // })
      //     .then(function(res){
      //       console.log(res);
      //       console.log('连接成功');
      //       if(res.data.message_type==="token_expired"){
      //         that.$message({
      //           showClose: true,
      //           message: '登录已过期，请重新登录！',
      //           type: 'error'
      //         });
      //       }
      //       // console.log(res.data)
      //       that.paper_details=res.data.paper_info
      //       console.log(that.paper_details)
      //
      //     })
      //     .catch(function(err){
      //       console.log(err)
      //       if(err.message==="Network Error"){
      //         that.$message({
      //           showClose: true,
      //           message: '连接错误，请重试！',
      //           type: 'error'
      //         });
      //       }
      //     })
    },
    // 获取历史记录
    getHistory() {
      var that = this;
      that.axios({
        method: "get",
        url: "http://42.192.44.52:8000/search/history/",
        params: {
          message_type: "get_history",
          token: this.token
        }
      })
          .then(function (res) {
            console.log(res)
            console.log('连接成功')
            that.history = res.data.history
            that.token = res.data.token
            console.log(that.history)
            console.log(that.token)
            console.log(res.data)
          })
          .catch(function (err) {
            console.log(err)
            console.log('连接失败')
          })
    },

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

    addTab(targetName) {
      let newTabName = ++this.tabIndex + '';
      this.editableTabs.push({
        title: 'New Tab',
        name: newTabName,
        content: Paper_info
      });
      this.editableTabsValue = newTabName;
    },
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

    //监听结果显示标签页选择事件
    handleClick(tab, event) {
      console.log('tab：', tab);
      console.log('event', event)
      console.log(tab.name)
      if (tab.name === 'paper') {
        console.log('请求paper数据')
        this.paper_page_Info.currentNumber = 1
        this.paperInfo()
      }
      if (tab.name === 'clue') {
        console.log('请求clue数据')
        this.clue_page_Info.currentNumber = 1
        this.clueInfo()
      }
      if (tab.name === 'network') {
        console.log('请求network数据')
        // this.clue_page_Info.currentNumber=0
        this.clueInfo()
        console.log('开始绘图')
        this.draw_network()
      }
    },
    //获取时间戳并获取该记录的paper_info
    gettimestamp(timestamp) {
      this.timestamp = timestamp
      console.log(this.timestamp)
      this.tabName = 'paper'
      this.paperInfo()
    },
    // 监听paper_info页码值改变的事件
    handleCurrentChange1(newPage) {
      console.log('当前paper_info页码为：', newPage)
      //把最新的页码（newPage）赋值给 动态的 pagenum
      this.paper_page_Info.currentNumber = newPage
      //获取到最新显示的页码值  重新发送axios请求 这里是封装好的请求方法
      this.paperInfo()
    },
    // 监听clue_info页码值改变的事件
    handleCurrentChange2(newPage) {
      console.log('当前clue_info页码为：', newPage)
      //把最新的页码（newPage）赋值给 动态的 pagenum
      this.clue_page_Info.currentNumber = newPage
      //获取到最新显示的页码值  重新发送axios请求 这里是封装好的请求方法
      this.clueInfo()
    },


    //跳转至登录页面
    gotoLogin() {
      this.$router.push('login')
    },
    //跳转至注册页面
    gotoRegister() {
      this.$router.push('register')
    },
    //提交搜索请求
    handleSearch() {
      if (this.keywords === '') {
        this.$message('输入不能为空');
      } else {
        console.log('发送搜索请求')
        var that = this;
        that.axios({
          method: "post",
          url: "http://42.192.44.52:8000/search/",
          data: qs.stringify({
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
            .then(function (res) {
              console.log(res);
              console.log('已成功发送搜索请求');
              console.log(res.data)
            })
            .catch(function (err) {
              console.log(err)
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
    // paperInfo() {
    //   console.log('请求paper数据')
    //   var that=this;
    //   that.axios({
    //     method:"post",
    //     url:"http://42.192.44.52:8000/search/paper_info/",
    //     data:qs.stringify({
    //       "token": this.token,
    //       "message_type": "get_paper_info",
    //       "timestamp": this.timestamp,
    //       "page_num": this.paper_page_Info.currentNumber
    //       // "page_num": 1
    //     })
    //   })
    //       .then(function(res){
    //         console.log(res);
    //         console.log('连接成功');
    //         console.log(res.data)
    //         that.paper_result=res.data.paper_info
    //         that.paper_page_Info.total=res.data.total
    //       })
    //       .catch(function(err){
    //         console.log(err)
    //       })
    //
    // },
    //获取当前页clue_info数据
    // clueInfo() {
    //   console.log('请求clue数据')
    //   var that=this;
    //   that.axios({
    //     method:"post",
    //     url:"http://42.192.44.52:8000/search/clue_info/",
    //     data:qs.stringify({
    //       "token": this.token,
    //       "message_type": "get_clue_info",
    //       "timestamp": this.timestamp,
    //       "page_num": this.clue_page_Info.currentNumber
    //       // "page_num": 1
    //     })
    //   })
    //       .then(function(res){
    //         console.log(res);
    //         console.log('连接成功');
    //         console.log(res.data)
    //         that.clue_result=res.data.clue_info
    //         that.clue_page_Info.total=res.data.total
    //       })
    //       .catch(function(err){
    //         console.log(err)
    //       })
    //
    // },
    paperInfo() {
      if (this.paper_page_Info.currentNumber === 1) {
        this.paper_result = example.paper_info_1
      }
      if (this.paper_page_Info.currentNumber === 2) {
        this.paper_result = example.paper_info_2
      }
      if (this.paper_page_Info.currentNumber === 3) {
        this.paper_result = example.paper_info_3
      }
      if (this.paper_page_Info.currentNumber === 4) {
        this.paper_result = example.paper_info_4
      }
    },
    clueInfo() {
      console.log('请求clue数据')
      this.clue_result = example.clue_info;
      this.network_data = network_result
      // this.network_data = asd_net
    },
    getdrawInfo(class1,class2) {
      this.selected_network = {nodes: [], edges: []};
      // this.network_data.forEach((data) => {
      //   // console.log(data.is_BFS_edge)
      //   if(data.Edge_Type===this.drawSelect&&data.is_BFS_edge){
      //     this.selected_network.nodes.push({
      //       id: data.Node1,
      //       label: data.Node1,
      //       class: class1
      //     })
      //     this.selected_network.nodes.push({
      //       id: data.Node2,
      //       label: data.Node2,
      //       class: class2
      //     })
      //     this.selected_network.edges.push({
      //       source: data.Node1,
      //       target: data.Node2,
      //       weight: data.Weight,
      //       paper: data.Paper_List,
      //       origin_text: data.Original_Text
      //     })
      //   }
      //
      //   // switch (data.Edge_Type) {
      //   //   case "bacteria_to_disease": {
      //   //     this.networkData_selector.bacteria_to_disease.nodes.push({
      //   //       id: data.Node1,
      //   //       label: data.Node1,
      //   //       // class:"bacteria",
      //   //       type: 'circle',
      //   //       size: 30,
      //   //       style: {
      //   //         fill: '#ffeda0',
      //   //         stroke: '#fff'
      //   //       },
      //   //     });
      //   //     this.networkData_selector.bacteria_to_disease.nodes.push({
      //   //       id: data.Node2,
      //   //       label: data.Node2,
      //   //       // class:"disease",
      //   //       type: 'rect',
      //   //       size: [25, 25],
      //   //       style: {
      //   //         fill: '#d7301f',
      //   //         stroke: '#fff'
      //   //       },
      //   //     });
      //   //     this.networkData_selector.bacteria_to_disease.edges.push({
      //   //       source: data.Node1,
      //   //       target: data.Node2,
      //   //       weight: data.Weight,
      //   //       // label: clue_info.Paper_List,
      //   //     });
      //   //     break;
      //   //   }
      //   // }
      //
      //
      // });
      if(this.drawSelect==="BFS"){
        this.network_data.forEach((data) => {
          // console.log(data.is_BFS_edge)
          // if(data.is_BFS_edge){
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
          // }
        });
      }else{
        this.network_data.forEach((data) => {
          // console.log(data.is_BFS_edge)
          if(data.Edge_Type===this.drawSelect){
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
      console.log(!this.selected_network.edges)
      if(!this.selected_network.edges){
        console.log('无数据，请重新选择')
      }
    },
    draw_network(class1,class2) {

      this.getdrawInfo(class1,class2);

      const nodes = this.selected_network.nodes;
      const edges = this.selected_network.edges;
      nodes.forEach((node) => {
        if (!node.style) {
          node.style = {};
        }
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
    },

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
  display: -moz-inline-box;
  display: inline-block;
  color: #A9A9A9;
}

.el-scrollbar__wrap {
  overflow-x: auto;
  overflow-y: auto;
  height: calc(100% + 20px); /*多出来的20px是横向滚动条默认的样式*/

}

.el-scrollbar .el-scrollbar__wrap .el-scrollbar__view {
  white-space: nowrap;
  display: inline-block;
}

</style>
