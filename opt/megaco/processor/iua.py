#from jsonschema import Draft4Validator
#import jsonschema
#import argparse
import random
#import json
import math
import sys
#import os
import struct
import binascii
import time

class IUA_Message:

	def __init__(self, message_class, message_type, version=1, spare=0):
		self.version = version
		self.spare = spare
		self.mes_class = message_class
		self.mes_type = message_type
		self.length = None
		self.parameters = []

	def Define_Message_Classes(self):
		classes = {
		  0 : "Management message (MGMT)",
		  1 : "Transfer messages (TRANSF)",
		  2 : "SS7 signalling network management messages (SSNM)",
		  3 : "ASP state maintenance messages (ASPSM)",
		  4 : "ASP traffic maintenance messages (ASPTM)",
		  5 : "Q.921/Q.931 boundary primitives transport (QPTM)",
		  6 : "MTP2 User Adaptation messages (MAUP)",
		  7 : "Connectionless messages (CLM)",
		  8 : "Connection-oriented messages (COM)",
		  9 : "Routing key management messages (RKM)",
		  10 : "Interface Identifier management messages (IIM)"
		}
		return classes

	def Define_QPTM_Message_Types(self):
		types = {
		  0: "Reserved",
		  1: "Data Request Message (DATA REQ)",
		  2: "Data Indication Message (DATA IND)",
		  3: "Unit Data Request Message (UNIT DATA REQ)",
		  4: "Unit Data Indication Message (UNIT DATA IND)",
		  5: "Establish Request (ESTAB REQ)",
		  6: "Establish Confirm (ESTAB CONF",
		  7: "Establish Indication (ESTAB IND)",
		  8: "Release Request (RELEASE REQ)",
		  9: "Release Confirm (RELEASE CONF)",
		  10: "Release Indication (RELEASE IND)"
		}
		return types

	def Define_ASPSM_Message_Types(self):
		types = {
		  1 : "ASP Up (ASP UP)",
		  2 : "ASP Down (ASP DOWN)",
		  3 : "Heartbeat (BEAT)",
		  4 : "ASP Up Ack (ASP UP ACK)",
		  5 : "ASP Down Ack (ASP DOWN ACK)",
		  6 : "Heartbeat Ack (BEAT ACK)"
		}
		return types

	def Define_ASPTM_Message_Types(self):
		types = {
		  1 : "ASP Active (ASP ACTIVE)",
		  2 : "ASP Inactive (ASP INACTIVE)",
		  3 : "ASP Active Ack (ASP ACTIVE ACK)",
		  4 : "ASP Inactive Ack (ASP INACTIVE ACK)"
		}
		return types

	def Define_MGMT_Message_Types(self):
		types = {
		  0 : "Error (ERROR)",
		  1 : "Notify (NOTIFY)",
		  2 : "TEI Status Request (TEI STATUS REQ)",
		  3 : "TEI Status Confirm (TEI STATUS CONF)",
		  4 : "TEI Status Indication (TEI STATUS IND)"
		}
		return types

class IUA_Parameter:

	def __init__(self, tag):
		self.tag = tag
		self.length = 8
		self.value = None

	def Define_Parameter_Tags(self):
		tags = {
		  1 : "Interface Identifier Integer",
		  3 : "Interface Identifier Text", 
		  4 : "Info String",
		  5 : "DLCI",  # SAPI, TEI
		  7 : "Diagnostic Information",
		  8 : "Interface Identifier Integer Range",
		  9 : "Heartbeat Data",
		  11 : "Traffic Mode Type",
		  12 : "Error Code",
		  13 : "Status Type/Identification",
		  14 : "Protocol data",
		  15 : "Reason",
		  16 : "Status",
		  17 : "ASP Identifier"
		}
		return tags

	def Define_Reason_Parameter_Values(self):
		values = {
		  0 : "RELEASE_MGMT",
		  1 : "RELEASE_PHYS",     
		  2 : "RELEASE_DM", 
		  3 : "RELEASE_OTHER"   
		}
		return values

	def Define_Status_Parameter_Values(self):
		values = {
		  0 : "ASSIGNED",
		  1 : "UNASSIGNED"
		}
		return values

	def Define_Traffic_Mode_Type_Values(self):
		values = {
		  1 : "Override",
		  2 : "Load-share"
		}
		return values

	def Define_Error_Code_Values(self):
		values = {
		  1 : "Invalid Version",
		  2 : "Invalid Interface Identifier",
		  3 : "Unsupported Message Class",
		  4 : "Unsupported Message Type",
		  5 : "Unsupported Traffic Handling Mode",
		  6 : "Unexpected Message",
		  7 : "Protocol Error",
		  8 : "Unsupported Interface Identifier Type",
		  9 : "Invalid Stream Identifier",
		  10 : "Unassigned TEI",
		  11 : "Unrecognized SAPI",
		  12 : "Invalid TEI, SAPI combination",
		  13 : "Refused - Management Blocking",
		  14 : "ASP Identifier Required",
		  15 : "Invalid ASP Identifier"
		}
		return values

	def Define_Status_Type_Values(self):
		types = {
		  1 : "AS State Change",
		  2 : "Other"
		}
		return types

	def Define_AS_State_Change_Status_Information_Values(self):
		values = {
		  2 : "AS_Inactive",
		  3 : "AS_Active",
		  4 : "AS_Pending"
		}
		return values

	def Define_Other_Status_Information_Values(self):
		values = {
		  1 : "Insufficient ASP resources active in AS",
		  2 : "Alternate ASP Active",
		  3 : "ASP Failure"
		}
		return values

