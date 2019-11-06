import random
import math
import sys
import struct
import binascii

class MTP3_Data:

	def __init__(self):
		self.sio = None
		self.routing_label = None
		self.service_data = None

	class Service_Information_Octet:

		def __init__(self, network_indicator, service_indicator=None, spare=0):
			self.network_indicator = network_indicator
			self.spare = spare
			self.service_indicator = service_indicator

	class Routing_Label:

		def __init__(self, dpc, opc, link_selector):
			self.dpc = dpc
			self.opc = opc
			self.link_selector = link_selector

	def Define_Network_Indicator_Values(self):
		values = {
		  0 : "International network",
		  1 : "International network reserved",
		  2 : "National network",
		  3 : "National network reserved"
		}
		return values

	def Define_Service_Indicator_Values(self):
		values = {
		  0 : "Signaling network management messages",
		  1 : "Signaling network testing and maintenance messages",
		  3 : "SCCP",
		  4 : "Telephone User Part",
		  5 : "ISDN User Part",
		  6 : "Data User Part (call and circuit-related messages)",
		  7 : "Data User Part (facility registration and cancellation messages)",
		  9 : "Broadband ISDN User Part",
		 10 : "Satellite ISDN User Part"
		}
		return values

# SCCP is not realized

class SCCP_Data:

	def __init__(self):
		self.data = None

class SCCP_Message_Builder:
	
	def __init__(self):
		pass

class SCCP_Binary_Convertor:

	def __init__(self):
		pass

	def Convert_Service_Data(self, service_data):
		binary_service_data = b""
		service_data_length = 0
		return (binary_service_data, service_data_length)

class SCCP_Message_Parser:

	def __init__(self):
		pass

# ISUP. To make one class for ISUP

class ISUP_Data:

	def __init__(self, cic, mes_type):
		self.cic = cic
		self.mes_type = mes_type
		self.mandatory_parameters = []
		self.optional_parameters = []

class Access_Delivery_Information:

	def __init__(self, value):
		self.value = value & 0b00000001

class Access_Transport:

	def __init__(self):
		self.value = []

	def Build(self, value):
		if type(value) == bytes:
			self.value = self.Extract_Bytes(value)
		elif type(value) == list:
			self.value = list(value)
		return self

	def Extract_Bytes(self, binary_value):
		bytes_list = []
		for value in binary_value:
			bytes_list.append(value)
		return bytes_list

class Automatic_Congestion_Level:

	def __init__(self, value):
		self.value = value

class Backward_Call_Indicators:
	
	def __init__(self, value):
		self.charge_indicator = (value & 0b0000001100000000) >> 8
		self.called_party_status_indicator = (value & 0b0000110000000000) >> 10
		self.called_party_category_indicator = (value & 0b0011000000000000) >> 12
		self.end_to_end_method_indicator = (value & 0b1100000000000000) >> 14
		self.interworking_indicator = value & 0b0000000000000001
		self.end_to_end_information_indicator = (value & 0b0000000000000010) >> 1
		self.isdn_user_part_indicator = (value & 0b0000000000000100) >> 2
		self.holding_indicator = (value & 0b0000000000001000) >> 3
		self.isdn_access_indicator = (value & 0b0000000000010000) >> 4
		self.echo_control_device_indicator = (value & 0b0000000000100000) >> 5
		self.sccp_method_indicator = (value & 0b0000000011000000) >> 6

class Call_Diversion_Information:

	def __init__(self, value):
		self.value = value & 0b00000111
		self.redirecting_reason = (value & 0b01111000) >> 3
		self.spare = (value & 0b10000000) >> 7

class Call_History_Information:

	def __init__(self, value):
		self.value = value

class Call_Reference:

	def __init__(self):
		self.call_identity = []
		self.signalling_point_code = None
		self.spare = 0

	def Build(self, value):
		if type(value) == bytes:
			self.call_identity = self.Extract_Bytes(value[:3])
			self.signalling_point_code = int.from_bytes(value[3], byteorder="big") + int.from_bytes(value[4], byteorder="big")*256
		elif type(value) == list:
			self.call_identity = list(value[0])
			self.signalling_point_code = value[1]
		return self

	def Extract_Bytes(self, binary_value):
		bytes_list = []
		for value in binary_value:
			bytes_list.append(value)
		return bytes_list

class Calling_Party_Number:

	def __init__(self):
		self.odd_even_indicator = None
		self.nature_of_address_indicator = None
		self.ni_indicator = None
		self.numbering_plan_indicator = None
		self.address_presentation_restricted_indicator = None
		self.screening_indicator = None
		self.digits = []

	def Build(self, value):
		self.odd_even_indicator = (value[0] & 0b10000000) >> 7
		self.nature_of_address_indicator = value[0] & 0b01111111
		self.ni_indicator = (value[1] & 0b10000000) >> 7
		self.numbering_plan_indicator = (value[1] & 0b01110000) >> 4
		self.address_presentation_restricted_indicator = (value[1] & 0b00001100) >> 2
		self.screening_indicator = value[1] & 0b00000011
		if type(value) == bytes:
			self.digits = self.Extract_Digits(value[2:])
		elif type(value) == list:
			self.digits = list(value[2])
		return self

	def Extract_Digits(self, binary_value):
		digits_list = []
		for signal_pair in binary_value:
			address_signal1 = signal_pair & 0b00001111
			digits_list.append(address_signal1)
			address_signal2 = (signal_pair & 0b11110000) >> 4
			digits_list.append(address_signal2)
		if self.odd_even_indicator == 1:
			del digits_list[-1]
		return digits_list

class Calling_Party_Category:

	def __init__(self, value):
		self.value = value

class Called_Party_Number:

	def __init__(self):
		self.odd_even_indicator = None
		self.nature_of_address_indicator = None
		self.inn_indicator = None
		self.numbering_plan_indicator = None
		self.spare = None
		self.digits = []

	def Build(self, value):
		self.odd_even_indicator = (value[0] & 0b10000000) >> 7
		self.nature_of_address_indicator = value[0] & 0b01111111
		self.inn_indicator = (value[1] & 0b10000000) >> 7
		self.numbering_plan_indicator = (value[1] & 0b01110000) >> 4
		self.spare = value[1] & 0b00001111
		if type(value) == bytes:
			self.digits = self.Extract_Digits(value[2:])
		elif type(value) == list:
			self.digits = list(value[2])
		return self

	def Extract_Digits(self, binary_value):
		digits_list = []
		for signal_pair in binary_value:
			address_signal1 = signal_pair & 0b00001111
			digits_list.append(address_signal1)
			address_signal2 = (signal_pair & 0b11110000) >> 4
			digits_list.append(address_signal2)
		if self.odd_even_indicator == 1:
			del digits_list[-1]
		return digits_list

class Cause_Indicators:
	
	def __init__(self):
		self.location = None
		self.spare = None
		self.coding_standard = None
		self.cause_value = None
		self.diagnostic = None

	def Build(self, value):
		self.location = value[0] & 0b00001111
		self.spare = (value[0] & 0b00010000) >> 4
		self.coding_standard = (value[0] & 0b01100000) >> 5
		self.cause_value = value[1] & 0b01111111
		if type(value) == bytes:
			self.diagnostic = self.Diagnostic_Handling(value[3:], (value[0] & 0b10000000) >> 7, (value[1] & 0b10000000) >> 7)
		elif type(value) == list:
			self.diagnostic = value[2]
		return self

	def Diagnostic_Handling(self, diagnostic_info, *extentions):
		if extentions == (1,1):
			return None
		else:
			return self.Diagnostic(diagnostic_info)

	class Diagnostic:

		def __init__(self, info):
			self.info = info
			
class Circuit_Group_Supervision_Message_Type:

	def __init__(self, value):
		self.circuit_group_supervision_message_type_indicator = value & 0b00000011
		self.spare = (value & 0b11111100) >> 2

class Closed_User_Group_Interlock_Code:

	def __init__(self):
		self.digits = []
		self.code = None

	def Build(self, value):
		if type(value) == bytes:
			self.digits = self.Extract_Digits(value[:2])
			self.code = int.from_bytes(value[2], byteorder="big")*256 + int.from_bytes(value[3], byteorder="big")
		elif type(value) == list:
			self.digits = list(value[0])
			self.code = value[1]
		return self

	def Extract_Digits(self, binary_value):
		digits_list = []
		for signal_pair in binary_value:
			address_signal1 = (signal_pair & 0b11110000) >> 4
			digits_list.append(address_signal1)
			address_signal2 = signal_pair & 0b00001111
			digits_list.append(address_signal2)
		return digits_list

