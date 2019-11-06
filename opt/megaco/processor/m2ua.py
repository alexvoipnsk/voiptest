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
import processor.isup as isup
import time

class M2UA_Message:

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

	def Define_MAUP_Message_Types(self):
		types = {
		  1 : "Data (DATA)",
		  2 : "Establish Request (ESTAB REQ)",
		  3 : "Establish Confirm (ESTAB CONF)",
		  4 : "Release Request (RELEASE REQ)",
		  5 : "Release Confirm (RELEASE CONF)",
		  6 : "Release Indication (RELEASE IND)",
		  7 : "State Request (STATE REQ)",
		  8 : "State Confirm (STATE CONF)",
		  9 : "State Indication (STATE IND)",
		  10 : "Data Retrieval Request (RETREIVAL REQ)",
		  11 : "Data Retrieval Confirm (RETREIVAL CONF)",
		  12 : "Data Retrieval Indication (RETREIVAL IND)",
		  13 : "Data Retrieval Complete Indication (RETREIVAL COMPL IND)",
		  14 : "Congestion Indication (CONGESTION IND)",
		  15 : "Data Acknowledge (DATA ACK)"
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
		  1 : "Notify (NOTIFY)"
		}
		return types

	def Define_IIM_Message_Types(self):
		types = {
		  1 : "Registration Request (REG REQ)",
		  2 : "Registration Response (REG RSP)",
		  3 : "Deregistration Request (DEREG REQ)",
		  4 : "Deregistration Response (DEREG RSP)"
		}
		return types

