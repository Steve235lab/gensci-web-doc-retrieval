<template>
  <div v-loading="draw_loading" element-loading-text="拼命加载中">
    <div id="network" style="width: 100%;height: 100%">
      <el-select v-model="drawSelected" placeholder="请选择" @change="select_network" style="float: left">
        <el-option
            v-for="item in drawOptions"
            :key="item"
            :label="item"
            :value="item">
        </el-option>
      </el-select>
    </div>
  </div>
</template>

<script>
import G6 from "@antv/g6";
let graph;
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
      type: Array,
      default: function (){
        return []
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
    new_network:{
      type:String,
      default:function (){
        return ''
      }
    }
  },
  data(){
    return{
      drawSelected:this.drawSelect,

    }
  },
  computed:{
    draw_loading: function (){
      return this.loading
    }
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
      itemTypes: ['node', 'edge'],
      // custom the tooltip's content
      // 自定义 tooltip 内容
      getContent: (e) => {
        const outDiv = document.createElement('div');
        outDiv.style.width = '300px';
        outDiv.style.height = '200px';
        const model = e.item.getModel();
        if (e.item.getType() === 'node') {
          outDiv.innerHTML = `${model.id}`;
        } else {
          // const source = e.item.getSource();
          // const target = e.item.getTarget();
          // outDiv.innerHTML = `来源：${source.getModel().name}<br/>去向：${target.getModel().name}`;
          outDiv.innerHTML = `<div style="height:200px;width:300px;overflow: auto">Paper_List：${model.paper}<br/>Original_Text：${model.origin_text}</div>`;
        }
        return outDiv;
      },
    });
    graph = new G6.Graph({
      container: 'network',
      width: 1200,
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
        // center: [200, 200], // 可选，默认为图的中心
        gravity: 0, // 可选
        speed: 2, // 可选
        clustering: true, // 可选
        clusterGravity: 5, // 可选
        maxIteration: 300, // 可选，迭代次数
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
  methods:{
    // 选择绘制的网络图
    select_network() {
      this.draw_loading=true
      console.log(this.new_network)
      console.log(this.drawSelected)
      // this.draw_network()
      var nodeType_selector = this.drawSelected.split('_')
      if(nodeType_selector.length===1){
        this.draw_network(nodeType_selector[0],nodeType_selector[0])
      }else{
        this.draw_network(nodeType_selector[0],nodeType_selector[2])
      }
      console.log(nodeType_selector.length)
      console.log(nodeType_selector[0])
    },
    //绘图数据预处理
    getdrawInfo(class1,class2) {
      this.selected_network = {nodes: [], edges: []};
      if(this.drawSelected==="BFS"){
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
      this.draw_loading=false
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

<style scoped>
#network {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0;

}
</style>