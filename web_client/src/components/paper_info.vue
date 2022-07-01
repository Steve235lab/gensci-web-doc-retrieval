<template>
  <div>
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
      <el-table-column label="Date" prop="Publication_Date" sortable width="100"></el-table-column>
      <el-table-column label="Pmid" prop="Pmid" sortable width="100"></el-table-column>
      <el-table-column label="Journal" prop="Journal" sortable width="150"></el-table-column>
      <el-table-column label="If" prop="Journal_If" sortable width="100"></el-table-column>
      <el-table-column label="Sample_Size" prop="Sample_Size" sortable width="150"></el-table-column>
      <el-table-column label="Publication_Type" prop="Publication_Type" sortable width="200"></el-table-column>

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
  methods: {
    handleCurrentChange(newPage){
      this.current_page=newPage
      console.log(this.current_page)
      this.$emit('update_paper', this.current_page);
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