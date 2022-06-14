# Web开发小组分工与技术路线

**王义成 2022/6/13**

---

## 1. 项目需求拆分

### 1.1 前端
* 前端界面设计与搭建
* 输入：N个关键词查询，要支持AND OR
* 输出：提供两个表格文件的下载入口，页面显示摘要信息与线索串联图
* 显示排序后的搜索结果
* 文献跳转

### 1.2 后端
* 网站后台搭建
* 功能模块整合串联
* 与前端对接

### 1.3 数据库（低优先级）
将数据库从excel迁移到MySQL大概率需要对已有的查找、可视化脚本进行重构，所以计划在完成Web基本功能的开发之后再进行。

* 数据库迁移
* 数据库与内存对象读写交互
* 重构新数据库下的查找与可视化功能

---

## 2. 人员分工
* 前端开发：姜灵旻、王蕾雯（有合作经验，具体工作自行协调）
* 后端--网站后台搭建、与前端交互：王义成
* 后端--功能模块整合串联、项目部署：田亮玉
* 数据库及关联功能模块重构（低优先级）：王义成、田亮玉

---

## 3. 技术路线
* 前端：使用Bootstrap框架
* 后端：python + django
* 数据库：已有部分先继续使用excel文件，待基本功能开发完成后再考虑转移到MySQL下
* 项目部署：Docker
* 协同开发与版本控制：GitHub私有仓库

---

## 4. 项目排期
|     | 第1周 | 第2周 | 第3周 | 第4周 |
| :--: | :--: | :--: | :--: | :--: |
前端 | 进行页面的总体设计，总结项目要求，熟悉远程协同开发工具与git版本管理，熟悉前端页面开发插件与语言的基本使用方法，开始项目的基础工作 | 进行具体的、细节的输入输出端的整体框架搭建，根据设计页面进行代码的编写 | 完成第二周未完成的工作，进行项目部署，与后端进行匹配，完善细节 | 整理开发文档，项目的收尾与交付 |
后端 | 确定前后端数据交互协议与撰写开发文档，熟悉远程协同开发工具与Git版本管理，新建django项目并编写网站路由 | 编写业务逻辑（处理请求并应答、搜索结果排序），对已有功能模块整合串联 | 编写并完善业务逻辑，项目部署，迁移数据库 | 重构数据库相关功能模块，整理开发文档，项目收尾与交付 |