<template>
  <div>
  <div v-for="(row,item) in paper_details" :key="row" v-show="row">
    <p>
      <el-row :gutter="10">
        <!--                          左侧标题-->
        <el-col :span="5">
          <span class="table-expand-label" v-if="item==='Chinese_Title'" style="float: left">&emsp;中文标题 : </span>
          <span class="table-expand-label" v-else-if="item==='Chinese_Abstract'" style="float: left">&emsp;中文摘要 : </span>
          <span class="table-expand-label" v-else style="float: left">&emsp;{{ item }} : </span>
        </el-col>
        <!--                          右侧具体内容及格式-->
        <el-col :span="19" >
          <b v-if="item==='Title'||item ==='Chinese_Title'" style="float: left;text-align:left;">{{ row }}</b>
          <i v-else-if="item==='Authors'||item==='First_Author'||item==='Corresponding_Author'"
             style="font-family: 'Times New Roman',serif;float: left;text-align:left;">{{ row }}</i>
          <span v-else-if="item==='Abstract'||item==='Publication_Type'" v-html="row" style="float: left;text-align:left;"></span>
          <span v-else style="float: left;text-align:left;" >{{ row }}</span>
        </el-col>
      </el-row>


    </p>

  </div>
  </div>
</template>

<script>
export default {
  name: "paper_details",
  props: {
    paper_details: {
      type: Array,
      default: function (){
        return []
      }
    },

  }
}
</script>

<style scoped>

</style>