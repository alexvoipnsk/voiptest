from jsonschema import Draft4Validator
import jsonschema
import argparse
import random
import json
import math
import sys
import os
import struct
import binascii
import modules.confparse as confparse
import modules.scriptparse as scriptparse

class Script_Former:

    def Body_Former(self, file_path, args):
        code = 0
        strcount = 0
        recvbuf = 15000
        m2ua_ppid = "0x02000000"
        while (True):
            strcount += 1
            try:
                line = input()
                if line == "<scenario>" and strcount == 1:
                    pass
                else:
                    print ("Bad script syntax: <scenario>")
                    code = 100
                    break
                if line.startswith("<sock_open"):
                    if line.endswith("/>"):
                        sockparams = line.split(" ")
                        if sockparams[3] == "sctp":
                            print ("#Create SCTP socket")
                            print ("recv_buf = {0}".format(recvbuf))
                            print ("sk{0} = sctp.sctpsocket_tcp(socket.AF_INET)".format(sockparams[1]))
                        elif sockparams[3] == "tcp":
                            pass
                        else:
                            pass
                        print ("sk{0}.bind((address{1},port{2}))".format(sockparams[1]))
                        print ("sk{0}.connect((address{1},port{2}))".format(sockparams[1]))
                    else:
                        print ("Bad script syntax: <sock_open x y transport proto />")
                        code = 100
                        break
                if line.startswith("<sock_close"):
                    if line.endswith("/>"):
                        sockparams = line.split(" ")
                        print ("#Close SCTP socket")
                        print ("sk{0}.close()".format(sockparams[1]))
                    else:
                        print ("Bad script syntax: <sock_close x />")
                        code = 100
                        break
                if line.startswith("<send"):
                    if line.endswith("/>"):
                        params = line.split(" ")
                        print ("message = builder.Build_{0}_Message()".format(params[2]))
                        if sockparams[4] == "m2ua":
                            print ("sk{0}.sctp_send(message,ppid={1})".format(params[1], m2ua_ppid))
                if line == "</scenario>":
                    code = 0
                    break
            except EOFError:
                code = 100
                break
        return code        

    def Form_M2UA_Header(self):
        print ("#!/usr/bin/env python3\a\a")
        print ("import logging")
        print ("import socket")
        print ("import sctp")
        print ("import sys")
        print ("import modules.m2ua as m2ua\a\a")

    def Form_Config_Param(self, config):
#        ConfParser = confparse.Config_Parser()
#        config = ConfParser.Parse_Config(gconfpath)
        print ("#Config parameters values")
        i = 0
        while i < len(config.sock_id):
            print ("address{0} = {1}".format(config.sock_id[i], config.sock_ipaddr[i]))
            print ("port{0} = {1}".format(config.sock_id[i], config.sock_port[i]))
            i += 1
        i = 0
        while i < len(config.sigtran_par_id):
            print ("{1}{0} = {2}".format(config.sigtran_par_id[i], config.sigtran_par_type[i], config.sigtran_par_value[i]))
            i += 1        
        print ("\a#Message builder and parser")
        print ("builder = m2ua.Message_Builder()")
        print ("parser = m2ua.Message_Parser()\a")


    def File_Former(self, script, config):
        self.Form_M2UA_Header()
        self.Form_Config_Param(config)
        sys.exit(0)
        Body_Former()



        return path, code

