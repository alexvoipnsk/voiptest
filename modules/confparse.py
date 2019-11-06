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

class Argument:

    def __init__(self):
        # main conf
        self.dut_proto = []

        # socket conf
        self.sock_id = []
        self.sock_ipaddr = []
        self.sock_port = []

        # user conf
        self.user_id = []
        self.user_username = []
        self.user_authname = []
        self.user_password = []
        self.user_domain = []

        # device conf
        self.device_id = []
        self.device_type = []
        self.device_sw = [] 
        self.device_management_proto = []
        self.device_ipaddr = []
        self.device_port = []
        self.device_login = []
        self.device_password = []

        # sigtran conf
        self.sigtran_par_id = []
        self.sigtran_par_type = []
        self.sigtran_par_value = [] 

class Config_Parser:

#    def File_Existence_Check(self, file_path):
#        if type(file_path) != str:
#            raise argparse.ArgumentTypeError("argument must be string")
#        else:
#            if not os.path.exists(file_path):
#                raise argparse.ArgumentTypeError("file \"%s\" does not exist" % file_path)
#            else:
#                return file_path

#    def Define_Args(self):
#        args = argparse.ArgumentParser(description="List of possible command line arguments")
#        args.add_argument("-c", "--config", action="store", type=self.File_Existence_Check, required=True, dest="config", help="set script config")
#        return args

    def Load_Config_File(self, config_path):
        file = open(config_path, "r", encoding="utf-8")
        try:
            config = json.loads(file.read())
        except json.decoder.JSONDecodeError:
            file.close()
            print("Validation error: wrong JSON format: %s" % sys.exc_info()[1])
            sys.exit(107)
        else:
            file.close()
        return config

    def Define_Config_Schema(self):
        schema = {
            '$schema': 'http://json-schema.org/draft-04/schema#', 
            'title': 'Config schema',
            'type': 'object',
            'properties':
                {
                    'sock': {'type': 'array', 'items': {'type': 'object', 'properties': {'id': {'type': 'integer', 'minimum': 0, 'maximum': 99}, 'ipaddr': {'type': 'string', 'minLength': 7, 'maxLength': 15}, 'port': {'type': 'integer', 'minimum': 1024, 'maximum': 65535}}}},
                    'user': {'type': 'array', 'items': {'type': 'object', 'properties': {'id': {'type': 'integer', 'minimum': 0, 'maximum': 99}, 'username': {'type': 'string', 'minLength': 1, 'maxLength': 255}, 'authname': {'type': 'string', 'minLength': 1, 'maxLength': 255}, 'password': {'type': 'string', 'minLength': 1, 'maxLength': 63}, 'domain': {'type': 'string', 'minLength': 1, 'maxLength': 255}}}},
                    'device': {'type': 'array', 'items': {'type': 'object', 'properties': {'id': {'type': 'integer', 'minimum': 0, 'maximum': 99}, 'type': {'type': 'string', 'minLength': 1, 'maxLength': 15}, 'sw': {'type': 'string', 'minLength': 1, 'maxLength': 15}, 'proto': {'type': 'string', 'minLength': 1, 'maxLength': 15}, 'ipaddr': {'type': 'string', 'minLength': 7, 'maxLength': 15}, 'port': {'type': 'integer', 'minimum': 1, 'maximum': 65535}, 'login': {'type': 'string', 'minLength': 1, 'maxLength': 255}, 'password': {'type': 'string', 'minLength': 1, 'maxLength': 63}}}},
                    'sigtran': {'type': 'array', 'items': {'type': 'object', 'properties': {'id': {'type': 'integer', 'minimum': 0, 'maximum': 99}, 'type': {'type': 'string', 'minLength': 1, 'maxLength': 63}, 'value': {'type': 'string', 'minLength': 1, 'maxLength': 63}}}}
                },
                "required" : ['sock']
            }
        return schema

    def Errors_Output(self, errors):
        for e in errors:
            if len(e.path) == 0:
                print("Validation error: %s" % e.message)
                sys.exit(107)
            else:
                print("Validation error: %s (property \"%s\")" % (e.message, e.path.pop()))
                sys.exit(107)

    def Validate_Config(self, config):
        schema = self.Define_Config_Schema()
        errors = sorted(Draft4Validator(schema).iter_errors(config), key=lambda e: e.path)
        if errors:
            self.Errors_Output(errors)

    def Arguments_Forming(self, config):
        arguments = Argument()
        # Parse sock config
        i = 0
        for _ in config["sock"]:
            arguments.sock_id.append(config["sock"][i]["id"])
            arguments.sock_ipaddr.append(config["sock"][i]["ipaddr"])
            arguments.sock_port.append(config["sock"][i]["port"])
            i += 1
        # Parse user config
        try:
            i = 0
            for _ in config["user"]:
                arguments.user_id.append(config["user"][i]["id"])
                arguments.user_username.append(config["user"][i]["username"])
                try:
                    arguments.user_authname.append(config["user"][i]["authname"])
                except KeyError:
                    arguments.user_authname.append("Null")
                try:
                    arguments.user_password.append(config["user"][i]["password"])
                except KeyError:
                    arguments.user_password.append("Null")
                try:  
                    arguments.user_domain.append(config["user"][i]["domain"])  
                except KeyError:
                    arguments.user_domain.append("Null")  
                i += 1
        except KeyError:
            print ("No block __user__ in configuration")
        # Parse device config
        try:    
            i = 0
            for _ in config["device"]:
                arguments.device_id.append(config["device"][i]["id"])
                arguments.device_type.append(config["device"][i]["type"])
                arguments.device_sw.append(config["device"][i]["sw"])
                arguments.device_management_proto.append(config["device"][i]["proto"])
                arguments.device_ipaddr.append(config["device"][i]["ipaddr"])  
                arguments.device_port.append(config["device"][i]["port"])
                arguments.device_login.append(config["device"][i]["login"])  
                arguments.device_password.append(config["device"][i]["password"])
                i += 1
        except KeyError:
            print ("No block __device__ in configuration")
        # Parse sigtran config
        try:
            i = 0
            for _ in config["sigtran"]:
                arguments.sigtran_par_id.append(config["sigtran"][i]["id"])
                arguments.sigtran_par_type.append(config["sigtran"][i]["type"])
                arguments.sigtran_par_value.append(config["sigtran"][i]["value"])
                i += 1
        except KeyError:
            print ("No block __sigtran__ in configuration")

        return arguments

    def Parse_Config(self, ConfPath):
#        args = self.Define_Args()
#        arguments = args.parse_args()
#        config = self.Load_Config_File(arguments.config)
        config = self.Load_Config_File(ConfPath)
        self.Validate_Config(config)
        arguments = self.Arguments_Forming(config)
        return arguments

