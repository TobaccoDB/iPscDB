# iPscDB项目
## 一、项目简介
- iPscDB 是一个单细胞转录组数据资源库，其中包含了细胞标记物、单细胞图谱以及丰富的数据分析工具。目前，已收集了 23 种模式植物的数据，包括拟南芥、水稻、玉米、番茄和烟草等，涵盖了超过 270，480 个标记基因和超过 300 万份单细胞数据，为不同植物和组织中的细胞整合及单细胞研究提供了全面且相对准确的细胞标记物和细胞图谱。
- 系统网址：https://www.tobaccodb.org/ipscdb/homePage
- 代码地址：https://github.com/TobaccoDB/iPscDB.git

## 二、项目结构
- frontend：前端项目
  - public：静态资源
  - src：源代码
    - api：API 接口
    - components：组件
    - router：路由
    - store：状态管理
    - utils：工具函数
    - App.vue：主应用组件
    - main.js：入口文件
  - .env.development：开发环境配置文件
  - .env.production：生产环境配置文件
  - babel.config.js：Babel 配置文件
  - package.json：项目依赖配置文件
  - vue.config.js：Vue 配置文件 
- backend：后端项目
  - service-api：API 服务
    - excel：Excel 临时文件处理模块
    - logs：日志文件
    - plant_marker：应用程序
    - static：静态文件
    - temps：临时文件
    - manage.py：Django 管理脚本
    - requirements.txt：Python 依赖配置文件
    - local_settings：配置文件
    - Dockerfile：Docker 配置文件
  - service-analysis：数据分析服务
    - logs：日志文件
    - django_server：应用程序
    - pids：进程 ID 文件
    - celery_restart.sh：Celery 重启脚本
    - celert_start.sh：Celery 启动脚本
    - celery_stopwait.sh：Celery 停止脚本
    - manage.py：Django 管理脚本
    - requirements.txt：Python 依赖配置文件
    - local_settings：配置文件
    - Dockerfile：Docker 配置文件
    - start.sh：启动脚本
- .env：环境变量配置文件
- docker-compose.yml：Docker 配置文件
- README.md：项目说明文档

## 三、项目启动
### 1、本地启动
- 前端启动
进入 frontend 目录，执行以下命令启动前端项目（前提需要安装node服务可以参考官网安装）：
  ```bash
  npm install
  npm run dev
  ```
- 后端启动
进入 backend 目录（需要本地安装python3.9，已经安装mysql数据库服务），
  - 启动 service-api 服务，进入到service-api目录（根据自己本地的数据库配置修改local_settings.py数据库信息）：
  执行以下命令启动：
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python manage.py runserver 0.0.0.0:8001
    ``` 
  - 启动 service-analysis 服务， 进入到service-analysis目录（根据自己本地的数据库配置修改local_settings.py数据库信息）：
  执行以下命令启动：
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python manage.py runserver 0.0.0.0:8002
    ``` 
