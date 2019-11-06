#!/usr/bin/env python3

import os, sys, signal, argparse, subprocess, time, logging 
from datetime import date

#modulepath = cwd + "/modules/"
#sys.path.append(modulepath)
#print (sys.path[-1])

import modules.m2ua.m2ua as m2ua
import modules.m2ua.m2uacheck as m2uacheck
import modules.confparse as confparse
import modules.scriptparse as scriptparse

from html.parser import HTMLParser
from xml.sax.handler import DTDHandler

from lxml import etree


def File_Existence_Check(file_path):
    if type(file_path) != str:
        raise argparse.ArgumentTypeError("argument must be string")
    else:
        if not os.path.exists(file_path):
            raise argparse.ArgumentTypeError("file \"%s\" does not exist" % file_path)
        else:
            return file_path

def Define_Args():
    args = argparse.ArgumentParser(description="List of possible command line arguments")
    args.add_argument("-s", "--script", action="store", type=File_Existence_Check, required=True, dest="script", help="set script")
    args.add_argument("-c", "--config", action="store", type=File_Existence_Check, required=False, dest="config", help="set global config file")
    args.add_argument("-l", "--logging", action="store_true", required=False, dest="logging", help="set logging usage")
    args.add_argument("-v", "--verbose", action="count", required=False, dest="verbose", help="set verbose level, use -v (CRITICAL), -vv (ERROR), -vvv (WARNING), -vvvv (INFO), -vvvvv (DEBUG)")
    args.add_argument("-j", "--job", action="store", required=False, dest="job", help="set job name")
    return args

class Script_Former:

    def Body_Former(self, scrypt, config, path, test_file):
        code = 0
        strcount = 0
        scenopenflag = False
        recvbuf = 15000
        m2ua_ppid = "0x02000000"
        # XML parse and validate
        xmlparser = etree.XMLParser(strip_cdata=False)
        tree = etree.parse(path, xmlparser)
        docinfo = tree.docinfo
        dtdfilename = docinfo.doctype.split('"', 2)
        dtdfilepath = cwd + "/tests/xml/" + dtdfilename[1] 
        dtd = etree.DTD(dtdfilepath)        
        if dtd.validate(tree):    # If valid XML file
        	root = tree.getroot()
        	testname = root.attrib # Scriptname
        	for line in root:
        		if line.tag == "sock_open":
        			proto = line.attrib["proto"]
        			if line.attrib["transport"] == "sctp":
        				test_file.write ("\n#Create SCTP socket\n")
        				test_file.write ("recv_buf = {0}\n".format(recvbuf))
        				test_file.write ("sk{0} = sctp.sctpsocket_tcp(socket.AF_INET)\n".format(line.attrib["local"]))
        				try: 
        					xxx = line.attrib["timeout"]
        					test_file.write ("sk{0}.settimeout({1})\n".format(line.attrib["local"], int(line.attrib["timeout"])))
        				except KeyError:
        					test_file.write ("sk{0}.settimeout({1})\n".format(line.attrib["local"], 30))
        			elif line.attrib["transport"] == "tcp":
        				pass
        			else:
        				pass
        			test_file.write ("sk{0}.bind((address{0}, port{0}))\n".format(line.attrib["local"]))
        			test_file.write ("sk{0}.connect((address{1}, port{1}))\n".format(line.attrib["local"], line.attrib["remote"]))
        		if line.tag == "sock_close":
        			test_file.write ("\n#Close SCTP socket\n")
        			test_file.write ("sk{0}.close()\n".format(line.attrib["local"]))
        		if line.tag == "send":
        			sendinfo = executor.Values_Exec(line.text.strip(), 'send')
        			if sendinfo[2]:
	        			test_file.write ("\nmessage = builder.Build_{0}_Message({1})\n".format(sendinfo[1], sendinfo[3]))
	        		else:
	        			test_file.write ("\nmessage = builder.Build_{0}_Message()\n".format(sendinfo[1]))
        			if proto == "m2ua":
        				test_file.write ("sk{0}.sctp_send(message,ppid={1})\n".format(line.attrib["socket"], m2ua_ppid))
        		if line.tag == "recv":
        			recvinfo = executor.Values_Exec(line.text.strip(), "recv")
        			if recvinfo[1] == "NO MESSAGE":
        				test_file.write ("\ntry:\n")
        				test_file.write ("        message = sk{0}.recv({1})\n".format(line.attrib["socket"], recvbuf))
        				test_file.write ("        print ('NOK')\n")
        				test_file.write ("except socket.timeout:\n")
        				test_file.write ("        print('No message OK')\n")
        			else:
        				test_file.write ("\nmessage = sk{0}.recv({1})\n".format(line.attrib["socket"], recvbuf))
        				test_file.write ("obj_message = parser.Parse_Message(message)\n")
        				if recvinfo[2]:
        					test_file.write ("validation_result = validator.Validate_Message_W_Params(obj_message, '{0}', '{1}', {2})\n".format(line.attrib["class"], recvinfo[1], recvinfo[3]))
        				else:
        					test_file.write ("validation_result = validator.Validate_Message(obj_message, '{0}', '{1}')\n".format(line.attrib["class"], recvinfo[1]))

    def Form_M2UA_Header(self, test_file):
        test_file.write ("#!/usr/bin/env python3\n\n")
        test_file.write ("import logging\n")
        test_file.write ("import socket\n")
        test_file.write ("import sctp\n")
        test_file.write ("import sys\n")
        test_file.write ("import modules.m2ua.m2ua as m2ua\n\n")

    def Form_Config_Param(self, config, test_file):
        test_file.write ("#Config parameters values\n")
        i = 0
        while i < len(config.sock_id):
            test_file.write ("address{0} = '{1}'\n".format(config.sock_id[i], config.sock_ipaddr[i]))
            test_file.write ("port{0} = {1}\n".format(config.sock_id[i], config.sock_port[i]))
            i += 1
        i = 0
        while i < len(config.sigtran_par_id):
            test_file.write ("{1}{0} = {2}\n".format(config.sigtran_par_id[i], config.sigtran_par_type[i], config.sigtran_par_value[i]))
            i += 1        
        test_file.write ("\n#Message builder and parser\n")
        test_file.write ("builder = m2ua.Message_Builder()\n")
        test_file.write ("parser = m2ua.Message_Parser()\n")
        test_file.write ("validator = m2ua.Parameters_Validator()\n")

    def File_Former(self, script, config):
        self.Form_M2UA_Header()
        self.Form_Config_Param(config)
        self.Body_Former() 
        return path, code

