<template>
  <div>
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
                <el-col :span="3">
                  <span class="table-expand-label">&emsp;{{ item }} : </span>
                </el-col>
                <el-col :span="21">
                  <span v-if="item==='Paper_List'">
                      <span v-for="(pmid,index) in Pmid_separated(row) " :key=index>
                        <el-link :underline="false" @click="getpaperdetails(pmid)">{{pmid}}</el-link>
                        {{ index === Pmid_separated(row).length - 1 ? '' : '|'}}
                      </span>
                    </span>
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
      <el-table-column label="Paper_List" prop="Paper_List" sortable>
        <template slot-scope="props">
          <div v-for="(row,item) in props.row" :key="item">
            <span v-if="item==='Paper_List'">
              <span v-for="(pmid,index) in Pmid_separated(row) " :key=index>
                <el-link :underline="false" @click="getpaperdetails(pmid)">{{pmid}}</el-link>
                {{ index === Pmid_separated(row).length - 1 ? '' : '|'}}
              </span>
            </span>
          </div>
        </template>
      </el-table-column>

    </el-table>
    <el-row :gutter="20">
      <el-col :span="12" :offset="6" justify="center">
        <el-pagination @current-change="handleCurrentChange"
                       :current-page="current_page" :page-size="20"
                       :hide-on-single-page="true"
                       layout="total, prev, pager, next ,jumper" :total="clue_total">
        </el-pagination>
      </el-col>
    </el-row>
  </div>

</template>

<script>
export default {
  name: "clue_info",
  props: {
    clue_result: {
      type: Array,
      default: function (){
        return []
      }
    },
    clue_page: {
      type: Number,
      default: function () {
        return 1
      }
    },
    clue_total: {
      type: Number,
      default: 0
    },
  },
  data() {
    return {
      current_page: 1,
    }
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
    handleCurrentChange(newPage){
      this.current_page=newPage
      console.log(this.current_page)
      this.$emit('update_clue', this.current_page);
    },
    getpaperdetails(pmid){
      this.$emit('paper_details', pmid);
    },

  }
}
</script>

<style scoped>
.table-expand-label {
  width: 100px;
  display:-moz-inline-box;
  display:inline-block;
  color: #A9A9A9;
}
</style>