<template>
  <div>
    <el-table
        :data="paper_result"
        border
        @sort-change="changeTableSort"
        style="width: 100%"
        height=600>
      <el-table-column type="expand">
        <!--                  折叠面板-文章详情-->
        <template slot-scope="props">
          <div v-for="(row,index) in props.row" :key="row" v-show="row">
            <p>
              <el-row :gutter="10">
                <!--                          左侧标题-->
                <el-col :span="5">
                  <span class="table-expand-label" v-if="index==='Chinese_Title'">&emsp;中文标题 : </span>
                  <span class="table-expand-label" v-else-if="index==='Chinese_Abstract'">&emsp;中文摘要 : </span>
                  <span class="table-expand-label" v-else>&emsp;{{ index }} : </span>
                </el-col>
                <!--                          右侧具体内容及格式-->
                <el-col :span="19">
                  <b v-if="index==='Title'||index ==='Chinese_Title'">{{ row }}</b>
                  <i v-else-if="index==='Authors'||index==='First_Author'||index==='Corresponding_Author'"
                     style="font-family: 'Times New Roman',serif">{{ row }}</i>
                  <span v-else-if="index==='Abstract'" v-html="row"></span>
                  <span v-else-if="index==='Publication_Type'||index==='Location'||index==='Organization'">
                    <span v-for="item in Line_Feed(row)" :key=item>{{item}}<br/></span>
                  </span>
                  <span v-else>{{ row }}</span>
                </el-col>
              </el-row>


            </p>

          </div>
        </template>
        <!--                  表格纵列-->
      </el-table-column>
      <el-table-column label="Title" prop="Title" width="400"></el-table-column>
      <el-table-column label="Date" prop="Publication_Date" sortable="custom" width="100"></el-table-column>
      <el-table-column label="Pmid" prop="Pmid" width="100"></el-table-column>
      <el-table-column label="Journal" prop="Journal" width="150"></el-table-column>
      <el-table-column label="If" prop="Journal_If" sortable="custom" width="100"></el-table-column>
      <el-table-column label="Sample_Size" prop="Sample_Size" width="150" align="center"></el-table-column>
      <el-table-column label="Publication_Type" prop="Publication_Type" width="200">
      <template slot-scope="props">
        <div v-for="(row,index) in props.row" :key="index">
            <span v-if="index==='Publication_Type'">
              <span v-for="item in Line_Feed(row)" :key=item>{{item}}<br/></span>
            </span>
        </div>
      </template>
      </el-table-column>

    </el-table>

    <el-row :gutter="20">
      <el-col :span="12" :offset="6" justify="center">
        <el-pagination @current-change="handleCurrentChange"
                       :current-page="current_page" :page-size="10"
                       :hide-on-single-page="true"
                       layout="total, prev, pager, next ,jumper" :total="paper_total">
        </el-pagination>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import qs from "qs";
import example from "../../../test_data/example_test.json";

export default {
  name: "paper_info",
  props: {
    paper_result: {
      type: Array,
      default: function (){
        return []
      }
    },
    paper_page: {
      type: Number,
      default: function () {
        return 1
      }
    },
    paper_total: {
      type: Number,
      default: 0
    },
  },
  data() {
    return {
      current_page: 1,
    }
  },
  computed:{
    Line_Feed: function (){
      return function (text){
        return Array.from(new Set(text.split('\n')))
      }
    },
  },
  methods: {
    handleCurrentChange(newPage){
      this.current_page=newPage
      console.log(this.current_page)
      this.$emit('update_paper', this.current_page);
    },
    changeTableSort(column){
      console.log(column)
      if(column.order==='descending'||column.order===null){
        column.order='reverse'
      }else if(column.order==='ascending'){
        column.order='positive'
      }
      this.$emit('changesort_paper',[column.prop,column.order])
    },
  }
}
</script>

<style scoped>
.table-expand-label {
  width: 180px;
  display:-moz-inline-box;
  display:inline-block;
  color: #A9A9A9;
}
</style>