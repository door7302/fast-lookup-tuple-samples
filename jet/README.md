# JetClient python client

This is a simple script to illustrate the how to program fast-lookup-tuple entries by using the JET API. This is covered by the following Juniper Techpost: 

## Install py dependencies

Make sure you have all dependencies. 

```shell
pip3 install -r requirements.txt
```

## Router configuration 

Enable GRPC server (SSL is recommanded for simplicity we use clear-text mode) - here we bind the gRPC server to the tcp port 9339. 

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
2024-08-22 02:02:07,558 [INFO] Job file has been successfully opened
2024-08-22 02:02:07,602 [INFO] Connected to gRPC Server
2024-08-22 02:02:07,603 [INFO] Create implicit JET filter named ON_DEMAND_JET
2024-08-22 02:02:07,613 [INFO] JET filter successfully created
2024-08-22 02:02:07,613 [INFO] Bind the implicit JET filter to interface ae66.0
2024-08-22 02:02:07,621 [INFO] JET filter successfully bound
2024-08-22 02:02:09,622 [INFO] Try to add a term for entry: ['204.252.199.150', '114.184.14.25', '17', '39920', '9315']
2024-08-22 02:02:09,631 [INFO] Term successfully added
2024-08-22 02:02:10,632 [INFO] Try to add a term for entry: ['198.62.131.92', '23.125.240.10', '17', '29434', '46651']
2024-08-22 02:02:10,641 [INFO] Term successfully added
2024-08-22 02:02:11,642 [INFO] Try to add a term for entry: ['47.236.74.182', '17.56.131.127', '6', '42127', '63867']
2024-08-22 02:02:11,652 [INFO] Term successfully added
2024-08-22 02:02:12,654 [INFO] Try to add a term for entry: ['48.135.165.38', '189.118.44.129', '17', '9594', '181']
2024-08-22 02:02:12,663 [INFO] Term successfully added
2024-08-22 02:02:13,664 [INFO] Try to add a term for entry: ['39.80.244.79', '201.240.2.248', '6', '8969', '4900']
2024-08-22 02:02:13,673 [INFO] Term successfully added
2024-08-22 02:02:14,674 [INFO] Try to add a term for entry: ['119.239.243.156', '62.49.49.95', '6', '3999', '28921']
2024-08-22 02:02:14,683 [INFO] Term successfully added
2024-08-22 02:02:15,683 [INFO] Try to remove a term for entry: ['47.236.74.182', '17.56.131.127', '6', '42127', '63867']
2024-08-22 02:02:15,692 [INFO] Term successfully deleted
2024-08-22 02:02:16,694 [INFO] All done, time to sleep... Type Ctrl^C for quitting - JET filter will be automatically removed.
```

As explained in the TechPost the JET filter "ON_DEMAND_JET" has been provisionned on the PFE. From the user, this filter is hidden and the program and statistics can be retrieve only by using PFE shell commands or using JET API to collect stats remotely. Just for illustration purposes, let's have a look into of the output of some PFE commands. Here we work on a MX304. 

```shell
# Attche the vty to FPC0 
start shell pfe network fpc0

# list the firewall filters and have a look at your filter name
root@fpc0:pfe> show firewall | match "token|ON_DEMAND_JET" 
Name                                   Index          Token            Status
ON_DEMAND_JET                          100663298       4455            DMEM

# Check the program of the filter - use the token id above
root@fpc0:pfe> show sandbox token 4455

AftNode : bindMask:0xf AftFilterTemplate token:4455 group:0 tag:dfw(dfw) TagIndex:440 nodeMask:Default OptParams:  = app:70.87./16
{FilterName:ON_DEMAND_JET Index:100663298 FilterState:FilterEnd flags:0x0000000000000000 flagsSet:No specific flags set
}
JnhHandle :  JnhHandleFilterTemplate Jnh:0x0 PfeInst:0 Paddr:0x0 Vaddr:0x0 JnhDecodeAllowed:Yes
Filter index = 100663298
Optimization flag: 0xf7
Filter notify host id = 0
Pfe Mask = 0xFFFFFFFF
jnh inst = 0x0
Filter properties: None
Filter state = CONSISTENT
term 8bbbec4c1610fa733cb6cf1dfb
term priority 0
    fast-lookup-tuple
        39.80.244.79.201.240.2.248.6.8969.4900/104 -> action in 25537ef085412ca6a5bdd8e36b
        48.135.165.38.189.118.44.129.17.9594.181/104 -> action in dfcee617798b05da99889fc241
        119.239.243.156.62.49.49.95.6.3999.28921/104 -> action in 427df5222036b1701bbcd475b5
        198.62.131.92.23.125.240.10.17.29434.46651/104 -> action in a53e419714def97971acc2b8b1
        204.252.199.150.114.184.14.25.17.39920.9315/104
        false branch to match action in rule END
 
    then
        discard
        count cpt-8bbbec4c1610fa733cb6cf1dfb
term a53e419714def97971acc2b8b1
term priority 0
 
    then
        discard
        count cpt-a53e419714def97971acc2b8b1
term dfcee617798b05da99889fc241
term priority 0
 
    then
        discard
        count cpt-dfcee617798b05da99889fc241
term 25537ef085412ca6a5bdd8e36b
term priority 0
 
    then
        discard
        count cpt-25537ef085412ca6a5bdd8e36b
term 427df5222036b1701bbcd475b5
term priority 0
 
    then
        discard
        count cpt-427df5222036b1701bbcd475b5
term END
term priority 0
 
    then
        accept
        count all
Previous nodes count: 1      
Next nodes count    : 0      
Entries count       : 0          

# finaly collect filter counters - use the index of the filter (above)
root@fpc0:pfe> show firewall counter index 100663298 
Name                            Packets         Bytes
all                             13059117383     5420033541186
cpt-25537ef085412ca6a5bdd8e36b  0               0     
cpt-427df5222036b1701bbcd475b5  0               0     
cpt-8bbbec4c1610fa733cb6cf1dfb  0               0     
cpt-a53e419714def97971acc2b8b1  0               0     
cpt-dfcee617798b05da99889fc241  0               0     


```

Well done...You rock. 
