import argparse
from ncclient import manager
from ncclient.transport.errors import AuthenticationError
from socket import gaierror
import logging
import sys
from ncclient.xml_ import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Simple Netconf ephemeral DB - Fast Tuple client")
    parser.add_argument('-r', '--router', nargs=1, help='target router name', required=True)
    parser.add_argument('-u', '--user', nargs=1, help='Username', required=True)
    parser.add_argument('-p', '--pwd', nargs=1, help='Password', required=True)
    parser.add_argument('-j', '--jobs', nargs=1, help='Name of the file that contains jobs', required=True)
    parser.add_argument('-e', '--ephemeral', nargs=1, help='Name of the Ephemeral DB', required=True)
    parser.add_argument('-l', '--list', nargs=1, help='Name of the Fast Five Tuples List', required=True)
    options = parser.parse_args()

    warn_to_ignore = ["statement not found","statement has no contents", "No objects matched", "is protected"]

    # configure logger
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    sh.setFormatter(formatter)
    logger.addHandler(sh) 

    # Retrieve arguments 
    router = options.router[0]
    user = options.user[0]
    password = options.pwd[0]
    filename = options.jobs[0]
    epheInst = options.ephemeral[0]
    prfxList = options.list[0]

    # Open filename includiing the jobs to commit 
    try:
        with open(filename, 'r') as file:
            file_lines = file.readlines()
            
        file_lines = [line.strip() for line in file_lines]

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
    
    # Create the job RPC
    rpc = ""
    for entry in file_lines:
        line = entry.split(";")
        if line[0].lower() == "a":
            # This is "set"
            rpc+= f"set policy-options fast-lookup-tuple-list {prfxList} {line[1]}\n"
        else:
            # This is "delete"
            rpc+= f"delete policy-options fast-lookup-tuple-list {prfxList} {line[1]}\n"
    
    if len(rpc) == 0:
        logger.error("File is empty - nothing to do - exit")
        exit()
    
    rpc = rpc[:-1]
    
    logger.info("Job list has been successfully prepared")    

    # Open The Netconf session
    try:
        conn = manager.connect(host=router,
                                port=830,
                                username=user,
                                password=password,
                                timeout=60,
                                device_params={'name': 'default'},
                                hostkey_verify=False)
    except AuthenticationError:
        logger.error("Unable to open Netconf session - authentication failed")
        exit()
    except gaierror: 
        logger.error("Unable to open Netconf session - connexion failed")
        exit()
    except Exception as e:
        logger.error("Unable to open Netconf session - {e}")
        exit()
    
    logger.info("Netconf session has been successfully opened")    

    # open the ephemeral DB 
    try:
        openRpc = f"<open-configuration><ephemeral-instance>{epheInst}</ephemeral-instance></open-configuration>"
        returnValue = conn.rpc(to_ele(openRpc))
    except Exception as e:
        logger.error("Unable to open the configuration database - {e}")
        exit()

    # load the config 
    try:
        loadRpc = f'<load-configuration action="set" format="text"><configuration-set>{rpc}</configuration-set></load-configuration>'
        returnValue = conn.rpc(to_ele(loadRpc))
    except Exception as e:
        logger.error("Unable to load the configuration - {e}")
        exit()
    
    logger.info("Configuration has been successfully loaded")    

    # commit the config
    try:
        conn.commit()
    except Exception as e:
        logger.error("Unable to commit the configuration - {e}")
        exit()

    logger.info("Configuration has been successfully committed")    

    # close the session
    try:
        conn.close_session()
    except Exception as e:
        logger.error("Unable to close the Netconf session - {e}")
        exit()
    
    logger.info("All jobs done, bye...")  