class Binary_Convertor:

	def __init__(self):
		self.common_iua_header_pattern = struct.Struct(">B B B B L")
		self.iua_parameter_header_pattern = struct.Struct(">H H")
		self.iua_padding_parameter_pattern = struct.Struct(">B")
		self.iua_parameter_header_length = 4
		self.iua_header_length = 8

	def Convert_Int_To_Bytes(self, int_value, bytes_number):
		bytes_string = int_value.to_bytes(bytes_number, byteorder="big")
		return bytes_string

	def Convert_Bytes_To_Int(self, bytes_string):
		int_value = int.from_bytes(bytes_string, byteorder="big")
		return int_value

	def Bytes_Number_Counting(self, int_value):
		hex_value = hex(int_value)[2:]
		bytes_number = math.ceil(len(hex_value) / 2)
		return bytes_number 

	def Create_IUA_Parameter_Padding(self, padding_bytes_number):
		padding_value = (0)
		padding_byte = self.iua_padding_parameter_pattern.pack(padding_value)
		padding = padding_byte * padding_bytes_number
		return padding

	def Searching_For_Multiple_Length(self, parameter_length):
		initial_parameter_length = parameter_length
		for i in range(1,4):
			parameter_length = initial_parameter_length + i
			if parameter_length % 4 == 0:
				multiple_length = parameter_length
				break
		else:
			raise IUA_Error("padding bytes counting error")
		return multiple_length

	def Forming_IUA_Parameter_Padding(self, parameter_length):
		if parameter_length % 4 == 0:
			return b""
		else:
			multiple_length = self.Searching_For_Multiple_Length(parameter_length)
			padding_bytes_number = multiple_length - parameter_length
			padding = self.Create_IUA_Parameter_Padding(padding_bytes_number)
			return padding

	def String_Parameter_Length_Check(self, string_parameter_value, parameter_length):
		if len(string_parameter_value) != parameter_length - self.iua_parameter_header_length:
			raise IUA_Error("iua str parameter length \"%s\" is bigger than allowable length" % len(string_parameter_value))

	def Convert_String_Parameter_Value(self, parameter_value, parameter_length=None):
		binary_parameter_value = parameter_value.encode("utf-8")
		if parameter_length:
			binary_parameter_length = parameter_length
			self.String_Parameter_Length_Check(binary_parameter_value, parameter_length)
		else:
			binary_parameter_length = len(binary_parameter_value) + self.iua_parameter_header_length
		return (binary_parameter_value, binary_parameter_length)

	def Convert_Int_Parameter_Value(self, parameter_value, parameter_length=None):
		if parameter_length:
			binary_parameter_length = parameter_length
			try:
				binary_parameter_value = parameter_value.to_bytes(parameter_length - self.iua_parameter_header_length, byteorder="big")
			except OverflowError:
				raise IUA_Error("iua int parameter value is \"%s\" is bigger than allowable value"% parameter_value)
		else:
			value_length = self.Bytes_Number_Counting(parameter_value)
			binary_parameter_value = parameter_value.to_bytes(value_length, byteorder="big")
			binary_parameter_length = value_length + self.iua_parameter_header_length
		return (binary_parameter_value, binary_parameter_length)

	def Convert_List_Parameter_Value(self, parameters_list):
		total_parameter_length = self.iua_parameter_header_length
		total_binary_parameter_value = b""
		for parameter in parameters_list:
			if type(parameter) == int:
				binary_parameter_value, dummy = self.Convert_Int_Parameter_Value(parameter, parameter_length=8)
				total_binary_parameter_value = total_binary_parameter_value + binary_parameter_value
				total_parameter_length = total_parameter_length + 4
			elif type(parameter) == IUA_Parameter:
				binary_parameter, binary_parameter_length = self.Convert_IUA_Parameter(parameter)
				total_binary_parameter_value = total_binary_parameter_value + binary_parameter
				total_parameter_length = total_parameter_length + binary_parameter_length
			else:
				raise IUA_Error("unsupported element type in parameters list")
		return (total_binary_parameter_value, total_parameter_length)

	def Convert_Decimal_To_Bin(self, decimal_value, length):
		bin_value = bin(decimal_value)[2:]
		end_of_padding = False
		while not end_of_padding:
			if len(bin_value) != length:
				bin_value = "0" + bin_value
			else:
				end_of_padding = True
		return bin_value

	def IUA_Parameter_Forming(self, parameter_value, parameter_length=None):
		print ("tt", type(parameter_value))
		if type(parameter_value) == str:
			binary_parameter_value, binary_parameter_length = self.Convert_String_Parameter_Value(parameter_value, parameter_length)
		elif type(parameter_value) == int:
			binary_parameter_value, binary_parameter_length = self.Convert_Int_Parameter_Value(parameter_value, parameter_length)
		elif type(parameter_value) == list:
			binary_parameter_value, binary_parameter_length = self.Convert_List_Parameter_Value(parameter_value)
		elif type(parameter_value) == isup.MTP3_Data:
			binary_parameter_value, binary_parameter_length = self.isup_bin_conv.Convert_MTP3_Data(parameter_value)
		else:
			raise IUA_Error("unsupported type of iua parameter")
		return (binary_parameter_value, binary_parameter_length)

	def Convert_IUA_Parameter_Value(self, object_parameter):
		if not object_parameter.length:
			binary_parameter_value, parameter_length = self.IUA_Parameter_Forming(object_parameter.value)
		elif object_parameter.length < 4:
			raise IUA_Error("iua parameter length must not be less than 4")
		elif object_parameter.length == 4:
			binary_parameter_value = b""
			parameter_length = object_parameter.length
		else:
			binary_parameter_value, parameter_length = self.IUA_Parameter_Forming(object_parameter.value, object_parameter.length)
		return (binary_parameter_value, parameter_length)

	def Convert_IUA_Parameter(self, object_parameter): 
		binary_parameter_value, parameter_length = self.Convert_IUA_Parameter_Value(object_parameter)
		packet_values = (object_parameter.tag, parameter_length)
		binary_parameter_header = self.iua_parameter_header_pattern.pack(*packet_values)
		padding = self.Forming_IUA_Parameter_Padding(parameter_length)
		binary_parameter = binary_parameter_header + binary_parameter_value + padding
		return (binary_parameter, parameter_length + len(padding))

	def Get_IUA_Parameters_Info(self, object_message):
		parameters_length = 0
		binary_parameters_list = []
		for parameter in object_message.parameters:
			binary_parameter, parameter_length = self.Convert_IUA_Parameter(parameter)
			binary_parameters_list.append(binary_parameter)
			parameters_length = parameters_length + parameter_length
		return (binary_parameters_list, parameters_length)

	def Get_IUA_Parameters_String(self, parameters_list):
		parameters_string = b""
		for parameter in parameters_list:
			parameters_string = parameters_string + parameter
		return parameters_string 

	def Convert_IUA_Message(self, object_message):
		binary_parameters_list, parameters_length = self.Get_IUA_Parameters_Info(object_message)
		object_message.length = self.iua_header_length + parameters_length 
		packet_values = (object_message.version, object_message.spare, object_message.mes_class, object_message.mes_type, object_message.length)
		iua_header = self.common_iua_header_pattern.pack(*packet_values)
		iua_parameters = self.Get_IUA_Parameters_String(binary_parameters_list)
		iua_message = iua_header + iua_parameters
		return iua_message

class Message_Builder:

	def __init__(self):
#		self.isdn_bld = q931.Message_Builder()
		self.convertor = Binary_Convertor()

	def _Iua_make_message_handler(self):
		return { "ESTAB_REQ" : self.Build_Establish_Request,
				 "ESTAB_CONF" : self.Build_Establish_Confirmation,
				 "ESTAB_IND" : self.Build_Establish_Indication, #
				 "RELEASE_REQ" : self.Build_Release_Request, #---
				 "RELEASE_CONF" : self.Build_Release_Confirmation, #
				 "RELEASE_IND" : self.Build_Release_Indication,#
#				 "DATA_REQ" : self.Build_Data_Request, #---
#				 "DATA_IND" : self.Build_Data_Indication,#
#				 "UNIT_DATA_REQ" : self.Build_Unit_Data_Request, #
#				 "UNIT_DATA_IND" : self.Build_Unit_Data_Indication,#
				 "ASP_UP" : self.Build_ASP_UP_Message,
				 "ASP_UP_ACK" : self.Build_ASP_UP_ACK_Message,
				 "ASP_DOWN" : self.Build_ASP_DOWN_Message,
				 "ASP_DOWN_ACK" : self.Build_ASP_DOWN_ACK_Message,
				 "BEAT" : self.Build_BEAT_Message,
				 "BEAT_ACK" : self.Build_BEAT_ACK_Message,
				 "ASP_ACTIVE" : self.Build_ASP_ACTIVE_Message,
				 "ASP_ACTIVE_ACK" : self.Build_ASP_ACTIVE_ACK_Message,
				 "ASP_INACTIVE" : self.Build_ASP_INACTIVE_Message,
				 "ASP_INACTIVE_ACK" : self.Build_ASP_INACTIVE_ACK_Message,
				 "ERROR" : self.Build_ERR_Message,
				 "NOTIFY" : self.Build_NTFY_Message,
				 "TEI_STATUS_REQ" : self.Build_TEI_Status_Request, #---
				 "TEI_STATUS_CONF" : self.Build_TEI_Status_Confirmation, #
				 "TEI_STATUS_IND" : self.Build_TEI_Status_Indication,#
				 "TEI_QUERY_REQ" : self.Build_TEI_Query_Request#---
				  }

