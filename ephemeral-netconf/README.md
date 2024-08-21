# Ephemeral DB python client

This is a simple script to illustrate the "flowspec lite" use-case covered by the following Juniper Techpost: 

We'll highlight the power of Ephemeral-DB (for very fast commit) and the fast-lookup-tuple feature implemented in Junos 24.2R1. 

## Install py dependencies

Make sure you have all dependencies. 

```shell
pip3 install -r requirements.txt
```

## Router configuration 

Enable netconf:

```junos
edit

set system services netconf ssh

commit comment "add-netconf" and-quit 
````

Create a Ephemeral DB on your device - choose the name you want. Here below, I used the name "fwf_instance"

```junos
edit

set system configuration-database ephemeral instance fwf_instance
set system configuration-database ephemeral ignore-ephemeral-default

commit comment "add-ephemeral-db" and-quit 
```

Then create a simple filter, here "FAST-LOOKUP-TUPLE-FILTER", with 2 terms. The first when will block all 5-tuple entries included in the fast-lookup-tuple-list. This list will be dynamically updated by our script. The second term will accept anything. 

Create also an empty fast-lookup-tuple-list, here "FLOWS_TO_BLOCK". Remember the name of this list for later. Finally, applied your filter on a given interface and direction. 

```junos
edit

set firewall family inet filter FAST-LOOKUP-TUPLE-FILTER term 1 from fast-lookup-tuple-list FLOWS_TO_BLOCK
set firewall family inet filter FAST-LOOKUP-TUPLE-FILTER term 1 then count TERM1-CPT
set firewall family inet filter FAST-LOOKUP-TUPLE-FILTER term 1 then discard
set firewall family inet filter FAST-LOOKUP-TUPLE-FILTER term end then accept

set policy-options fast-lookup-tuple-list FLOWS_TO_BLOCK 

set interfaces ae66 unit 0 family inet filter input FAST-LOOKUP-TUPLE-FILTER

commit comment "add-filtering-config" and-quit 
```

## Play with the script 

There are 3 samples "jobs" files provided. Each file contains a list of five-tuple entries to add or remove. The format is 

```shell
<a|d>;<destination-address>:<source-address>:<proto>:<src-port>:<dest-port>
```
**a** means "add" and **b** means "delete" 

- The first file: jobs1.txt contains a list of random 5-tuple to add in the prefix-list you configured previously.  
- The second file: jobs2.txt will remove one entry 
- The third file: jobs3.txt will remove all the entries created by jobs1.txt 

Let's play with the script to dynamically add several entries in our ephemeral DB "fwf_instance" for our list "FLOWS_TO_BLOCK".

```shell
python3 ephclient.py -r <router-name> -u <rw-username> -p <password> -e fwf_instance -l FLOWS_TO_BLOCK -j jobs.txt
```

Check entries have been well provisionned:

```junos
show ephemeral-configuration instance fwf_instance  

show ephemeral-configuration instance fwf_instance | count
```

Now, try to delete one entry by applying "jobs2": 

```shell
python3 ephclient.py -r <router-name> -u <rw-username> -p <password> -e fwf_instance -l FLOWS_TO_BLOCK -j jobs2.txt
```

Check the fast-lookup-tuple-list has been updated:

```junos
show ephemeral-configuration instance fwf_instance  

show ephemeral-configuration instance fwf_instance | count  
```

As expected there is one less entry. Finally run "jobs3" to remove all entries. 

```shell
python3 ephclient.py -r <router-name> -u <rw-username> -p <password> -e fwf_instance -l FLOWS_TO_BLOCK -j jobs3.txt
```

Check the fast-lookup-tuple-list is now empty:
```junos
show ephemeral-configuration instance fwf_instance  
```

Well done...You rock. 
