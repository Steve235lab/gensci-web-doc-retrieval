<template>
  <div v-loading="draw_loading" element-loading-text="拼命加载中" >
<!--  <div>-->
    <div id="network" style="width: 100%;height: 100%;position: relative" >
      <el-select v-model="drawSelected" placeholder="请选择" @change="select_network" style="float: left">
        <el-option
            v-for="item in drawOptions"
            :key="item"
            :label="item"
            :value="item">
        </el-option>
      </el-select>
    </div>
    <div style="position: absolute;width: 100%;top:400px;background-color: rgb(255,255,255,0.9)">
      <el-table
          :header-cell-style="{background:'rbg(255,255,255,0.9)',color:'rbg(255,255,255,0.9)'}"
          v-if="table_flag"
          :data="selected_edgeInfo"
          element-loading-text="拼命加载中"
          :default-expand-all=true
          style="width: 100%"
          height=300>
        <!--                折叠面板-->
              <el-table-column type="expand" style="word-break:break-all; white-space: pre-line;padding-left: 10px;padding-right: 10px">
                <template slot-scope="props">
                  <div v-for="(row,item) in props.row" :key="row" v-show="row">
                    <p id="expand">
                      <!--              <el-row :gutter="10">-->
                      <!--                <el-col :span="3">-->
                      <!--                  <span class="table-expand-label">&emsp;{{ item }} : </span>-->
                      <!--                </el-col>-->
                      <!--                <el-col :span="21">-->

                      <span v-if="item==='Original_Text'" >
                            <span v-for="(text,index) in Text_separated(row) " :key=index>
                              <span v-for="(new_text,index) in separated(text)" :key=index>
                                <span v-if="index===0">
                                  <span v-for="(final,index) in separated_again(new_text)" :key="index">
                                    <el-link v-if="index===1" :underline="false" @click="getpaperdetails(final)">{{final}}</el-link>
                                    <span v-else>{{final}}</span>
                                    {{ index === separated_again(new_text).length - 1 ? '' : ':' }}
                                  </span><br/>
                                </span>
                                <span v-else>{{new_text}}</span>
                              </span>
                              <!--                      <span  @click="getpaperdetails(text)">{{text}}<br/></span>-->
                              <el-divider v-if="index !== Text_separated(row).length - 1"></el-divider>
                            </span>
                          </span>
                      <!--                  <span v-else-if="item==='Paper_List'">-->
                      <!--                    <span v-for="(pmid,index) in Text_separated(row) " :key=index>-->
                      <!--                      <el-link :underline="false" @click="getpaperdetails(pmid)">{{pmid}}</el-link>-->
                      <!--                      {{ index === Text_separated(row).length - 1 ? '' : '|' }}-->
                      <!--                    </span>-->
                      <!--                  </span>-->
                      <!--                  <span v-else>{{ row }}</span>-->
                      <!--                </el-col>-->
                      <!--              </el-row>-->
                    </p>

                  </div>
                </template>
              </el-table-column>
        <!--                表格纵列-->
        <el-table-column label="Node1" prop="Node1" />
        <el-table-column label="Edge_Type" prop="Edge_Type" />
        <el-table-column label="Node2" prop="Node2" />
        <el-table-column label="Weight" prop="Weight" sortable/>
        <!--      <el-table-column label="Paper_List" prop="Paper_List" sortable>-->
        <!--        <template slot-scope="props">-->
        <!--          <div v-for="(row,item) in props.row" :key="item">-->
        <!--            <span v-if="item==='Paper_List'">-->
        <!--              <span v-for="(pmid,index) in Pmid_separated(row) " :key=index>-->
        <!--                <el-link :underline="false" @click="getpaperdetails(pmid)">{{pmid}}</el-link>-->
        <!--                {{ index === Pmid_separated(row).length - 1 ? '' : '|'}}-->
        <!--              </span>-->
        <!--            </span>-->
        <!--          </div>-->
        <!--        </template>-->
        <!--      </el-table-column>-->

      </el-table>
    </div>

    <div id="test" v-show="finished" style="position: absolute;width: 200px;top:80px;background-color: rgb(100,100,100,0.1);border: gray;text-align: center;">
        Legend
    </div>



  </div>
