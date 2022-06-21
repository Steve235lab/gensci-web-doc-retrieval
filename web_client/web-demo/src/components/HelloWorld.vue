<template>

  <div class="common-layout">
    <el-container>
      <el-header>
        <el-row :gutter="20">
          <el-col :span="12" :offset="6"
          ><div id="search" class="mt-4 ">
            <el-input
                v-model="input"
                placeholder="Please input"
                class="input-with-select"
                clearable
                style="height:40px;"
            >
              <template #append>
                <el-button type="primary" :icon="Search"  @click="Search"/>
              </template>
            </el-input>
          </div></el-col>
        </el-row>
       </el-header>
      <el-container>
        <el-aside width="20%">
          <div style="height:30px;">历史搜索记录</div>
          <div v-for="history in history_list" style="height:30px;">{{history}}</div>
        </el-aside>
        <el-main >
           <div class="example-pagination-block">
             <el-table :data="paper_info" style="width: 80% "  height=600>
               <el-table-column type="expand">
                 <template #default="props">
                   <div m="4">
                     <p v-for="(item,key) in props.row" v-show="item">{{key }}:{{ item }}</p>
                   </div>
                 </template>
               </el-table-column>
               <el-table-column label="Title" prop="Title" width="400" />
               <el-table-column label="Date" prop="Publication_Date"  width="100" sortable/>
               <el-table-column label="First_Author" prop="First_Author"  width="200" />
               <el-table-column label="Keywords" prop="Keywords" />
             </el-table>
             <el-row :gutter="20">
               <el-col :span="12" :offset="6"
               ><el-pagination layout="prev, pager, next" :total="50" />
               </el-col>
             </el-row>

           </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>


<script lang="ts" setup>
import {ref, VueElement} from 'vue'
import type { TableColumnCtx } from 'element-plus/es/components/table/src/table-column/defaults'
import {paper_info} from '../test/result.json'
import {history_list} from '../test/history_list.json'
defineProps({
  msg: String
})
import {
  Check,
  Delete,
  Edit,
  Message,
  Search,
  Star,
} from '@element-plus/icons-vue'

const input = ref('')






</script>

<style scoped>
a {
  color: #42b983;
}
.input-with-select .el-input-group__prepend {
  background-color: var(--el-fill-color-blank);
}

</style>


