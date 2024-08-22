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


Well done...You rock. 
