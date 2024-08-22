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
python3 ephclient.py -r <router-name> -u <rw-username> -p <password> -e fwf_instance -l FLOWS_TO_BLOCK -j jobs1.txt
2024-08-22 01:27:48,962 [INFO] Job file has been successfully opened
2024-08-22 01:27:48,963 [INFO] Job list has been successfully prepared
2024-08-22 01:27:49,461 [INFO] Netconf session has been successfully opened
2024-08-22 01:27:49,700 [INFO] Configuration has been successfully loaded
2024-08-22 01:27:50,030 [INFO] Configuration has been successfully committed
2024-08-22 01:27:50,132 [INFO] All jobs done, bye...
```

Check entries have been well provisionned:

```junos
show ephemeral-configuration instance fwf_instance  
policy-options {
    fast-lookup-tuple-list FLOWS_TO_BLOCK {
        101.47.18.4:184.107.232.153:17:46921:36908;
        104.210.216.94:1.207.48.66:17:24458:42576;
        112.121.130.104:125.252.225.66:6:37310:38836;
        117.204.162.195:6.55.58.229:17:46779:39175;
        119.239.243.156:62.49.49.95:6:3999:28921;
        119.82.162.214:158.145.33.6:6:64958:28559;
        123.135.136.219:187.133.101.2:17:14148:27148;
        124.120.226.131:49.30.184.117:6:49848:18034;
        132.216.96.113:9.70.21.168:17:58086:43029;
        134.35.138.85:139.231.55.91:6:33666:53557;
        14.40.255.64:144.27.183.250:6:48984:17197;
        147.14.168.10:157.41.136.229:6:31988:25168;
        156.57.172.165:50.109.69.70:17:18421:19492;
        16.226.54.23:49.253.197.116:6:52087:56651;
        170.23.201.75:42.240.64.6:17:58401:49325;
        176.32.69.95:122.115.54.247:6:7691:34216;
        176.5.94.96:179.54.161.87:6:2911:43987;
        178.174.36.5:85.239.217.100:6:55952:43802;
        184.227.9.231:117.254.118.97:17:34623:59489;
        194.200.151.232:74.232.131.35:17:49742:49900;
        198.62.131.92:23.125.240.10:17:29434:46651;
        2.148.201.36:162.36.148.193:17:55492:64036;
        204.252.199.150:114.184.14.25:17:39920:9315;
        24.152.121.190:104.42.119.119:17:53319:11457;
        3.143.172.222:207.47.218.205:6:61662:43458;
        39.80.244.79:201.240.2.248:6:8969:4900;
        47.111.149.195:124.192.247.116:6:45073:60035;
        47.236.74.182:17.56.131.127:6:42127:63867;
        48.135.165.38:189.118.44.129:17:9594:181;
        61.12.46.183:138.13.152.163:6:54053:2677;
        61.85.90.150:11.204.66.142:6:36236:32707;
        68.164.218.203:198.191.121.6:6:60988:30058;
        69.102.26.242:71.223.170.46:17:42462:35468;
        73.158.159.131:65.107.22.88:17:37038:55244;
        79.134.146.121:202.177.83.184:17:57990:50807;
        81.62.36.126:191.148.112.147:6:21553:60564;
        98.160.46.142:177.90.40.122:6:31672:62096;
    }
}

show ephemeral-configuration instance fwf_instance | count
Count: 42 lines
```

Now, try to delete one entry by applying "jobs2": 

```shell
python3 ephclient.py -r <router-name> -u <rw-username> -p <password> -e fwf_instance -l FLOWS_TO_BLOCK -j jobs2.txt
2024-08-22 01:33:40,437 [INFO] Job file has been successfully opened
2024-08-22 01:33:40,437 [INFO] Job list has been successfully prepared
2024-08-22 01:33:40,990 [INFO] Netconf session has been successfully opened
2024-08-22 01:33:41,195 [INFO] Configuration has been successfully loaded
2024-08-22 01:33:41,509 [INFO] Configuration has been successfully committed
2024-08-22 01:33:41,612 [INFO] All jobs done, bye...
```

Check the fast-lookup-tuple-list has been updated:

```junos
show ephemeral-configuration instance fwf_instance  
policy-options {
    fast-lookup-tuple-list FLOWS_TO_BLOCK {
        101.47.18.4:184.107.232.153:17:46921:36908;
        104.210.216.94:1.207.48.66:17:24458:42576;
        112.121.130.104:125.252.225.66:6:37310:38836;
        117.204.162.195:6.55.58.229:17:46779:39175;
        119.239.243.156:62.49.49.95:6:3999:28921;
        119.82.162.214:158.145.33.6:6:64958:28559;
        123.135.136.219:187.133.101.2:17:14148:27148;
        124.120.226.131:49.30.184.117:6:49848:18034;
        132.216.96.113:9.70.21.168:17:58086:43029;
        134.35.138.85:139.231.55.91:6:33666:53557;
        14.40.255.64:144.27.183.250:6:48984:17197;
        147.14.168.10:157.41.136.229:6:31988:25168;
        156.57.172.165:50.109.69.70:17:18421:19492;
        16.226.54.23:49.253.197.116:6:52087:56651;
        170.23.201.75:42.240.64.6:17:58401:49325;
        176.32.69.95:122.115.54.247:6:7691:34216;
        176.5.94.96:179.54.161.87:6:2911:43987;
        178.174.36.5:85.239.217.100:6:55952:43802;
        184.227.9.231:117.254.118.97:17:34623:59489;
        194.200.151.232:74.232.131.35:17:49742:49900;
        198.62.131.92:23.125.240.10:17:29434:46651;
        2.148.201.36:162.36.148.193:17:55492:64036;
        204.252.199.150:114.184.14.25:17:39920:9315;
        24.152.121.190:104.42.119.119:17:53319:11457;
        3.143.172.222:207.47.218.205:6:61662:43458;
        39.80.244.79:201.240.2.248:6:8969:4900;
        47.111.149.195:124.192.247.116:6:45073:60035;
        47.236.74.182:17.56.131.127:6:42127:63867;
        61.12.46.183:138.13.152.163:6:54053:2677;
        61.85.90.150:11.204.66.142:6:36236:32707;
        68.164.218.203:198.191.121.6:6:60988:30058;
        69.102.26.242:71.223.170.46:17:42462:35468;
        73.158.159.131:65.107.22.88:17:37038:55244;
        79.134.146.121:202.177.83.184:17:57990:50807;
        81.62.36.126:191.148.112.147:6:21553:60564;
        98.160.46.142:177.90.40.122:6:31672:62096;
    }
}

show ephemeral-configuration instance fwf_instance | count  
Count: 41 lines
```

As expected there is one less entry. Finally run "jobs3" to remove all entries. 

```shell
python3 ephclient.py -r <router-name> -u <rw-username> -p <password> -e fwf_instance -l FLOWS_TO_BLOCK -j jobs3.txt
2024-08-22 01:36:57,417 [INFO] Job file has been successfully opened
2024-08-22 01:36:57,418 [INFO] Job list has been successfully prepared
2024-08-22 01:36:57,879 [INFO] Netconf session has been successfully opened
2024-08-22 01:36:58,094 [INFO] Configuration has been successfully loaded
2024-08-22 01:36:58,389 [INFO] Configuration has been successfully committed
2024-08-22 01:36:58,491 [INFO] All jobs done, bye...
```

Check the fast-lookup-tuple-list is now empty:
```junos
show ephemeral-configuration instance fwf_instance  
policy-options {
    fast-lookup-tuple-list FLOWS_TO_BLOCK;
}
```

Well done...You rock. 