# Build parameters

	def Get_IUA_Parameter_Info(self, object_parameter):
		if object_parameter.tag == 11:
			parameter_info = object_parameter.Define_Traffic_Mode_Type_Values()
			return (parameter_info, "traffic mode type")
		elif object_parameter.tag == 12:
			parameter_info = object_parameter.Define_Error_Code_Values()
			return (parameter_info, "error code")
		elif object_parameter.tag == 13:
			parameter_info = object_parameter.Define_Status_Type_Values()
			return (parameter_info, "status type")
		elif object_parameter.tag == 15:
			parameter_info = object_parameter.Define_Reason_Parameter_Values()
			return (parameter_info, "reason")
		elif object_parameter.tag == 16:
			parameter_info = object_parameter.Define_Status_Parameter_Values()
			return (parameter_info, "status")
		else:
			raise IUA_Error("iua parameter tag \"%s\" does not support" % object_parameter.tag)

	def Get_Parameter_Value(self, object_parameter, parameter_definition):
		parameter_values, parameter_name = self.Get_IUA_Parameter_Info(object_parameter)
		if type(parameter_definition) == int:
			for parameter_number in parameter_values.keys():
				if parameter_definition == parameter_number:
					break
			else:
				raise IUA_Error("\"%s\" is unknown iua %s parameter value" % (parameter_definition, parameter_name))
			return parameter_definition
		elif type(parameter_definition) == str:
			for parameter_number, parameter_description in parameter_values.items():
				if parameter_definition.lower().replace(" ", "_") == parameter_description.lower().replace(" ", "_"):
					parameter_value = parameter_number
					break
			else:
				raise IUA_Error("\"%s\" is unknown iua %s parameter value" % (parameter_definition, parameter_name))
			return parameter_value
		else:
			raise IUA_Error("iua %s parameter must be int or str" % parameter_name)

	def Get_Status_Information_Value(self, object_parameter, status_type, status_information):
		if status_type == 1:
			status_information_values = object_parameter.Define_AS_State_Change_Status_Information_Values()
		else:
			status_information_values = object_parameter.Define_Other_Status_Information_Values()
		if type(status_information) == int:
			for parameter_number in status_information_values.keys():
				if status_information == parameter_number:
					break
			else:
				raise IUA_Error("\"%s\" is unknown iua status information parameter value of status type \"%s\"" % (status_information, status_type))
			return status_information
		elif type(status_information) == str:
			for parameter_number, parameter_description in status_information_values.items():
				if status_information.lower().replace(" ", "_") == parameter_description.lower().replace(" ", "_"):
					parameter_value = parameter_number
					break
			else:
				raise IUA_Error("\"%s\" is unknown iua status information parameter value of status type \"%s\"" % (status_information, status_type))
			return parameter_value
		else:
			raise IUA_Error("iua status information parameter must be int or str")

	def Composite_Parameter_Value_Forming(self, first_value, second_value):
		binary_first_value = self.convertor.Convert_Int_To_Bytes(int_value=first_value, bytes_number=2)
		binary_second_value = self.convertor.Convert_Int_To_Bytes(int_value=second_value, bytes_number=2)
		binary_composite_value = binary_first_value + binary_second_value
		composite_value = self.convertor.Convert_Bytes_To_Int(binary_composite_value)
		return composite_value

	def Build_StatusType_Parameter(self, status_type_definition, status_information_definition):
		status = IUA_Parameter(tag=13)
		status_type = self.Get_Parameter_Value(status, status_type_definition)
		status_information = self.Get_Status_Information_Value(status, status_type, status_information_definition)
		status.value = self.Composite_Parameter_Value_Forming(status_type, status_information)
		return status

	def Build_DLCI_Parameter(self, sapi_definition, tei_definition):
		dlci = IUA_Parameter(tag=5)
		if type(sapi_definition) != int:
			raise IUA_Error("SAPI must be int")
		elif sapi_definition not in range(64):
			raise IUA_Error("SAPI must be in range(0-63)")
		if type(tei_definition) != int:
			raise IUA_Error("TEI must be int")
		elif sapi_definition not in range(128):
			raise IUA_Error("TEI must be in range(0-127)")			
		dlci.value = sapi_definition*4*256 + tei_definition*2 + 1
		return dlci

	def Build_Status_Parameter(self, status_definition):
		status = IUA_Parameter(tag=16)
		status.value = self.Get_Parameter_Value(status, status_definition)
		return status

	def Build_Reason_Parameter(self, status_definition):
		reason = IUA_Parameter(tag=15)
		reason.value = self.Get_Parameter_Value(reason, reason_definition)
		return reason

	def Build_Diagnostic_Information_Parameter(self, diagnostic_information_definition):
		diagnostic_information = IUA_Parameter(tag=7)
		diagnostic_information.length = None
		if type(diagnostic_information_definition) == int or type(diagnostic_information_definition) == str:
			diagnostic_information.value = diagnostic_information_definition
			return diagnostic_information
		else:
			raise IUA_Error("iua diagnostic information parameter must be int or str")

	def Build_Info_String_Parameter(self, info_string_definition):
		info_string = IUA_Parameter(tag=4)
		info_string.length = None
		if type(info_string_definition) == str:
			info_string.value = info_string_definition
			return info_string
		else:
			raise IUA_Error("iua info string parameter must be str")

	def Build_ASP_Identifier_Parameter(self, asp_identifier_definition):
		asp_identifier = IUA_Parameter(tag=17)
		if type(asp_identifier_definition) == int:
			asp_identifier.value = asp_identifier_definition
			return asp_identifier
		else:
			raise IUA_Error("iua asp identifier parameter must be int")

	def Build_Heartbeat_Data_Parameter(self, heartbeat_data_definition):
		heartbeat_data = IUA_Parameter(tag=9)
		heartbeat_data.length = None
		if type(heartbeat_data_definition) == str or type(heartbeat_data_definition) == int:
			heartbeat_data.value = heartbeat_data_definition
			return heartbeat_data
		else:
			raise IUA_Error("iua heartbeat data parameter must be int or str")

	def Tuples_To_List_Distribution(self, tuples_list):
		array = []
		for element in tuples_list:
			for value in element:
				array.append(value)
		return array

	def Interface_Identifiers_Range_Check(self, identifiers_range):
		if len(identifiers_range) != 2:
			raise IUA_Error("identifier range must be described only by start and stop identifiers in list")
		else:
			for identifier in identifiers_range:
				if type(identifier) != int:
					raise IUA_Error("identifier range must consist only of int identifiers")

	def Interface_Identifiers_List_Check(self, interface_identifiers_list):
		if type(interface_identifiers_list) != list:
			raise IUA_Error("interface_identifiers argument must be list")
		else:
			first_permitted_type = type(interface_identifiers_list[0])
			if first_permitted_type == int:
				second_permitted_type = list #tuple
			elif first_permitted_type == list: #tuple:
				second_permitted_type = int
			elif first_permitted_type == str:
				second_permitted_type = str
			else:
				raise IUA_Error("wrong identifier type in interface_identifiers argument")
			for identifier in interface_identifiers_list:
				if type(identifier) != first_permitted_type and type(identifier) != second_permitted_type:
					raise IUA_Error("incorrect identifier in interface_identifiers argument")
				if type(identifier) == list: #tuple:
					self.Interface_Identifiers_Range_Check(identifier)

	def Interface_Identifiers_List_Distribution(self, interface_identifiers_list):
		self.Interface_Identifiers_List_Check(interface_identifiers_list)
		if type(interface_identifiers_list[0]) == str:
			return (interface_identifiers_list, None, "str_identifiers")
		else:
			int_identifiers_list = []
			int_range_identifiers_list = []
			for identifier in interface_identifiers_list:
				if type(identifier) == int:
					int_identifiers_list.append(identifier)
				else:
					int_range_identifiers_list.append(identifier)
			int_range_identifiers_list = self.Tuples_To_List_Distribution(int_range_identifiers_list)
			if int_identifiers_list and not int_range_identifiers_list:
				return (int_identifiers_list, None, "int_identifiers")
			elif int_range_identifiers_list and not int_identifiers_list:
				return (int_range_identifiers_list, None, "int_range_identifiers")
			else:
				return (int_identifiers_list, int_range_identifiers_list, "complex_int_identifiers")

	def Build_Int_Interface_Identifier_Parameter(self, interface_identifier_value):
		interface_identifier = IUA_Parameter(tag=1)
		interface_identifier.value = interface_identifier_value
		return interface_identifier

	def Build_Int_Range_Interface_Identifier_Parameter(self, interface_identifier_value):
		interface_identifier = IUA_Parameter(tag=8)
		interface_identifier.length = None
		interface_identifier.value = interface_identifier_value
		return interface_identifier

	def Build_Str_Interface_Identifier_Parameter(self, interface_identifier_value):
		interface_identifier = IUA_Parameter(tag=3)
		interface_identifier.length = None
		interface_identifier.value = interface_identifier_value
		return interface_identifier

	def Identifiers_List_Filtering(self, interface_identifiers_list):
		for parameter in interface_identifiers_list:
			if parameter.tag == 8:
				interface_identifiers_list.remove(parameter)
		if len(interface_identifiers_list) != 0:
			return interface_identifiers_list
		else:
			raise IUA_Error("interface_identifiers argument elements must be int or str")

	def Build_Interface_Identifier_Parameters(self, interface_identifiers_list, without_int_range=False):
		main_list, secondary_list, info_tag = self.Interface_Identifiers_List_Distribution(interface_identifiers_list)
		interface_identifiers_list = []
		if info_tag == "str_identifiers":
			for identifier in main_list:
				str_identifier = self.Build_Str_Interface_Identifier_Parameter(identifier)
				interface_identifiers_list.append(str_identifier)
		elif info_tag == "int_identifiers":
			for identifier in main_list:
				int_identifier = self.Build_Int_Interface_Identifier_Parameter(identifier)
				interface_identifiers_list.append(int_identifier)
		elif info_tag == "int_range_identifiers":
			int_range_identifier = self.Build_Int_Range_Interface_Identifier_Parameter(main_list)
			interface_identifiers_list.append(int_range_identifier) 
		else:
			for identifier in main_list:
				int_identifier = self.Build_Int_Interface_Identifier_Parameter(identifier)
				interface_identifiers_list.append(int_identifier)
			int_range_identifier = self.Build_Int_Range_Interface_Identifier_Parameter(secondary_list)
			interface_identifiers_list.append(int_range_identifier)
		if without_int_range:
			interface_identifiers_list = self.Identifiers_List_Filtering(interface_identifiers_list)
		return interface_identifiers_list 

	def Build_Traffic_Mode_Type_Parameter(self, traffic_mode_type_definition):
		traffic_mode_type = IUA_Parameter(tag=11)
		traffic_mode_type.value = self.Get_Parameter_Value(traffic_mode_type, traffic_mode_type_definition)
		return traffic_mode_type

	def Build_Error_Code_Parameter(self, error_code_definition):
		error_code = IUA_Parameter(tag=12)
		error_code.value = self.Get_Parameter_Value(error_code, error_code_definition)
		return error_code