class M2UA_Parameter:

	def __init__(self, tag):
		self.tag = tag
		self.length = 8
		self.value = None

	def Define_Parameter_Tags(self):
		tags = {
		  1 : "Interface Identifier Integer",
		  3 : "Interface Identifier Text",
		  4 : "Info String",
		  7 : "Diagnostic Information",
		  8 : "Interface Identifier Integer Range",
		  9 : "Heartbeat Data",
		  11 : "Traffic Mode Type",
		  12 : "Error Code",
		  13 : "Status Type/Information",
		  17 : "ASP Identifier",
		  19 : "Correlation Id",
		  768 : "Protocol Data 1",
		  769 : "Protocol Data 2",
		  770 : "State",
		  771 : "Event",
		  772 : "Congestion Status",
		  773 : "Discard Status",
		  774 : "Action",
		  775 : "Sequence Number",
		  776 : "Retrieval Result",
		  777 : "Link Key",
		  778 : "Local-LK-Identifier",
		  779 : "Signalling Data Terminal Identifier",
		  780 : "Signalling Data Link Identifier",
		  781 : "Registration Result",
		  782 : "Registration Status",
		  783 : "De-Registration Result",
		  784 : "De-Registration Status"
		}
		return tags

	def Define_State_Parameter_Values(self):
		values = {
		  0 : "STATUS_LPO_SET",
		  1 : "STATUS_LPO_CLEAR",
		  2 : "STATUS_EMER_SET",
		  3 : "STATUS_EMER_CLEAR",
		  4 : "STATUS_FLUSH_BUFFERS",
		  5 : "STATUS_CONTINUE",
		  6 : "STATUS_CLEAR_RTB",
		  7 : "STATUS_AUDIT",
		  8 : "STATUS_CONG_CLEAR",
		  9 : "STATUS_CONG_ACCEPT",
		  10 : "STATUS_CONG_DISCARD"
		}
		return values

	def Define_Event_Parameter_Values(self):
		values = {
		  1 : "EVENT_RPO_ENTER",
		  2 : "EVENT_RPO_EXIT",
		  3 : "EVENT_LPO_ENTER",
		  4 : "EVENT_LPO_EXIT"
		}
		return values

	def Define_Congestion_And_Discard_Status_Values(self):
		values = {
		  0 : "LEVEL_NONE",
		  1 : "LEVEL_1",
		  2 : "LEVEL_2",
		  3 : "LEVEL_3"
		}
		return values

	def Define_Action_Values(self):
		values = {
		  1 : "ACTION_RTRV_BSN",
		  2 : "ACTION_RTRV_MSGS"
		}
		return values

	def Define_Result_Values(self):
		values = {
		  0 : "RESULT_SUCCESS",
		  1 : "RESULT_FAILURE"
		}
		return values

	def Define_Traffic_Mode_Type_Values(self):
		values = {
		  1 : "Override",
		  2 : "Load-share",
		  3 : "Broadcast"
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
		  13 : "Refused - Management Blocking",
		  14 : "ASP Identifier Required",
		  15 : "Invalid ASP Identifier",
		  16 : "ASP Active for Interface Identifier(s)",
		  17 : "Invalid Parameter Value",
		  18 : "Parameter Field Error",
		  19 : "Unexpected Parameter",
		  22 : "Missing Parameter"
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

	def Define_Registration_Status_Values(self):
		values = {
		  0 : "Successfully Registered",
		  1 : "Unknown",
		  2 : "Invalid SDLI",
		  3 : "Invalid SDTI",
		  4 : "Invalid Link Key",
		  5 : "Permission Denied",
		  6 : "Overlapping Link Key",
		  7 : "Link Key not Provisioned",
		  8 : "Insufficient Resources"
		}
		return values

	def Define_Deregistration_Status_Values(self):
		values = {
		  0 : "Successfully De-registered",
		  1 : "Unknown",
		  2 : "Invalid Interface Identifier",
		  3 : "Permission Denied",
		  4 : "Not Registered"
		}
		return values

"""class SCCP_Message_Parser:

	def __init__(self):
		pass

class ISUP_Message_Parser:

	def __init__(self):
		self.parameters_handlers = {
		  1 : self.IAM_Parameters_Handler,
		  2 : self.SAM_Parameters_Handler,
		  6 : self.ACM_Parameters_Handler,
		  9 : self.ANM_Parameters_Handler,
		  12 : self.REL_Parameters_Handler,
		  16 : self.RLC_Parameters_Handler,
		  17 : self.No_Parameters_Handler,
		  18 : self.No_Parameters_Handler,
		  19 : self.No_Parameters_Handler,
		  20 : self.No_Parameters_Handler,
		  21 : self.No_Parameters_Handler,
		  22 : self.No_Parameters_Handler,
		  23 : self.GRS_Parameters_Handler,
		  24 : self.CGx_Parameters_Handler,
		  25 : self.CGx_Parameters_Handler,
		  26 : self.CGx_Parameters_Handler,
		  27 : self.CGx_Parameters_Handler,
		  36 : self.No_Parameters_Handler,
		  41 : self.GRS_Parameters_Handler,
		  42 : self.GRS_Parameters_Handler,
		  46 : self.No_Parameters_Handler,
		  47 : self.CFN_Parameters_Handler,
		  48 : self.No_Parameters_Handler
		}

	def Get_Variable_Parameters(self, binary_data):
		try:
			number_of_pointers = binary_data[0]
		except IndexError:
			raise ISUP_Error("no pointers to parameters")
		if number_of_pointers == 1:
			#return [binary_data[1:]]
			return [binary_data[2:]]
		elif number_of_pointers == 0:
			return [b""]
		variable_parameters = []
		end_of_pointers = False
		pointers_counter = 0
		while not end_of_pointers:
			pointer = int.from_bytes(binary_data[pointers_counter : pointers_counter + 1], byteorder="big")
			#print("   -pointer:", pointer)
			length_position = pointers_counter + pointer
			length = binary_data[length_position]
			#print("   -length:", length)
			pointers_counter += 1
			if pointers_counter == number_of_pointers:
				if pointer == 0:
					value = b""
				else:
					value = binary_data[length_position:]
				variable_parameters.append(value)
				end_of_pointers = True
			else:
				value = binary_data[length_position + 1 : length_position + 1 + length]
				variable_parameters.append(value)
		return variable_parameters

	def IAM_Parameters_Handler(self, binary_data):
		pattern = struct.Struct("> B H B B")
		try:
			unpacked_data = pattern.unpack(binary_data[:5])
		except struct.error:
			raise ISUP_Error("invalid IAM fixed mandatory part")
		else:
			#Сборка обязательных фиксированных параметров
			connection_indicators = Nature_Of_Connection_Indicators(unpacked_data[0])
			#print("satellite_indicator:", connection_indicators.satellite_indicator)
			#print("continuity_check_indicator:", connection_indicators.continuity_check_indicator)
			#print("echo_control_device_indicator:", connection_indicators.echo_control_device_indicator)
			#print("spare:", connection_indicators.spare)
			forward_call_indicators = Forward_Call_Indicators(unpacked_data[1])
			#print("isdn_access_indicator:", forward_call_indicators.isdn_access_indicator)
			#print("sccp_method_indicator:", forward_call_indicators.sccp_method_indicator)
			#print("spare:", forward_call_indicators.spare)
			#print("for_national_use:", forward_call_indicators.for_national_use)
			#print("national_international_call_indicator:", forward_call_indicators.national_international_call_indicator)
			#print("end_to_end_method_indicator:", forward_call_indicators.end_to_end_method_indicator)
			#print("interworking_indicator:", forward_call_indicators.interworking_indicator)
			#print("end_to_end_information_indicator:", forward_call_indicators.end_to_end_information_indicator)
			#print("isdn_user_part_indicator:", forward_call_indicators.isdn_user_part_indicator)
			#print("isdn_user_part_preference_indicator:", forward_call_indicators.isdn_user_part_preference_indicator)
			calling_party_category = Calling_Party_Category(unpacked_data[2])
			transmission_medium_requirement = Transmission_Medium_Requirement(unpacked_data[3])
			#Сборка обязательных переменных параметров
			variable_parameters = self.Get_Variable_Parameters(binary_data[5:])
			called_party_number = Called_Party_Number().Build(variable_parameters[0])
			#Сборка опциональных параметров
			optional_parameters = self.Optional_Parameters_Handler(variable_parameters[1])
			#print("nature_of_address_indicator:", called_party_number.nature_of_address_indicator)
			#print("odd_even_indicator:", called_party_number.odd_even_indicator)
			#print("spare:", called_party_number.spare)
			#print("numbering_plan_indicator:", called_party_number.numbering_plan_indicator)
			#print("inn_indicator:", called_party_number.inn_indicator)
			#print("digits:", called_party_number.digits)
			#Формирование списков параметров
			mandatory_parameters = [connection_indicators, forward_call_indicators, calling_party_category, transmission_medium_requirement, called_party_number]
			return (mandatory_parameters, optional_parameters)

	def ACM_Parameters_Handler(self, binary_data):
		pattern = struct.Struct("> H")
		try:
			unpacked_data = pattern.unpack(binary_data[:2])
		except struct.error:
			raise ISUP_Error("invalid ACM fixed mandatory part")
		else:
			#Сборка обязательных фиксированных параметров
			backward_call_indicators = Backward_Call_Indicators(unpacked_data[0])
			#print("interworking_indicator:", backward_call_indicators.interworking_indicator)
			#print("end_to_end_information_indicator:", backward_call_indicators.end_to_end_information_indicator)
			#print("isdn_user_part_indicator:", backward_call_indicators.isdn_user_part_indicator)
			#print("holding_indicator:", backward_call_indicators.holding_indicator)
			#print("isdn_access_indicator:", backward_call_indicators.isdn_access_indicator)
			#print("echo_control_device_indicator:", backward_call_indicators.echo_control_device_indicator)
			#print("sccp_method_indicator:", backward_call_indicators.sccp_method_indicator)
			#print("charge_indicator:", backward_call_indicators.charge_indicator)
			#print("called_party_status_indicator:", backward_call_indicators.called_party_status_indicator)
			#print("called_party_category_indicator:", backward_call_indicators.called_party_category_indicator)
			#print("end_to_end_method_indicator:", backward_call_indicators.end_to_end_method_indicator)
			#Сборка опциональных параметров
			variable_parameters = self.Get_Variable_Parameters(binary_data[2:])
			optional_parameters = self.Optional_Parameters_Handler(variable_parameters[0])
			#Формирование списков параметров
			mandatory_parameters = [backward_call_indicators]
			return (mandatory_parameters, optional_parameters)

	def ANM_Parameters_Handler(self, binary_data):
		#Сообщение ANM не содержит обязательных параметров
		mandatory_parameters = []
		#Сборка опциональных параметров
		variable_parameters = self.Get_Variable_Parameters(binary_data)
		optional_parameters = self.Optional_Parameters_Handler(variable_parameters[0])
		return (mandatory_parameters, optional_parameters)

	def REL_Parameters_Handler(self, binary_data):
		#Сборка обязательных переменных параметров
		variable_parameters = self.Get_Variable_Parameters(binary_data)
		cause_indicators = Cause_Indicators().Build(variable_parameters[0])
		#print("location:", cause_indicators.location)
		#print("spare", cause_indicators.spare)
		#print("coding_standard:", cause_indicators.coding_standard)
		#print("cause_value:", cause_indicators.cause_value)
		#print("diagnostic:", cause_indicators.diagnostic)
		mandatory_parameters = [cause_indicators]
		#Сборка опциональных параметров
		optional_parameters = self.Optional_Parameters_Handler(variable_parameters[1])
		return (mandatory_parameters, optional_parameters)

	def RLC_Parameters_Handler(self, binary_data):
		#Сообщение RLC не содержит обязательных параметров
		mandatory_parameters = []
		#Сборка опциональных параметров
		variable_parameters = self.Get_Variable_Parameters(binary_data)
		optional_parameters = self.Optional_Parameters_Handler(variable_parameters[0])
		return (mandatory_parameters, optional_parameters)

	def GRS_Parameters_Handler(self, binary_data):
		#Сборка обязательных переменных параметров
		optional_parameters = list()
		variable_parameters = self.Get_Variable_Parameters(binary_data[0:])
		mandatory_parameters = Range_And_Status().Build(variable_parameters[0])
		return (mandatory_parameters, optional_parameters)

	def No_Parameters_Handler(self, binary_data):
		#Сборка обязательных переменных параметров
		optional_parameters = list()
		mandatory_parameters = list()
		return (mandatory_parameters, optional_parameters)

	def CGx_Parameters_Handler(self, binary_data):
		optional_parameters = list()
		pattern = struct.Struct("> B")
		try:
			unpacked_data = pattern.unpack(binary_data[:1])
		except struct.error:
			raise ISUP_Error("invalid CGU fixed mandatory part")
		else:
			#Сборка обязательных фиксированных параметров
			circuit_group_supervision_message_type_indicators = Circuit_Group_Supervision_Message_Type(unpacked_data[0])
			variable_parameters = self.Get_Variable_Parameters(binary_data[1:])
			range_and_status = Range_And_Status().Build(variable_parameters[0])
		mandatory_parameters = [circuit_group_supervision_message_type_indicators, range_and_status]
		return (mandatory_parameters, optional_parameters)

	def CFN_Parameters_Handler(self, binary_data):
		#Сборка обязательных переменных параметров
		variable_parameters = self.Get_Variable_Parameters(binary_data)
		cause_indicators = Cause_Indicators().Build(variable_parameters[0])
		#print("location:", cause_indicators.location)
		#print("spare", cause_indicators.spare)
		#print("coding_standard:", cause_indicators.coding_standard)
		#print("cause_value:", cause_indicators.cause_value)
		#print("diagnostic:", cause_indicators.diagnostic)
		mandatory_parameters = [cause_indicators]
		#Сборка опциональных параметров
		optional_parameters = self.Optional_Parameters_Handler(variable_parameters[1])
		return (mandatory_parameters, optional_parameters)

	def SAM_Parameters_Handler(self, binary_data):
		#Сборка обязательных переменных параметров
		variable_parameters = self.Get_Variable_Parameters(binary_data)
		subsequent_number = Subsequent_Number().Build(variable_parameters[0])
		#print("#----------------------------------------#")
		#print("    spare:", subsequent_number.spare)
		#print("    odd_even_indicator:", subsequent_number.odd_even_indicator)
		#print("    digits:", subsequent_number.digits)
		#print("#----------------------------------------#")
		mandatory_parameters = [subsequent_number]
		#Сборка опциональных параметров
		optional_parameters = self.Optional_Parameters_Handler(variable_parameters[1])
		return (mandatory_parameters, optional_parameters)

	def Optional_Parameters_Handler(self, binary_data):
		return binary_data

	def Add_Bit_Paddings(self, bin_value):
		end_of_padding = False
		while not end_of_padding:
			if len(bin_value) != 8:
				bin_value = "0" + bin_value
			else:
				end_of_padding = True
		return bin_value

	def Parse_CIC_Value(self, cic_bytes):
		byte1 = bin(int.from_bytes(cic_bytes[:1], byteorder="big"))[2:]
		byte2 = bin(int.from_bytes(cic_bytes[1:], byteorder="big"))[2:]
		byte1 = self.Add_Bit_Paddings(byte1)
		cic_value = int((byte2 + byte1), 2)
		return cic_value

	def Parse_Protocol_Data(self, binary_data):
		#Извлечение значений cic и message type
		cic = self.Parse_CIC_Value(binary_data[:2])
		mes_type = int.from_bytes(binary_data[2:3], byteorder="big")
		#Создание объекта isup
		isup_data = isup.ISUP_Data(cic=cic, mes_type=mes_type)
		#Обработка параметров сообщения
		try:
			isup_data.mandatory_parameters, isup_data.optional_parameters = self.parameters_handlers[mes_type](binary_data[3:])
		except KeyError:
			raise ISUP_Error("unknown or unsupported message type: \"%s\"" % mes_type)
		else:
			return isup_data
"""

class Binary_Convertor:

	def __init__(self):
		self.isup_bin_conv = isup.Binary_Convertor() 
		self.common_m2ua_header_pattern = struct.Struct(">B B B B L")
		self.m2ua_parameter_header_pattern = struct.Struct(">H H")
		self.m2ua_padding_parameter_pattern = struct.Struct(">B")
		self.mtp3_routing_label_pattern = struct.Struct(">B B B B")
		self.m2ua_parameter_header_length = 4
		self.m2ua_header_length = 8
#		self.mtp3_data_length = 5

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

	def Create_M2UA_Parameter_Padding(self, padding_bytes_number):
		padding_value = (0)
		padding_byte = self.m2ua_padding_parameter_pattern.pack(padding_value)
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
			raise M2UA_Error("padding bytes counting error")
		return multiple_length

	def Forming_M2UA_Parameter_Padding(self, parameter_length):
		if parameter_length % 4 == 0:
			return b""
		else:
			multiple_length = self.Searching_For_Multiple_Length(parameter_length)
			padding_bytes_number = multiple_length - parameter_length
			padding = self.Create_M2UA_Parameter_Padding(padding_bytes_number)
			return padding

	def String_Parameter_Length_Check(self, string_parameter_value, parameter_length):
		if len(string_parameter_value) != parameter_length - self.m2ua_parameter_header_length:
			raise M2UA_Error("m2ua str parameter length \"%s\" is bigger than allowable length" % len(string_parameter_value))

	def Convert_String_Parameter_Value(self, parameter_value, parameter_length=None):
		binary_parameter_value = parameter_value.encode("utf-8")
		if parameter_length:
			binary_parameter_length = parameter_length
			self.String_Parameter_Length_Check(binary_parameter_value, parameter_length)
		else:
			binary_parameter_length = len(binary_parameter_value) + self.m2ua_parameter_header_length
		return (binary_parameter_value, binary_parameter_length)

	def Convert_Int_Parameter_Value(self, parameter_value, parameter_length=None):
		if parameter_length:
			binary_parameter_length = parameter_length
			try:
				binary_parameter_value = parameter_value.to_bytes(parameter_length - self.m2ua_parameter_header_length, byteorder="big")
			except OverflowError:
				raise M2UA_Error("m2ua int parameter value is \"%s\" is bigger than allowable value"% parameter_value)
		else:
			value_length = self.Bytes_Number_Counting(parameter_value)
			binary_parameter_value = parameter_value.to_bytes(value_length, byteorder="big")
			binary_parameter_length = value_length + self.m2ua_parameter_header_length
		return (binary_parameter_value, binary_parameter_length)

	def Convert_List_Parameter_Value(self, parameters_list):
		total_parameter_length = self.m2ua_parameter_header_length
		total_binary_parameter_value = b""
		for parameter in parameters_list:
			if type(parameter) == int:
				binary_parameter_value, dummy = self.Convert_Int_Parameter_Value(parameter, parameter_length=8)
				total_binary_parameter_value = total_binary_parameter_value + binary_parameter_value
				total_parameter_length = total_parameter_length + 4
			elif type(parameter) == M2UA_Parameter:
				binary_parameter, binary_parameter_length = self.Convert_M2UA_Parameter(parameter)
				total_binary_parameter_value = total_binary_parameter_value + binary_parameter
				total_parameter_length = total_parameter_length + binary_parameter_length
			else:
				raise M2UA_Error("unsupported element type in parameters list")
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

	def M2UA_Parameter_Forming(self, parameter_value, parameter_length=None):
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
			raise M2UA_Error("unsupported type of m2ua parameter")
		return (binary_parameter_value, binary_parameter_length)

	def Convert_M2UA_Parameter_Value(self, object_parameter):
		if not object_parameter.length:
			binary_parameter_value, parameter_length = self.M2UA_Parameter_Forming(object_parameter.value)
		elif object_parameter.length < 4:
			raise M2UA_Error("m2ua parameter length must not be less than 4")
		elif object_parameter.length == 4:
			binary_parameter_value = b""
			parameter_length = object_parameter.length
		else:
			binary_parameter_value, parameter_length = self.M2UA_Parameter_Forming(object_parameter.value, object_parameter.length)
		return (binary_parameter_value, parameter_length)

	def Convert_M2UA_Parameter(self, object_parameter): 
		binary_parameter_value, parameter_length = self.Convert_M2UA_Parameter_Value(object_parameter)
		packet_values = (object_parameter.tag, parameter_length)
		binary_parameter_header = self.m2ua_parameter_header_pattern.pack(*packet_values)
		padding = self.Forming_M2UA_Parameter_Padding(parameter_length)
		binary_parameter = binary_parameter_header + binary_parameter_value + padding
		return (binary_parameter, parameter_length + len(padding))

	def Get_M2UA_Parameters_Info(self, object_message):
		parameters_length = 0
		binary_parameters_list = []
		for parameter in object_message.parameters:
			binary_parameter, parameter_length = self.Convert_M2UA_Parameter(parameter)
			binary_parameters_list.append(binary_parameter)
			parameters_length = parameters_length + parameter_length
		return (binary_parameters_list, parameters_length)

	def Get_M2UA_Parameters_String(self, parameters_list):
		parameters_string = b""
		for parameter in parameters_list:
			parameters_string = parameters_string + parameter
		return parameters_string 

	def Convert_M2UA_Message(self, object_message):
		binary_parameters_list, parameters_length = self.Get_M2UA_Parameters_Info(object_message)
		object_message.length = self.m2ua_header_length + parameters_length 
		packet_values = (object_message.version, object_message.spare, object_message.mes_class, object_message.mes_type, object_message.length)
		m2ua_header = self.common_m2ua_header_pattern.pack(*packet_values)
		m2ua_parameters = self.Get_M2UA_Parameters_String(binary_parameters_list)
		m2ua_message = m2ua_header + m2ua_parameters
		return m2ua_message

class Message_Builder:

	def __init__(self):
		self.isup_bld = isup.Message_Builder()
#		self.mtp3 = None
		self.convertor = Binary_Convertor()

	def _M2ua_make_message_handler(self):
		return { "ESTAB_REQ" : self.Build_Establish_Request,
				 "ESTAB_CONF" : self.Build_Establish_Confirmation,
				 "DATA_ACK" : self.Build_Data_Acknowledge,
				 "STATE_REQ" : self.Build_State_Request,
				 "STATE_CONF" : self.Build_State_Confirm,
				 "STATE_IND" : self.Build_State_Indication,
				 "CONGESTION_IND" : self.Build_Congestion_Indication,
				 "RETREIVAL_REQ" : self.Build_Data_Retrieval_Request,
				 "RETREIVAL_CONF" : self.Build_Data_Retrieval_Confirm,
				 "RETREIVAL_IND" : self.Build_Data_Retrieval_Indication,
				 "RETREIVAL_COMPL_IND" : self.Build_Data_Retrieval_Complete_Indication,
				 "RELEASE_REQ" : self.Build_Release_Request,
				 "RELEASE_CONF" : self.Build_Release_Confirmation,
				 "RELEASE_IND" : self.Build_Release_Indication,
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
				 "REG_REQ" : self.Build_REG_REQ_Message,
				 "REG_RSP" : self.Build_REG_RSP_Message,
				 "DEREG_REQ" : self.Build_DEREG_REQ_Message,
				 "DEREG_RSP" : self.Build_DEREG_RSP_Message,
				 "DATA" : self.Build_DATA_Message }

	def Get_M2UA_Parameter_Info(self, object_parameter):
		if object_parameter.tag == 11:
			parameter_info = object_parameter.Define_Traffic_Mode_Type_Values()
			return (parameter_info, "traffic mode type")
		elif object_parameter.tag == 12:
			parameter_info = object_parameter.Define_Error_Code_Values()
			return (parameter_info, "error code")
		elif object_parameter.tag == 13:
			parameter_info = object_parameter.Define_Status_Type_Values()
			return (parameter_info, "status type")
		elif object_parameter.tag == 770:
			parameter_info = object_parameter.Define_State_Parameter_Values()
			return (parameter_info, "state")
		elif object_parameter.tag == 771:
			parameter_info = object_parameter.Define_Event_Parameter_Values()
			return (parameter_info, "event")
		elif object_parameter.tag == 772:
			parameter_info = object_parameter.Define_Congestion_And_Discard_Status_Values()
			return (parameter_info, "congestion status")
		elif object_parameter.tag == 773:
			parameter_info = object_parameter.Define_Congestion_And_Discard_Status_Values()
			return (parameter_info, "discard status")
		elif object_parameter.tag == 774:
			parameter_info = object_parameter.Define_Action_Values()
			return (parameter_info, "action")
		elif object_parameter.tag == 776:
			parameter_info = object_parameter.Define_Result_Values()
			return (parameter_info, "result")
		elif object_parameter.tag == 782:
			parameter_info = object_parameter.Define_Registration_Status_Values()
			return (parameter_info, "registration status")
		elif object_parameter.tag == 784:
			parameter_info = object_parameter.Define_Deregistration_Status_Values()
			return (parameter_info, "deregistration status")
		else:
			raise M2UA_Error("m2ua parameter tag \"%s\" does not support" % object_parameter.tag)

	def Get_Parameter_Value(self, object_parameter, parameter_definition):
		parameter_values, parameter_name = self.Get_M2UA_Parameter_Info(object_parameter)
		if type(parameter_definition) == int:
			for parameter_number in parameter_values.keys():
				if parameter_definition == parameter_number:
					break
			else:
				raise M2UA_Error("\"%s\" is unknown m2ua %s parameter value" % (parameter_definition, parameter_name))
			return parameter_definition
		elif type(parameter_definition) == str:
			for parameter_number, parameter_description in parameter_values.items():
				if parameter_definition.lower().replace(" ", "_") == parameter_description.lower().replace(" ", "_"):
					parameter_value = parameter_number
					break
			else:
				raise M2UA_Error("\"%s\" is unknown m2ua %s parameter value" % (parameter_definition, parameter_name))
			return parameter_value
		else:
			raise M2UA_Error("m2ua %s parameter must be int or str" % parameter_name)

	def Generate_Correlation_Id(self):
		correlation_id_value = random.randint(1,math.pow(2,32))
		return correlation_id_value

	def Build_State_Parameter(self, state_definition):
		state = M2UA_Parameter(tag=770)
		state.value = self.Get_Parameter_Value(state, state_definition)
		return state

	def Build_Event_Parameter(self, event_definition):
		event = M2UA_Parameter(tag=771)
		event.value = self.Get_Parameter_Value(event, event_definition)
		return event

	def Build_Result_Parameter(self, result_definition):
		result = M2UA_Parameter(tag=776)
		result.value = self.Get_Parameter_Value(result, result_definition)
		return result

	def Build_Action_Parameter(self, action_definition):
		action = M2UA_Parameter(tag=774)
		action.value = self.Get_Parameter_Value(action, action_definition)
		return action

	def Build_Sequence_Number_Parameter(self, sequence_number_definition):
		sequence_number = M2UA_Parameter(tag=775)
		if type(sequence_number_definition) == int:
			sequence_number.value = sequence_number_definition
			return sequence_number
		else:
			raise M2UA_Error("m2ua sequence number parameter must be int")

	def Build_Congestion_Status_Parameter(self, congestion_status_definition):
		congestion_status = M2UA_Parameter(tag=772)
		congestion_status.value = self.Get_Parameter_Value(congestion_status, congestion_status_definition)
		return congestion_status

	def Build_Discard_Status_Parameter(self, discard_status_definition):
		discard_status = M2UA_Parameter(tag=773)
		discard_status.value = self.Get_Parameter_Value(discard_status, discard_status_definition)
		return discard_status

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
				raise M2UA_Error("\"%s\" is unknown m2ua status information parameter value of status type \"%s\"" % (status_information, status_type))
			return status_information
		elif type(status_information) == str:
			for parameter_number, parameter_description in status_information_values.items():
				if status_information.lower().replace(" ", "_") == parameter_description.lower().replace(" ", "_"):
					parameter_value = parameter_number
					break
			else:
				raise M2UA_Error("\"%s\" is unknown m2ua status information parameter value of status type \"%s\"" % (status_information, status_type))
			return parameter_value
		else:
			raise M2UA_Error("m2ua status information parameter must be int or str")

	def Composite_Parameter_Value_Forming(self, first_value, second_value):
		binary_first_value = self.convertor.Convert_Int_To_Bytes(int_value=first_value, bytes_number=2)
		binary_second_value = self.convertor.Convert_Int_To_Bytes(int_value=second_value, bytes_number=2)
		binary_composite_value = binary_first_value + binary_second_value
		composite_value = self.convertor.Convert_Bytes_To_Int(binary_composite_value)
		return composite_value

	def Build_Status_Parameter(self, status_type_definition, status_information_definition):
		status = M2UA_Parameter(tag=13)
		status_type = self.Get_Parameter_Value(status, status_type_definition)
		status_information = self.Get_Status_Information_Value(status, status_type, status_information_definition)
		status.value = self.Composite_Parameter_Value_Forming(status_type, status_information)
		return status

	def Build_Correlation_Id_Parameter(self, cid=None):
		correlation_id = M2UA_Parameter(tag=19)
		if cid:
			correlation_id.value = cid
		else:
			correlation_id.value = self.Generate_Correlation_Id()
		return correlation_id

	def Build_Deregistration_Status_Parameter(self, deregistration_status_definition):
		deregistration_status = M2UA_Parameter(tag=784)
		deregistration_status.value = self.Get_Parameter_Value(deregistration_status, deregistration_status_definition)
		return deregistration_status

	def Build_Registration_Status_Parameter(self, registration_status_definition):
		registration_status = M2UA_Parameter(tag=782)
		registration_status.value = self.Get_Parameter_Value(registration_status, registration_status_definition)
		return registration_status

	def Build_Signalling_Data_Link_Identifier(self, link_identifier_definition):
		link_identifier = M2UA_Parameter(tag=780)
		if type(link_identifier_definition) == int:
			link_identifier.value = self.Composite_Parameter_Value_Forming(0, link_identifier_definition)
			return link_identifier
		else:
			raise M2UA_Error("m2ua sdl identifier parameter must be int")

	def Build_Signalling_Data_Terminal_Identifier_Parameter(self, terminal_identifier_definition):
		terminal_identifier = M2UA_Parameter(tag=779)
		if type(terminal_identifier_definition) == int:
			terminal_identifier.value = self.Composite_Parameter_Value_Forming(0, terminal_identifier_definition)
			return terminal_identifier
		else:
			raise M2UA_Error("m2ua sdt identifier parameter must be int")

	def Build_Local_LK_Identifier_Parameter(self, local_lk_identifier_definition):
		local_lk_identifier = M2UA_Parameter(tag=778)
		if type(local_lk_identifier_definition) == int:
			local_lk_identifier.value = local_lk_identifier_definition
			return local_lk_identifier
		else:
			raise M2UA_Error("m2ua local lk identifier parameter must be int")

	def Composite_Parameters_List_Check(self, parameters_list, argument_name, elements_number=3):
		if type(parameters_list) != list:
			raise M2UA_Error("%s argument must be list" % argument_name)
		elif len(parameters_list) == 0:
			raise M2UA_Error("%s argument must not be empty" % argument_name)
		else:
			for element in parameters_list:
				if type(element) != tuple:
					raise M2UA_Error("wrong element type in %s argument" % argument_name)
				elif len(element) != elements_number:
					raise M2UA_Error("%s must be described by %s elements in tuple" % (argument_name, elements_number))

	def Build_Link_Key_Parameters(self, link_keys_definition):
		self.Composite_Parameters_List_Check(link_keys_definition, "link_keys")
		link_keys_list = []
		for parameter in link_keys_definition:
			link_key = M2UA_Parameter(tag=777)
			link_key.length = None
			link_key_identifiers_list = []
			local_lk_identifier = self.Build_Local_LK_Identifier_Parameter(parameter[0])
			link_key_identifiers_list.append(local_lk_identifier)
			terminal_identifier = self.Build_Signalling_Data_Terminal_Identifier_Parameter(parameter[1])
			link_key_identifiers_list.append(terminal_identifier)
			link_identifier = self.Build_Signalling_Data_Link_Identifier(parameter[2])
			link_key_identifiers_list.append(link_identifier)
			link_key.value = link_key_identifiers_list
			link_keys_list.append(link_key)
		return link_keys_list

	def Build_Deregistration_Result_Parameters(self, deregistration_results_definition):
		self.Composite_Parameters_List_Check(deregistration_results_definition, "deregistration_results", elements_number=2)
		results_list = []
		for parameter in deregistration_results_definition:
			dereg_result = M2UA_Parameter(tag=783)
			dereg_result.length = None
			dereg_result_list = []
			if type(parameter[0]) == int:
				interface_identifier = self.Build_Int_Interface_Identifier_Parameter(parameter[0])
			elif type(parameter[0]) == str:
				interface_identifier = self.Build_Str_Interface_Identifier_Parameter(parameter[0])
			else:
				raise M2UA_Error("unsupported value type in interface_identifier argument")
			dereg_result_list.append(interface_identifier)
			deregistration_status = self.Build_Deregistration_Status_Parameter(parameter[1])
			dereg_result_list.append(deregistration_status)
			dereg_result.value = dereg_result_list
			results_list.append(dereg_result)
		return results_list

	def Build_Registration_Result_Parameters(self, registration_results_definition):
		self.Composite_Parameters_List_Check(registration_results_definition, "registration_results")
		results_list = []
		for parameter in registration_results_definition:
			reg_result = M2UA_Parameter(tag=781)
			reg_result.length = None
			reg_result_list = []
			local_lk_identifier = self.Build_Local_LK_Identifier_Parameter(parameter[0])
			reg_result_list.append(local_lk_identifier)
			registration_status = self.Build_Registration_Status_Parameter(parameter[1])
			reg_result_list.append(registration_status)
			if type(parameter[2]) == int:
				interface_identifier = self.Build_Int_Interface_Identifier_Parameter(parameter[2])
			elif type(parameter[2]) == str:
				interface_identifier = self.Build_Str_Interface_Identifier_Parameter(parameter[2])
			else:
				raise M2UA_Error("unsupported value type in interface_identifier argument")
			reg_result_list.append(interface_identifier)
			reg_result.value = reg_result_list
			results_list.append(reg_result)
		return results_list

	def Build_Diagnostic_Information_Parameter(self, diagnostic_information_definition):
		diagnostic_information = M2UA_Parameter(tag=7)
		diagnostic_information.length = None
		if type(diagnostic_information_definition) == int or type(diagnostic_information_definition) == str:
			diagnostic_information.value = diagnostic_information_definition
			return diagnostic_information
		else:
			raise M2UA_Error("m2ua diagnostic information parameter must be int or str")

	def Build_Info_String_Parameter(self, info_string_definition):
		info_string = M2UA_Parameter(tag=4)
		info_string.length = None
		if type(info_string_definition) == str:
			info_string.value = info_string_definition
			return info_string
		else:
			raise M2UA_Error("m2ua info string parameter must be str")

	def Build_ASP_Identifier_Parameter(self, asp_identifier_definition):
		asp_identifier = M2UA_Parameter(tag=17)
		if type(asp_identifier_definition) == int:
			asp_identifier.value = asp_identifier_definition
			return asp_identifier
		else:
			raise M2UA_Error("m2ua asp identifier parameter must be int")

	def Build_Heartbeat_Data_Parameter(self, heartbeat_data_definition):
		heartbeat_data = M2UA_Parameter(tag=9)
		heartbeat_data.length = None
		if type(heartbeat_data_definition) == str or type(heartbeat_data_definition) == int:
			heartbeat_data.value = heartbeat_data_definition
			return heartbeat_data
		else:
			raise M2UA_Error("m2ua heartbeat data parameter must be int or str")

	def Tuples_To_List_Distribution(self, tuples_list):
		array = []
		for element in tuples_list:
			for value in element:
				array.append(value)
		return array

	def Interface_Identifiers_Range_Check(self, identifiers_range):
		if len(identifiers_range) != 2:
			raise M2UA_Error("identifier range must be described only by start and stop identifiers in list")
		else:
			for identifier in identifiers_range:
				if type(identifier) != int:
					raise M2UA_Error("identifier range must consist only of int identifiers")

	def Interface_Identifiers_List_Check(self, interface_identifiers_list):
		if type(interface_identifiers_list) != list:
			raise M2UA_Error("interface_identifiers argument must be list")
		else:
			first_permitted_type = type(interface_identifiers_list[0])
			if first_permitted_type == int:
				second_permitted_type = list #tuple
			elif first_permitted_type == list: #tuple:
				second_permitted_type = int
			elif first_permitted_type == str:
				second_permitted_type = str
			else:
				raise M2UA_Error("wrong identifier type in interface_identifiers argument")
			for identifier in interface_identifiers_list:
				if type(identifier) != first_permitted_type and type(identifier) != second_permitted_type:
					raise M2UA_Error("incorrect identifier in interface_identifiers argument")
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
		interface_identifier = M2UA_Parameter(tag=1)
		interface_identifier.value = interface_identifier_value
		return interface_identifier

	def Build_Int_Range_Interface_Identifier_Parameter(self, interface_identifier_value):
		interface_identifier = M2UA_Parameter(tag=8)
		interface_identifier.length = None
		interface_identifier.value = interface_identifier_value
		return interface_identifier

	def Build_Str_Interface_Identifier_Parameter(self, interface_identifier_value):
		interface_identifier = M2UA_Parameter(tag=3)
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
			raise M2UA_Error("interface_identifiers argument elements must be int or str")

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
		traffic_mode_type = M2UA_Parameter(tag=11)
		traffic_mode_type.value = self.Get_Parameter_Value(traffic_mode_type, traffic_mode_type_definition)
		return traffic_mode_type

	def Build_Error_Code_Parameter(self, error_code_definition):
		error_code = M2UA_Parameter(tag=12)
		error_code.value = self.Get_Parameter_Value(error_code, error_code_definition)
		return error_code

	def Build_TTC_Protocol_Data_Parameter(self):
		ttc_protocol_data = M2UA_Parameter(tag=769)
		ttc_protocol_data.length = None
		ttc_protocol_data.value = None
		return ttc_protocol_data

	def Build_DATA_Message(self, protocol_data_1, interface_identifiers=[], message_class=6, message_type=1, version=1):
		ISUP_handler = self.isup_bld._MTP3_ISUP_make_message_handler()
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers, without_int_range=True)
		object_message.parameters = interface_identifiers_list
		protocol_data = M2UA_Parameter(tag=768)
		protocol_data.length = None
		protocol_data.value = ISUP_handler[protocol_data_1["message"]][0](ISUP_handler[protocol_data_1["message"]][1], protocol_data_1)
		object_message.parameters.append(protocol_data)
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_Establish_Request(self, interface_identifiers=[], message_class=6, message_type=2, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_Establish_Confirmation(self, interface_identifiers=[], message_class=6, message_type=3, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_Data_Acknowledge(self, correlation_id, interface_identifiers=[], message_class=6, message_type=15, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
		correlation_id = self.Build_Correlation_Id_Parameter(cid=correlation_id)
		object_message.parameters.append(correlation_id)
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_State_Request(self, state, interface_identifiers=[], message_class=6, message_type=7, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
		state = self.Build_State_Parameter(state)
		object_message.parameters.append(state)
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_State_Confirm(self, state, interface_identifiers=[], message_class=6, message_type=8, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
		state = self.Build_State_Parameter(state)
		object_message.parameters.append(state)
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_State_Indication(self, event, interface_identifiers=[], message_class=6, message_type=9, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
		event = self.Build_Event_Parameter(event)
		object_message.parameters.append(event)
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_Congestion_Indication(self, congestion_status, interface_identifiers=[], discard_status=None, message_class=6, message_type=14, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
		congestion_status = self.Build_Congestion_Status_Parameter(congestion_status)
		object_message.parameters.append(congestion_status)
		if discard_status:
			discard_status = self.Build_Discard_Status_Parameter(discard_status)
			object_message.parameters.append(discard_status)
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_Data_Retrieval_Request(self, action, interface_identifiers=[], sequence_number=None, message_class=6, message_type=10, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
		action = self.Build_Action_Parameter(action)
		object_message.parameters.append(action)
		if sequence_number:
			sequence_number = self.Build_Sequence_Number_Parameter(sequence_number)
			object_message.parameters.append(sequence_number)
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_Data_Retrieval_Confirm(self, action, result, interface_identifiers=[], sequence_number=None, message_class=6, message_type=11, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
		action = self.Build_Action_Parameter(action)
		object_message.parameters.append(action)
		result = self.Build_Result_Parameter(result)
		object_message.parameters.append(result)
		if sequence_number:
			sequence_number = self.Build_Sequence_Number_Parameter(sequence_number)
			object_message.parameters.append(sequence_number)
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_Data_Retrieval_Indication(self, interface_identifiers=[], message_class=6, message_type=12, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_Data_Retrieval_Complete_Indication(self, interface_identifiers=[], message_class=6, message_type=13, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_Release_Request(self, interface_identifiers=[], message_class=6, message_type=4, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_Release_Confirmation(self, interface_identifiers=[], message_class=6, message_type=5, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_Release_Indication(self, interface_identifiers=[], message_class=6, message_type=6, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_ASP_UP_Message(self, asp_identifier=None, info_string=None, message_class=3, message_type=1, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		if asp_identifier:
			asp_identifier = self.Build_ASP_Identifier_Parameter(asp_identifier)
			object_message.parameters.append(asp_identifier)
		if info_string:
			info_string = self.Build_Info_String_Parameter(info_string)
			object_message.parameters.append(info_string)
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_ASP_UP_ACK_Message(self, info_string=None, message_class=3, message_type=4, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		if info_string:
			info_string = self.Build_Info_String_Parameter(info_string)
			object_message.parameters.append(info_string)
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_ASP_DOWN_Message(self, info_string=None, message_class=3, message_type=2, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		if info_string:
			info_string = self.Build_Info_String_Parameter(info_string)
			object_message.parameters.append(info_string)
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_ASP_DOWN_ACK_Message(self, info_string=None, message_class=3, message_type=5, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		if info_string:
			info_string = self.Build_Info_String_Parameter(info_string)
			object_message.parameters.append(info_string)
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_BEAT_Message(self, heartbeat_data=None, message_class=3, message_type=3, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		if heartbeat_data:
			heartbeat_data = self.Build_Heartbeat_Data_Parameter(heartbeat_data)
			object_message.parameters.append(heartbeat_data)
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_BEAT_ACK_Message(self, heartbeat_data=None, message_class=3, message_type=6, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		if heartbeat_data:
			heartbeat_data = self.Build_Heartbeat_Data_Parameter(heartbeat_data)
			object_message.parameters.append(heartbeat_data)
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_ASP_ACTIVE_Message(self, traffic_mode_type=None, interface_identifiers=[], info_string=None, message_class=4, message_type=1, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
		if traffic_mode_type:
			traffic_mode_type = self.Build_Traffic_Mode_Type_Parameter(traffic_mode_type)
			object_message.parameters.append(traffic_mode_type)
		if info_string:
			info_string = self.Build_Info_String_Parameter(info_string)
			object_message.parameters.append(info_string)
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_ASP_ACTIVE_ACK_Message(self, traffic_mode_type=None, interface_identifiers=[], info_string=None, message_class=4, message_type=3, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
		if traffic_mode_type:
			traffic_mode_type = self.Build_Traffic_Mode_Type_Parameter(traffic_mode_type)
			object_message.parameters.append(traffic_mode_type)
		if info_string:
			info_string = self.Build_Info_String_Parameter(info_string)
			object_message.parameters.append(info_string)
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_ASP_INACTIVE_Message(self, interface_identifiers=[], info_string=None, message_class=4, message_type=2, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
		if info_string:
			info_string = self.Build_Info_String_Parameter(info_string)
			object_message.parameters.append(info_string)
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_ASP_INACTIVE_ACK_Message(self, interface_identifiers=[], info_string=None, message_class=4, message_type=4, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
		if info_string:
			info_string = self.Build_Info_String_Parameter(info_string)
			object_message.parameters.append(info_string)
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_ERR_Message(self, error_code, interface_identifiers=[], diagnostic_information=None, message_class=0, message_type=0, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
		error_code = self.Build_Error_Code_Parameter(error_code)
		object_message.parameters.append(error_code)
		if diagnostic_information:
			diagnostic_information = self.Build_Diagnostic_Information_Parameter(diagnostic_information)
			object_message.parameters.append(diagnostic_information)
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_NTFY_Message(self, status_type, status_information, asp_identifier=None, interface_identifiers=[], info_string=None, 
		                                                                               message_class=0, message_type=1, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		if interface_identifiers:
			interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers)
			object_message.parameters = interface_identifiers_list
		status = self.Build_Status_Parameter(status_type, status_information)
		object_message.parameters.append(status)
		if asp_identifier:
			asp_identifier = self.Build_ASP_Identifier_Parameter(asp_identifier)
			object_message.parameters.append(asp_identifier)
		if info_string:
			info_string = self.Build_Info_String_Parameter(info_string)
			object_message.parameters.append(info_string)
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_REG_REQ_Message(self, link_keys, message_class=10, message_type=1, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		link_keys_list = self.Build_Link_Key_Parameters(link_keys)
		object_message.parameters = link_keys_list
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_REG_RSP_Message(self, registration_results, message_class=10, message_type=2, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		registration_results_list = self.Build_Registration_Result_Parameters(registration_results)
		object_message.parameters = registration_results_list
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_DEREG_REQ_Message(self, interface_identifiers, message_class=10, message_type=3, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		interface_identifiers_list = self.Build_Interface_Identifier_Parameters(interface_identifiers, without_int_range=True)
		object_message.parameters = interface_identifiers_list
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

	def Build_DEREG_RSP_Message(self, deregistration_results, message_class=10, message_type=4, version=1):
		object_message = M2UA_Message(int(message_class), int(message_type), int(version))
		deregistration_results_list = self.Build_Deregistration_Result_Parameters(deregistration_results)
		object_message.parameters = deregistration_results_list
		binary_message = self.convertor.Convert_M2UA_Message(object_message)
		return binary_message

class Message_Parser:

	def __init__(self):
		self.sccp_parser = isup.SCCP_Message_Parser()
		self.isup_parser = isup.ISUP_Message_Parser()
		self.common_m2ua_header_pattern = struct.Struct(">B B B B L")
		self.m2ua_parameter_header_pattern = struct.Struct(">H H")

		
#		self.sio_network_indicator_mask = 0b11000000
#		self.sio_spare_mask = 0b00110000
#		self.sio_service_indicator_mask = 0b00001111
#		self.routing_label_dpc_mask = 16383
#		self.routing_label_opc_mask = 268419072
#		self.routing_label_link_selector_mask = 4026531840


	def Define_M2UA_Parameter_Handlers(self):
		handlers = {
		  (1,11,12,13,17,19,770,771,772,773,774,775,776,778,779,780,782,784) : self.Int_M2UA_Parameter_Value_Handling,
		  (3,4) : self.Str_M2UA_Parameter_Value_Handling,
		  (8,) : self.Int_Range_M2UA_Parameter_Value_Handling,
		  (7,9) : self.Polymorphic_M2UA_Parameter_Value_Handling,
		  (768,) : self.M2UA_Protocol_Data_Handling,
		  (769,) : self.M2UA_TTC_Protocol_Data_Handling,
		  (777,781,783) : self.M2UA_Composite_Parameters_Handling
		}
		return handlers

#	def Define_Service_Data_Handlers(self):
#		handlers = {
#		  3 : self.SCCP_Data_Forming,
#		  5 : self.ISUP_Data_Forming
#		}
#		return handlers

	def Get_M2UA_Class_Description(self, object_message):
		classes = object_message.Define_Message_Classes()
		for class_number,description in classes.items():
		    if object_message.mes_class == class_number:
		    	class_description = description
		    	break
		else:
			raise M2UA_Error("m2ua class \"%s\" does not supported" % object_message.mes_class)
		return class_description

	def Get_M2UA_Message_Types(self, object_message):
		if object_message.mes_class == 0:
			message_types = object_message.Define_MGMT_Message_Types()
		elif object_message.mes_class == 3:
			message_types = object_message.Define_ASPSM_Message_Types()
		elif object_message.mes_class == 4:
			message_types = object_message.Define_ASPTM_Message_Types()
		elif object_message.mes_class == 6:
			message_types = object_message.Define_MAUP_Message_Types()
		elif object_message.mes_class == 10:
			message_types = object_message.Define_IIM_Message_Types()
		else:
			raise M2UA_Error("m2ua class \"%s\" does not supported" % object_message.mes_class)
		return message_types

	def Get_M2UA_Parameter_Tags(self, m2ua_parameter):
		return m2ua_parameter.Define_Parameter_Tags()

	def Get_M2UA_Type_Description(self, object_message):
		message_types = self.Get_M2UA_Message_Types(object_message)
		for type_number, description in message_types.items():
			if object_message.mes_type == type_number:
				type_description = description
				break
		else:
			raise M2UA_Error("\"%s\" is unknown m2ua message type" % object_message.mes_type)
		return type_description

	def Get_Message_Info(self, object_message):
		print("----------------Message Info ----------------")
		print("Version:", object_message.version)
		print("Spare:", object_message.spare)
		print("Class:", object_message.mes_class)
		print("     -", self.Get_M2UA_Class_Description(object_message))
		print("Type:", object_message.mes_type)
		print("     -", self.Get_M2UA_Type_Description(object_message))
		print("---------------------------------------------")

	def M2UA_Message_Class_Check(self, m2ua_header):
		message_classes = m2ua_header.Define_Message_Classes()
		for class_number in message_classes.keys():
			if m2ua_header.mes_class == class_number:
				break
		else:
			raise M2UA_Error("\"%s\" is unknown m2ua class" % m2ua_header.mes_class)

	def M2UA_Message_Type_Check(self, m2ua_header):
		message_types = self.Get_M2UA_Message_Types(m2ua_header)
		for type_number in message_types.keys():
			if m2ua_header.mes_type == type_number:
				break
		else:
			raise M2UA_Error("\"%s\" is unknown m2ua message type" % m2ua_header.mes_type)

	def M2UA_Message_Length_Check(self, m2ua_header):
		if m2ua_header.length < 8:
			raise M2UA_Error("m2ua message length \"%s\" is too short" % m2ua_header.length)

	def M2UA_Header_Check(self, m2ua_header):
		if m2ua_header.version != 1:
			raise M2UA_Error("m2ua version \"%s\" is not 1" % m2ua_header.version)
		if m2ua_header.spare != 0:
			raise M2UA_Error("m2ua spare \"%s\" is not zero" % m2ua_header.spare)
		self.M2UA_Message_Class_Check(m2ua_header)
		self.M2UA_Message_Type_Check(m2ua_header)
		self.M2UA_Message_Length_Check(m2ua_header)

	def M2UA_Header_Forming(self, binary_header):
		try:
			unpacked_data = self.common_m2ua_header_pattern.unpack(binary_header)
		except struct.error:
			if not binary_header:
				raise M2UA_Error("message was not received")
			else:
				raise M2UA_Error("received message is not m2ua message")
		else:
			m2ua_header = M2UA_Message(version=unpacked_data[0], spare=unpacked_data[1], message_class=unpacked_data[2], message_type=unpacked_data[3])
			m2ua_header.length = unpacked_data[4]
			self.M2UA_Header_Check(m2ua_header)
			return m2ua_header

#	def SCCP_Data_Forming(self, binary_data):
#		sccp_data = isup.SCCP_Data()
#		sccp_data.data = binary_data
#		return sccp_data

#	def ISUP_Data_Forming(self, binary_data):
#		isup_data = self.isup_parser.Parse_Protocol_Data(binary_data)
#		return isup_data

	def Padding_Bytes_Counting(self, parameter_length):
		initial_parameter_length = parameter_length
		for i in range(1,4):
			parameter_length = initial_parameter_length + i
			if parameter_length % 4 == 0:
				multiple_length = parameter_length
				break
		else:
			raise M2UA_Error("padding bytes counting error")
		paddings_number = multiple_length - initial_parameter_length
		return paddings_number

	def M2UA_Parameters_Shifting(self, m2ua_data, parameter_length):
		m2ua_data = m2ua_data[parameter_length:]
		return m2ua_data

	def M2UA_Parameter_Padding_Removing(self, m2ua_data, parameter_length):
		paddings_number = self.Padding_Bytes_Counting(parameter_length)
		m2ua_data = m2ua_data[:parameter_length] + m2ua_data[parameter_length + paddings_number:]
		return m2ua_data

	def M2UA_Parameter_Tag_Check(self, m2ua_parameter):
		parameter_tags = m2ua_parameter.Define_Parameter_Tags()
		for tag_number in parameter_tags.keys():
			if m2ua_parameter.tag == tag_number:
				break
		else:
			raise M2UA_Error("\"%s\" is unknown m2ua parameter tag value" % m2ua_parameter.tag)

	def M2UA_TTC_Protocol_Data_Handling(self, binary_protocol_data):
		raise M2UA_Error("mtp3 ttc data parsing not supported now")

#"""	def MTP3_Spare_Check(self, spare):
#		if spare != 0:
#			raise M2UA_Error("mtp3 spare is not zero value")
#
#	def MTP3_Service_Indicator_Check(self, mtp3_object, service_indicator):
#		service_indicators = mtp3_object.Define_Service_Indicator_Values()
#		for indicator in service_indicators.keys():
#			if service_indicator == indicator:
#				break
#		else:
#			raise M2UA_Error("\"%s\" is unknown mtp3 service indicator value" % service_indicator)

#	def MTP3_Network_Indicator_Check(self, mtp3_object, network_indicator):
#		network_indicators = mtp3_object.Define_Network_Indicator_Values()
#		for indicator in network_indicators.keys():
#			if network_indicator == indicator:
#				break
#		else:
#			raise M2UA_Error("\"%s\" is unknown mtp3 network indicator value" % network_indicator)

#	def MTP3_SIO_Data_Check(self, mtp3_object, network_indicator, spare, service_indicator):
#		self.MTP3_Network_Indicator_Check(mtp3_object, network_indicator)
#		self.MTP3_Spare_Check(spare)
#		self.MTP3_Service_Indicator_Check(mtp3_object, service_indicator)

#	def Service_Data_Forming(self, service_indicator, binary_data):
#		service_data_handlers = self.Define_Service_Data_Handlers()
#		for indicator, handler in service_data_handlers.items():
#			if indicator == service_indicator:
#				service_data = service_data_handlers[service_indicator](binary_data)
#				break
#		else:
#			service_data = binary_data
#		return service_data

#	def MTP3_Service_Information_Octet_Forming(self, mtp3_object, binary_sio_data):
#		sio_value = int.from_bytes(binary_sio_data, byteorder="big")
#		network_indicator = (sio_value & self.sio_network_indicator_mask) >> 6
#		spare = sio_value & self.sio_spare_mask
#		service_indicator = sio_value & self.sio_service_indicator_mask
#		self.MTP3_SIO_Data_Check(mtp3_object, network_indicator, spare, service_indicator)
#		sio_data = mtp3_object.Service_Information_Octet(network_indicator=network_indicator, spare=spare, service_indicator=service_indicator)
#		return sio_data

#	def Add_Bit_Paddings(self, bin_value):
#		end_of_padding = False
#		while not end_of_padding:
#			if len(bin_value) != 8:
#				bin_value = "0" + bin_value
#			else:
#				end_of_padding = True
#		return bin_value

#	def DPC_Value_Forming(self, binary_data):
#		byte1 = self.Add_Bit_Paddings(bin(binary_data[0])[2:])
#		byte2 = self.Add_Bit_Paddings(bin(binary_data[1])[2:])
#		dpc_value = int(byte2[2:] + byte1, 2)
#		return dpc_value

#	def OPC_Value_Forming(self, binary_data):
#		byte2 = self.Add_Bit_Paddings(bin(binary_data[1])[2:])
#		byte3 = self.Add_Bit_Paddings(bin(binary_data[2])[2:])
#		byte4 = self.Add_Bit_Paddings(bin(binary_data[3])[2:])
#		opc_value = int(byte4[-4:] + byte3 + byte2[:2], 2)
#		return opc_value

#	def Link_Selector_Value_Forming(self, binary_data):
#		byte4 = self.Add_Bit_Paddings(bin(binary_data[3])[2:])
#		link_selector_value = int(byte4[:4], 2)
#		return link_selector_value

#	def MTP3_Routing_Label_Forming(self, mtp3_object, binary_routing_label_data):
#		dpc = self.DPC_Value_Forming(binary_routing_label_data)
#		opc = self.OPC_Value_Forming(binary_routing_label_data)
#		link_selector = self.Link_Selector_Value_Forming(binary_routing_label_data)
#		routing_label = mtp3_object.Routing_Label(dpc=dpc, opc=opc, link_selector=link_selector)
#		return routing_label
		
	def M2UA_Protocol_Data_Handling(self, binary_protocol_data):
		#MTP3 object building
		mtp3_data = isup.MTP3_Data()
		#Building SIO data
		mtp3_data.sio = self.isup_parser.MTP3_Service_Information_Octet_Forming(mtp3_object=mtp3_data, binary_sio_data=binary_protocol_data[:1])
		#Building routing label
		mtp3_data.routing_label = self.isup_parser.MTP3_Routing_Label_Forming(mtp3_object=mtp3_data, binary_routing_label_data=binary_protocol_data[1:5])
		#Service data
		mtp3_data.service_data = self.isup_parser.Service_Data_Forming(service_indicator=mtp3_data.sio.service_indicator, binary_data=binary_protocol_data[5:])
		return mtp3_data

	def M2UA_Composite_Parameters_Handling(self, binary_parameter_value):
		parameter_value = self.M2UA_Parameters_Forming(binary_parameter_value)
		return parameter_value

	def Polymorphic_M2UA_Parameter_Value_Handling(self, binary_parameter_value):
		parameter_value = binascii.hexlify(binary_parameter_value)
		return parameter_value

	def Int_Range_M2UA_Parameter_Value_Handling(self, binary_parameter_value):
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

	def Str_M2UA_Parameter_Value_Handling(self, binary_parameter_value):
		parameter_value = binary_parameter_value.decode("utf-8")
		return parameter_value

	def Int_M2UA_Parameter_Value_Handling(self, binary_parameter_value):
		parameter_value = int.from_bytes(binary_parameter_value, byteorder="big")
		return parameter_value

	def M2UA_Parameter_Value_Forming(self, parameter_tag, binary_parameter_value):
		#Empty parameter has None value
		if not binary_parameter_value:
			return None
		parameter_handlers = self.Define_M2UA_Parameter_Handlers()
		parameter_value = None
		for parameter_tags, handler in parameter_handlers.items():
			for tag in parameter_tags:
				if parameter_tag == tag:
					parameter_value = handler(binary_parameter_value)
		if parameter_value == None:
			raise M2UA_Error("unsupported parameter tag: %s" % parameter_tag)
		else:
			return parameter_value

	def M2UA_Parameters_Forming(self, m2ua_data):
		#Empty list for parameter collecting
		m2ua_parameters = []
		#Сycle stop сondition
		end_of_parameters = False
		while not end_of_parameters:
			#Extracting tag and length atributes from parameter
			parameter_tag = m2ua_data[:2]
			parameter_length = m2ua_data[2:4]
			parameter_header = parameter_tag + parameter_length
			unpacked_data = self.m2ua_parameter_header_pattern.unpack(parameter_header)
			#Building parameter by tag
			m2ua_parameter = M2UA_Parameter(unpacked_data[0])
			#Checking tag for existence 
			self.M2UA_Parameter_Tag_Check(m2ua_parameter)
			#Parameter length determining
			m2ua_parameter.length = unpacked_data[1]
			#Removing padding bytes if parameter length is not multiple of 4
			if m2ua_parameter.length % 4 != 0:
				m2ua_data = self.M2UA_Parameter_Padding_Removing(m2ua_data, m2ua_parameter.length)
			#Parameter value extracting 
			binary_parameter_value = m2ua_data[4:m2ua_parameter.length]
			#Parameter value assignment
			m2ua_parameter.value = self.M2UA_Parameter_Value_Forming(m2ua_parameter.tag, binary_parameter_value)
			#Append formed parameter to list
			m2ua_parameters.append(m2ua_parameter)
			#Byte string shifting along parameter length
			m2ua_data = self.M2UA_Parameters_Shifting(m2ua_data, m2ua_parameter.length)
			#Stop condition checking
			if not m2ua_data:
				end_of_parameters = True
		return m2ua_parameters 

	def Parse_Message(self, binary_message):
		#Retrieving the M2UA header bytes from the binary message
		binary_m2ua_header = binary_message[:8]
		#Building M2UA header object
		m2ua_data = self.M2UA_Header_Forming(binary_m2ua_header)
		#Building M2UA parameters if they exist
		if m2ua_data.length > 8:
			m2ua_parameters = self.M2UA_Parameters_Forming(binary_message[8:])
			m2ua_data.parameters = m2ua_parameters
		return m2ua_data

class M2UA_Error(Exception):

	def __init__(self, description):
		self.description = description

class Message_Validator:

	def __init__(self):
		self.parser = Message_Parser()
		self.parameters_list = M2UA_Parameter(tag=0)
		self.isup_parser = isup.ISUP_Message_Parser()

	def Define_Exec_Handlers(self):
		handlers = {
		  1 : self.Int_Parameter_Value_Handling,
		  11 : self.Int_Parameter_Value_Handling,
		  12 : self.Int_Parameter_Value_Handling,
		  13 : self.Status_Parameter_Value_Handling,
		  17 : self.Int_Parameter_Value_Handling,
		  19 : self.Int_Parameter_Value_Handling,
		  770 : self.Int_Parameter_Value_Handling,
		  771 : self.Int_Parameter_Value_Handling,
		  772 : self.Int_Parameter_Value_Handling,
		  773 : self.Int_Parameter_Value_Handling,
		  774 : self.Int_Parameter_Value_Handling,
		  775 : self.Int_Parameter_Value_Handling,
		  776 : self.Int_Parameter_Value_Handling,
		  778 : self.Int_Parameter_Value_Handling,
		  779 : self.Int_Parameter_Value_Handling,
		  780 : self.Int_Parameter_Value_Handling,
		  782 : self.Int_Parameter_Value_Handling,
		  784 : self.Int_Parameter_Value_Handling,
		  3 : self.Str_Parameter_Value_Handling,
		  4 : self.Str_Parameter_Value_Handling,
		  8 : self.Int_Range_Parameter_Value_Handling,
		  7 : self.Polymorphic_Parameter_Value_Handling,
		  9 : self.Polymorphic_Parameter_Value_Handling,
		  768 : self.Protocol_Data_Handling,
		  769 : self.TTC_Protocol_Data_Handling,
		  777 : self.Composite_Parameters_Handling,
		  781 : self.Composite_Parameters_Handling,
		  783 : self.Composite_Parameters_Handling
		}
		return handlers

	def Get_Tag_Parameters_list(self, tag):
		if tag == 11:
			parameter_info = self.parameters_list.Define_Traffic_Mode_Type_Values()
		elif tag == 12:
			parameter_info = self.parameters_list.Define_Error_Code_Values()
		elif tag == 13:
			parameter_info = self.parameters_list.Define_Status_Type_Values()
		elif tag == 770:
			parameter_info = self.parameters_list.Define_State_Parameter_Values()
		elif tag == 771:
			parameter_info = self.parameters_list.Define_Event_Parameter_Values()
		elif ((tag == 772) or (tag ==773)):
			parameter_info = self.parameters_list.Define_Congestion_And_Discard_Status_Values()
		elif tag == 774:
			parameter_info = self.parameters_list.Define_Action_Values()
		elif tag == 776:
			parameter_info = self.parameters_list.Define_Result_Values()
		elif tag == 782:
			parameter_info = self.parameters_list.Define_Registration_Status_Values()
		elif tag == 784:
			parameter_info = self.parameters_list.Define_Deregistration_Status_Values()
		else:
			raise M2UA_Error("m2ua parameter tag \"%s\" does not support" % tag)
		return parameter_info

	def Get_Tag_Parameters_list_13(self, status_value):
		if status_value == 1:
			parameter_info = self.parameters_list.Define_AS_State_Change_Status_Information_Values()
		elif status_value == 2:
			parameter_info = self.parameters_list.Define_Other_Status_Information_Values()
		else:
			raise M2UA_Error("m2ua Status parameter value \"%s\" does not support" % status_value)
		return parameter_info

	def Protocol_Data_Handling(self, binary_protocol_data):
		#MTP3 object building
		mtp3_data = isup.MTP3_Data()
		#Building SIO data
		mtp3_data.sio = self.isup_parser.MTP3_Service_Information_Octet_Forming(mtp3_object=mtp3_data, binary_sio_data=binary_protocol_data[:1])
		#Building routing label
		mtp3_data.routing_label = self.isup_parser.MTP3_Routing_Label_Forming(mtp3_object=mtp3_data, binary_routing_label_data=binary_protocol_data[1:5])
		#Service data
		mtp3_data.service_data = self.isup_parser.Service_Data_Forming(service_indicator=mtp3_data.sio.service_indicator, binary_data=binary_protocol_data[5:])
		return mtp3_data

	def Composite_Parameters_Handling(self, tag, in_parameter_value):
		if type(in_parameter_value) == bytes:
			return in_parameter_value
		elif type(in_parameter_value) == list:
			return in_parameter_value
		else:
			raise M2UA_Error("Type of parameter: "+str(tag)+" is not BYTES or LIST")

	def Polymorphic_Parameter_Value_Handling(self, tag, in_parameter_value):
		if type(in_parameter_value) == bytes:
			return in_parameter_value
		elif type(in_parameter_value) == list:
			binary_parameter_value = bytes(in_parameter_value)
			parameter_value = binascii.hexlify(binary_parameter_value)
			return parameter_value
		else:
			raise M2UA_Error("Type of parameter: "+str(tag)+" is not BYTES or LIST")

	def TTC_Protocol_Data_Handling(self, binary_protocol_data):
		raise M2UA_Error("mtp3 ttc data validation not supported now")

	def Int_Range_Parameter_Value_Handling(self, tag, in_parameter_value):
		if	type(in_parameter_value) == list:
			if type(in_parameter_value[0]) == list:
				for _value in in_parameter_value:
					if len(_value) != 2:
						raise M2UA_Error("identifier range must be described only by start and stop identifiers in list")
					if not (int(_value[0]) or int(_value[1])):
						raise M2UA_Error("identifiers values must be integer")
				return in_parameter_value
			elif type(in_parameter_value[0]) == int:
				if len(in_parameter_value) != 2:
					raise M2UA_Error("identifier range must be described only by start and stop identifiers in list")
				if in_parameter_value[0] >= in_parameter_value[1]:
					raise M2UA_Error("identifier range start identifier must be less than stop identifier")
				return [in_parameter_value]
			else:
				raise M2UA_Error("Type of parameter: "+str(tag)+" is not LIST")
		else:
			raise M2UA_Error("Type of parameter: "+str(tag)+" is not LIST")

	def Int_Parameter_Value_Handling(self, tag, in_parameter_value):
		if type(in_parameter_value) == int or type(in_parameter_value) == list:
			return in_parameter_value
		else:
			parameter_info = self.Get_Tag_Parameters_list(tag)
			for _key,_value in parameter_info.items():
				if in_parameter_value.lower().replace(" ", "_") == _value.lower().replace(" ", "_"):
					return _key
			raise M2UA_Error("Type of parameter: "+tag+" is not INTEGER")

	def Str_Parameter_Value_Handling(self, tag, in_parameter_value):
		try:
			parameter_value = str(in_parameter_value)
			return parameter_value
		except:
			raise M2UA_Error("Type of parameter: "+tag+" is not STRING")

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
				raise M2UA_Error("m2ua Information parameter value \"%s\" does not support" % information)
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
						raise M2UA_Error("m2ua Information parameter value \"%s\" does not support" % information)
			raise M2UA_Error("m2ua Status parameter value \"%s\" does not support" % status)

	def M2UA_Message_Class_Type_Check(self, message, config_message):
		types = self.parser.Get_M2UA_Message_Types(message)
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
			result, description_mes = self.M2UA_Message_Class_Type_Check(message, config_message)
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
									raise M2UA_Error("Configuration data is not valid")
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
							raise M2UA_Error("Configuration data is not valid")
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
								raise M2UA_Error("Configuration data is not valid")
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
								raise M2UA_Error("Configuration data is not valid")
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
								raise M2UA_Error("Configuration data is not valid")
					else:
						temp_string +=_val
			print ("::::",mes_params)
			return message_row_type, mes_params
		else:
			return "NO_MESSAGE", mes_params




		