class Connected_Number:

	def __init__(self):
		self.odd_even_indicator = None
		self.nature_of_address_indicator = None
		self.spare = None
		self.numbering_plan_indicator = None
		self.address_presentation_restricted_indicator = None
		self.screening_indicator = None
		self.digits = []

	def Build(self, value):
		self.odd_even_indicator = (value[0] & 0b10000000) >> 7
		self.nature_of_address_indicator = value[0] & 0b01111111
		self.spare = (value[1] & 0b10000000) >> 7
		self.numbering_plan_indicator = (value[1] & 0b01110000) >> 4
		self.address_presentation_restricted_indicator = (value[1] & 0b00001100) >> 2
		self.screening_indicator = value[1] & 0b00000011
		if type(value) == bytes:
			self.digits = self.Extract_Digits(value[2:])
		elif type(value) == list:
			self.digits = list(value[2])
		return self

	def Extract_Digits(self, binary_value):
		digits_list = []
		for signal_pair in binary_value:
			address_signal1 = signal_pair & 0b00001111
			digits_list.append(address_signal1)
			address_signal2 = (signal_pair & 0b11110000) >> 4
			digits_list.append(address_signal2)
		if self.odd_even_indicator == 1:
			del digits_list[-1]
		return digits_list

class Continuity_Indicators:

	def __init__(self, value):
		self.continuity_indicator = value & 0b00000001
		self.spare = (value & 0b11111110) >> 1

class Echo_Control_Information:

	def __init__(self, value):
		self.outgoing_echo_control_device_information_indicator = value & 0b00000011
		self.incoming_echo_control_device_information_indicator = (value & 0b00001100) >> 2
		self.outgoing_echo_control_device_request_indicator = (value & 0b00110000) >> 4
		self.incoming_echo_control_device_request_indicator = (value & 0b11000000) >> 6

class Event_Information:

	def __init__(self, value):
		self.event_indicator = value & 0b01111111
		self.event_presentation_restricted_indicator = (value & 0b10000000) >> 7

class Facility_Indicator:

	def __init__(self, value):
		self.value = value 

class Forward_Call_Indicators:

	def __init__(self, value):
		self.national_international_call_indicator = (value & 0b0000000100000000) >> 8
		self.end_to_end_method_indicator = (value & 0b0000011000000000) >> 9
		self.interworking_indicator = (value & 0b0000100000000000) >> 11
		self.end_to_end_information_indicator = (value & 0b0001000000000000) >> 12
		self.isdn_user_part_indicator = (value & 0b0010000000000000) >> 13
		self.isdn_user_part_preference_indicator = (value & 0b1100000000000000) >> 14
		self.isdn_access_indicator = value & 0b0000000000000001
		self.sccp_method_indicator = (value & 0b0000000000000110) >> 1
		self.spare = (value & 0b0000000000001000) >> 3
		self.for_national_use = (value & 0b0000000011110000) >> 4

class Generic_Number:

	def __init__(self):
		self.number_qualifier_indicator = None
		self.odd_even_indicator = None
		self.nature_of_address_indicator = None
		self.ni_indicator = None
		self.numbering_plan_indicator = None
		self.address_presentation_restricted_indicator = None
		self.screening_indicator = None
		self.digits = []

	def Build(self, value):
		self.number_qualifier_indicator = value[0]
		self.odd_even_indicator = (value[1] & 0b10000000) >> 7
		self.nature_of_address_indicator = value[1] & 0b01111111
		self.ni_indicator = (value[2] & 0b10000000) >> 7
		self.numbering_plan_indicator = (value[2] & 0b01110000) >> 4
		self.address_presentation_restricted_indicator = (value[2] & 0b00001100) >> 2
		self.screening_indicator = value[2] & 0b00000011
		if type(value) == bytes:
			self.digits = self.Extract_Digits(value[3:])
		elif type(value) == list:
			self.digits = list(value[3])
		return self

	def Extract_Digits(self, binary_value):
		digits_list = []
		for signal_pair in binary_value:
			address_signal1 = signal_pair & 0b00001111
			digits_list.append(address_signal1)
			address_signal2 = (signal_pair & 0b11110000) >> 4
			digits_list.append(address_signal2)
		if self.odd_even_indicator == 1:
			del digits_list[-1]
		return digits_list

class Information_Request_Indicators:

    def __init__(self, value):
         self.calling_party_address_request_indicator = value & 0b0000000000000001
         self.holding_indicator = (value & 0b0000000000000010) >> 1
         self.calling_party_category_request_indicator = (value & 0b0000000000001000) >> 3
         self.charge_information_request_indicator = (value & 0b0000000000010000) >> 4
         self.malicious_call_identification_request_indicator = (value & 0b0000000010000000) >> 7
         self.spare = 0

class Information_Indicators:
    
    def __init__(self, value):
        self.calling_party_address_response_indicator = value & 0b0000000000000011
        self.hold_provided_indicator = (value & 0b0000000000000100) >> 2
        self.calling_party_category_response_indicator = (value & 0b0000000000100000) >> 5
        self.charge_information_response_indicator = (value & 0b0000000001000000) >> 6
        self.solicited_information_indicator = (value & 0b0000000010000000) >> 7
        self.spare = 0	

class Location_Number:

	def __init__(self):
		self.odd_even_indicator = None
		self.nature_of_address_indicator = None
		self.inn_indicator = None
		self.numbering_plan_indicator = None
		self.address_presentation_restricted_indicator = None
		self.screening_indicator = None
		self.digits = []

	def Build(self, value):
		self.odd_even_indicator = (value[0] & 0b10000000) >> 7
		self.nature_of_address_indicator = value[0] & 0b01111111
		self.inn_indicator = (value[1] & 0b10000000) >> 7
		self.numbering_plan_indicator = (value[1] & 0b01110000) >> 4
		self.address_presentation_restricted_indicator = (value[1] & 0b00001100) >> 2
		self.screening_indicator = value[1] & 0b00000011
		if type(value) == bytes:
			self.digits = self.Extract_Digits(value[2:])
		elif type(value) == list:
			self.digits = list(value[2])
		return self

	def Extract_Digits(self, binary_value):
		digits_list = []
		for signal_pair in binary_value:
			address_signal1 = signal_pair & 0b00001111
			digits_list.append(address_signal1)
			address_signal2 = (signal_pair & 0b11110000) >> 4
			digits_list.append(address_signal2)
		if self.odd_even_indicator == 1:
			del digits_list[-1]
		return digits_list

class MCID_Request_Indicators:

	def __init__(self, value):
		self.mcid_indicator = value & 0b00000001
		self.holding_indicator = (value & 0b00000010) >> 1
		self.spare = (value & 0b11111100) >> 2

class Optional_Backward_Call_Indicators:

	def __init__(self, value):
		self.inband_information_indicator = value & 0b00000001
		self.call_diversion_may_occur_indicator = (value & 0b00000010) >> 1
		self.simple_segmentation_indicator = (value & 0b00000100) >> 2
		self.mlpp_user_indicator = (value & 0b00001000) >> 3
		self.spare = (value & 0b11110000) >> 4

class Optional_Forward_Call_Indicators:

	def __init__(self, value):
		self.closed_user_group_call_indicator = value & 0b00000011
		self.simple_segmentation_indicator = (value & 0b00000100) >> 2
		self.spare = (value & 0b01111000) >> 3
		self.connected_line_identity_request_indicator = (value & 0b10000000) >> 7
		
class MCID_Response_Indicators:

	def __init__(self, value):
		self.mcid_indicator = value & 0b00000001
		self.holding_indicator = (value & 0b00000010) >> 1
		self.spare = (value & 0b11111100) >> 2

class Nature_Of_Connection_Indicators:

	def __init__(self, value):
		self.satellite_indicator = value & 0b00000011
		self.continuity_check_indicator = (value & 0b00001100) >> 2
		self.echo_control_device_indicator = (value & 0b00010000) >> 4
		self.spare = (value & 0b11100000) >> 5

class Original_Called_Number:

	def __init__(self):
		self.odd_even_indicator = None
		self.nature_of_address_indicator = None
		self.numbering_plan_indicator = None
		self.address_presentation_restricted_indicator = None
		self.spare = 0
		self.digits = []

	def Build(self, value):
		self.odd_even_indicator = (value[0] & 0b10000000) >> 7
		self.nature_of_address_indicator = value[0] & 0b01111111
		self.numbering_plan_indicator = (value[1] & 0b01110000) >> 4
		self.address_presentation_restricted_indicator = (value[1] & 0b00001100) >> 2
		if type(value) == bytes:
			self.digits = self.Extract_Digits(value[2:])
		elif type(value) == list:
			self.digits = list(value[2])
		return self

	def Extract_Digits(self, binary_value):
		digits_list = []
		for signal_pair in binary_value:
			address_signal1 = signal_pair & 0b00001111
			digits_list.append(address_signal1)
			address_signal2 = (signal_pair & 0b11110000) >> 4
			digits_list.append(address_signal2)
		if self.odd_even_indicator == 1:
			del digits_list[-1]
		return digits_list

class Origination_ISC_Point_Code:

	def __init__(self, value):
		self.signalling_point_code = value
		self.spare = 0

