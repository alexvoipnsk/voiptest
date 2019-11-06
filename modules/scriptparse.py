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
        self.preconf = []
        self.type = None
        self.postconf = []
        self.test = []
        self.bug = 0

class Script_Parser:

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
#        args.add_argument("-s", "--script", action="store", type=self.File_Existence_Check, required=True, dest="config", help="set script config")
#        return args

    def Load_Script_File(self, config_path):
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
                    'preconf': {'type': 'array', 'items': {'type': 'integer', 'minimum': 0, 'maximum': 15}},
                    'type': {'type': 'string', 'minLength': 1, 'maxLength': 255},
                    'test': {'type': 'array', 'items': {'type': 'object', 'properties': {'id': {'type': 'integer', 'minimum': 0, 'maximum': 99}, 'name': {'type': 'string', 'minLength': 1, 'maxLength': 255}, 'dut_proto': {'type': 'array', 'items': {'type': 'string', 'minLength': 1, 'maxLength': 63}}, 'script': {'type': 'string', 'minLength': 1, 'maxLength': 255}, 'delay': {'type': 'integer', 'minimum': 0, 'maximum': 99}, 'bug': {'type': 'integer', 'minimum': 0, 'maximum': 1}}}},
                    'postconf': {'type': 'array', 'items': {'type': 'integer', 'minimum': 0, 'maximum': 15}}
                },
                "required" : ["type", "test"]
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
        arguments.preconf = config["preconf"]
        arguments.type = config["type"]
        if arguments.type not in ["sequential", "parallel"]:
            print ("Invalid test suite type")
        # Parse test suite
        for arg in config["test"]:
            if len(arg) == 6:
                arguments.test.append((arg["id"], arg["name"], arg["dut_proto"], arg["script"], arg["delay"], arg["bug"]))
            else:
                arguments.test.append((arg["id"], arg["name"], arg["dut_proto"], arg["script"], arg["delay"], 0))
        return arguments

    def Parse_Script(self, path):
#        args = self.Define_Args()
#        arguments = args.parse_args()
        scrypt = self.Load_Script_File(path)
        self.Validate_Config(scrypt)
        arguments = self.Arguments_Forming(scrypt)
        return arguments