# Build messages

#	def Build_DATA_Message(self, protocol_data_1, interface_identifiers=[], message_class=6, message_type=1, version=1):
#		ISUP_handler = self.isup_bld._MTP3_ISUP_make_message_handler()
#		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
#		interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers, without_int_range=True)
#		object_message.parameters = interface_identifiers_list
#		protocol_data = IUA_Parameter(tag=14)
#		protocol_data.length = None
#		protocol_data.value = ISUP_handler[protocol_data_1["message"]][0](ISUP_handler[protocol_data_1["message"]][1], protocol_data_1)
#		object_message.parameters.append(protocol_data)
#		binary_message = self.convertor.Convert_M2UA_Message(object_message)
#		return binary_message

	def Build_Establish_Request(self, sapi, tei, interface_identifiers=[], message_class=5, message_type=5, version=1):
		object_message = IUA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers and sapi and tei:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
			dlci = Build_DLCI_Parameter(sapi, tei)
			object_message.parameters.append(dlci)
		else:
			raise IUA_Error("missed mandatory parameter: sapi or tei or iid")
		binary_message = self.convertor.Convert_IUA_Message(object_message)
		return binary_message

	def Build_Establish_Confirmation(self, sapi, tei, interface_identifiers=[], message_class=5, message_type=6, version=1):
		object_message = IUA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers and sapi and tei:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
			dlci = Build_DLCI_Parameter(sapi, tei)
			object_message.parameters.append(dlci)
		else:
			raise IUA_Error("missed mandatory parameter: sapi or tei or iid")
		binary_message = self.convertor.Convert_IUA_Message(object_message)
		return binary_message

	def Build_Establish_Indication(self, sapi, tei, interface_identifiers=[], message_class=5, message_type=7, version=1):
		object_message = IUA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers and sapi and tei:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
			dlci = Build_DLCI_Parameter(sapi, tei)
			object_message.parameters.append(dlci)
		else:
			raise IUA_Error("missed mandatory parameter: sapi or tei or iid")
		binary_message = self.convertor.Convert_IUA_Message(object_message)
		return binary_message

	def Build_Release_Request(self, sapi, tei, reason, interface_identifiers=[], message_class=5, message_type=8, version=1):
		object_message = IUA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers and sapi and tei and reason:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
			dlci = Build_DLCI_Parameter(sapi, tei)
			object_message.parameters.append(dlci)
			reason = self.Build_Reason_Parameter(reason)
			object_message.parameters.append(reason)
		else:
			raise IUA_Error("missed mandatory parameter: sapi or tei or iid or reason")
		binary_message = self.convertor.Convert_IUA_Message(object_message)
		return binary_message

	def Build_Release_Confirmation(self, sapi, tei, reason, interface_identifiers=[], message_class=5, message_type=9, version=1):
		object_message = IUA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers and sapi and tei and reason:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
			dlci = Build_DLCI_Parameter(sapi, tei)
			object_message.parameters.append(dlci)
			reason = self.Build_Reason_Parameter(reason)
			object_message.parameters.append(reason)
		else:
			raise IUA_Error("missed mandatory parameter: sapi or tei or iid or reason")
		binary_message = self.convertor.Convert_IUA_Message(object_message)
		return binary_message

	def Build_Release_Indication(self, sapi, tei, reason, interface_identifiers=[], message_class=5, message_type=10, version=1):
		object_message = IUA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers and sapi and tei and reason:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
			dlci = Build_DLCI_Parameter(sapi, tei)
			object_message.parameters.append(dlci)
			reason = self.Build_Reason_Parameter(reason)
			object_message.parameters.append(reason)
		else:
			raise IUA_Error("missed mandatory parameter: sapi or tei or iid or reason")
		binary_message = self.convertor.Convert_IUA_Message(object_message)
		return binary_message

	def Build_ASP_UP_Message(self, asp_identifier=None, info_string=None, message_class=3, message_type=1, version=1):
		object_message = IUA_Message(int(message_class), int(message_type), int(version))
		if asp_identifier:
			asp_identifier = self.Build_ASP_Identifier_Parameter(asp_identifier)
			object_message.parameters.append(asp_identifier)
		if info_string:
			info_string = self.Build_Info_String_Parameter(info_string)
			object_message.parameters.append(info_string)
		binary_message = self.convertor.Convert_IUA_Message(object_message)
		return binary_message

	def Build_ASP_UP_ACK_Message(self, info_string=None, message_class=3, message_type=4, version=1):
		object_message = IUA_Message(int(message_class), int(message_type), int(version))
		if info_string:
			info_string = self.Build_Info_String_Parameter(info_string)
			object_message.parameters.append(info_string)
		binary_message = self.convertor.Convert_IUA_Message(object_message)
		return binary_message

	def Build_ASP_DOWN_Message(self, info_string=None, message_class=3, message_type=2, version=1):
		object_message = IUA_Message(int(message_class), int(message_type), int(version))
		if info_string:
			info_string = self.Build_Info_String_Parameter(info_string)
			object_message.parameters.append(info_string)
		binary_message = self.convertor.Convert_IUA_Message(object_message)
		return binary_message

	def Build_ASP_DOWN_ACK_Message(self, info_string=None, message_class=3, message_type=5, version=1):
		object_message = IUA_Message(int(message_class), int(message_type), int(version))
		if info_string:
			info_string = self.Build_Info_String_Parameter(info_string)
			object_message.parameters.append(info_string)
		binary_message = self.convertor.Convert_IUA_Message(object_message)
		return binary_message

	def Build_BEAT_Message(self, heartbeat_data=None, message_class=3, message_type=3, version=1):
		object_message = IUA_Message(int(message_class), int(message_type), int(version))
		if heartbeat_data:
			heartbeat_data = self.Build_Heartbeat_Data_Parameter(heartbeat_data)
			object_message.parameters.append(heartbeat_data)
		binary_message = self.convertor.Convert_IUA_Message(object_message)
		return binary_message

	def Build_BEAT_ACK_Message(self, heartbeat_data=None, message_class=3, message_type=6, version=1):
		object_message = IUA_Message(int(message_class), int(message_type), int(version))
		if heartbeat_data:
			heartbeat_data = self.Build_Heartbeat_Data_Parameter(heartbeat_data)
			object_message.parameters.append(heartbeat_data)
		binary_message = self.convertor.Convert_IUA_Message(object_message)
		return binary_message

	def Build_ASP_ACTIVE_Message(self, traffic_mode_type=None, interface_identifiers=[], info_string=None, message_class=4, message_type=1, version=1):
		object_message = IUA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
		if traffic_mode_type:
			traffic_mode_type = self.Build_Traffic_Mode_Type_Parameter(traffic_mode_type)
			object_message.parameters.append(traffic_mode_type)
		if info_string:
			info_string = self.Build_Info_String_Parameter(info_string)
			object_message.parameters.append(info_string)
		binary_message = self.convertor.Convert_IUA_Message(object_message)
		return binary_message

	def Build_ASP_ACTIVE_ACK_Message(self, traffic_mode_type=None, interface_identifiers=[], info_string=None, message_class=4, message_type=3, version=1):
		object_message = IUA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
		if traffic_mode_type:
			traffic_mode_type = self.Build_Traffic_Mode_Type_Parameter(traffic_mode_type)
			object_message.parameters.append(traffic_mode_type)
		if info_string:
			info_string = self.Build_Info_String_Parameter(info_string)
			object_message.parameters.append(info_string)
		binary_message = self.convertor.Convert_IUA_Message(object_message)
		return binary_message

	def Build_ASP_INACTIVE_Message(self, interface_identifiers=[], info_string=None, message_class=4, message_type=2, version=1):
		object_message = IUA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
		if info_string:
			info_string = self.Build_Info_String_Parameter(info_string)
			object_message.parameters.append(info_string)
		binary_message = self.convertor.Convert_IUA_Message(object_message)
		return binary_message

	def Build_ASP_INACTIVE_ACK_Message(self, interface_identifiers=[], info_string=None, message_class=4, message_type=4, version=1):
		object_message = IUA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
		if info_string:
			info_string = self.Build_Info_String_Parameter(info_string)
			object_message.parameters.append(info_string)
		binary_message = self.convertor.Convert_IUA_Message(object_message)
		return binary_message

	def Build_ERR_Message(self, error_code, diagnostic_information=None, message_class=0, message_type=0, version=1):
		object_message = IUA_Message(int(message_class), int(message_type), int(version))
		error_code = self.Build_Error_Code_Parameter(error_code)
		object_message.parameters.append(error_code)
		if diagnostic_information:
			diagnostic_information = self.Build_Diagnostic_Information_Parameter(diagnostic_information)
			object_message.parameters.append(diagnostic_information)
		binary_message = self.convertor.Convert_IUA_Message(object_message)
		return binary_message

	def Build_NTFY_Message(self, status_type, status_information, asp_identifier=None, interface_identifiers=[], info_string=None, 
		                                                                               message_class=0, message_type=1, version=1):
		object_message = IUA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
		status = self.Build_StatusType_Parameter(status_type, status_information)
		object_message.parameters.append(status)
		if asp_identifier:
			asp_identifier = self.Build_ASP_Identifier_Parameter(asp_identifier)
			object_message.parameters.append(asp_identifier)
		if info_string:
			info_string = self.Build_Info_String_Parameter(info_string)
			object_message.parameters.append(info_string)
		binary_message = self.convertor.Convert_IUA_Message(object_message)
		return binary_message

	def Build_TEI_Status_Request(self, sapi, tei, status, message_class=0, message_type=2, version=1):
		object_message = IUA_Message(int(message_class), int(message_type), int(version))
		if sapi and tei:
			dlci = Build_DLCI_Parameter(sapi, tei)
			object_message.parameters.append(dlci)
		else:
			raise IUA_Error("missed mandatory parameter: sapi or tei")
		status = self.Build_Status_Parameter(status)
		object_message.parameters.append(status)
		binary_message = self.convertor.Convert_IUA_Message(object_message)
		return binary_message

	def Build_TEI_Status_Confirmation(self, sapi, tei, status, message_class=0, message_type=3, version=1):
		object_message = IUA_Message(int(message_class), int(message_type), int(version))
		if sapi and tei:
			dlci = Build_DLCI_Parameter(sapi, tei)
			object_message.parameters.append(dlci)
		else:
			raise IUA_Error("missed mandatory parameter: sapi or tei")
		status = self.Build_Status_Parameter(status)
		object_message.parameters.append(status)
		binary_message = self.convertor.Convert_IUA_Message(object_message)
		return binary_message

	def Build_TEI_Status_Indication(self, sapi, tei, status, message_class=0, message_type=4, version=1):
		object_message = IUA_Message(int(message_class), int(message_type), int(version))
		if sapi and tei:
			dlci = Build_DLCI_Parameter(sapi, tei)
			object_message.parameters.append(dlci)
		else:
			raise IUA_Error("missed mandatory parameter: sapi or tei")
		status = self.Build_Status_Parameter(status)
		object_message.parameters.append(status)
		binary_message = self.convertor.Convert_IUA_Message(object_message)
		return binary_message

	def Build_TEI_Query_Request(self, sapi, tei, message_class=0, message_type=5, version=1):
		object_message = IUA_Message(int(message_class), int(message_type), int(version))
		if sapi and tei:
			dlci = Build_DLCI_Parameter(sapi, tei)
			object_message.parameters.append(dlci)
		else:
			raise IUA_Error("missed mandatory parameter: sapi or tei")
		binary_message = self.convertor.Convert_IUA_Message(object_message)
		return binary_message

