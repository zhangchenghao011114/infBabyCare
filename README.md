## django-docker-tutorial

*《软件工程》，清华大学软件学院*

Docker + Django + Mysql + Ngnix + Gunicorn 的示例，帮助同学们快速理解 Docker 以及 docker-compose 的使用。

### 涉及 Docker 镜像的官方链接

1. [MySQL](https://hub.docker.com/_/mysql)
2. [Nginx](https://hub.docker.com/_/nginx)
3. [Python](https://hub.docker.com/_/python)

### 安装Docker

请参考 [Docker-从入门到实践](https://yeasy.gitbook.io/docker_practice/install)。

### 启动项目

1. 将目录中的 `.env_example` 文件复制一份，重命名为 `.env`；

2. 补全 `.env` 文件中数据库名和数据库密码，用于 MySQL 镜像的配置使用；

3. 将第2步中补全的数据库名和密码填写到 `django_app/settings.py` 的 `DATABASES` 设置当中，可以全局搜索 `[DB_NAME]` 和 `[DB_PASSWORD]` 可快速定位；

4. 执行命令 `docker-compose up` 启动项目；

   * 首次启动会先下载所需的基础镜像，请耐心等待；

   * 可能会出现连接不上数据库的问题，是因为 MySQL 镜像初次使用需要一定的初始化过程；

     >  If the application you're trying to connect to MySQL does not handle MySQL downtime or waiting for MySQL to start gracefully, then putting a connect-retry loop before the service starts might be necessary. 

   * Django 会重试连接数据库，等 MySQL 初始化完成后可完成连接

5. 在 `8001` 端口访问[启动的应用](http://localhost:8001)。

### 其他指令

1. 停止项目：`docker-compose down`
2. 查看运行中的容器: `docker ps`
3. 根据 Dockerfile 构建镜像: `docker build -t foo:v1.0.0 .`
   * `-t` 后面跟着的是镜像名和可选的标签名 `name[:tag]`
   * 末尾的 `.` 表示使用当前目录下的 Dockerfile