class Parameter_Compatibility_Information:

	def __init__(self):
		self.parameters = []

	def Build(self, value):
		if type(value) == bytes:
			self.parameters = self.Form_List(value)
		elif type(value) == list:
			self.parameters = value
		return self

	def Form_List(self, binary_value):
		param_list = []
		sub_param_list = []
		len_value = len(binary_value)
		if not len_value % 3:
			n=0
			for _value in binary_value:
				if n % 3 != 0:
					n += 1
				else:
					param_list.append(sub_param_list)
					sub_param_list = []
				sub_param_list.append(_value)
			param_list.append(sub_param_list)
		else:
			raise ISUP_Error("invalid binary data")
		return param_list

class Propagation_Delay_Counter:

	def __init__(self, value):
		self.value = value

class Range_And_Status:

	def __init__(self):
		self.range = None
		self.status = []

	def Build(self, value):
		self.range = value[0]
		if len(value) != 1:
			if type(value) == bytes:
				self.status = value[1:]
			elif type(value) == list:
				if type(value[1]) == list:
					self.status = list(value[1])
				elif type(value[1]) == int:
					self.status.append(value[1])
		return self

class Redirecting_Number:

	def __init__(self):
		self.odd_even_indicator = None
		self.nature_of_address_indicator = None
		self.numbering_plan_indicator = None
		self.address_presentation_restricted_indicator = None
		self.spare = 0
		self.digits = []

	def Build(self, value):
		self.odd_even_indicator = (value[0] & 0b10000000) >> 7
		self.nature_of_address_indicator = value[0] & 0b01111111
		self.numbering_plan_indicator = (value[1] & 0b01110000) >> 4
		self.address_presentation_restricted_indicator = (value[1] & 0b00001100) >> 2
		if type(value) == bytes:
			self.digits = self.Extract_Digits(value[2:])
		elif type(value) == list:
			self.digits = list(value[2])
		return self

	def Extract_Digits(self, binary_value):
		digits_list = []
		for signal_pair in binary_value:
			address_signal1 = signal_pair & 0b00001111
			digits_list.append(address_signal1)
			address_signal2 = (signal_pair & 0b11110000) >> 4
			digits_list.append(address_signal2)
		if self.odd_even_indicator == 1:
			del digits_list[-1]
		return digits_list

class Redirection_Information:

	def __init__(self, value):
		self.redirecting_indicator = value & 0b0000000000000111
		self.original_redirection_reason = (value & 0b0000000011110000) >> 4
		self.redirection_counter = (value & 0b0000011100000000) >> 8
		self.redirecting_reason = (value & 0b1111000000000000) >> 12
		self.spare = 0

class Redirection_Number:

	def __init__(self):
		self.odd_even_indicator = None
		self.nature_of_address_indicator = None
		self.ni_indicator = None
		self.numbering_plan_indicator = None
		self.address_presentation_restricted_indicator = None
		self.screening_indicator = None
		self.digits = []

	def Build(self, value):
		self.odd_even_indicator = (value[0] & 0b10000000) >> 7
		self.nature_of_address_indicator = value[0] & 0b01111111
		self.ni_indicator = (value[1] & 0b10000000) >> 7
		self.numbering_plan_indicator = (value[1] & 0b01110000) >> 4
		self.address_presentation_restricted_indicator = (value[1] & 0b00001100) >> 2
		self.screening_indicator = value[1] & 0b00000011
		if type(value) == bytes:
			self.digits = self.Extract_Digits(value[2:])
		elif type(value) == list:
			self.digits = list(value[2])
		return self

	def Extract_Digits(self, binary_value):
		digits_list = []
		for signal_pair in binary_value:
			address_signal1 = signal_pair & 0b00001111
			digits_list.append(address_signal1)
			address_signal2 = (signal_pair & 0b11110000) >> 4
			digits_list.append(address_signal2)
		if self.odd_even_indicator == 1:
			del digits_list[-1]
		return digits_list

class Redirection_Number_Restriction:

	def __init__(self, value):
		self.presentation_restricted_indicator = value & 0b00000011
		self.spare = (value & 0b11111100) >> 2

class Signalling_Point_Code:

	def __init__(self, value):
		self.signalling_point_code = value
		self.spare = 0

class Subsequent_Number:

	def __init__(self):
		self.spare = None
		self.odd_even_indicator = None
		self.digits = []

	def Build(self, value):
		if type(value) == list:
			self.digits = value
		elif type(value) == bytes:
			self.spare = value[0] & 0b01111111
			self.odd_even_indicator = (value[0] & 0b10000000) >> 7
			self.digits = self.Extract_Digits(value[1:])
		return self

	def Extract_Digits(self, binary_value):
		digits_list = []
		for signal_pair in binary_value:
			address_signal1 = signal_pair & 0b00001111
			digits_list.append(address_signal1)
			address_signal2 = (signal_pair & 0b11110000) >> 4
			digits_list.append(address_signal2)
		if self.odd_even_indicator == 1:
			del digits_list[-1]
		return digits_list

class Suspend_Resume_Indicators:

	def __init__(self, value):
		self.suspend_resume_indicator = value & 0b00000001
		self.spare = (value & 0b11111110) >> 1

class Transmission_Medium_Requirement:

	def __init__(self, value):
		self.value = value

class Transmission_Medium_Requirement_Prime:

	def __init__(self, value):
		self.value = value

class Transmission_Medium_Used:

	def __init__(self, value):
		self.value = value

class User_Service_Information:

	def __init__(self, value):
		self.value = value

class User_Service_Information_Prime:

	def __init__(self, value):
		self.value = value

class User_Teleservice_Information:

	def __init__(self, value):
		self.value = value

class User_To_User_Information:

	def __init__(self, value):
		self.value = value

class ISUP_Message_Parser:

	def __init__(self):
		self.sio_network_indicator_mask = 0b11000000
		self.sio_spare_mask = 0b00110000
		self.sio_service_indicator_mask = 0b00001111
		self.routing_label_dpc_mask = 16383
		self.routing_label_opc_mask = 268419072
		self.routing_label_link_selector_mask = 4026531840
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
		  48 : self.No_Parameters_Handler,
		  52 : self.No_Parameters_Handler,
		  53 : self.No_Parameters_Handler }#UP_

	def Define_Service_Data_Handlers(self):
		handlers = {
		  3 : self.SCCP_Data_Forming,
		  5 : self.ISUP_Data_Forming
		}
		return handlers

	def SCCP_Data_Forming(self, binary_data):
		sccp_data = SCCP_Data()
		sccp_data.data = binary_data
		return sccp_data

	def ISUP_Data_Forming(self, binary_data):
		isup_data = self.Parse_Protocol_Data(binary_data)
		return isup_data

	def MTP3_Spare_Check(self, spare):
		if spare != 0:
			raise ISUP_Error("mtp3 spare is not zero value")

	def MTP3_Service_Indicator_Check(self, mtp3_object, service_indicator):
		service_indicators = mtp3_object.Define_Service_Indicator_Values()
		for indicator in service_indicators.keys():
			if service_indicator == indicator:
				break
		else:
			raise ISUP_Error("\"%s\" is unknown mtp3 service indicator value" % service_indicator)

	def MTP3_Network_Indicator_Check(self, mtp3_object, network_indicator):
		network_indicators = mtp3_object.Define_Network_Indicator_Values()
		for indicator in network_indicators.keys():
			if network_indicator == indicator:
				break
		else:
			raise ISUP_Error("\"%s\" is unknown mtp3 network indicator value" % network_indicator)

	def MTP3_SIO_Data_Check(self, mtp3_object, network_indicator, spare, service_indicator):
		self.MTP3_Network_Indicator_Check(mtp3_object, network_indicator)
		self.MTP3_Spare_Check(spare)
		self.MTP3_Service_Indicator_Check(mtp3_object, service_indicator)

	def Service_Data_Forming(self, service_indicator, binary_data):
		service_data_handlers = self.Define_Service_Data_Handlers()
		for indicator, handler in service_data_handlers.items():
			if indicator == service_indicator:
				service_data = service_data_handlers[service_indicator](binary_data)
				break
		else:
			service_data = binary_data
		return service_data

	def MTP3_Service_Information_Octet_Forming(self, mtp3_object, binary_sio_data):
		sio_value = int.from_bytes(binary_sio_data, byteorder="big")
		network_indicator = (sio_value & self.sio_network_indicator_mask) >> 6
		spare = sio_value & self.sio_spare_mask
		service_indicator = sio_value & self.sio_service_indicator_mask
		self.MTP3_SIO_Data_Check(mtp3_object, network_indicator, spare, service_indicator)
		sio_data = mtp3_object.Service_Information_Octet(network_indicator=network_indicator, spare=spare, service_indicator=service_indicator)
		return sio_data

	def Add_Bit_Paddings(self, bin_value):
		end_of_padding = False
		while not end_of_padding:
			if len(bin_value) != 8:
				bin_value = "0" + bin_value
			else:
				end_of_padding = True
		return bin_value

	def DPC_Value_Forming(self, binary_data):
		byte1 = self.Add_Bit_Paddings(bin(binary_data[0])[2:])
		byte2 = self.Add_Bit_Paddings(bin(binary_data[1])[2:])
		dpc_value = int(byte2[2:] + byte1, 2)
		return dpc_value

	def OPC_Value_Forming(self, binary_data):
		byte2 = self.Add_Bit_Paddings(bin(binary_data[1])[2:])
		byte3 = self.Add_Bit_Paddings(bin(binary_data[2])[2:])
		byte4 = self.Add_Bit_Paddings(bin(binary_data[3])[2:])
		opc_value = int(byte4[-4:] + byte3 + byte2[:2], 2)
		return opc_value

	def Link_Selector_Value_Forming(self, binary_data):
		byte4 = self.Add_Bit_Paddings(bin(binary_data[3])[2:])
		link_selector_value = int(byte4[:4], 2)
		return link_selector_value

	def MTP3_Routing_Label_Forming(self, mtp3_object, binary_routing_label_data):
		dpc = self.DPC_Value_Forming(binary_routing_label_data)
		opc = self.OPC_Value_Forming(binary_routing_label_data)
		link_selector = self.Link_Selector_Value_Forming(binary_routing_label_data)
		routing_label = mtp3_object.Routing_Label(dpc=dpc, opc=opc, link_selector=link_selector)

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
		isup_data = ISUP_Data(cic=cic, mes_type=mes_type)
		#Обработка параметров сообщения
		try:
			isup_data.mandatory_parameters, isup_data.optional_parameters = self.parameters_handlers[mes_type](binary_data[3:])
		except KeyError:
			raise ISUP_Error("unknown or unsupported message type: \"%s\"" % mes_type)
		else:
			return isup_data