class Message_Parser:

	def __init__(self):
		self.common_iua_header_pattern = struct.Struct(">B B B B L")
		self.iua_parameter_header_pattern = struct.Struct(">H H")

	def Define_IUA_Parameter_Handlers(self):
		handlers = {
		  (1,5,11,12,13,15,16,17) : self.Int_IUA_Parameter_Value_Handling,
		  (3,4) : self.Str_IUA_Parameter_Value_Handling,
		  (8,) : self.Int_Range_IUA_Parameter_Value_Handling,
#		  (14,) : self.IUA_Protocol_Data_Handling,
		  (7,9) : self.Polymorphic_IUA_Parameter_Value_Handling
		}
		return handlers

	def Get_IUA_Class_Description(self, object_message):
		classes = object_message.Define_Message_Classes()
		for class_number,description in classes.items():
		    if object_message.mes_class == class_number:
		    	class_description = description
		    	break
		else:
			raise IUA_Error("iua class \"%s\" does not supported" % object_message.mes_class)
		return class_description

	def Get_IUA_Message_Types(self, object_message):
		if object_message.mes_class == 0:
			message_types = object_message.Define_MGMT_Message_Types()
		elif object_message.mes_class == 3:
			message_types = object_message.Define_ASPSM_Message_Types()
		elif object_message.mes_class == 4:
			message_types = object_message.Define_ASPTM_Message_Types()
		elif object_message.mes_class == 5:
			message_types = object_message.Define_QPTM_Message_Types()
		else:
			raise IUA_Error("iua class \"%s\" does not supported" % object_message.mes_class)
		return message_types

	def Get_IUA_Parameter_Tags(self, iua_parameter):
		return iua_parameter.Define_Parameter_Tags()

	def Get_IUA_Type_Description(self, object_message):
		message_types = self.Get_IUA_Message_Types(object_message)
		for type_number, description in message_types.items():
			if object_message.mes_type == type_number:
				type_description = description
				break
		else:
			raise IUA_Error("\"%s\" is unknown iua message type" % object_message.mes_type)
		return type_description

	def Get_Message_Info(self, object_message):
		print("----------------Message Info ----------------")
		print("Version:", object_message.version)
		print("Spare:", object_message.spare)
		print("Class:", object_message.mes_class)
		print("     -", self.Get_IUA_Class_Description(object_message))
		print("Type:", object_message.mes_type)
		print("     -", self.Get_IUA_Type_Description(object_message))
		print("---------------------------------------------")

	def IUA_Message_Class_Check(self, iua_header):
		message_classes = iua_header.Define_Message_Classes()
		for class_number in message_classes.keys():
			if iua_header.mes_class == class_number:
				break
		else:
			raise IUA_Error("\"%s\" is unknown iua class" % iua_header.mes_class)

	def IUA_Message_Type_Check(self, iua_header):
		message_types = self.Get_IUA_Message_Types(iua_header)
		for type_number in message_types.keys():
			if iua_header.mes_type == type_number:
				break
		else:
			raise IUA_Error("\"%s\" is unknown iua message type" % iua_header.mes_type)

	def IUA_Message_Length_Check(self, iua_header):
		if iua_header.length < 8:
			raise IUA_Error("iua message length \"%s\" is too short" % iua_header.length)

	def IUA_Header_Check(self, iua_header):
		if iua_header.version != 1:
			raise IUA_Error("iua version \"%s\" is not 1" % iua_header.version)
		if iua_header.spare != 0:
			raise IUA_Error("iua spare \"%s\" is not zero" % iua_header.spare)
		self.IUA_Message_Class_Check(iua_header)
		self.IUA_Message_Type_Check(iua_header)
		self.IUA_Message_Length_Check(iua_header)

	def IUA_Header_Forming(self, binary_header):
		try:
			unpacked_data = self.common_iua_header_pattern.unpack(binary_header)
		except struct.error:
			if not binary_header:
				raise IUA_Error("message was not received")
			else:
				raise IUA_Error("received message is not iua message")
		else:
			iua_header = IUA_Message(version=unpacked_data[0], spare=unpacked_data[1], message_class=unpacked_data[2], message_type=unpacked_data[3])
			iua_header.length = unpacked_data[4]
			self.IUA_Header_Check(iua_header)
			return iua_header

	def Padding_Bytes_Counting(self, parameter_length):
		initial_parameter_length = parameter_length
		for i in range(1,4):
			parameter_length = initial_parameter_length + i
			if parameter_length % 4 == 0:
				multiple_length = parameter_length
				break
		else:
			raise IUA_Error("padding bytes counting error")
		paddings_number = multiple_length - initial_parameter_length
		return paddings_number

	def IUA_Parameters_Shifting(self, iua_data, parameter_length):
		iua_data = iua_data[parameter_length:]
		return iua_data

	def IUA_Parameter_Padding_Removing(self, iua_data, parameter_length):
		paddings_number = self.Padding_Bytes_Counting(parameter_length)
		iua_data = iua_data[:parameter_length] + iua_data[parameter_length + paddings_number:]
		return iua_data

	def IUA_Parameter_Tag_Check(self, iua_parameter):
		parameter_tags = iua_parameter.Define_Parameter_Tags()
		for tag_number in parameter_tags.keys():
			if iua_parameter.tag == tag_number:
				break
		else:
			raise IUA_Error("\"%s\" is unknown iua parameter tag value" % iua_parameter.tag)

	def Add_Bit_Paddings(self, bin_value):
		end_of_padding = False
		while not end_of_padding:
			if len(bin_value) != 8:
				bin_value = "0" + bin_value
			else:
				end_of_padding = True
		return bin_value

	def IUA_Protocol_Data_Handling(self, binary_protocol_data):
