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