</template>

<script>
import G6 from "@antv/g6";
// import { GraphLayoutPredict } from '@antv/vis-predict-engine';
let graph;
let test;
import insertCss from 'insert-css';
// const { GraphLayoutPredict } = window.GraphLayoutPredict
import example from "../../../test_data/example_test.json"
let shift = true;
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

export default {
  name: "network",
  props: {
    network_data: {
      type: Array,
      default: function (){
        return []
      }
    },
    drawSelect: {
      type: String,
      default: function (){
        return ''
      }
    },
    drawOptions: {
      type: Array,
      default: function (){
        return []
      }
    },
    loading: {
      type: Boolean,
      default: function (){
        return true
      }
    },
  },
  data(){
    return{
      finished:false,
      drawSelected:this.drawSelect,
      selected_edgeInfo:[],
      selected_nodeInfo:[],
      test:example.clue_info,
      draw_loading:this.loading,
      table_flag:false,
      legendData:{nodes: [],edges:[]},
    }
  },
  watch:{
    loading(newloading){
      this.draw_loading=newloading
    }
  },
  computed:{
    // draw_loading: function (){
    //   return this.loading
    // },
    Text_separated: function (){
      return function (text){
        return text.split('|')
      }
    },
    separated: function (){
      return function (text){
        return text.split(';')
      }
    },
    separated_again: function (){
      return function (text){
        return text.split(':')
      }
    },

  },
  mounted() {
    const tooltip = new G6.Tooltip({
      offsetX: 10,
      offsetY: 10,
      // v4.2.1 起支持配置 trigger，click 代表点击后出现 tooltip。默认为 mouseenter
      trigger: 'click',
      fixToNode: [1, 0.5],
      // the types of items that allow the tooltip show up
      // 允许出现 tooltip 的 item 类型
      itemTypes: ['node'],
      // custom the tooltip's content
      // 自定义 tooltip 内容
      getContent: (e) => {
        const outDiv = document.createElement('div');
        outDiv.style.width = 'fit-content';
        outDiv.style.height = 'fit-content';
        const model = e.item.getModel();
        if (e.item.getType() === 'node') {
          outDiv.innerHTML = `${model.id}`;
        }
        return outDiv;
      },
    });
    graph = new G6.Graph({
      container: 'network',
      width: 1200,
      height: 600,
      linkCenter: true,
      // 是否开启画布自适应。开启后图自动适配画布大小。
      fitView: true,
      //v3.5.1 后支持。开启后，图将会被平移，图的中心将对齐到画布中心，但不缩放。优先级低于 fitView
      fitCenter: true,
      //渲染方式 svg/canvas
      // renderer: 'svg',
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
          // fill: 'lightsteelblue',
          stroke: 'red',
          lineWidth: 2,
        },
        activeByLegend: {
          lineWidth: 10,
          strokeOpacity: 0.5
        },
        inactiveByLegend: {
          opacity: 0.5
        }

      },
      // 边在各状态下的样式
      edgeStateStyles: {
        // click 状态为 true 时的样式
        click: {
          stroke: 'red',
          lineAppendWidth: 5,
        },
        activeByLegend: {
          lineWidth: 3
        },
        inactiveByLegend: {
          opacity: 0.5
        }
      },
      // 布局
      layout: {
        type: 'fruchterman',
        // center: [200, 200], // 可选，默认为图的中心
        gravity: 1, // 可选
        speed: 20, // 可选
        clustering: true, // 可选
        clusterGravity: 0.1, // 可选
        // maxIteration: 500, // 可选，迭代次数
        // // linkDistance: 1000,
        // preventOverlap: true,
        // nodeStrength: -10,         // 可选
        // edgeStrength: 0.1,        // 可选
        // nodeSize: 30,             // 可选
        onTick: () => {           // 可选
          console.log('ticking');
        },
        onLayoutEnd: () => {      // 可选
          console.log('force layout done');
          this.draw_loading=false
          this.finished=true
          console.log("完成绘制")


        },
        workerEnabled: true,      // 可选，开启 web-worker
        gpuEnabled: true          // 可选，开启 GPU 并行计算，G6 4.0 支持
      },
      // 内置交互
      modes: {
        default: ['drag-canvas', 'zoom-canvas', 'drag-node','brush-select','click-select'],
        'click-select':{

          }
      },
      // plugins: [minimap,legend],
      plugins: [tooltip],
    });
    test = new G6.Graph({
      container: 'test',
      width: 200,
      height: 150,
      // linkCenter: true,
      // // 是否开启画布自适应。开启后图自动适配画布大小。
      // fitView: true,
      // //v3.5.1 后支持。开启后，图将会被平移，图的中心将对齐到画布中心，但不缩放。优先级低于 fitView
      // fitCenter: true,
      // 节点默认配置
      defaultNode: {
        style: {
          fill: '#f5b89a',
        },
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
      // 布局
      layout: {
        type: 'grid',
        nodeSize: 30,
        cols:3,
        workerEnabled: true,      // 可选，开启 web-worker
        // gpuEnabled: true          // 可选，开启 GPU 并行计算，G6 4.0 支持
        // center: [200, 200], // 可选，默认为图的中心
      },
    });
  },
  methods:{
    // 选择绘制的网络图
    select_network() {
      this.draw_loading=true
      this.finished=false
      // console.log(this.new_network)
      // console.log(this.drawSelected)
      // this.draw_network()
      var nodeType_selector = this.drawSelected.split('_')
      if(nodeType_selector.length===1){
        this.draw_network(nodeType_selector[0],nodeType_selector[0])
      }else{
        this.draw_network(nodeType_selector[0],nodeType_selector[2])
      }
      // console.log(nodeType_selector.length)
      // console.log(nodeType_selector[0])
    },
    //绘图数据预处理
    getdrawInfo(class1,class2) {
      this.legendData.nodes=[]
      this.selected_network = {nodes: [], edges: []};
      if(this.drawSelected==="BFS"){
        this.drawOptions.forEach((data) => {
          if(data!=='BFS'){
            var nodeType = data.split('_')
            if(nodeType.length===1){
              this.legendData.nodes.push({
                id: nodeType[0],
                label:nodeType[0],
              })
            }else{
              this.legendData.nodes.push({
                id: nodeType[0],
                label:nodeType[0],
              })
              this.legendData.nodes.push({
                id: nodeType[2],
                label:nodeType[2],
              })
            }
          }
        })
        this.network_data.forEach((data) => {
          // console.log(data.is_BFS_edge)
          if(data.is_BFS_edge){
            var nodeType_selector = data.Edge_Type.split('_')
            if(nodeType_selector.length===1){
              var node1_type = nodeType_selector[0];
              var node2_type = nodeType_selector[0];
              this.selected_network.edges.push({
                source: data.Node1,
                target: data.Node2,
                edge_type: node1_type,
                weight: data.Weight,
                paper: data.Paper_List,
                original_text: data.Original_Text
              })
            }else{
              node1_type = nodeType_selector[0];
              node2_type = nodeType_selector[2];
              this.selected_network.edges.push({
                source: data.Node1,
                target: data.Node2,
                edge_type: node1_type+' to '+node2_type,
                weight: data.Weight,
                paper: data.Paper_List,
                original_text: data.Original_Text
              })
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

          }
        });
      }else{
        this.legendData.nodes.push({
          id: class1,
          label:class1,
        })
        if(class1!==class2){
          this.legendData.nodes.push({
            id: class2,
            label:class2,
          })
        }
        this.network_data.forEach((data) => {
          // console.log(data.is_BFS_edge)
          if(data.Edge_Type===this.drawSelected&&data.is_BFS_edge){

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
              edge_type: this.drawSelected,
              weight: data.Weight,
              paper: data.Paper_List,
              original_text: data.Original_Text
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
      this.legendtest()

      const nodes = this.selected_network.nodes;
      const edges = this.selected_network.edges;
      if(edges.length===0) {
        this.$message({
          showClose: true,
          message: '无数据，请重新选择！',
          type: 'warning'
        });
        this.draw_loading=false
      }

      nodes.forEach((node) => {
        if (!node.style) {
          node.style = {};
        }
        // console.log(node.class)
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
        if (edge.weight === 1) {
          edge.class='weight=1'
          edge.style.opacity = 0.5;
        } else {
          edge.style.opacity = 0.8;
          edge.class='weight>1'
          // console.log(edge)
        }

      });
      // graph.clear();
      graph.data(this.selected_network);
      graph.render();



      // 监听鼠标进入节点
      graph.on('node:mouseenter', (e) => {
        const nodeItem = e.item;
        // 设置目标节点的 hover 状态 为 true
        graph.setItemState(nodeItem, 'active', true);

      });
      // 监听鼠标离开节点
      graph.on('node:mouseleave', (e) => {
        const nodeItem = e.item;
        // 设置目标节点的 hover 状态 false
        graph.setItemState(nodeItem, 'active', false);
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
        // console.log(e.item);
      });
      // 监听鼠标点击边
      graph.on('edge:click', (e) => {
        // 先将所有当前有 click 状态的边的 click 状态置为 false
        this.table_flag=true
        const clickEdges = graph.findAllByState('edge', 'click');
        clickEdges.forEach((ce) => {
          graph.setItemState(ce, 'click', false);
        });
        const edgeItem = e.item;
        // 设置目标边的 click 状态 为 true
        this.selected_edgeInfo=[];
        graph.setItemState(edgeItem, 'click', true);
        const model = e.item.getModel();
        this.selected_edgeInfo.push({
          Id:model.id,
          Node1:model.source,
          Node2:model.target,
          Edge_Type:model.edge_type,
          Weight:model.weight,
          Original_Text:model.original_text
        })
        // console.log('test1:',this.selected_edgeInfo);
      });
      // 监听框选事件
      graph.on('nodeselectchange', (e) => {
        // console.log('e.selectedItems:',e.selectedItems )
        this.selected_edgeInfo=[];
        if(e.selectedItems.edges.length===0){
          // console.log('no edge')
          const clickEdges = graph.findAllByState('edge', 'click');
          clickEdges.forEach((ce) => {
            graph.setItemState(ce, 'click', false);
          });
          this.table_flag=false
        }else{
          this.table_flag=true
        }
        if(e.selectedItems.nodes.length===0){
          // console.log('no node')
          const clickNodes = graph.findAllByState('node', 'click');
          clickNodes.forEach((cn) => {
            graph.setItemState(cn, 'click', false);
          });
        }
        e.selectedItems.edges.forEach((edge) => {
          const model = edge._cfg.model
          this.selected_edgeInfo.push({
            Id:model.id,
            Node1:model.source,
            Node2:model.target,
            Edge_Type:model.edge_type,
            Weight:model.weight,
            Original_Text:model.original_text
          })
        });
        // e.selectedItems.nodes.forEach((node) => {
        //   const model = node._cfg.model
        //   console.log(model)
        //   this.selected_nodeInfo.push({
        //     Id:model.id,
        //     Node_Type:model.class,
        //   })
        // });

      });



    },
    //请求单篇paper数据
    getpaperdetails(pmid){
      this.$emit('paper_details', pmid);
    },
    legendtest(){
      const nodes = this.legendData.nodes;
      nodes.forEach((node) => {
        if (!node.style) {
          node.style = {};
        }
        // console.log(node.class)
        // node.style.lineWidth = 1;
        node.type = 'rect';
        node.size = [20, 20];
        node.style.radius = 5;
        node.style.stroke = '#fff';
        switch (node.id) {
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
          default: {
            node.style.fill = '#9ad0f5';
            break;
          }
        }
      });
      test.data(this.legendData)
      test.render()
    }
  }
}
</script>

<style scoped>
#network {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0;
}

/*最外层透明*/
/deep/ .el-table, /deep/ .el-table__expanded-cell{
  background-color: transparent;
}
/* 表格内背景颜色 */
/deep/ .el-table th,
/deep/ .el-table tr,
/deep/ .el-table td {
  background-color: transparent;
}


</style>