# Q921 MODULE NEED
		#MTP3 object building
		mtp3_data = isup.MTP3_Data()
		#Building SIO data
		mtp3_data.sio = self.MTP3_Service_Information_Octet_Forming(mtp3_object=mtp3_data, binary_sio_data=binary_protocol_data[:1])
		#Building routing label
		mtp3_data.routing_label = self.MTP3_Routing_Label_Forming(mtp3_object=mtp3_data, binary_routing_label_data=binary_protocol_data[1:5])
		#Service data
		mtp3_data.service_data = self.Service_Data_Forming(service_indicator=mtp3_data.sio.service_indicator, binary_data=binary_protocol_data[5:])
		return mtp3_data

	def IUA_Composite_Parameters_Handling(self, binary_parameter_value):
		parameter_value = self.IUA_Parameters_Forming(binary_parameter_value)
		return parameter_value

	def Polymorphic_IUA_Parameter_Value_Handling(self, binary_parameter_value):
		parameter_value = binascii.hexlify(binary_parameter_value)
		return parameter_value

	def Int_Range_IUA_Parameter_Value_Handling(self, binary_parameter_value):
		int_range_parameter_values = []
		end_of_ranges = False
		while not end_of_ranges:
			start_identifier = int.from_bytes(binary_parameter_value[:4], byteorder="big")
			stop_identifier = int.from_bytes(binary_parameter_value[4:8], byteorder="big")
			int_range_parameter_values.append([start_identifier, stop_identifier])
			binary_parameter_value = binary_parameter_value[8:]
			if not binary_parameter_value:
				end_of_ranges = True
		return int_range_parameter_values

	def Str_IUA_Parameter_Value_Handling(self, binary_parameter_value):
		parameter_value = binary_parameter_value.decode("utf-8")
		return parameter_value

	def Int_IUA_Parameter_Value_Handling(self, binary_parameter_value):
		parameter_value = int.from_bytes(binary_parameter_value, byteorder="big")
		return parameter_value

	def IUA_Parameter_Value_Forming(self, parameter_tag, binary_parameter_value):
		#Empty parameter has None value
		if not binary_parameter_value:
			return None
		parameter_handlers = self.Define_IUA_Parameter_Handlers()
		parameter_value = None
		for parameter_tags, handler in parameter_handlers.items():
			for tag in parameter_tags:
				if parameter_tag == tag:
					parameter_value = handler(binary_parameter_value)
		if parameter_value == None:
			raise IUA_Error("unsupported parameter tag: %s" % parameter_tag)
		else:
			return parameter_value

	def IUA_Parameters_Forming(self, iua_data):
		#Empty list for parameter collecting
		iua_parameters = []
		#Сycle stop сondition
		end_of_parameters = False
		while not end_of_parameters:
			#Extracting tag and length atributes from parameter
			parameter_tag = iua_data[:2]
			parameter_length = iua_data[2:4]
			parameter_header = parameter_tag + parameter_length
			unpacked_data = self.iua_parameter_header_pattern.unpack(parameter_header)
			#Building parameter by tag
			iua_parameter = IUA_Parameter(unpacked_data[0])
			#Checking tag for existence 
			self.IUA_Parameter_Tag_Check(iua_parameter)
			#Parameter length determining
			iua_parameter.length = unpacked_data[1]
			#Removing padding bytes if parameter length is not multiple of 4
			if iua_parameter.length % 4 != 0:
				iua_data = self.IUA_Parameter_Padding_Removing(iua_data, iua_parameter.length)
			#Parameter value extracting 
			binary_parameter_value = iua_data[4:iua_parameter.length]
			#Parameter value assignment
			iua_parameter.value = self.IUA_Parameter_Value_Forming(iua_parameter.tag, binary_parameter_value)
			#Append formed parameter to list
			iua_parameters.append(iua_parameter)
			#Byte string shifting along parameter length
			iua_data = self.IUA_Parameters_Shifting(iua_data, iua_parameter.length)
			#Stop condition checking
			if not iua_data:
				end_of_parameters = True
		return iua_parameters 

	def Parse_Message(self, binary_message):
		#Retrieving the IUA header bytes from the binary message
		binary_iua_header = binary_message[:8]
		#Building IUA header object
		iua_data = self.IUA_Header_Forming(binary_iua_header)
		#Building IUA parameters if they exist
		if iua_data.length > 8:
			iua_parameters = self.IUA_Parameters_Forming(binary_message[8:])
			iua_data.parameters = iua_parameters
		return iua_data

