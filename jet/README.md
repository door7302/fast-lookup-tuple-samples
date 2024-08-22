# JetClient python client

This is a simple script to illustrate the how to program fast-lookup-tuple entries by using the JET API. This is covered by the following Juniper Techpost: 

## Install py dependencies

Make sure you have all dependencies. 

```shell
pip3 install -r requirements.txt
```

## Router configuration 

Enable GRPC server (SSL is recommanded for simplicity we use clear-text mode) - here we vind the port 9339 to gRPC server. 

```junos
edit

set system services extension-service request-response grpc clear-text port 9339
set system services extension-service request-response grpc skip-authentication
set system services extension-service notification allow-clients address 0.0.0.0/0

commit comment "add-grpc-server" and-quit 
````

## Play with the script 

All the JET proto files are located in ./proto folder. The firewall filter API is described in ./proto/2/jnx_firewall_service.proto 
This file and some others (for dependencies) have been compiled via protoc tools. All requiered files have been already compiled for you and stored in the ./lib directory. Here we just share the command we used for compiling those files:

```
# For illustration only:
python3 -m grpc_tools.protoc -I./2 --python_out=. --grpc_python_out=. 2/jnx_common_base_types.proto 2/jnx_common_addr_types.proto 2/jnx_firewall_service.proto 2/authentication_service
```

There is on jobs.txt file that contains the list of five-tuple entries to add or delete via the JET API. The format is 

```shell
<a|d>;<destination-address>:<source-address>:<proto>:<src-port>:<dest-port>
```
**a** means "add" and **b** means "delete" 

Let's play with the script - here we will applied a dynamic filter (here, "ON_DEMAND_JET") to a given interface (here, ae66.0) - and we will provision the jobs included in jobs.txt

```
python3 jetclient.py -t <router-name:port> -u <rw-username> -p <password> -i ae66.0 -f ON_DEMAND_JET -j jobs.txt
```



Well done...You rock. 