class MTN_SNM_Data:

	def __init__(self, mes_group, mes_type, value=None):
		self.mes_group = mes_group
		self.mes_type = mes_type
		self.value = value

class MTN_SNM_Builder:

	def Build_MTN_SNM_Data(self, kwargs):
		temp = 0
		for _key,_value in kwargs.items():
			if _key == "value":
				temp =1
		if temp == 1:
			mtn_data = MTN_SNM_Data(kwargs["mes_group"], kwargs["mes_type"], kwargs["value"])
		else:
			mtn_data = MTN_SNM_Data(kwargs["mes_group"], kwargs["mes_type"])
		return mtn_data

class ISUP_Message_Builder:

	def __init__(self):
		self.mandatory_part_lengths = self.Define_Mandatory_Part_Lengths()
		self.parameter_builders = self.Define_Parameter_Builders()
		self.address_signals = (0,1,2,3,4,5,6,7,8,9,11,12,15)

	def Define_Parameter_Builders(self):
		builders = {
		  "nature_of_connection_indicators" : self.Build_Nature_Of_Connection_Indicators,
		  "forward_call_indicators" : self.Build_Forward_Call_Indicators,
		  "calling_party_category" : self.Build_Calling_Party_Category,
		  "transmission_medium_requirement" : self.Build_Transmission_Medium_Requirement,
		  "called_party_number" : self.Build_Called_Party_Number,
		  "backward_call_indicators" : self.Build_Backward_Call_Indicators,
		  "cause_indicators" : self.Build_Cause_Indicators,
		  "range_and_status" : self.Build_Range_And_Status,
		  "subsequent_number" : self.Build_Subsequent_Number,
		  "circuit_group_supervision_message_type" : self.Build_Circuit_Group_Supervision_Message_Type
		}
		return builders

	def Define_Mandatory_Part_Lengths(self):
		#Код сообщения : количество обязательных параметров (фиксированных и переменных)
		lengths = {
		  1 : 5,
		  2 : 1,
		  6 : 1,
		  9 : 0,
		  12 : 1,
		  16 : 0,
		  17 : 0,
		  18 : 0,
		  19 : 0,
		  20 : 0,
		  21 : 0,		  
		  22 : 0,
		  23 : 1,
		  24 : 2,
		  25 : 2,
		  26 : 2,
		  27 : 2,
		  36 : 0,
		  41 : 1,
		  42 : 1,
		  46 : 0,
		  47 : 1,
		  48 : 0,
		  52 : 0,
		  53 : 0
		}
		return lengths

	def Build_Nature_Of_Connection_Indicators(self, value):
		if type(value) != int:
			raise ISUP_Error("nature_of_connection_indicators must be int value")
		else:
			return Nature_Of_Connection_Indicators(value)

	def Build_Forward_Call_Indicators(self, value):
		if type(value) != int:
			raise ISUP_Error("forward_call_indicators must be int value")
		else:
			return Forward_Call_Indicators(value)

	def Build_Calling_Party_Category(self, value):
		if type(value) != int:
			raise ISUP_Error("calling_party_category must be int value")
		else:
			return Calling_Party_Category(value)

	def Build_Transmission_Medium_Requirement(self, value):
		if type(value) != int:
			raise ISUP_Error("transmission_medium_requirement must be int value")
		else:
			return Transmission_Medium_Requirement(value)
	
	def Build_Circuit_Group_Supervision_Message_Type(self, value):
		if type(value) != int:
			raise ISUP_Error("circuit_group_supervision_message_type must be int value")
		else:
			return Circuit_Group_Supervision_Message_Type(value)

	def Check_Raw_Range_and_Status_Value(self, value):
		if type(value) != list and (len(value) != 1 or len(value) != 2):
			raise ISUP_Error("range and status value must be list by pattern: \"[byte1_range] or [byte1_range, (byte_status1, byte_statusN)]\"")
		elif type(value[0]) != int: 
			raise ISUP_Error("range value be integer")
		else:
			if len(value) == 2:
				pass
				#for status in value[1]: 
				#	if status not in range(0,256): 
				#		raise ISUP_Error("invalid status value (0, 255)")

	def Build_Range_And_Status(self, value):
		self.Check_Raw_Range_and_Status_Value(value)
		return Range_And_Status().Build(value)

	def Check_Raw_CDPN_Value(self, value):
#		try:
#			value[2] = str(value[2])
#			value[2] = tuple(map(int, value[2]))
#		except:
#			pass
		if type(value) != list or len(value) != 3:
			raise ISUP_Error("called_party_number value must be list by pattern: \"[byte1, byte2, (addr_sig1, addr_sigN)]\"")
		elif type(value[0]) != int or type(value[1]) != int or type(value[2]) != list:
			raise ISUP_Error("called_party_number_value must match the pattern: \"[byte1, byte2, (addr_sig1, addr_sigN)]\"")
		else:
			for address_signal in value[2]:
				if not address_signal in self.address_signals:
					raise ISUP_Error("invalid address signals list")

	def Build_Called_Party_Number(self, value):
		self.Check_Raw_CDPN_Value(value)
		return Called_Party_Number().Build(value)

	def Build_Backward_Call_Indicators(self, value):
		if type(value) != int:
			raise ISUP_Error("backward_call_indicators must be int value")
		else:
			return Backward_Call_Indicators(value)

	def Check_Raw_Cause_Indicators_Value(self, value):
		if type(value) != list or len(value) != 3:
			raise ISUP_Error("cause_indicators value must be a list by pattern: \"[byte1, byte2, diagnostic]\"")
		elif type(value[0]) != int or type(value[1]) != int:
			raise ISUP_Error("cause_indicators value must match the pattern: \"[byte1, byte2, diagnostic]\"") 

	def Build_Cause_Indicators(self, value):
		self.Check_Raw_Cause_Indicators_Value(value)
		return Cause_Indicators().Build(value)

	def Check_Raw_Subsequent_Number_Value(self, value):
		if type(value) != list:
			raise ISUP_Error("subsequent_number value must be a list by pattern: \"[addr_sig1, addr_sigN]\"")
		else:
			for address_signal in value:
				if not address_signal in self.address_signals:
					raise ISUP_Error("invalid address signals list")

	def Build_Subsequent_Number(self, value):
		self.Check_Raw_Subsequent_Number_Value(value)
		return Subsequent_Number().Build(value)

	def Parameters_Building(self, parameters_dict):
		parameters = []
		for key, value in parameters_dict.items():
			parameter = self.parameter_builders[key](value)
			parameters.append(parameter)
		return parameters

	def Form_Parameters_Dict(self, keys_list, parameters):
		parameters_dict = {}
		for key in keys_list:
			parameters_dict[key] = parameters[key]
		return parameters_dict 

	def Form_Keys_Lists(self, keys_list, mandatory_part_length):
		mandatory_keys_list = keys_list[1 : 1 + mandatory_part_length]
		optional_keys_list = keys_list[1 + mandatory_part_length:]
		return (mandatory_keys_list, optional_keys_list)

	def Get_Parameters_Keys(self, parameters):
		keys_list = []
		for key in parameters.keys():
			keys_list.append(key)
		return keys_list

	def Split_Parameters(self, parameters):
		try:
			mandatory_part_length = self.mandatory_part_lengths[parameters["mes_type"]]
		except KeyError:
			raise ISUP_Error("unknown or unsupported message type: \"%s\"" % parameters["mes_type"])
		else:
			parameters.pop("mes_type")
			keys_list = self.Get_Parameters_Keys(parameters)
			mandatory_keys_list, optional_keys_list = self.Form_Keys_Lists(keys_list, mandatory_part_length)
			mandatory_part = self.Form_Parameters_Dict(mandatory_keys_list, parameters)
			optional_part = self.Form_Parameters_Dict(optional_keys_list, parameters)
			return (mandatory_part, optional_part)

	def Build_Protocol_Data(self, kwargs):
		print("j1",kwargs)
		isup_data = ISUP_Data(kwargs["cic"], kwargs["mes_type"])
		mandatory_part, optional_part = self.Split_Parameters(kwargs)
		print("LLL", mandatory_part, "KKK", optional_part)
		isup_data.mandatory_parameters = self.Parameters_Building(mandatory_part)
		isup_data.optional_parameters = self.Parameters_Building(optional_part)
		#print("cic:", isup_data.cic)
		#print("mes_type:", isup_data.mes_type)
		#print("mandatory_parameters:", isup_data.mandatory_parameters)
		#print("optional_parameters:", isup_data.optional_parameters)
		return isup_data

