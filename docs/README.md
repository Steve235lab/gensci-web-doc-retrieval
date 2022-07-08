# 项目环境配置信息与部署

**王义成 2022/7/8 创建**

---
## 1. 后端环境配置信息

### 1.1 python版本

3.7或3.9均测试通过，推荐先创建空的python虚拟环境

### 1.2 依赖项

见 web_server/requirements.txt

```
pip install -r requirements.txt
```

### 1.3 MySQL数据库版本

8.0.29 MySQL Community Server - GPL

### 1.4 部署

* 安装MySQL，并注册用户，创建项目数据库

* 安装python，创建虚拟环境，安装依赖项

* 更改 controller.py 中的配置

* 激活虚拟环境，运行 SQL/ 目录下的两个 .py 脚本，生成数据表

* 终端切换至 web_server/ 目录下，运行指令：

    * 本地调试
        ```
        python manage.py runserver
        ```

    * 映射至服务器防火墙（腾讯云为例），用于外部访问
        ```
        python manage.py runserver 0.0.0.0:8000
        ```

* 服务器防火墙开放8000端口

## 2. 前端环境配置
* 在node.js官网下载最新版安装包，下载完成后安装即可
* 打开cmd，输入node -v 查看安装是否成功，若显示版本号，说明成功安装
* 跳转至需要添加的项目路径，安装npm淘宝镜像，输入npm config set registry https://registry.npm.taobao.org
* 输入npm config get registry查看是否安装成功，若成功则执行npm run start，并且所在项目文件夹会多出一个node_modules文件夹，若安装失败可以改变本机的sass下载的数据源，执行npm config set sass-binary-site http://npm.taobao.org/mirrors/node-sass 后执行npm install
* node和npm都成功安装后，在cmd输入npm install -g vue-cli，等待vue脚手架构建工具安装，安装成功后即完成环境配置，根据需要调用的函数安装对应的环境，如npm install --save js.md5即可在Vue中使用md5加密了