# Command string arguments
argums = Define_Args()

# Определяем и сохраняем текущий путь к файлу - это корень
try:
    cwd = os.path.dirname(os.path.realpath(__file__))
    os.chdir(cwd)
except:
    pass

# Logging and verbose level
log=argums.parse_args().logging
verb=argums.parse_args().verbose
log_name_form=os.path.dirname(argums.parse_args().script).split("/")
if argums.parse_args().job:
    logfpath=cwd + "/log/" + str(date.today()) + "/" + argums.parse_args().job
    logfname=logfpath + "/" + str(log_name_form[-2]) + "_" + str(log_name_form[-1]) + ".log"
else:
    logfpath=cwd + "/log/" + str(date.today()) 
    logfname=logfpath + "/" + str(log_name_form[-2]) + "_" + str(log_name_form[-1]) + ".log"
os.makedirs(logfpath ,mode=0o777,exist_ok=True)
#log_file = open(logfname, "w").close()
logger = logging.getLogger("PyTest")
logging.basicConfig(format = u'%(asctime)-8s %(levelname)-8s [%(module)s -> %(funcName)s:%(lineno)d] %(message)-8s', filename=logfname, filemode='w')  
if log:
    logger.addHandler()



    if verb >=5:
        logger.setLevel(10)   
    elif verb==4:
        logger.setLevel(20)  
    elif verb==3:
        logger.setLevel(30)  
    elif verb==2:
        logger.setLevel(40) 
    else:
        logger.setLevel(50)       
else:
    logger.setLevel(100)    

# Config path
if argums.parse_args().config:
	gconfpath = argums.parse_args().config
else:
	gconfpath = os.path.normpath(os.path.dirname(argums.parse_args().script) + "/../config.json")
logger.debug("Configuration path: %s", gconfpath)
	
# Parse test script
ScrParser = scriptparse.Script_Parser()
testconf = ScrParser.Parse_Script(argums.parse_args().script)
logger.debug("Test script directory: %s", os.path.dirname(argums.parse_args().script))

# Parse config
ConfParser = confparse.Config_Parser()
config = ConfParser.Parse_Config(gconfpath)

# Execute test script parameters
executor = m2ua.Config_Executor()

# Do preconf
pass

# test execute
if testconf.type == "sequential":
    logger.info("Test execute: Sequential test type")
    for test in testconf.test:
        if test[5]:
            logger.warning("Test execute: Test ({0}:{1}) will not be executed, because bug in DUT software exist".format(test[0], test[1]))
        else:
            for value in test[2]: # mdfy for more than one value
                if value == "m2ua":
                    logger.info("Test execute: M2UA protocol test")
                    test_file = open("run.py", "w")     # make try construction
                    ScrRunner = Script_Former()
                    ScrRunner.Form_M2UA_Header(test_file)
                    ScrRunner.Form_Config_Param(config, test_file)
                    scrName = os.path.dirname(argums.parse_args().script) + "/" + test[3]
                    ScrRunner.Body_Former(test, config, scrName, test_file)
                    test_file.close()     # make try construction
                    os.chmod("run.py", 0o777)

                    if test_file:
                        logger.info("Test execute: Test ({0}:{1}) starts".format(test[0], test[1]))
                        subprocess.run("./run.py")

                else:
                    pass
                time.sleep(test[4])
else:
    logger.info("Test execute: Parallel test type")
    pass



# Do postconf
pass

code = 127
sys.exit(code)