class MTN_SNM_Binary_Convertor:

	def Convert_Service_Data(self, service_data):
		byteN = bytes()
		byte_len = bytes()
		mes_group_value = self.Convert_Bin_To_Decimal(bin(service_data.mes_group))
		mes_type_value = self.Convert_Bin_To_Decimal(bin(service_data.mes_type)+'0000')
		byte1_value = mes_group_value + mes_type_value
		byte1 = byte1_value.to_bytes(1, byteorder="big")
		if service_data.value is not None:
			if type(service_data.value) == str or type(service_data.value) == int:			
				len_value = len(str(service_data.value))
				#if len_value < 1 or len_value > 30:
				if len_value < 1 or len_value > 15:
					raise ISUP_Error("len value must be in range of 1 and 30")
				#if len_value % 2 != 0:
				#	len_value += 1
				#	str_servdata = '0' + str(service_data.value)
				#else:
				str_servdata = str(service_data.value)
				n=0
				while n<(len_value):
					byteN += str_servdata[n].encode()
					n += 1
					#byteN += int(self.Convert_Str_To_Hex(str_servdata[n] + '0') + self.Convert_Str_To_Hex(str_servdata[n+1])).to_bytes(1, byteorder="big")
					#n += 2
				#bin_len_value = self.Convert_Bin_To_Decimal(bin(len_value//2)+'0000')
				bin_len_value = self.Convert_Bin_To_Decimal(bin(len_value)+'0000')
				byte_len = bin_len_value.to_bytes(1, byteorder="big")
			elif type(service_data.value) == bytes:
				print("type bytes")
				len_value = len(service_data.value)
				bin_len_value = self.Convert_Bin_To_Decimal(bin(len_value//2)+'0000')
				byte_len = bin_len_value.to_bytes(1, byteorder="big")
				byteN = service_data.value
			else:
				print("bug")
				pass
		binary_service_data = byte1 + byte_len + byteN
		service_data_length = len(binary_service_data)
		return (binary_service_data, service_data_length)

	def Convert_Bin_To_Decimal(self, bin_value):
		if not bin_value:
			bin_value = "0"
		decimal_value = int(bin_value, 2)
		return decimal_value

	def Convert_Str_To_Hex(self, hex_value):
		if not hex_value:
			hex_value = "0"
		try:
			decimal_value = int(hex_value, 16)
		except:
			raise ISUP_Error("Value must be in hex range from 0 to F")
		return decimal_value

class ISUP_Binary_Convertor:

	def __init__(self):
		self.parameter_convertors = self.Define_Parameter_Convertors()
		self.fixed_parameters_number = self.Define_Mandatory_Fixed_Parameters_Numbers()
		self.optional_parameters_possible = self.Define_Optional_Part_Possibility()
		self.isup_header_length = 3

	def Define_Parameter_Convertors(self):
		convertors = {
		  Nature_Of_Connection_Indicators : self.Convert_Nature_Of_Connection_Indicators,
		  Forward_Call_Indicators : self.Convert_Forward_Call_Indicators,
		  Calling_Party_Category : self.Convert_Calling_Party_Category,
		  Transmission_Medium_Requirement : self.Convert_Transmission_Medium_Requirement,
		  Called_Party_Number : self.Convert_Called_Party_Number,
		  Backward_Call_Indicators : self.Convert_Backward_Call_Indicators,
		  Range_And_Status : self.Convert_Range_And_Status_Indicators,
		  Cause_Indicators : self.Convert_Cause_Indicators,
		  Subsequent_Number : self.Convert_Subsequent_Number,
		  Circuit_Group_Supervision_Message_Type : self.Convert_Circuit_Group_Supervision_Message_Type
		}
		return convertors

	def Define_Mandatory_Fixed_Parameters_Numbers(self):
		#Код сообщения : количество обязательных фиксированных параметров
		lengths = {
		  1 : 4,
		  2 : 0,
		  6 : 1,
		  9 : 0,
		  12 : 0,
		  16 : 0,
		  17 : 0,
		  18 : 0,
		  19 : 0,
		  20 : 0,
		  21 : 0,		  
		  22 : 0,
		  23 : 0,
		  24 : 1,
		  25 : 1,
		  26 : 1,
		  27 : 1,
		  36 : 0,
		  41 : 0,
		  42 : 0,
		  46 : 0,
		  47 : 0,
		  48 : 0,
		  52 : 0,
		  53 : 0
		}
		return lengths

	def Define_Optional_Part_Possibility(self):
		#Код сообщения : количество обязательных фиксированных параметров
		possible = {
		  1 : True, #IAM
		  2 : True, #SAM
		  6 : True, #ACM
		  9 : True, #ANM
		  12 : True, #Release
		  16 : True, #RLC
		  17 : False, #CCR
		  18 : False, #RSC
		  19 : False, #BLO
		  20 : False, #UBL
		  21 : False, #BLA		  
		  22 : False, #UBA
		  23 : False, #GRS
		  24 : False, #CGB
		  25 : False, #CGU
		  26 : False, #CGBA
		  27 : False, #CGUA
		  36 : False, #Overload, (national use)
		  46 : False, #Unequipped circuit identification code, (national use)
		  41 : False, #GRA
		  42 : False, #GRU
		  47 : True, #CFN
		  48 : False, #Loop back acknowledgement, (national use)
		  52 : True,
		  53 : True
		}
		return possible

	def Convert_Range_And_Status_Indicators(self, parameter):
		byte1_value = parameter.range
		byte1 = byte1_value.to_bytes(1, byteorder="big")
		binary_status = self.Convert_Status(parameter.status)
		binary_parameter = byte1 + binary_status
		return binary_parameter

	def Convert_Status(self, status):
		binary_status = b""
		for _value in status:
			binary_status = _value.to_bytes(1, byteorder="big")
			binary_status += binary_status
		return binary_status

	def Convert_Nature_Of_Connection_Indicators(self, parameter):
		parameter_length = 1
		parameter_value = parameter.satellite_indicator
		parameter_value += parameter.continuity_check_indicator << 2
		parameter_value += parameter.echo_control_device_indicator << 4
		parameter_value += parameter.spare << 5
		binary_parameter = parameter_value.to_bytes(parameter_length, byteorder="big")
		return binary_parameter

	def Convert_Forward_Call_Indicators(self, parameter):
		parameter_length = 2
		parameter_value = parameter.isdn_access_indicator
		parameter_value += parameter.sccp_method_indicator << 1
		parameter_value += parameter.spare << 3
		parameter_value += parameter.for_national_use << 4
		parameter_value += parameter.national_international_call_indicator << 8
		parameter_value += parameter.end_to_end_method_indicator << 9
		parameter_value += parameter.interworking_indicator << 11
		parameter_value += parameter.end_to_end_information_indicator << 12
		parameter_value += parameter.isdn_user_part_indicator << 13
		parameter_value += parameter.isdn_user_part_preference_indicator << 14
		binary_parameter = parameter_value.to_bytes(parameter_length, byteorder="big")
		return binary_parameter

	def Convert_Calling_Party_Category(self, parameter):
		parameter_length = 1
		binary_parameter = parameter.value.to_bytes(parameter_length, byteorder="big")
		return binary_parameter

	def Convert_Transmission_Medium_Requirement(self, parameter):
		parameter_length = 1
		binary_parameter = parameter.value.to_bytes(parameter_length, byteorder="big")
		return binary_parameter

	def Convert_Circuit_Group_Supervision_Message_Type(self, parameter):
		parameter_length = 1
		parameter_value = parameter.circuit_group_supervision_message_type_indicator
		parameter_value += parameter.spare
		binary_parameter = parameter_value.to_bytes(parameter_length, byteorder="big")
		return binary_parameter

	def Convert_Address_Signals(self, digits):
		binary_address_signals = b""
		if len(digits) % 2 != 0:
			digits.append(0)
		pairs_number = len(digits) // 2
		for index in range(0, len(digits), 2):
			digit_pair = digits[index:index+2]
			digit_pair_value = digit_pair[0] + (digit_pair[1] << 4)
			binary_digit_pair = digit_pair_value.to_bytes(1, byteorder="big")
			binary_address_signals += binary_digit_pair
		return binary_address_signals

	def Convert_Called_Party_Number(self, parameter):
		byte1_value = parameter.nature_of_address_indicator
		byte1_value += parameter.odd_even_indicator << 7
		byte2_value = parameter.spare
		byte2_value += parameter.numbering_plan_indicator << 4
		byte2_value += parameter.inn_indicator << 7
		byte1 = byte1_value.to_bytes(1, byteorder="big")
		byte2 = byte2_value.to_bytes(1, byteorder="big")
		binary_indicators = byte1 + byte2
		binary_digits = self.Convert_Address_Signals(parameter.digits)
		binary_parameter = binary_indicators + binary_digits
		return binary_parameter

	def Convert_Backward_Call_Indicators(self, parameter):
		parameter_length = 2
		parameter_value = parameter.charge_indicator << 8
		parameter_value += parameter.called_party_status_indicator << 10
		parameter_value += parameter.called_party_category_indicator << 12
		parameter_value += parameter.end_to_end_method_indicator << 14
		parameter_value += parameter.interworking_indicator
		parameter_value += parameter.end_to_end_information_indicator << 1
		parameter_value += parameter.isdn_user_part_indicator << 2
		parameter_value += parameter.holding_indicator << 3
		parameter_value += parameter.isdn_access_indicator << 4
		parameter_value += parameter.echo_control_device_indicator << 5
		parameter_value += parameter.sccp_method_indicator << 6
		binary_parameter = parameter_value.to_bytes(parameter_length, byteorder="big")
		return binary_parameter

	def Convert_Cause_Indicators(self, parameter):
		byte1_value = parameter.location
		byte1_value += parameter.spare << 4
		byte1_value += parameter.coding_standard << 5
		byte1_value += 128 #extention indicator
		byte2_value = parameter.cause_value
		byte2_value += 128 #extention indicator
		byte1 = byte1_value.to_bytes(1, byteorder="big")
		byte2 = byte2_value.to_bytes(1, byteorder="big")
		diagnostic = b""
		binary_parameter = byte1 + byte2 + diagnostic
		return binary_parameter

	def Convert_Subsequent_Number(self, parameter):
		if len(parameter.digits) % 2 == 0:
			odd_even_indicator = 0
		else:
			odd_even_indicator = 1
		byte1 = (0 + (odd_even_indicator << 7)).to_bytes(1, byteorder="big")
		binary_digits = self.Convert_Address_Signals(parameter.digits)
		binary_parameter = byte1 + binary_digits
		return binary_parameter

	def Convert_Optional_Parameters(self, parameters):
		return b""

	def Get_Common_Mandatory_Variable_Parameters_Length(self, parameters_dict):
		common_length = 0
		for parameter,length in parameters_dict.items():
			common_length += length
		return common_length

	def Convert_Mandatory_Variable_Parameters(self, parameters):
		mandatory_variable_parameters = {}
		for parameter in parameters:
			binary_parameter = self.parameter_convertors[type(parameter)](parameter)
			parameter_length = len(binary_parameter)
			binary_parameter = parameter_length.to_bytes(1, byteorder="big") + binary_parameter
			mandatory_variable_parameters[binary_parameter] = parameter_length + 1
		common_parameters_length = self.Get_Common_Mandatory_Variable_Parameters_Length(mandatory_variable_parameters)
		return (mandatory_variable_parameters, common_parameters_length)

	def Get_Previous_Parameters_Length(self, index, mandatory_variable_parameters):
		parameters_keys = []
		previous_parameters_length = 0
		for parameter_key in mandatory_variable_parameters.keys():
			parameters_keys.append(parameter_key)
		parameters_keys = parameters_keys[:index-1]
		for parameter_key in parameters_keys:
			previous_parameters_length += mandatory_variable_parameters[parameter_key]
		return previous_parameters_length

	def Get_Binary_Pointers_Values(self, pointers_values):
		binary_pointers = b""
		for pointer_value in pointers_values:
			#if pointer_value:
			binary_pointers += pointer_value.to_bytes(1, byteorder="big")
		return binary_pointers

	def Get_Binary_Variable_Parameters(self, mandatory_variable_parameters_dict):
		binary_parameters = b""
		for parameter in mandatory_variable_parameters_dict.keys():
			binary_parameters += parameter
		return binary_parameters

	def Convert_Variable_Part(self, mandatory_parameters, optional_pointer, optional_part):
		pointers_number = len(mandatory_parameters) 
		if pointers_number == 1:
			mand_pointer = True
		else:
			mand_pointer = False
		#if optional_pointer == True:
		#	pointers_number += 1
		#pointers_values = [None] * pointers_number
		print("JJJ", mandatory_parameters, optional_pointer, optional_part, pointers_number)
		pointers_values = list()
		mandatory_variable_parameters, mandatory_parameters_length = self.Convert_Mandatory_Variable_Parameters(mandatory_parameters)
		if mand_pointer == True and optional_pointer == False:
			pointers_values = [1]
		elif mand_pointer == False and optional_pointer == False:
			pointers_values = []
		elif mand_pointer == True and optional_pointer == True:
			pointers_values = [2]
			if not optional_part:
				pointers_values.append(0)
			else:
				pointers_values.append(mandatory_parameters_length + 1)
		elif mand_pointer == False and optional_part == False:
			pointers_values = [0]
		else:
			pointers_values = [1]
		print ("JJJ1", pointers_values)
#		for index in range(1, pointers_number + 1):
#			if index == 1 and not optional_pointer:
#				pointers_values[index-1] = 1
#				pass 
#			elif index == 1 and not optional_part:
				#pointers_values[-index] = 0
#			elif index == 1:
#				pointers_values[-index] = mandatory_parameters_length + index
#			else:
#				previous_parameters_length = self.Get_Previous_Parameters_Length(index, mandatory_variable_parameters)
#				pointers_values[-index] = mandatory_parameters_length - previous_parameters_length + index
		binary_parameters = self.Get_Binary_Variable_Parameters(mandatory_variable_parameters)
		pointers = self.Get_Binary_Pointers_Values(pointers_values)
		variable_part = pointers + binary_parameters
		return variable_part

	def Convert_Mandatory_Fixed_Part(self, parameters):
		binary_parameters = b""
		for parameter in parameters:
			print ("kkk",parameter)
			binary_parameter = self.parameter_convertors[type(parameter)](parameter)
			binary_parameters += binary_parameter
		return binary_parameters

	def Convert_Bin_To_Decimal(self, bin_value):
		if not bin_value:
			bin_value = "0"
		decimal_value = int(bin_value, 2)
		return decimal_value

	def Form_CIC_Bytes(self, cic_value):
		bin_cic_value = bin(cic_value)[2:]
		bin_cic_length = len(bin_cic_value)
		if bin_cic_length <= 8:
			byte1_value = self.Convert_Bin_To_Decimal(bin_cic_value)
			byte2_value = 0
		else:
			byte1_value = self.Convert_Bin_To_Decimal(bin_cic_value[bin_cic_length-8:])
			byte2_value = self.Convert_Bin_To_Decimal(bin_cic_value[:bin_cic_length-8])
		return (byte1_value, byte2_value)

	def Convert_CIC(self, cic_value):
		if cic_value < 0 or cic_value > 4095:
			raise ISUP_Error("cic value must be in range of 0 and 4095")
		byte1_value, byte2_value = self.Form_CIC_Bytes(cic_value) 
		byte1 = byte1_value.to_bytes(1, byteorder="big")
		byte2 = byte2_value.to_bytes(1, byteorder="big")
		binary_cic = byte1 + byte2
		return binary_cic

	def Convert_Service_Data(self, service_data):
		cic = self.Convert_CIC(service_data.cic)
		mes_type = service_data.mes_type.to_bytes(1, byteorder="big")
		isup_header = cic + mes_type
		number_of_fixed_parameters = self.fixed_parameters_number[service_data.mes_type]
		fixed_part = self.Convert_Mandatory_Fixed_Part(service_data.mandatory_parameters[:number_of_fixed_parameters])
		optional_part = self.Convert_Optional_Parameters(service_data.optional_parameters)
		possible_optional = self.optional_parameters_possible[service_data.mes_type]
		if service_data.optional_parameters == [] and possible_optional == False:
			variable_part = self.Convert_Variable_Part(service_data.mandatory_parameters[number_of_fixed_parameters:], optional_pointer=False, optional_part=False)
		elif service_data.optional_parameters == [] and possible_optional == True:
			variable_part = self.Convert_Variable_Part(service_data.mandatory_parameters[number_of_fixed_parameters:], optional_pointer=True, optional_part=False)
		else:
			variable_part = self.Convert_Variable_Part(service_data.mandatory_parameters[number_of_fixed_parameters:], optional_pointer=True, optional_part=bool(optional_part))
		binary_service_data = isup_header + fixed_part + variable_part + optional_part
		service_data_length = len(binary_service_data)
		return (binary_service_data, service_data_length)

class ISUP_Error(Exception):

	def __init__(self, description):
		self.description = description

class Binary_Convertor:

	def __init__(self):
		self.sccp_binary_convertor = SCCP_Binary_Convertor()
		self.isup_binary_convertor = ISUP_Binary_Convertor()
		self.mtn_snm_binary_convertor = MTN_SNM_Binary_Convertor()
#		self.common_m2ua_header_pattern = struct.Struct(">B B B B L")
#		self.m2ua_parameter_header_pattern = struct.Struct(">H H")
#		self.m2ua_padding_parameter_pattern = struct.Struct(">B")
		self.mtp3_routing_label_pattern = struct.Struct(">B B B B")
		self.m2ua_parameter_header_length = 4
#		self.m2ua_header_length = 8
		self.mtp3_data_length = 5

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

#	def Create_M2UA_Parameter_Padding(self, padding_bytes_number):
#		padding_value = (0)
#		padding_byte = self.m2ua_padding_parameter_pattern.pack(padding_value)
#		padding = padding_byte * padding_bytes_number
#		return padding

#	def Searching_For_Multiple_Length(self, parameter_length):
#		initial_parameter_length = parameter_length
#		for i in range(1,4):
#			parameter_length = initial_parameter_length + i
#			if parameter_length % 4 == 0:
#				multiple_length = parameter_length
#				break
#		else:
#			raise ISUP_Error("padding bytes counting error")
#		return multiple_length

#	def Forming_M2UA_Parameter_Padding(self, parameter_length):
#		if parameter_length % 4 == 0:
#			return b""
#		else:
#			multiple_length = self.Searching_For_Multiple_Length(parameter_length)
#			padding_bytes_number = multiple_length - parameter_length
#			padding = self.Create_M2UA_Parameter_Padding(padding_bytes_number)
#			return padding

#	def String_Parameter_Length_Check(self, string_parameter_value, parameter_length):
#		if len(string_parameter_value) != parameter_length - self.m2ua_parameter_header_length:
#			raise ISUP_Error("m2ua str parameter length \"%s\" is bigger than allowable length" % len(string_parameter_value))

#	def Convert_String_Parameter_Value(self, parameter_value, parameter_length=None):
#		binary_parameter_value = parameter_value.encode("utf-8")
#		if parameter_length:
#			binary_parameter_length = parameter_length
#			self.String_Parameter_Length_Check(binary_parameter_value, parameter_length)
#		else:
#			binary_parameter_length = len(binary_parameter_value) + self.m2ua_parameter_header_length
#		return (binary_parameter_value, binary_parameter_length)

#	def Convert_Int_Parameter_Value(self, parameter_value, parameter_length=None):
#		if parameter_length:
#			binary_parameter_length = parameter_length
#			try:
#				binary_parameter_value = parameter_value.to_bytes(parameter_length - self.m2ua_parameter_header_length, byteorder="big")
#			except OverflowError:
#				raise ISUP_Error("m2ua int parameter value is \"%s\" is bigger than allowable value"% parameter_value)
#		else:
#			value_length = self.Bytes_Number_Counting(parameter_value)
#			binary_parameter_value = parameter_value.to_bytes(value_length, byteorder="big")
#			binary_parameter_length = value_length + self.m2ua_parameter_header_length
#		return (binary_parameter_value, binary_parameter_length)

#	def Convert_List_Parameter_Value(self, parameters_list):
#		total_parameter_length = self.m2ua_parameter_header_length
#		total_binary_parameter_value = b""
#		for parameter in parameters_list:
#			if type(parameter) == int:
#				binary_parameter_value, dummy = self.Convert_Int_Parameter_Value(parameter, parameter_length=8)
#				total_binary_parameter_value = total_binary_parameter_value + binary_parameter_value
#				total_parameter_length = total_parameter_length + 4
#			elif type(parameter) == M2UA_Parameter:
#				binary_parameter, binary_parameter_length = self.Convert_M2UA_Parameter(parameter)
#				total_binary_parameter_value = total_binary_parameter_value + binary_parameter
#				total_parameter_length = total_parameter_length + binary_parameter_length
#			else:
#				raise M2UA_Error("unsupported element type in parameters list")
#		return (total_binary_parameter_value, total_parameter_length)

	def Convert_SIO_Data(self, sio):
		sio_value = sio.service_indicator
		sio_value += sio.spare << 4 
		sio_value += sio.network_indicator << 6
		binary_sio_data = sio_value.to_bytes(1, byteorder="big")
		return binary_sio_data

	def Convert_Decimal_To_Bin(self, decimal_value, length):
		bin_value = bin(decimal_value)[2:]
		end_of_padding = False
		while not end_of_padding:
			if len(bin_value) != length:
				bin_value = "0" + bin_value
			else:
				end_of_padding = True
		return bin_value

	def Convert_Routing_Label_Data(self, routing_label):
		dpc = self.Convert_Decimal_To_Bin(routing_label.dpc, length=14)
		opc = self.Convert_Decimal_To_Bin(routing_label.opc, length=14)
		link_selector = self.Convert_Decimal_To_Bin(routing_label.link_selector, length=4)
		byte4_value = int(opc[:4], 2) + (int(link_selector,2) << 4)
		byte3_value = int(opc[4:12], 2)
		byte2_value = int(dpc[:6], 2) + (int(opc[-2:], 2) << 6)
		byte1_value = int(dpc[-8:],2)
		bytes_values = (byte1_value, byte2_value, byte3_value, byte4_value)
		binary_routing_label_data = self.mtp3_routing_label_pattern.pack(*bytes_values)
		return binary_routing_label_data

	def Convert_Service_Data(self, service_indicator, service_data):
		if service_indicator == 3:
			return self.sccp_binary_convertor.Convert_Service_Data(service_data)
		elif service_indicator == 5:
			return self.isup_binary_convertor.Convert_Service_Data(service_data)
		elif service_indicator == 0 or service_indicator == 1:
			return self.mtn_snm_binary_convertor.Convert_Service_Data(service_data)

	def Convert_MTP3_Data(self, mtp3_data):
		mtp3_binary_data = self.Convert_SIO_Data(mtp3_data.sio) + self.Convert_Routing_Label_Data(mtp3_data.routing_label)
		service_data, service_data_length = self.Convert_Service_Data(mtp3_data.sio.service_indicator, mtp3_data.service_data) 
		binary_parameter_value = mtp3_binary_data + service_data
		binary_parameter_length = self.m2ua_parameter_header_length + self.mtp3_data_length + service_data_length
		return (binary_parameter_value, binary_parameter_length)

#	def M2UA_Parameter_Forming(self, parameter_value, parameter_length=None):
#		if type(parameter_value) == str:
#			binary_parameter_value, binary_parameter_length = self.Convert_String_Parameter_Value(parameter_value, parameter_length)
#		elif type(parameter_value) == int:
#			binary_parameter_value, binary_parameter_length = self.Convert_Int_Parameter_Value(parameter_value, parameter_length)
#		elif type(parameter_value) == list:
#			binary_parameter_value, binary_parameter_length = self.Convert_List_Parameter_Value(parameter_value)
#		elif type(parameter_value) == MTP3_Data:
#			binary_parameter_value, binary_parameter_length = self.Convert_MTP3_Data(parameter_value)
#		else:
#			raise M2UA_Error("unsupported type of m2ua parameter")
#		return (binary_parameter_value, binary_parameter_length)

#	def Convert_M2UA_Parameter_Value(self, object_parameter):
#		if not object_parameter.length:
#			binary_parameter_value, parameter_length = self.M2UA_Parameter_Forming(object_parameter.value)
#		elif object_parameter.length < 4:
#			raise M2UA_Error("m2ua parameter length must not be less than 4")
#		elif object_parameter.length == 4:
#			binary_parameter_value = b""
#			parameter_length = object_parameter.length
#		else:
#			binary_parameter_value, parameter_length = self.M2UA_Parameter_Forming(object_parameter.value, object_parameter.length)
#		return (binary_parameter_value, parameter_length)

#	def Convert_M2UA_Parameter(self, object_parameter): 
#		binary_parameter_value, parameter_length = self.Convert_M2UA_Parameter_Value(object_parameter)
#		packet_values = (object_parameter.tag, parameter_length)
#		binary_parameter_header = self.m2ua_parameter_header_pattern.pack(*packet_values)
#		padding = self.Forming_M2UA_Parameter_Padding(parameter_length)
#		binary_parameter = binary_parameter_header + binary_parameter_value + padding
#		return (binary_parameter, parameter_length + len(padding))

#	def Get_M2UA_Parameters_Info(self, object_message):
#		parameters_length = 0
#		binary_parameters_list = []
#		for parameter in object_message.parameters:
#			binary_parameter, parameter_length = self.Convert_M2UA_Parameter(parameter)
#			binary_parameters_list.append(binary_parameter)
#			parameters_length = parameters_length + parameter_length
#		return (binary_parameters_list, parameters_length)

#	def Get_M2UA_Parameters_String(self, parameters_list):
#		parameters_string = b""
#		for parameter in parameters_list:
#			parameters_string = parameters_string + parameter
#		return parameters_string 

#	def Convert_M2UA_Message(self, object_message):
#		binary_parameters_list, parameters_length = self.Get_M2UA_Parameters_Info(object_message)
#		object_message.length = self.m2ua_header_length + parameters_length 
#		packet_values = (object_message.version, object_message.spare, object_message.mes_class, object_message.mes_type, object_message.length)
#		m2ua_header = self.common_m2ua_header_pattern.pack(*packet_values)
#		m2ua_parameters = self.Get_M2UA_Parameters_String(binary_parameters_list)
#		m2ua_message = m2ua_header + m2ua_parameters
#		return m2ua_message

class Message_Builder:

	def __init__(self):
		self.mtp3 = None
		self.sccp_builder = SCCP_Message_Builder()
		self.isup_builder = ISUP_Message_Builder()
		self.mtn_snm_builder = MTN_SNM_Builder()
		self.convertor = Binary_Convertor()

	def _MTP3_ISUP_make_message_handler(self):
		return { "SLTM" : [self.Build_SLTM, 1],
				 "SLTA" : [self.Build_SLTA, 2],
				 "TRA" : [self.Build_TRA, 1],
				 "APT" : [self.Build_Message, 65],
				 "ACM" : [self.Build_Message, 6],
				 "ANM" : [self.Build_Message, 9],
				 "BLA" : [self.Build_Message, 21],
				 "BLO" : [self.Build_Message, 19],
				 "CCR" : [self.Build_Message, 17],
				 "CFN" : [self.Build_Message, 47],
				 "CRG" : [self.Build_Message, 49],
				 "CGB" : [self.Build_Message, 24],
				 "CGU" : [self.Build_Message, 25],
				 "CGBA" : [self.Build_Message, 26],
				 "CGUA" : [self.Build_Message, 27], 
				 "CON" : [self.Build_Message, 7],
				 "COT" : [self.Build_Message, 5],
				 "CPG" : [self.Build_Message, 44],
				 "CQM" : [self.Build_Message, 42],
				 "CQR" : [self.Build_Message, 43],
				 "FAA" : [self.Build_Message, 32],
				 "FAC" : [self.Build_Message, 33],
				 "FAR" : [self.Build_Message, 31],
				 "FRJ" : [self.Build_Message, 21],
				 "FOT" : [self.Build_Message, 8],
				 "GRS" : [self.Build_Message, 23],
				 "GRA" : [self.Build_Message, 41],				 
				 "IAM" : [self.Build_Message, 1],
				 "INF" : [self.Build_Message, 4],
				 "INR" : [self.Build_Message, 3],
				 "IDR" : [self.Build_Message, 54],
				 "IDS" : [self.Build_Message, 55],
				 "LPA" : [self.Build_Message, 36],
				 "LPP" : [self.Build_Message, 64],
				 "NRM" : [self.Build_Message, 50],
				 "OLM" : [self.Build_Message, 48],
				 "PRI" : [self.Build_Message, 66],
				 "PAM" : [self.Build_Message, 40],
				 "REL" : [self.Build_Message, 12],
				 "RES" : [self.Build_Message, 14],
				 "RLC" : [self.Build_Message, 16],
				 "RSC" : [self.Build_Message, 18],
				 "SGM" : [self.Build_Message, 56],
				 "SAM" : [self.Build_Message, 2],
				 "SUS" : [self.Build_Message, 13],
				 "UBL" : [self.Build_Message, 20],
				 "UBLA" : [self.Build_Message, 22],
				 "UCIC" : [self.Build_Message, 46],
				 "USR" : [self.Build_Message, 47],
				 "UPA" : [self.Build_Message, 53],
				 "UPT" : [self.Build_Message, 52] }


	def Define_MTP3_Properties(self, opc, dpc, link_selector, network_indicator):
		self.mtp3 = MTP3_Data()
		self.mtp3.sio = self.mtp3.Service_Information_Octet(network_indicator=network_indicator)
		self.mtp3.routing_label = self.mtp3.Routing_Label(dpc=dpc, opc=opc, link_selector=link_selector)

	def Build_Service_Data(self, service_indicator, kwargs):
		if service_indicator == 3:
			raise ISUP_Error("SCCP service does not supported now")
		elif service_indicator == 5:
			service_data = self.isup_builder.Build_Protocol_Data(kwargs)
			return service_data
		elif service_indicator == 1 or service_indicator == 0:
			service_data = self.mtn_snm_builder.Build_MTN_SNM_Data(kwargs)
			return service_data
		else:
			raise ISUP_Error("Service does not supported now")

# Mainantance

	def Build_SLTA(self, mes_type, protocol_data):
		arguments = dict()
		self.Define_MTP3_Properties(opc=protocol_data["opc"], dpc=protocol_data["dpc"], link_selector=protocol_data["sls"], network_indicator=protocol_data["ni"])
		overlay_data = self.mtp3
		overlay_data.sio.service_indicator = 1
		arguments["mes_group"] = 1
		arguments["mes_type"] = mes_type
		arguments["value"] = protocol_data["test_message"]
		overlay_data.service_data = self.Build_Service_Data(service_indicator=overlay_data.sio.service_indicator, kwargs = arguments)
		return overlay_data

	def Build_SLTM(self, mes_type, protocol_data):
		arguments = dict()
		self.Define_MTP3_Properties(opc=protocol_data["opc"], dpc=protocol_data["dpc"], link_selector=protocol_data["sls"], network_indicator=protocol_data["ni"])
		overlay_data = self.mtp3
		overlay_data.sio.service_indicator = 1
		arguments["mes_group"] = 1
		arguments["mes_type"] = 1
		arguments["value"] = protocol_data["test_message"]
		overlay_data.service_data = self.Build_Service_Data(service_indicator=overlay_data.sio.service_indicator, kwargs = arguments)
		return overlay_data

	def Build_TRA(self, mes_type, protocol_data):
		arguments = dict()
		self.Define_MTP3_Properties(opc=protocol_data["opc"], dpc=protocol_data["dpc"], link_selector=protocol_data["sls"], network_indicator=protocol_data["ni"])
		overlay_data = self.mtp3
		overlay_data.sio.service_indicator = 0
		arguments["mes_group"] = 7
		arguments["mes_type"] = 1
		overlay_data.service_data = self.Build_Service_Data(service_indicator=overlay_data.sio.service_indicator, kwargs = arguments)
		return overlay_data

# ISUP

	def Build_Message(self, mes_type, protocol_data):
		arguments = dict()
		self.Define_MTP3_Properties(opc=protocol_data["opc"], dpc=protocol_data["dpc"], link_selector=protocol_data["sls"], network_indicator=protocol_data["ni"])
		overlay_data = self.mtp3
		overlay_data.sio.service_indicator = 5
		arguments = protocol_data
		arguments.pop("opc")
		arguments.pop("dpc")
		arguments.pop("sls")
		arguments.pop("ni")
		arguments.pop("message")
		arguments.update({"mes_type" : mes_type})
		overlay_data.service_data = self.Build_Service_Data(service_indicator=overlay_data.sio.service_indicator, kwargs = arguments)
		return overlay_data


#	def Build_IAM_Message(self, protocol_data):
#		arguments = dict()
#		self.Define_MTP3_Properties(opc=protocol_data["opc"], dpc=protocol_data["dpc"], link_selector=protocol_data["sls"], network_indicator=protocol_data["ni"])
#		overlay_data = self.mtp3
#		overlay_data.sio.service_indicator = 1
#		arguments = protocol_data
#		arguments.update(["mes_type"], 1)
#		arguments["cic"] = protocol_data["cic"]
#		arguments["forward_call_indicators"] = protocol_data["forward_call_indicators"]
#		arguments["calling_party_category"] = protocol_data["calling_party_category"]
#		arguments["transmission_medium_requirement"] = protocol_data["transmission_medium_requirement"]
#		arguments["called_party_number"] = protocol_data["called_party_number"]
#		overlay_data.service_data = self.Build_Service_Data(service_indicator=5, kwargs = arguments)
#		return overlay_data
#
#	def Build_ACM_Message(self, protocol_data):
#		arguments = dict()
#		self.Define_MTP3_Properties(opc=protocol_data["opc"], dpc=protocol_data["dpc"], link_selector=protocol_data["sls"], network_indicator=protocol_data["ni"])
#		overlay_data = self.mtp3
#		overlay_data.sio.service_indicator = 1
#		arguments = protocol_data
#		arguments.update(["mes_type"], 6)
#		overlay_data.service_data = self.Build_Service_Data(service_indicator=5, kwargs = arguments)
#		return overlay_data
