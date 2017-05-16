# ict-demo-GA
[IntegrCiTy] Stockholm General Assembly DEMO

docker run -d --hostname my-rabbit -p 5672:5672 --name some-rabbit rabbitmq:alpine

docker run -d --hostname my-redis -p 6379:6379 --name some-redis redis:alpine

docker run -it --rm integrcity/orchestrator host_rabbitmq config_file schedule_file

docker run -it --rm integrcity/fmu_node host_rabbitmq host_redis wrap_file
