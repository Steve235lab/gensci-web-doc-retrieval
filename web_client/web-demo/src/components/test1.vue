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
                <el-button type="primary" :icon="Search"  />
              </template>
            </el-input>
          </div></el-col>
        </el-row>

       </el-header>
      <el-container>
        <el-aside width="400px">Aside</el-aside>
        <el-main>
          <div style="height:600px;overflow:auto;">
            <div v-for="paper in paper_info" style="width:800px">
              <div style="color:#0071bc;font-size:20px">{{ paper.Title }}</div>
              <p style="height:30px;float:left;">{{ paper.First_Author }}</p>
              <p style="height:20px;">

                <span style="color:green;height:40px;line-height:40px;float:left">PMID:{{ paper.Pmid }}</span>
                <span style="color:green;height:40px;line-height:40px;float:left">{{ paper.Journal }}</span>
              </p>
              <el-divider />
            </div>
          </div>
          <el-row :gutter="20">
            <el-col :span="12" :offset="6"
            ><el-pagination layout="prev, pager, next" :total="50" />
            </el-col>
          </el-row>



        </el-main>
      </el-container>
    </el-container>
  </div>



</template>

<script lang="ts" setup>


import { ref } from 'vue'
import type { TableColumnCtx } from 'element-plus/es/components/table/src/table-column/defaults'
import {paper_info} from '../test/result.json'

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

const count = ref(0)
const input = ref('')


</script>

<style scoped>

</style>