### 2、Docker 启动
#### Docker 启动项目说明文档
##### 1、前提条件
在使用 Docker 启动本项目之前，请确保你的系统已经安装了 Docker。不同操作系统安装 Docker 的方法如下：
- Linux 系统
以 Ubuntu 为例，打开终端，依次执行以下命令：
sudo apt update
sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker
对于其他 Linux 发行版，可以参考Docker 官方文档进行安装。
- macOS 系统
在 macOS 上，可以通过 Docker Desktop 进行安装。前往Docker 官方网站下载适合你系统版本的 Docker Desktop 安装包，双击安装包并按照提示完成安装。安装完成后，启动 Docker Desktop 即可。
- Windows 系统
Windows 用户同样可以使用 Docker Desktop 进行安装。访问Docker 官方网站，下载 Windows 版本的 Docker Desktop，安装过程中根据提示进行操作。安装完成后，打开 Docker Desktop，等待其初始化完成。
###### 2、项目配置
- 环境变量配置
本项目通过环境变量进行配置，在启动容器之前，需要根据实际需求设置环境变量。在项目根目录的.env文件，将文件配置替换为实际的数据库配置信息或其他项目所需的配置信息。
- docker-compose.yml 说明
因为项目包含多个服务（如后端服务、数据库服务等），使用docker-compose.yml文件来定义和管理这些服务。
```yaml
services:
  # ---------------------- 前端服务 ----------------------
  frontend:
    build: ./frontend
    volumes:
      # - /宿主机路径:/容器内路径:选项(权限)
      - ./data:/data
    ports:
      - "80:80"
    depends_on:
      - service-api
      - service-analysis
    networks:
      - app-network

  # ---------------------- 后端服务 ----------------------
  service-api:
    build: ./backend/service-api
    environment:
      - DB_HOST=db
      - DB_API_NAME=${DB_API_NAME}
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
      - API_BASE_URL=${API_BASE_URL}
    depends_on:
      - db
    networks:
      - app-network

  service-analysis:
    build: ./backend/service-analysis
    environment:
      - DB_HOST=db
      - DB_ANALYSIS_NAME=${DB_ANALYSIS_NAME}
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
      - ANALYSIS_BASE_URL=${ANALYSIS_BASE_URL}
    depends_on:
      - db
      - rabbitmq
    networks:
      - app-network

  # ---------------------- 共享服务 ----------------------
  db:
    image: mysql:8.0
    volumes:
      - mysql-data:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
      MYSQL_DATABASE: ${DB_API_NAME}, ${DB_ANALYSIS_NAME}
      MYSQL_USER: ${DB_USER}
      MYSQL_PASSWORD: ${DB_PASSWORD}
    command: ['mysqld', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_unicode_ci']
    networks:
      - app-network

  rabbitmq:
    image: rabbitmq:3.12.13-management-alpine
    volumes:
      - rabbitmq-data:/var/lib/rabbitmq
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      RABBITMQ_DEFAULT_USER: ${RABBITMQ_USER}
      RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASSWORD}
    networks:
      - app-network

networks:
  app-network:

volumes:
  mysql-data:
  rabbitmq-data:
```
- docker-compose.yml 说明
项目中，定义了多个服务：frontend服务用于运行项目的前端应用，service-api 服务用与运行项目的后端API服务，service-analysis 服务用于运行项目的后端service-analysis服务和Celery异步任务服务器，db 服务使用 MySQL 8.0 镜像作为数据库服务，rabbitmq服务使用 3.12.13-management-alpine 镜像作为消息队列服务。frontend服务依赖于service-api和service-analysis服务，并且通过端口映射将容器内的 80 端口映射到主机的 80 端口，同时将环境变量传递给容器。service-api服务依赖于db服务，并且通过端口映射将容器内的 8001 端口映射到主机的 8001 端口，同时将环境变量传递给容器。service-analysis服务依赖于db和rabbitmq服务并且通过端口映射将容器内的 8001 端口映射到主机的 8001 端口，同时将环境变量传递给容器。db服务则通过环境变量设置数据库的 root 密码和数据库名称，并使用卷来持久化存储数据库数据。rabbitmq服务则通过环境变量设置用户名和密码，并使用卷来持久化存储数据库数据。
##### 3、启动项目
- 使用docker-compose.yml管理项目，执行以下命令启动项目：
```bash
docker-compose up -d
```
-d参数表示以后台模式运行容器。启动完成后，可以通过浏览器访问http://localhost:80（假设项目运行在 80 端口）来查看项目是否正常启动。
###### 4、常见问题及解决方法
- 端口冲突
如果在启动容器时遇到端口冲突的问题，例如提示Error response from daemon: Ports are not available: exposing port TCP 0.0.0.0:8000 -> 0.0.0.0:0: listen tcp 0.0.0.0:8000: bind: address already in use，说明主机上的 8000 端口已经被其他进程占用。可以通过以下方式解决：
关闭占用该端口的进程。使用lsof -i:8000命令查看占用 8000 端口的进程，然后使用kill命令终止该进程。例如，如果查看结果显示进程 ID 为1234，则执行kill 1234。
修改项目的端口映射。在Dockerfile或docker-compose.yml文件中，将端口映射修改为其他未被占用的端口，如8080。
- 依赖安装失败
如果在构建镜像过程中，出现依赖安装失败的情况，例如提示Could not find a version that satisfies the requirement <package_name>，可能是因为依赖包的版本不兼容或无法从默认的包源获取。可以尝试以下解决方法：
检查requirements.txt文件中依赖包的版本是否正确，确保版本号与项目兼容。
更换包源。例如，在requirements.txt文件中指定使用国内的包源，如清华大学的 PyPI 镜像：
-i https://pypi.tuna.tsinghua.edu.cn/simple

或者在Dockerfile中安装依赖时指定包源：
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

- 容器无法正常启动
如果容器启动后很快退出，没有正常运行项目，可以通过以下命令查看容器的日志，以获取更多错误信息：
docker logs myproject-container

上述命令中的myproject-container是容器的名称，根据实际情况进行替换。通过查看日志，可以定位到具体的错误原因，如代码语法错误、配置文件读取失败等，并进行相应的修复。
###### 5、停止和删除项目
- 停止容器：
执行以下命令停止所有服务：
docker-compose down

- 删除容器
停止容器后，可以执行以下命令删除容器：
docker-compose down --volumes

通过以上步骤，你应该能够顺利使用 Docker 启动本项目。如果在操作过程中遇到其他问题，随时联系iPscDB的开发团队或查阅Docker官方文档。