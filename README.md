## infBabyCare Backend

*《软件工程》，清华大学软件学院*

Docker + Django + Mysql + Ngnix + Gunicorn 技术架构，作为清华大学软件工程课程大作业infBabyCare的后端

## 开发中常用的docker命令
* 进入容器
```shell
sudo docker exec -it infbabycare_app_1 /bin/bash
```
* 停止所有容器
```shell
sudo docker stop $(sudo docker ps -a -q)
```
* 删除所有容器
```shell
sudo docker rm $(sudo docker ps -a -q)
```

### 其他指令

1. 停止项目：`docker-compose down`
2. 查看运行中的容器: `docker ps`
3. 根据 Dockerfile 构建镜像: `docker build -t foo:v1.0.0 .`
   * `-t` 后面跟着的是镜像名和可选的标签名 `name[:tag]`
   * 末尾的 `.` 表示使用当前目录下的 Dockerfile