class IUA_Error(Exception):

	def __init__(self, description):
		self.description = description

class Message_Validator:

	def __init__(self):
		self.parser = Message_Parser()
		self.parameters_list = IUA_Parameter(tag=0)

	def Define_Exec_Handlers(self):
		handlers = {
		  1 : self.Int_Parameter_Value_Handling,
		  11 : self.Int_Parameter_Value_Handling,
		  12 : self.Int_Parameter_Value_Handling,
		  13 : self.Status_Parameter_Value_Handling,
		  17 : self.Int_Parameter_Value_Handling,
		  3 : self.Str_Parameter_Value_Handling,
		  4 : self.Str_Parameter_Value_Handling,
		  7 : self.Polymorphic_Parameter_Value_Handling,
		  8 : self.Int_Range_Parameter_Value_Handling,
		  9 : self.Polymorphic_Parameter_Value_Handling
		}
		return handlers

	def Get_Tag_Parameters_list(self, tag):
		if tag == 11:
			parameter_info = self.parameters_list.Define_Traffic_Mode_Type_Values()
		elif tag == 12:
			parameter_info = self.parameters_list.Define_Error_Code_Values()
		elif tag == 13:
			parameter_info = self.parameters_list.Define_Status_Type_Values()
		else:
			raise IUA_Error("iua parameter tag \"%s\" does not support" % tag)
		return parameter_info

	def Get_Tag_Parameters_list_13(self, status_value):
		if status_value == 1:
			parameter_info = self.parameters_list.Define_AS_State_Change_Status_Information_Values()
		elif status_value == 2:
			parameter_info = self.parameters_list.Define_Other_Status_Information_Values()
		else:
			raise IUA_Error("iua Status parameter value \"%s\" does not support" % status_value)
		return parameter_info

	def Polymorphic_Parameter_Value_Handling(self, tag, in_parameter_value):
		if type(in_parameter_value) == bytes:
			return in_parameter_value
		elif type(in_parameter_value) == list:
			binary_parameter_value = bytes(in_parameter_value)
			parameter_value = binascii.hexlify(binary_parameter_value)
			return parameter_value
		else:
			raise M2UA_Error("Type of parameter: "+str(tag)+" is not BYTES or LIST")

	def Int_Range_Parameter_Value_Handling(self, tag, in_parameter_value):
		if	type(in_parameter_value) == list:
			if type(in_parameter_value[0]) == list:
				for _value in in_parameter_value:
					if len(_value) != 2:
						raise IUA_Error("identifier range must be described only by start and stop identifiers in list")
					if not (int(_value[0]) or int(_value[1])):
						raise IUA_Error("identifiers values must be integer")
				return in_parameter_value
			elif type(in_parameter_value[0]) == int:
				if len(in_parameter_value) != 2:
					raise IUA_Error("identifier range must be described only by start and stop identifiers in list")
				if in_parameter_value[0] >= in_parameter_value[1]:
					raise IUA_Error("identifier range start identifier must be less than stop identifier")
				return [in_parameter_value]
			else:
				raise IUA_Error("Type of parameter: "+str(tag)+" is not LIST")
		else:
			raise IUA_Error("Type of parameter: "+str(tag)+" is not LIST")

	def Int_Parameter_Value_Handling(self, tag, in_parameter_value):
		if type(in_parameter_value) == int or type(in_parameter_value) == list:
			return in_parameter_value
		else:
			parameter_info = self.Get_Tag_Parameters_list(tag)
			for _key,_value in parameter_info.items():
				if in_parameter_value.lower().replace(" ", "_") == _value.lower().replace(" ", "_"):
					return _key
			raise IUA_Error("Type of parameter: "+tag+" is not INTEGER")

	def Str_Parameter_Value_Handling(self, tag, in_parameter_value):
		try:
			parameter_value = str(in_parameter_value)
			return parameter_value
		except:
			raise IUA_Error("Type of parameter: "+tag+" is not STRING")

	def Status_Parameter_Value_Handling(self, tag, int_parameter_value):
		status,information = int_parameter_value.split("/")
		try:
			status = int(status)
			try:
				information = int(information)
				return status*65536 + information 
			except:
				parameter_info = self.Get_Tag_Parameters_list_13(status)
				for _key,_value in parameter_info.items():
					if information.lower().replace(" ", "_") == _value.lower().replace(" ", "_"):
						return status*65536 + _key
				raise IUA_Error("iua Identification parameter value \"%s\" does not support" % information)
		except:
			parameter_info = self.Get_Tag_Parameters_list(tag)
			for _key,_value in parameter_info.items():
				if status.lower().replace(" ", "_") == _value.lower().replace(" ", "_"):
					status = _key
					try:
						information = int(information)
						return status*65536 + information 
					except:
						parameter_info = self.Get_Tag_Parameters_list_13(status)
						for _key,_value in parameter_info.items():
							if information.lower().replace(" ", "_") == _value.lower().replace(" ", "_"):
								return status*65536 + _key
						raise IUA_Error("iua Identification parameter value \"%s\" does not support" % information)
			raise IUA_Error("iua Status parameter value \"%s\" does not support" % status)

	def IUA_Message_Class_Type_Check(self, message, config_message):
		types = self.parser.Get_IUA_Message_Types(message)
		description = types[message.mes_type].replace(" ", "_")
		config_message = "("+config_message+")"
		if config_message in description:
			return (True, config_message)
		return (False, description)

	def Params_Value_Check(self, message, params):
		#Parameter value check
		print(":::", params)
		tags = self.parameters_list.Define_Parameter_Tags()
		param_handler = self.Define_Exec_Handlers()
		resultvalue = []
		result = True
		res_key = ''
		res_val = ''
		if not params:
			return (True, "No params for validation")
		if len(message.parameters) > 0:
			for key, value in params.items():
				print("___________________________")
				print (time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime()), ":Params_Value_Check function(for logging purpose) conf par", key, value)                                         #delete
				for parameter in message.parameters:
					print(time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime()), ":Params_Value_Check function(for logging purpose) recv_par", parameter.tag, parameter.value, type(parameter.value))                 #delete
					description = tags[parameter.tag].lower().replace(" ", "_")  
					try:
						key = int(key)
						if key == parameter.tag:
							value = param_handler[key](key, value)
							if type(value) == list: 
								if type(parameter.value) == list and len(value) == len(parameter.value):
									n=0
									flag = True
									while n < len(value):
										if value[n] != parameter.value[n]:
											flag = False
										n += 1
									if flag == True:
										resultvalue.append([True, key, value])
										continue
								elif type(parameter.value) == int:
									n=0
									flag = False
									while n < len(value):
										if value[n] == parameter.value:
											flag = True
											tempvalue = value[n]
										n += 1
									if flag == True:
										resultvalue.append([True, key, tempvalue])
										continue
								else:
									pass
							else:
								if value == parameter.value:
									resultvalue.append([True, key, value])
									continue
								else:
									pass
						else:
							pass
					except:
						if key == description:
							value = param_handler[parameter.tag](parameter.tag, value)
							if type(value) == list: 
								if type(parameter.value) == list and len(value) == len(parameter.value):
									n=0
									flag = True
									while n < len(value):
										if value[n] != parameter.value[n]:
											flag = False
										n += 1
									if flag == True:
										resultvalue.append([True, key, value])
										continue
								elif type(parameter.value) == int:
									n=0
									flag = False
									while n < len(value):
										if value[n] == parameter.value:
											flag = True
											tempvalue = value[n]
										n += 1
									if flag == True:
										resultvalue.append([True, key, tempvalue])
										continue
								else:
									pass
							else:
								print ("-----conf par", key, value, parameter.tag, parameter.value)
								if value == parameter.value:
									resultvalue.append([True, key, value])
									continue
								else:
									pass
						else:
							pass
				if resultvalue == []:
					resultvalue.append([False, key, value])
			for value in resultvalue:
				if value[0] == False:
					result = False
				res_key += str(value[1]) + " "
				res_val += str(value[2]) + " "
				print ("YYY", value[0], value[1], value[2], res_key, res_val, result)
			if result == False:
				return (False, "Tags: ("+res_key+") or their values: ("+res_val+") don't match")
			else:
				return (True, "Tags: ("+res_key+") and their values: ("+res_val+") are match")
		else:
			return (False, "No parameters received in message")

	def Validate_Message(self, message, config_message, config_message_params):				
		if type(message) == str:
			print ("||||", message, config_message)
			if message == config_message:
				return (True, "Validation for NO MESSAGE RECEIVED success")
			else:
				return (False, "Validation for NO MESSAGE RECEIVED fail")
		else:
			result, description_mes = self.IUA_Message_Class_Type_Check(message, config_message)
			if not result:
				return (False, "Message '%s' was received" % description_mes)
			result, description_tag = self.Params_Value_Check(message, config_message_params)
			return (result, "Valid message received: " + description_mes + ", "+ description_tag)

