# iPscDB
![17293d1c48780bb6fb9901ad9d14ac19](https://github.com/user-attachments/assets/7bffed40-96b3-4340-a57f-3b3023d4aadc)
## Welcome to iPscDB
- iPscDB is a single cell transcriptomic data resource that includes cell markers, single cell maps, and a wealth of data analysis tools. At present, data from 23 species of model plants, including Arabidopsis thaliana, rice, corn, tomato, and tobacco, including more than 270,480 marker genes and more than 3 million single cell data, have been collected, providing comprehensive and relatively accurate cell markers and cell maps for cell integration and single cell research in different plants and tissues.
- System website: https://www.tobaccodb.org/ipscdb/homePage
- Github: https://github.com/TobaccoDB/iPscDB.git

## Project structure
- frontend: Frontend project
  - public: Static resources
  - src: Source code
    - api: API interface
    - components: Components
    - router: Router
    - store: State management
    - utils: Utility functions
    - App.vue: Main application component
    - main.js: Entry file
  - .env.development: Development environment configuration file
  -.env.production: Production environment configuration file
  - babel.config.js: Babel configuration file
  - package.json: Project dependency configuration file
  - vue.config.js: Vue configuration file
- backend: Backend project
  - service-api: API service
    - excel: Excel temporary file processing module
    - logs: Log files
    - plant_marker: Application
    - static: Static files
    - temps: Temporary files
    - manage.py: Django management script
    - requirements.txt: Python dependency configuration file
    - local_settings: Configuration file
    - Dockerfile: Docker configuration file
  - service-analysis: Data analysis service
    - logs: Log files
    - django_server: Application
    - pids: Process ID files
    - celery_restart.sh: Celery restart script
    - celert_start.sh: Celery start script
    - celery_stopwait.sh: Celery stop script
    - manage.py: Django management script
    - requirements.txt: Python dependency configuration file
    - local_settings: Configuration file
    - Dockerfile: Docker configuration file
    - start.sh: Start script
-.env: Environment variable configuration file
- docker-compose.yml: Docker configuration file
- README.md: Project description document
## Project startup
### Local startup
- Frontend startup
Enter the frontend directory, execute the following command to start the frontend project (assuming you have installed the node service, you can refer to the official website for installation):
  ```bash
  npm install
  npm run dev
  ```
- Backend startup     
Enter the backend directory (assuming you have installed Python 3.9 and have installed the MySQL database service locally),
  - Start the service-api service, enter the service-api directory (modify the local_settings.py database information according to your local database configuration):
  Execute the following command to start:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python manage.py runserver 0.0.0.0:8001
    ```
  - Start the service-analysis service, enter the service-analysis directory (modify the local_settings.py database information according to your local database configuration):
  Execute the following command to start:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

  Execute the following command to start:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python manage.py runserver IP_ADDRESS    python manage.py runserver 0.0.0.0:8002
    ```
### Docker startup
#### Docker startup project documentation
##### Prerequisites
Before using Docker to start this project, make sure your system has Docker installed. Installation methods for different operating systems are as follows:
- Linux system
For Ubuntu, open the terminal and execute the following commands:
  ```bash
  sudo apt update
  sudo apt install docker.io
  sudo systemctl start docker
  sudo systemctl enable docker
  ```
For other Linux distributions, refer to the Docker official documentation for installation.
- macOS system
In macOS, you can install Docker Desktop. Visit the Docker official website to download the Windows version of Docker Desktop, and follow the instructions to complete the installation. After installation, start Docker Desktop.
- Windows system
Windows users can also install Docker Desktop. Visit the Docker official website, download the Windows version of Docker Desktop, and follow the instructions to complete the installation. After installation, open Docker Desktop, and wait for it to initialize.
##### Project configuration
- Environment variable configuration
This project uses environment variables for configuration. Before starting the container, you need to set the environment variables according to the actual requirements. In the root directory of the .env file, replace the file configuration with actual database configuration information or other project required configuration information.
- docker-compose.yml description
Because the project contains multiple services (such as frontend services, backend services, etc.), use docker-compose.yml to define and manage these services.
```yaml
services:
  # ---------------------- 前端服务 ----------------------
  frontend:
    build:./frontend
    volumes:
      # - /宿主机路径:/容器内路径:选项(权限)
      -./data:/data
    ports:
      - "80:80"
    depends_on:
      - service-api
      - service-analysis
    networks:
      - app-network
  # ---------------------- 后端服务 ----------------------
  service-api:
    build:./backend/service-api
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
    build:./backend/service-analysis
    environment:
      - DB_HOST=db
      - DB_ANALYSIS_NAME=${DB_ANALYSIS_NAME}
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
      - API_BASE_URL=${API_BASE_URL}
    depends_on:
      - db
      - rabbitmq
    networks:
      - app-network
  db:
    image: mysql:8.0
    volumes:
      - mysql-data:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
      MYSQL_DATABASE: ${DB_API_NAME}
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
- Docker-compose description
The docker-compose.yml file defines the services (such as frontend services, backend services, etc.) of the project. The services are defined in the services section, and each service is defined in a separate section.
In the project, multiple services were defined: the frontend service is used to run the front-end application of the project, the service-api service is used to run the back-end API service of the project, the service-analysis service is used to run the back-end service-analysis service and the Celery asynchronous task server, the db service uses the MySQL 8.0 image as the database service, and the rabbitmq service uses the 3.12.13-management-alpine image as the message queue service. The frontend service depends on the service-api and service-analysis services, and maps the 80 port inside the container to the 80 port on the host through port mapping, while passing environment variables to the container. The service-api service depends on the db service, and maps the 8001 port inside the container to the 8001 port on the host through port mapping, while passing environment variables to the container. The service-analysis service depends on the db and rabbitmq services and maps the 8001 port inside the container to the 8001 port on the host through port mapping, while passing environment variables to the container. The db service sets the root password and database name of the database through environment variables and uses volumes to persistently store the database data. The rabbitmq service sets the username and password through environment variables and uses volumes to persistently store the database data. The app-network network is used to connect the services, and the mysql-data and rabbitmq-data volumes are used to persistently store the database data.
##### Start the project
- Use docker-compose.yml to manage the project and execute the following command to start the project:
  ```bash
  docker-compose up -d
  ```

-d parameter runs the container in the background. After starting the project, you can access the project through the browser at URL_ADDRESS-d parameter runs the container in the background. After starting the project, you can access the project through the browser at http://localhost:80 (assuming the project runs on port 80).
###### Common problems and solutions
- Port conflict 
If you encounter port conflicts when starting the container, for example, when executing docker-compose up -d, you will see an error message similar to the following:
  ```bash
  Error response from daemon: Ports are not available: exposing port TCP 0.0.0.0:8000 -> 0.0.0.0:0: listen tcp 0.0.0.0:8000: bind: address already in use
  ```
This means that the host port 8000 is already in use by another process. You can solve this problem by:
Closing the process using the host port 8000. Use the lsof -i:8000 command to view the process using the host port 8000, and then use the kill command to terminate the process. For example, if the view result shows the process ID as 1234, execute kill 1234.
Modify the project port mapping. In the Dockerfile or docker-compose.yml file, modify the port mapping to an unused port, such as 8080.
- Dependency installation failure
If you encounter dependency installation failures during the image build process, for example, when executing docker-compose up -d, you will see an error message similar to the following:
  ```bash
  Could not find a version that satisfies the requirement <package_name>
  ```
This means that the dependency package version is not compatible or cannot be obtained from the default package source. You can try the following solutions:
Check the requirements.txt file for dependency package version compatibility. Ensure that the version number is compatible with the project.
Replace the package source. For example, in the requirements.txt file, specify a domestic package source, such as the PyPI mirror of the Tsinghua University:
  ```bash
Replace the package source. For example, in the requirements.txt file, specify a domestic package source, such as the PyPI mirror of the Tsinghua University:
  ```bash
  -i URL_ADDRESS  -i https://pypi.tuna.tsinghua.edu.cn/simple
  ```
Or in the Dockerfile, install dependencies with the specified package source:
  ```bash
Or in the Dockerfile, install dependencies with the specified package source:
bash
  RUN pip install --no-cache-dir -i URL_ADDRESS  RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
  ```
- Container startup failure
If the container starts and exits quickly without running the project, you can view the container logs to get more error information:
  ```bash
  docker logs myproject-container
  ```
The command above shows the container name as myproject-container. Replace it with the actual container name. By viewing the logs, you can locate the specific error reason, such as syntax errors in the code, failed configuration file reading, etc., and make the necessary fixes.
###### Stop and delete the project
- Stop the container:
Execute the following command to stop all services:
  ```bash
  docker-compose down
  ```
- Delete the container
Stop the container and then execute the following command to delete the container:
  ```bash
  docker-compose down --volumes
  ```
By following these steps, you should be able to successfully start this project using Docker. If you encounter other problems during operation, please contact the development team of iPscDB or refer to the official documentation of Docker.
