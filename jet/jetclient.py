# Before you need to compile proto files and move generated .py files in ./lib/ 
# cd junos-extension-toolkit/24.2/24.2R1.17/
# python3 -m grpc_tools.protoc -I./2 --python_out=. --grpc_python_out=. 2/jnx_common_base_types.proto 2/jnx_common_addr_types.proto 2/jnx_firewall_service.proto 2/authentication_service

import grpc
import sys
import os
import logging
import argparse
import time
import hashlib

# Add the 'lib' directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

import jnx_firewall_service_pb2 as pb
import jnx_common_addr_types_pb2 as pb2
import jnx_firewall_service_pb2_grpc as pb3
from authentication_service_pb2 import *

import authentication_service_pb2 as auth_pb2
import authentication_service_pb2_grpc as auth_pb2_grpc

def create_fixed_length_hash(input_string, length=13):
    input_bytes = input_string.encode('utf-8')
    hash_object = hashlib.sha256()
    hash_object.update(input_bytes)
    hash_bytes = hash_object.digest()
    fixed_length_hash = hash_bytes[:length]
    return str(fixed_length_hash.hex())

try: 
    if __name__ == '__main__':
        parser = argparse.ArgumentParser(description="Simple JET client - Fast Tuple client")
        parser.add_argument('-t', '--target', nargs=1, help='target router-name:port', required=True)
        parser.add_argument('-u', '--user', nargs=1, help='Username', required=True)
        parser.add_argument('-p', '--pwd', nargs=1, help='Password', required=True)
        parser.add_argument('-s', '--secure', nargs=1, help='Secure grpc channel - provide pem certificate', required=False)
        parser.add_argument('-i', '--interface', nargs=1, help='Interface on which we will bind the filter', required=True)
        parser.add_argument('-f', '--file', nargs=1, help='Filename with action', required=True)
        options = parser.parse_args()

        # configure logger
        logger = logging.getLogger('mylogger')
        logger.setLevel(logging.DEBUG)
        sh = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        sh.setFormatter(formatter)
        logger.addHandler(sh) 

        # Retrieve arguments 
        target = options.target[0]
        user = options.user[0]
        password = options.pwd[0]    
        filename = options.file[0]
        secure = False
        if options.secure:
            cert = options.secure[0]
            secure = True
        interface = options.interface[0]

        if ":" not in target:
            logger.error("target must have the format <router-name>:<port>")
            exit()
        
        # Open filename includiing the jobs to commit 
        try:
            with open(filename, 'r') as file:
                file_lines = file.readlines()
                
            file_lines = [line.strip() for line in file_lines]
            if len(file_lines) == 0:
                logger.error("File is empty - nothing to do - exit")
                exit()

        except FileNotFoundError:
            logger.error("The file was not found")
            exit()
        except IOError:
            logger.error("An I/O error occurred while handling the file")
            exit()
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            exit()
        
        logger.info("Job file has been successfully opened")    

        # open gRPC channel
        if secure:
            creds = grpc.ssl_channel_credentials(open(cert, 'rb').read(),None, None)
            channel = grpc.secure_channel(target , creds, options=(('grpc.ssl_target_name_override', target.split(":")[0].split(".")[0],),))
        else: 
            channel = grpc.insecure_channel(target)
        
        #create stub for authentication services
        stub = auth_pb2_grpc.LoginStub(channel)

        #Authenticate
        login_request = auth_pb2.LoginRequest(user_name=user, password=password, client_id="fastlookuptuple")
        login_response = stub.LoginCheck(login_request, 60)
        
        #Check if authentication is successful
        if login_response.result == True:
            logger.info("Connected to gRPC Server")
        else:
            logger.error("gRPC Server Connection failed!!!")
            logger.error(login_response.result)
            exit()
        
        mystub = pb3.FirewallStub(channel)

        ##################################################################################
        # create an implicit filter with only the last term 
        ##################################################################################
        logger.info("Create implicit JET filter named ON_DEMAND_5_TUPLE")

        # Create FilterTermInetTerminatingAction
        terminating_action = pb.FilterTermInetTerminatingAction(accept=True)
        
        # Create FilterTermInetNonTerminatingAction
        non_terminating_action = pb.FilterTermInetNonTerminatingAction(count=pb.ActionCounter(counter_name="all"))

        # Create FilterAdjacency
        adjacency = pb.FilterAdjacency(type=pb.FilterAdjacencyType.TERM_AFTER, term_name="")

        # Create FilterTermInetAction
        inet_action = pb.FilterTermInetAction(action_t=terminating_action, actions_nt=non_terminating_action)

        # Create FilterInetTerm
        inet_term = pb.FilterInetTerm(
            term_name="END",
            term_op=pb.FilterTermOperation.TERM_OPERATION_ADD,
            adjacency=adjacency,
            actions=inet_action
        )

        # Create FilterTerm
        filter_term = pb.FilterTerm(inet_term=inet_term)

        # Create FilterAddRequest
        filter_add_request = pb.FilterAddRequest(
            name="ON_DEMAND_5_TUPLE",
            type=pb.FilterTypes.TYPE_CLASSIC,
            family=pb.FilterFamilies.FAMILY_INET,
            flag=pb.FilterFlags.FLAGS_NONE,
            terms_list=[filter_term]
        )
        
        response = mystub.FilterAdd(filter_add_request)
    
        if response.sub_code != pb.FilterAddResponse.EOK:
            logger.error("Failed to create JET filter - server said:")
            logger.error(str(response))
            exit()

        logger.info("JET filter successfully created")

        ##################################################################################
        # Bind an implicit filter to interface
        ##################################################################################
        logger.info(f"Bind the implicit JET filter to interface {interface}")

        # create filter name 
        filter_name = pb.Filter(name="ON_DEMAND_5_TUPLE", family=pb.FilterFamilies.FAMILY_INET)
        
        # create bind point
        bind_point = pb.FilterBindObjPoint(interface_name=interface)
        
        # create the bind request
        filter_bind = pb.FilterObjBindAddRequest(
            filter=filter_name,
            obj_type=pb.FilterBindObjType.BIND_OBJ_TYPE_INTERFACE,
            bind_object=bind_point,
            bind_direction=pb.FilterBindDirection.BIND_DIRECTION_INPUT,
            bind_family=pb.FilterFamilies.FAMILY_INET
        )

        response = mystub.FilterBindAdd(filter_bind)

        if response.sub_code != pb.FilterAddResponse.EOK:
            logger.error("Failed to bind JET filter - server said:")
            logger.error(str(response))
            exit()

        logger.info("JET filter successfully bound")
        time.sleep(2)
            

        ##################################################################################
        # ADD dynamic entries 
        ##################################################################################

        # now iterate on each action 
        for action in file_lines:
            line = action.split(";")
            action = line[0].lower()
            fields = line[1].split(":")

            if len(fields) != 5:
                logger.error("This entry {line[1]} has not 5-tuple")
                continue
            
            # create a unique term name 
            term_name = create_fixed_length_hash(line[1])

            if action == "a":
                logger.info(f"Try to add a term for entry: {fields}")
            else:
                logger.info(f"Try to remove a term for entry: {fields}")
            
            # create the new term based of field
            # Create IpAddress using string format
            dst_ip_address = pb2.IpAddress(addr_string=fields[0])
            src_ip_address = pb2.IpAddress(addr_string=fields[1])

            # Create MatchIpAddress for both source and destination
            dst_addr = pb.MatchIpAddress(addr=dst_ip_address, prefix_length=32, operation=pb.MatchOperation.OP_EQUAL)
            src_addr = pb.MatchIpAddress(addr=src_ip_address, prefix_length=32, operation=pb.MatchOperation.OP_EQUAL)

            # Create MatchPort for both source and destination ports
            dst_port = pb.MatchPort(min=int(fields[4]), max=int(fields[4]), operation=pb.MatchOperation.OP_EQUAL)
            src_port = pb.MatchPort(min=int(fields[3]), max=int(fields[3]), operation=pb.MatchOperation.OP_EQUAL)

            # Create MatchProtocol
            protocol = pb.MatchProtocol(min=int(fields[2]), max=int(fields[2]), operation=pb.MatchOperation.OP_EQUAL)  

            # Create MatchFiveTupleExact
            five_tuple_exact = pb.MatchFiveTupleExact(
                dst_addr=dst_addr,
                src_addr=src_addr,
                dst_port=dst_port,
                src_port=src_port,
                protocol=protocol
            )

            # Create FilterTermMatchInet
            match_inet = pb.FilterTermMatchInet(five_tuple_exact=[five_tuple_exact])

            # Create FilterAdjacency
            adjacency = pb.FilterAdjacency(type=pb.FilterAdjacencyType.TERM_AFTER, term_name="END")

            # Create FilterTermInetNonTerminatingAction
            non_terminating_action = pb.FilterTermInetNonTerminatingAction(count=pb.ActionCounter(counter_name="cpt-term_name"))

            # Create FilterTermInetTerminatingAction
            terminating_action = pb.FilterTermInetTerminatingAction(discard=True)

            # Create FilterTermInetAction
            inet_action = pb.FilterTermInetAction(action_t=terminating_action, actions_nt=non_terminating_action)

            # Create FilterInetTerm
            if action == "a":
                inet_term = pb.FilterInetTerm(
                    term_name=term_name,
                    term_op=pb.FilterTermOperation.TERM_OPERATION_ADD,
                    adjacency=adjacency,
                    matches=match_inet,
                    actions=inet_action
                )
            else:
                inet_term = pb.FilterInetTerm(
                    term_name=term_name,
                    term_op=pb.FilterTermOperation.TERM_OPERATION_DELETE
                )

            # Create FilterTerm
            filter_term = pb.FilterTerm(inet_term=inet_term)

            # Create FilterModifyRequest
            filter_modify_request = pb.FilterModifyRequest(
                name="ON_DEMAND_5_TUPLE",
                type=pb.FilterTypes.TYPE_CLASSIC,
                family=pb.FilterFamilies.FAMILY_INET,
                flag=pb.FilterFlags.FLAGS_NONE,
                terms_list=[filter_term]
            )

            response = mystub.FilterModify(filter_modify_request)
            if response.sub_code != pb.FilterAddResponse.EOK:
                logger.error("Failed to modify the JET filter - server said:")
                logger.error(str(response))
                continue

            if action == "a":
                logger.info("Term successfully added")
            else:
                logger.info("Term successfully deleted")

            time.sleep(1)

        logger.info("All done, time to sleep... Type Ctrl^C for quitting - JET filter will be automatically removed.")    
        while True:
            time.sleep(1)
               
except KeyboardInterrupt:
    logger.info("Bye, close grpc session")
    channel.close()
    exit(0)