class Config_Executor:

	def Values_Exec(self, message_row):
		# Ecexute message type and paarmeters from CDATA
		print (";;;;", message_row)
		message_row_type = None
		mes_params = dict()
		if message_row:
			message_row = message_row.strip()
			row_comp = message_row.partition("(") 
			message_row_type = row_comp[0].upper().replace(" ", "_")
			if row_comp[2] and row_comp[2] != ")": 
				temp_string = ''
				param = ''
				flag_mess=False
				flag_list1 = False
				flag_list2 = False
				list1_vc = 0
				for _val in row_comp[2]:
					if _val == "'" or _val == '"':
						pass
					elif _val == "(":
						flag_mess = True
						mes_params[param] = dict()
						mes_params[param]["message"] = temp_string.strip().upper().replace(" ", "_")
						temp_string = ''
						param_in_mess = ''
					elif _val == "," or _val ==";":
						if param != '':
							if flag_mess:
								if param_in_mess != '':
									try:
										fin_string = int(temp_string.strip())
										if flag_list1 and not flag_list2:
											mes_params[param][param_in_mess].append(fin_string)
											list1_vc += 1
											temp_string = ''	
										elif flag_list2:
											mes_params[param][param_in_mess][list1_vc].append(fin_string)
											temp_string = ''				
										else:
											mes_params[param][param_in_mess] = fin_string
											temp_string = ''
											param_in_mess = ''
									except:
										fin_string = temp_string.strip()
										if fin_string:
											if flag_list1 and not flag_list2:
												mes_params[param][param_in_mess].append(fin_string)
												list1_vc += 1
												temp_string = ''	
											elif flag_list2:
												mes_params[param][param_in_mess][list1_vc].append(fin_string)
												temp_string = ''				
											else:
												mes_params[param][param_in_mess] = fin_string
												temp_string = ''
												param_in_mess = ''
								else:
									raise IUA_Error("Configuration data is not valid")
							else:
								try:
									fin_string = int(temp_string.strip())
									if flag_list1 and not flag_list2:
										mes_params[param].append(fin_string)
										list1_vc += 1
										temp_string = ''	
									elif flag_list2:
										mes_params[param][list1_vc].append(fin_string)
										temp_string = ''										
									else:
										mes_params[param] = fin_string
										temp_string = ''
										param = ''
								except:
									fin_string = temp_string.strip()
									if fin_string:
										if flag_list1 and not flag_list2:
											mes_params[param].append(fin_string)
											list1_vc += 1
											temp_string = ''	
										elif flag_list2:
											mes_params[param][list1_vc].append(fin_string)
											temp_string = ''										
										else:
											mes_params[param] = fin_string
											temp_string = ''
											param = ''
						else:
							raise IUA_Error("Configuration data is not valid")
					elif _val == ")":
						try:
							fin_string = int(temp_string.strip())
							if flag_mess:
								flag_mess = False
								mes_params[param][param_in_mess] = fin_string
								temp_string = ''
								param_in_mess = ''
							else:
								mes_params[param] = fin_string
								temp_string = ''
								param = ''
								continue
						except:
							fin_string = temp_string.strip()
							if flag_mess:
								flag_mess = False
								if fin_string:
									mes_params[param][param_in_mess] = fin_string
									temp_string = ''
									param_in_mess = ''
							else:
								if fin_string:
									mes_params[param] = fin_string
									temp_string = ''
									param = ''
								continue
					elif _val == "=":
						if flag_mess:
							param_in_mess = temp_string.strip().lower().replace(" ", "_")
							temp_string = ''
						else:
							param = temp_string.strip().lower().replace(" ", "_")
							temp_string = ''
					elif _val == "[":
						if flag_list1:
							if flag_list2:
								raise IUA_Error("Configuration data is not valid")
							else:
								flag_list2 = True
								if flag_mess:
									print("kkk",mes_params[param][param_in_mess])
									mes_params[param][param_in_mess].append(list())
								else:
									print("kkkf",mes_params[param])
									mes_params[param].append(list())
						else:
							flag_list1 = True
							if flag_mess:
								mes_params[param][param_in_mess] = list()
							else:
								mes_params[param] = list()
					elif _val == "]":
						try:
							fin_string = int(temp_string.strip())
							if flag_list1:
								if flag_list2:
									if flag_mess:
										mes_params[param][param_in_mess][list1_vc].append(fin_string)
										temp_string = ''
									else:
										mes_params[param][list1_vc].append(fin_string)
										temp_string = ''
									flag_list2 = False
								else:
									if flag_mess:
										mes_params[param][param_in_mess].append(fin_string)
										temp_string = ''
									else:
										mes_params[param].append(fin_string)
										temp_string = ''
									flag_list1 = False
									list1_vc = 0
								print ("HHH", param, fin_string, mes_params[param])
							else:
								raise IUA_Error("Configuration data is not valid")
						except:
							fin_string = temp_string.strip()
							if flag_list1:
								if flag_list2:
									if flag_mess:
										if fin_string:
											print("here11")
											mes_params[param][param_in_mess][list1_vc].append(fin_string)
											temp_string = ''
									else:
										if fin_string:
											print("here12")
											mes_params[param][list1_vc].append(fin_string)
											temp_string = ''
									flag_list2 = False									
								else:
									if flag_mess:
										if fin_string:
											print("here1")
											mes_params[param][param_in_mess].append(fin_string)
											temp_string = ''
									else:
										if fin_string:
											print("here2")
											mes_params[param].append(fin_string)
											temp_string = ''
									flag_list1 = False
									list1_vc = 0
								print ("HHH", param, fin_string, mes_params[param])
							else:
								raise IUA_Error("Configuration data is not valid")
					else:
						temp_string +=_val
			print ("::::",mes_params)
			return message_row_type, mes_params
		else:
			return "NO_MESSAGE", mes_params




		


