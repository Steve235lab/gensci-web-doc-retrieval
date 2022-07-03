<template>
  <div v-loading="loading" element-loading-text="拼命加载中" id="body">
    <div v-for="(row,index) in paper_details" :key="row" v-show="row" >
      <p>
        <el-row :gutter="10" type="flex" justify="end" style="flex-wrap: wrap;flex-direction: row">
          <!--                          左侧标题-->
          <el-col :sm="24" :md="6" :lg="5">
            <span class="label" v-if="index==='Chinese_Title'" style="float: left">中文标题 : </span>
            <span class="label" v-else-if="index==='Chinese_Abstract'" style="float: left">中文摘要 : </span>
            <span class="label" v-else style="float: left">{{ index }} : </span>
          </el-col>
          <!--                          右侧具体内容及格式-->
          <el-col :sm="24" :md="18" :lg="19" >
            <b v-if="index==='Title'||index ==='Chinese_Title'" style="float: left;text-align:left;">{{ row }}</b>
            <i v-else-if="index==='Authors'||index==='First_Author'||index==='Corresponding_Author'"
               style="font-family: 'Times New Roman',serif;float: left;text-align:left;">{{ row }}</i>
            <span v-else-if="index==='Abstract'" v-html="row" style="float: left;text-align:left;"></span>
            <span v-else-if="index==='Publication_Type'||index==='Location'||index==='Organization'">
              <span v-for="item in Line_Feed(row)" :key=item>{{item}}<br/></span>
            </span>
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
    loading: {
      type: Boolean,
      default: function (){
        return true
      }
    },
  },
  computed:{
    Line_Feed: function (){
      return function (text){
        return Array.from(new Set(text.split('\n')))
      }
    },
  }
}
</script>

<style scoped>
.label {
  width: 180px;
  display:-moz-inline-box;
  display:inline-block;
  color: #A9A9A9;
}
#body{
  margin-left:3%;
  margin-right:3%;
  line-height:1.5;
}
</style>