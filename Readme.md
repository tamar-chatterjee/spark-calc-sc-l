**Info**

- This calculator service is deployed in our Infra Swarm.
  - Manager Nodes
    - scs-aapse1a-d-ds2infsrv-m01
    - scs-aapse1b-d-ds2infsrv-m02
  - Worker Nodes
    - scs-aapse1a-d-ds2infsrv-w01
    - scs-aapse1b-d-ds2infsrv-w02
- We haven't setup an automated pipeline deployment as of now.
- We need to copy over the changes to deployment location [**/mnt/gluster_docker_volumes/spark-calc-sc**] in any swarm node.
- Use below commands to create a new image on the worker nodes.
  ```
  cd /mnt/gluster_docker_volumes/spark-calc-sc
  docker build -t spark-calc-sc:latest .
  ```
- Deploy the stack again from any of the master nodes.
  ```
  cd /mnt/gluster_docker_volumes/spark-calc-sc
  docker stack rm spark-calc-sc
  docker stack deploy -c docker-compose.yml spark-calc-sc
  ```
