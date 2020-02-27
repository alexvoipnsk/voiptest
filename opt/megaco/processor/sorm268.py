import struct
import binascii
import processor.sorm.command as command
import processor.sorm.message1 as message1
import processor.sorm.constants as const
import processor.sorm.text as text

class Message_Builder:

	def __init__(self):
		self.version = 268
		
	def _SORM_make_command_handler(self):
		return { 1 : self._Build_command1, 
		         2 : self._Build_command2,
		         3 : self._Build_command3,
		         4 : self._Build_command4,
		         5 : self._Build_command5,
		         6 : self._Build_command6,
		         7 : self._Build_command7,
		         8 : self._Build_command8,
		         9 : self._Build_command9,
		         10 : self._Build_command10,
		         11 : self._Build_command11,
		         12 : self._Build_command12,
		         13 : self._Build_command13, 
		         14 : self._Build_command14,
		         15 : self._Build_command15,
		         16 : self._Build_command16,
		         17 : self._Build_command17 }

	def _Build_command1(self, header):
		self._checkHeader(header[0], header[1])
		passwd = str(header[1])
		commBytes = command.CmdSORMStart({ const.Header.SORM_NUMBER: header[0], const.Header.PASSWORD: passwd})
		return bytes(commBytes)

	def _Build_command2(self, header):
		self._checkHeader(header[0], header[1])
		passwd = str(header[1])
		commBytes = command.CmdSORMStop({ const.Header.SORM_NUMBER: header[0], const.Header.PASSWORD: passwd})
		return bytes(commBytes)

	def _Build_command3(self, header, new_password):
		self._checkHeader(header[0], header[1])
		passwd = str(header[1])
		if type(new_password)!=int:
			raise SORM_Error("Invalid value 'NEW_PASSWORD': {0}. It must be one2six'length 'INTEGER' in range [0-999999]".format(new_password))
		if not(0<=new_password<=999999):
			raise SORM_Error("Invalid value 'NEW_PASSWORD': {0}. It must consist of one2six 'INTEGER' values in range [0-9]".format(new_password))
		newpasswd = str(new_password)
		commBytes = command.CmdPasswordSet({ const.Header.SORM_NUMBER: header[0], const.Header.PASSWORD: passwd, const.Payload.NEW_PASSWORD: newpasswd})
		return bytes(commBytes)

	def _Build_command4(self, header, line_group_number, line_group_type, line_a_number, line_b_number=255):
		self._checkHeader(header[0], header[1])
		passwd = str(header[1])
		self._checkLineNumber(line_a_number, line_b_number)
		self._checkLineGroupNumber(line_group_number)
		type_ksl = self._lineGroupTypeDefine(line_group_type)
		commBytes = command.CmdControlLineAdd({ const.Header.SORM_NUMBER: header[0], const.Header.PASSWORD: passwd, const.Payload.LINE_GROUP_NUMBER: line_group_number, const.Payload.LINE_GROUP_TYPE: type_ksl, const.Payload.LINE_A_NUMBER: line_a_number, const.Payload.LINE_B_NUMBER: line_b_number})
		return bytes(commBytes)

	def _Build_command5(self, header, object_number, object_type, control_category, line_group_number, priority, phone_number=-1, phone_type='ff', linkset_number=65535):
		self._checkHeader(header[0], header[1])
		passwd = str(header[1])
		self._checkObjectNumber(object_number)
		self._checkLinksetNumber(linkset_number)
		self._checkLineGroupNumber(line_group_number)
		type_object = self._objectTypeDefine(object_type)
		type_phone = self._phoneTypeDefine(phone_type)
		category = self._controlCategoryDefine(control_category)
		prio = self._priorityDefine(priority)
		phone = self._checkPhoneNumber(phone_number)
		commBytes = command.CmdObjectAdd({ const.Header.SORM_NUMBER: header[0], const.Header.PASSWORD: passwd, const.Payload.OBJECT_NUMBER: object_number, const.Payload.OBJECT_TYPE: type_object, const.Payload.PHONE_TYPE: type_phone, const.Payload.PHONE_NUMBER: phone, const.Payload.LINKSET_NUMBER: linkset_number, const.Payload.CONTROL_CATEGORY: category, const.Payload.LINE_GROUP_NUMBER: line_group_number, const.Payload.PRIORITY: prio})
		return bytes(commBytes)

	def _Build_command6(self, header, object_number, object_type, phone_number=-1, phone_type='ff', linkset_number=65535):
		self._checkHeader(header[0], header[1])
		passwd = str(header[1])
		self._checkObjectNumber(object_number)
		self._checkLinksetNumber(linkset_number)
		type_object = self._objectTypeDefine(object_type)
		type_phone = self._phoneTypeDefine(phone_type)
		phone = self._checkPhoneNumber(phone_number)
		commBytes = command.CmdObjectRemove({ const.Header.SORM_NUMBER: header[0], const.Header.PASSWORD: passwd, const.Payload.OBJECT_NUMBER: object_number, const.Payload.OBJECT_TYPE: type_object, const.Payload.PHONE_TYPE: type_phone, const.Payload.PHONE_NUMBER: phone, const.Payload.LINKSET_NUMBER: linkset_number})
		return bytes(commBytes)

	def _Build_command7(self, header, call_number, object_number, object_type, line_group_number):
		self._checkHeader(header[0], header[1])
		passwd = str(header[1])
		self._checkObjectNumber(object_number)
		self._checkCallNumber(call_number)
		self._checkLineGroupNumber(line_group_number)
		type_object = self._objectTypeDefine(object_type)
		commBytes = command.CmdControlLineConnect({ const.Header.SORM_NUMBER: header[0], const.Header.PASSWORD: passwd, const.Payload.CALL_NUMBER: call_number, const.Payload.OBJECT_NUMBER: object_number, const.Payload.OBJECT_TYPE: type_object, const.Payload.LINE_GROUP_NUMBER: line_group_number})
		return bytes(commBytes)

	def _Build_command8(self, header, call_number, object_number, object_type, line_a_number, line_b_number=255):
		self._checkHeader(header[0], header[1])
		passwd = str(header[1])
		self._checkLineNumber(line_a_number, line_b_number)
		type_object = self._objectTypeDefine(object_type)
		commBytes = command.CmdControlLineDisconnect({ const.Header.SORM_NUMBER: header[0], const.Header.PASSWORD: passwd, const.Payload.CALL_NUMBER: call_number, const.Payload.OBJECT_NUMBER: object_number, const.Payload.OBJECT_TYPE: type_object, const.Payload.LINE_A_NUMBER: line_a_number, const.Payload.LINE_B_NUMBER: line_b_number})
		return bytes(commBytes)

	def _Build_command9(self, header, line_group_number, line_a_number, line_b_number=255):
		self._checkHeader(header[0], header[1])
		passwd = str(header[1])
		self._checkLineGroupNumber(line_group_number)
		self._checkLineNumber(line_a_number, line_b_number)
		commBytes = command.CmdControlLineRemove({ const.Header.SORM_NUMBER: header[0], const.Header.PASSWORD: passwd, const.Payload.LINE_GROUP_NUMBER: line_group_number, const.Payload.LINE_A_NUMBER: line_a_number, const.Payload.LINE_B_NUMBER: line_b_number})
		return bytes(commBytes)

	def _Build_command10(self, header, object_number, object_type, phone_number=-1, phone_type='ff', linkset_number=65535):
		self._checkHeader(header[0], header[1])
		passwd = str(header[1])
		self._checkObjectNumber(object_number)
		self._checkLinksetNumber(linkset_number)
		type_object = self._objectTypeDefine(object_type)
		type_phone = self._phoneTypeDefine(phone_type)
		phone = self._checkPhoneNumber(phone_number)
		commBytes = command.CmdObjectGetInfo({ const.Header.SORM_NUMBER: header[0], const.Header.PASSWORD: passwd, const.Payload.OBJECT_NUMBER: object_number, const.Payload.OBJECT_TYPE: type_object, const.Payload.PHONE_TYPE: type_phone, const.Payload.PHONE_NUMBER: phone, const.Payload.LINKSET_NUMBER: linkset_number})
		return bytes(commBytes)

	def _Build_command11(self, header, line_group_number, line_group_type, line_a_number, line_b_number=255):
		self._checkHeader(header[0], header[1])
		passwd = str(header[1])
		self._checkLineGroupNumber(line_group_number)
		self._checkLineNumber(line_a_number, line_b_number)
		type_ksl = self._lineGroupTypeDefine(line_group_type)
		commBytes = command.CmdControlLineGetInfo({ const.Header.SORM_NUMBER: header[0], const.Header.PASSWORD: passwd, const.Payload.LINE_GROUP_NUMBER: line_group_number, const.Payload.LINE_GROUP_TYPE: type_ksl, const.Payload.LINE_A_NUMBER: line_a_number, const.Payload.LINE_B_NUMBER: line_b_number})
		return bytes(commBytes)

	def _Build_command12(self, header, phone_number=-1, phone_type='ff'):
		self._checkHeader(header[0], header[1])
		passwd = str(header[1])
		type_phone = self._phoneTypeDefine(phone_type)
		phone = self._checkPhoneNumber(phone_number)
		commBytes = command.CmdServicesGetInfo({ const.Header.SORM_NUMBER: header[0], const.Header.PASSWORD: passwd, const.Payload.PHONE_TYPE: type_phone, const.Payload.PHONE_NUMBER: phone})
		return bytes(commBytes)

	def _Build_command13(self, header):
		self._checkHeader(header[0], header[1])
		passwd = str(header[1])
		commBytes = command.CmdCommandInterrupt({ const.Header.SORM_NUMBER: header[0], const.Header.PASSWORD: passwd})
		return bytes(commBytes)

	def _Build_command14(self, header, test_message_number):
		self._checkHeader(header[0], header[1])
		passwd = str(header[1])
		if type(test_message_number)!=int:
			raise SORM_Error("Invalid value 'TEST_MESSAGE_NUMBER': {0}. It must be 'INTEGER' in range [0-255]".format(test_message_number))
		if not(0<=test_message_number<=255):
			raise SORM_Error("Invalid value 'TEST_MESSAGE_NUMBER': {0}. It must be 'INTEGER' in range [0-255]".format(test_message_number))
		commBytes = command.CmdTestRequest({ const.Header.SORM_NUMBER: header[0], const.Header.PASSWORD: passwd, const.Payload.TEST_MESSAGE_NUMBER: test_message_number})
		return bytes(commBytes)

	def _Build_command15(self, header, object_number, control_category, line_group_number, priority):
		self._checkHeader(header[0], header[1])
		passwd = str(header[1])
		self._checkObjectNumber(object_number)
		self._checkLineGroupNumber(line_group_number)
		category = self._controlCategoryDefine(control_category)
		prio = self._priorityDefine(priority)
		commBytes = command.CmdObjectChange({ const.Header.SORM_NUMBER: header[0], const.Header.PASSWORD: passwd, const.Payload.OBJECT_NUMBER: object_number, const.Payload.CONTROL_CATEGORY: category, const.Payload.LINE_GROUP_NUMBER: line_group_number, const.Payload.PRIORITY: prio})
		return bytes(commBytes)

	def _Build_command16(self, header, linkset_number=65535):
		self._checkHeader(header[0], header[1])
		passwd = str(header[1])
		self._checkLinksetNumber(linkset_number)
		commBytes = command.CmdLinksetGetInfo({ const.Header.SORM_NUMBER: header[0], const.Header.PASSWORD: passwd, const.Payload.LINKSET_NUMBER: linkset_number})
		return bytes(commBytes)

	def _Build_command17(self, header):
		self._checkHeader(header[0], header[1])
		passwd = str(header[1])
		commBytes = command.CmdFirmwareVersionGet({ const.Header.SORM_NUMBER: header[0], const.Header.PASSWORD: passwd})
		return bytes(commBytes)

	# Checkers

	def _checkHeader(self, ormNum, password):
		if type(ormNum)!=int:
			raise SORM_Error("Invalid value 'SORM_NUMBER': {0}. It must be 'INTEGER'".format(ormNum))
		if type(password)!=int:
			raise SORM_Error("Invalid value 'PASSWORD': {0}. It must be one-six'length 'INTEGER' in range [0-999999]".format(password))
		if not(0<=ormNum<=255):
			raise SORM_Error("Invalid value 'SORM_NUMBER': {0}. It must be 'INTEGER' in range [0-255]".format(ormNum))
		if not(0<=password<=999999):
			raise SORM_Error("Invalid value 'PASSWORD': {0}. It must consist of one2six 'INTEGER' values in range [0-9]".format(password))

	def _checkPhoneNumber(self, phone_number):
		if type(phone_number)!=int:
			raise SORM_Error("Invalid value 'PHONE_NUMBER': {0}. It must be 'INTEGER' in range [0-999999999999999999]".format(phone_number))
		if phone_number==-1:
			phone=''
		else:
			phone = str(phone_number)
			if len(phone)>18:
				raise SORM_Error("Invalid value 'PHONE_NUMBER': {0}. It must be 'INTEGER' in range [0-999999999999999999]".format(phone_number))
		return phone

	def _checkCallNumber(self, call_number):
		if type(call_number)!=int:
			raise SORM_Error("Invalid value 'CALL_NUMBER': {0}. It must be 'INTEGER' in range [0-65534]".format(call_number))
		if not(0<=call_number<=65535):
			raise SORM_Error("Invalid value 'CALL_NUMBER': {0}. It must be 'INTEGER' in range [0-65534]".format(call_number))

	def _checkObjectNumber(self, object_number):
		if type(object_number)!=int:
			raise SORM_Error("Invalid value 'OBJECT_NUMBER': {0}. It must be 'INTEGER' in range [0-65535]".format(object_number))
		if not(0<=object_number<=65535):
			raise SORM_Error("Invalid value 'OBJECT_NUMBER': {0}. It must be 'INTEGER' in range [0-65535]".format(object_number))

	def _checkLinksetNumber(self, linkset_number):			
		if type(linkset_number)!=int:
			raise SORM_Error("Invalid value 'LINKSET_NUMBER': {0}. It must be 'INTEGER' in range [0-65535]".format(linkset_number))
		if not(0<=linkset_number<=65535):
			raise SORM_Error("Invalid value 'LINKSET_NUMBER': {0}. It must be 'INTEGER' in range [0-65535]".format(linkset_number))

	def _checkLineGroupNumber(self, line_group_number):
		if type(line_group_number)!=int:
			raise SORM_Error("Invalid value 'LINE_GROUP_NUMBER': {0}. It must be 'INTEGER' in range [1-254]".format(line_group_number))
		if not(0<=line_group_number<=255):
			raise SORM_Error("Invalid value 'LINE_GROUP_NUMBER': {0}. It must be 'INTEGER' in range [1-254]".format(line_group_number))

	def _checkLineNumber(self, line_a_number, line_b_number):
		if type(line_a_number)!=int or type(line_b_number)!=int:
			raise SORM_Error("Invalid value 'LINE_A_NUMBER': {0} or 'LINE_B_NUMBER': {1}. It must be 'INTEGER' in range [1-254]".format(line_a_number, line_b_number))
		if not(0<=line_a_number<=255) or not(0<=line_b_number<=255):
			raise SORM_Error("Invalid value 'LINE_A_NUMBER': {0} or 'LINE_B_NUMBER': {1}. It must be 'INTEGER' in range [1-254]".format(line_a_number, line_b_number))

	def _lineGroupTypeDefine(self, type_ksl):
		if (type_ksl=='combined'):
			return 1
		elif (type_ksl=='separate'):
			return 17
		elif (type_ksl=='invalid'):
			return 26
		else:
			raise SORM_Error("Invalid value 'LINE_GROUP_TYPE': {0}. It must be 'STRING': 'combined'/'separate'/'invalid'".format(type_ksl))

	def _priorityDefine(self, prio):
		if (prio=='common'):
			return 2
		elif (prio=='high'):
			return 1
		elif (prio=='invalid'):
			return 26
		else:
			raise SORM_Error("Invalid value 'PRIORITY': {0}. It must be 'STRING': 'common'/'high'/'invalid'".format(prio))

	def _controlCategoryDefine(self, control_category):
		if (control_category=='combined'):
			return 1
		elif (control_category=='separate'):
			return 17
		elif (control_category=='statistical'):
			return 2
		elif (control_category=='invalid'):
			return 26
		else:
			raise SORM_Error("Invalid value 'CONTROL_CATEGORY': {0}. It must be 'STRING': 'combined'/'separate'/'statistical'/'invalid'".format(control_category))

	def _objectTypeDefine(self, object_type):
		if (object_type=='local'):
			return 1
		elif (object_type=='full'):
			return 2
		elif (object_type=='partial'):
			return 18
		elif (object_type=='trunk'):
			return 3
		elif (object_type=='invalid'):
			return 26
		else:
			raise SORM_Error("Invalid value 'OBJECT_TYPE': {0}. It must be 'STRING': 'local'/'full'/'partial'/'trunk'/'invalid'".format(object_type))

	def _phoneTypeDefine(self, phone_type):
		if (phone_type=='local'):
			return 1
		elif (phone_type=='russian'):
			return 4
		elif (phone_type=='other'):
			return 5
		elif (phone_type=='special'):
			return 6
		elif (phone_type=='imsi'):
			return 7
		elif (phone_type=='ff'):
			return 255
		elif (phone_type=='invalid'):
			return 26
		else:
			raise SORM_Error("Invalid value 'PHONE_TYPE': {0}. It must be 'STRING': 'local'/'russian'/'other'/'special'/'imsi'/'invalid'".format(phone_type))

class Message_Validator:

	def __init__(self):
		self.version = 268
		
	def _SORM_check_message_handler(self):
		return { 21 : self._checkMessage21,
				 22 : self._checkMessage22,
				 23 : self._checkMessage23,
				 26 : self._checkMessage26,
				 27 : self._checkMessage27,
				 28 : self._checkMessage28 }

	def _checkMessage21(self, payload, ormnum, failure_type, failure_code):
		message2 = message1.Msg1TestResponse({const.Header.SORM_NUMBER: ormnum, const.Payload.FAILURE_TYPE: failure_type, const.Payload.FAILURE_CODE: failure_code})
		message = bytes(message2)
		s = 'Message 0x21 validation.'
		result = True
		if payload:
			if len(payload)!=12:
				s += ' Wrong Message received: Expected length: 12, Received "{0}".'.format(len(payload))
				result = False			
			else:
				if payload[2]!=33:
					s += ' Wrong Message received: Expected: 0x21, Received: "{:02X}".'.format(payload[2])
					result = False
				else:
					s += ' Message 0x21 received.'
					if (message[1]!=payload[1]):
						s += ' Wrong ORM Number: Configured "{0}", received "{1}".'.format(message[1], payload[1])
						result = False
					if (payload[9]!=2):
						s += ' Wrong ORM Version: Expected "2", received "{0}".'.format(payload[9])
						result = False
					if (message[10]!=payload[10]):
						s += ' Wrong FAILURE_TYPE: Configured "{0}", received "{1}".'.format(message[10], payload[10])
						result = False
					if (message[11]!=payload[11]):
						s += ' Wrong FAILURE_CODE: Configured "{0}", received "{1}".'.format(message[11], payload[11])
						result = False
		else:
			s += ' ERROR: No message received'
			result = False
		return result, s

	def _checkMessage22(self, payload, ormnum):
		message2 = message1.Msg1FirmwareReboot({const.Header.SORM_NUMBER: ormnum})
		message = bytes(message2)
		s = 'Message 0x22 validation.'
		result = True
		if payload:
			if len(payload)!=10:
				s += ' Wrong Message received: Expected length: 10, Received "{0}".'.format(len(payload))
				result = False			
			else:
				if payload[2]!=34:
					s += ' Wrong Message received: Expected: 0x22, Received: "{:02X}".'.format(payload[2])
					result = False
				else:
					s += ' Message 0x22 received.'
					if (message[1]!=payload[1]):
						s += ' Wrong ORM Number: Configured "{0}", received "{1}".'.format(message[1], payload[1])
						result = False
					if (payload[9]!=2):
						s += ' Wrong ORM Version: Expected "2", received "{0}".'.format(payload[9])
						result = False
		else:
			s += ' ERROR: No message received'
			result = False
		return result, s

	def _checkMessage23(self, payload, ormnum, object_number, object_type, control_category, 
									 line_group_number, priority, phone_type='ff', phone_number=-1, linkset_number=65535, subscriber_set_state=255):
		message2 = message1.Msg1ObjectInfo({const.Header.SORM_NUMBER: ormnum, const.Payload.OBJECT_NUMBER: object_number, 
			const.Payload.OBJECT_TYPE: object_type, const.Payload.PHONE_TYPE: phone_type, const.Payload.PHONE_NUMBER: phone_number, 
			const.Payload.LINKSET_NUMBER: linkset_number, const.Payload.CONTROL_CATEGORY: control_category, 
			const.Payload.LINE_GROUP_NUMBER: line_group_number, const.Payload.PRIORITY: priority, 
			const.Payload.SUBSCRIBER_SET_STATE: subscriber_set_state})
		message = bytes(message2)
		s = 'Message 0x23 validation.'
		result = True
		if payload:
			if len(payload)!=30:
				s += ' Wrong Message received: Expected length: 30, Received "{0}".'.format(len(payload))
				result = False			
			else:
				if payload[2]!=35:
					s += ' Wrong Message received: Expected: 0x23, Received: "{:02X}".'.format(payload[2])
					result = False
				else:
					s += ' Message 0x23 received.'
					if (message[1]!=payload[1]):
						s += ' Wrong ORM Number: Configured "{0}", received "{1}".'.format(message[1], payload[1])
						result = False
					if (payload[9]!=2):
						s += ' Wrong ORM Version: Expected "2", received "{0}".'.format(payload[9])
						result = False
					if (message[10]!=payload[10] or message[11]!=payload[11]):
						s += ' Wrong OBJECT_NUMBER: Configured "{0},{1}", received "{2},{3}".'.format(message[10], message[11], payload[10], payload[11])
						result = False
					if (message[12]!=payload[12]):
						s += ' Wrong OBJECT_TYPE: Configured "{0}", received "{1}".'.format(message[12], payload[12])
						result = False
					if (message[13]!=payload[13]):
						s += ' Wrong PHONE_TYPE: Configured "{0}", received "{1}".'.format(message[13], payload[13])
						result = False
					if (message[14]!=payload[14]):
						s += ' Wrong PHONE_LENGTH: Configured "{0}", received "{1}".'.format(message[14], payload[14])
						result = False
					if (message[15]!=payload[15] or message[16]!=payload[16] or message[17]!=payload[17] or message[18]!=payload[18] or message[19]!=payload[19] or message[20]!=payload[20] or message[21]!=payload[21] or message[22]!=payload[22] or message[23]!=payload[23]):
						s += ' Wrong PHONE_TYPE: Configured "{0}", received "{1}".'.format(message[15:23], payload[15:23])
						result = False
					if (message[24]!=payload[24] or message[25]!=payload[25]):
						s += ' Wrong LINKSET_NUMBER: Configured "{0},{1}", received "{2},{3}".'.format(message[24], message[25], payload[24], payload[25])
						result = False
					if (message[26]!=payload[26]):
						s += ' Wrong CONTROL_CATEGORY: Configured "{0}", received "{1}".'.format(message[26], payload[26])
						result = False
					if (message[27]!=payload[27]):
						s += ' Wrong LINE_GROUP_NUMBER: Configured "{0}", received "{1}".'.format(message[27], payload[27])
						result = False						
					if (message[28]!=payload[28]):
						s += ' Wrong PRIORITY: Configured "{0}", received "{1}".'.format(message[28], payload[28])
						result = False
					if (message[29]!=payload[29]):
						s += ' Wrong SUBSCRIBER_SET_STATE: Configured "{0}", received "{1}".'.format(message[29], payload[29])
						result = False
		else:
			s += ' ERROR: No message received'
			result = False
		return result, s

	def _checkMessage26(self, payload, ormnum, intrusion_code):
		message2 = message1.Msg1Intrusion({const.Header.SORM_NUMBER: ormnum, const.Payload.INTRUSION_CODE: intrusion_code})
		message = bytes(message2)
		s = 'Message 0x26 validation.'
		result = True
		if payload:
			if len(payload)!=55:
				s += ' Wrong Message received: Expected length: 55, Received "{0}".'.format(len(payload))
				result = False			
			else:
				if payload[2]!=38:
					s += ' Wrong Message received: Expected: 0x26, Received: "{:02X}".'.format(payload[2])
					result = False
				else:
					s += ' Message 0x26 received.'
					if (message[1]!=payload[1]):
						s += ' Wrong ORM Number: Configured "{0}", received "{1}".'.format(message[1], payload[1])
						result = False
					if (payload[9]!=2):
						s += ' Wrong ORM Version: Expected "2", received "{0}".'.format(payload[9])
						result = False
					if (message[10]!=payload[10]):
						s += ' Wrong INTRUSION_CODE: Configured "{0}", received "{1}".'.format(message[10], payload[10])
						result = False
		else:
			s += ' ERROR: No message received'
			result = False
		return result, s

	def _checkMessage27(self, payload, ormnum, command_code, receipt_status):
		message2 = message1.Msg1ConfirmReceipt({const.Header.SORM_NUMBER: ormnum, const.Payload.COMMAND_CODE: command_code, const.Payload.RECEIPT_STATUS: receipt_status})
		message = bytes(message2)
		s = 'Message 0x27 validation.'
		result = True
		if payload:
			if len(payload)!=12:
				s += ' Wrong Message received: Expected length: 12, Received "{0}".'.format(len(payload))
				result = False			
			else:
				if payload[2]!=39:
					s += ' Wrong Message received: Expected: 0x27, Received: "{:02X}".'.format(payload[2])
					result = False
				else:
					s += ' Message 0x27 received.'
					if (message[1]!=payload[1]):
						s += ' Wrong ORM Number: Configured "{0}", received "{1}".'.format(message[1], payload[1])
						result = False
					if (payload[9]!=2):
						s += ' Wrong ORM Version: Expected "2", received "{0}".'.format(payload[9])
						result = False
					if (message[10]!=payload[10]):
						s += ' Wrong COMMAND_CODE: Configured "{0}", received "{1}".'.format(message[10], payload[10])
						result = False
					if (message[11]!=payload[11]):
						s += ' Wrong RECEIPT_STATUS: Configured "{0}", received "{1}".'.format(message[11], payload[11])
						result = False
		else:
			s += ' ERROR: No message received'
			result = False
		return result, s

	def _checkMessage28(self, payload, ormnum, command_code, execution_status):
		message2 = message1.Msg1ConfirmExecution({const.Header.SORM_NUMBER: ormnum, const.Payload.COMMAND_CODE: command_code, const.Payload.EXECUTION_STATUS: execution_status})
		message = bytes(message2)
		s = 'Message 0x28 validation.'
		result = True
		if payload:
			if len(payload)!=12:
				s += ' Wrong Message received: Expected length: 12, Received "{0}".'.format(len(payload))
				result = False			
			else:
				if payload[2]!=40:
					s += ' Wrong Message received: Expected: 0x28, Received "{:02X}".'.format(payload[2])
					result = False
				else:
					s += ' Message 0x28 received.'		
					if (message[1]!=payload[1]):
						s += ' Wrong ORM Number: Configured "{0}", received "{1}".'.format(message[1], payload[1])
						result = False
					if (payload[9]!=2):
						s += ' Wrong ORM Version: Expected "2", received "{0}".'.format(payload[9])
						result = False
					if (message[10]!=payload[10]):
						s += ' Wrong COMMAND_CODE: Configured "{0}", received "{1}".'.format(message[10], payload[10])
						result = False
					if (message[11]!=payload[11]):
						s += ' Wrong EXECUTION_STATUS: Configured "{0}", received "{1}".'.format(message[11], payload[11])
						result = False
		else:
			s += ' ERROR: No message received'
			result = False
		return result, s

	def _checkMessage29(self, payload, ormnum, test_message_number, control_channel_1_state, control_channel_2_state):
		message2 = message1.Msg1TestResponse({const.Header.SORM_NUMBER: ormnum, const.Payload.TEST_MESSAGE_NUMBER: test_message_number, 
						const.Payload.CONTROL_CHANNEL_1_STATE: control_channel_1_state, const.Payload.CONTROL_CHANNEL_2_STATE: control_channel_2_state})
		message = bytes(message2)
		s = 'Message 0x29 validation.'
		result = True
		if payload:
			if len(payload)!=13:
				s += ' Wrong Message received: Expected length: 13, Received "{0}".'.format(len(payload))
				result = False			
			else:
				if payload[2]!=41:
					s += ' Wrong Message received: Expected: 0x29, Received "{:02X}".'.format(payload[2])
					result = False
				else:
					s += ' Message 0x29 received.'		
					if (message[1]!=payload[1]):
						s += ' Wrong ORM Number: Configured "{0}", received "{1}".'.format(message[1], payload[1])
						result = False
					if (payload[9]!=2):
						s += ' Wrong ORM Version: Expected "2", received "{0}".'.format(payload[9])
						result = False
					if (message[10]!=payload[10]):
						s += ' Wrong TEST_MESSAGE_NUMBER: Configured "{0}", received "{1}".'.format(message[10], payload[10])
						result = False
					if (message[11]!=payload[11]):
						s += ' Wrong CONTROL_CHANNEL_1_STATE: Configured "{0}", received "{1}".'.format(message[11], payload[11])
						result = False
					if (message[12]!=payload[12]):
						s += ' Wrong CONTROL_CHANNEL_2_STATE: Configured "{0}", received "{1}".'.format(message[12], payload[12])
						result = False
		else:
			s += ' ERROR: No message received'
			result = False
		return result, s

	def _checkMessage2A(self, payload, ormnum, linkset_number, linkset_name):
		message2 = message1.Msg1LinksetInfo({const.Header.SORM_NUMBER: ormnum, const.Payload.LINKSET_NUMBER: linkset_number, const.Payload.LINKSET_NAME: linkset_name})
		message = bytes(message2)
		s = 'Message 0x2A validation.'
		result = True
		if payload:
			if len(payload)!=55:
				s += ' Wrong Message received: Expected length: 55, Received "{0}".'.format(len(payload))
				result = False			
			else:
				if payload[2]!=42:
					s += ' Wrong Message received: Expected: 0x2A, Received "{:02X}".'.format(payload[2])
					result = False
				else:
					s += ' Message 0x2A received.'		
					if (message[1]!=payload[1]):
						s += ' Wrong ORM Number: Configured "{0}", received "{1}".'.format(message[1], payload[1])
						result = False
					if (payload[9]!=2):
						s += ' Wrong ORM Version: Expected "2", received "{0}".'.format(payload[9])
						result = False
					if (message[10]!=payload[10] or message[11]!=payload[11]):
						s += ' Wrong LINKSET_NUMBER: Configured "{0},{1}", received "{2},{3}".'.format(message[10], message[11], payload[10], payload[11])
						result = False
					if (message[12:]!=payload[12:]):
						s += ' Wrong LINKSET_NAME: Configured "{0}", received "{1}".'.format(message[12:], payload[12:])
						result = False
		else:
			s += ' ERROR: No message received'
			result = False
		return result, s

	def _checkMessage2B(self, payload, ormnum, firmware_version, station_type):
		message2 = message1.Msg1FirmwareVersionInfo({const.Header.SORM_NUMBER: ormnum, const.Payload.FIRMWARE_VERSION: firmware_version, const.Payload.STATION_TYPE: station_type})
		message = bytes(message2)
		s = 'Message 0x2B validation.'
		result = True
		if payload:
			if len(payload)!=55:
				s += ' Wrong Message received: Expected length: 55, Received "{0}".'.format(len(payload))
				result = False			
			else:
				if payload[2]!=43:
					s += ' Wrong Message received: Expected: 0x2A, Received "{:02X}".'.format(payload[2])
					result = False
				else:
					s += ' Message 0x2A received.'		
					if (message[1]!=payload[1]):
						s += ' Wrong ORM Number: Configured "{0}", received "{1}".'.format(message[1], payload[1])
						result = False
					if (payload[9]!=2):
						s += ' Wrong ORM Version: Expected "2", received "{0}".'.format(payload[9])
						result = False
					if (message[10:53]!=payload[10:53]):
						s += ' Wrong FIRMWARE_VERSION: Configured "{0}", received "{1}".'.format(message[10:53], payload[10:53])
						result = False
					if (message[54]!=payload[54]):
						s += ' Wrong STATION_TYPE: Configured "{0}", received "{1}".'.format(message[54], payload[54])
						result = False
		else:
			s += ' ERROR: No message received'
			result = False
		return result, s




	def _checkMessage53(self, payload, ormnum, test_message_number, control_channel_1_state, control_channel_2_state):
		message2 = message2.Msg2TestResponse({const.Header.SORM_NUMBER: ormnum, const.Payload.TEST_MESSAGE_NUMBER: test_message_number, 
						const.Payload.CONTROL_CHANNEL_1_STATE: control_channel_1_state, const.Payload.CONTROL_CHANNEL_2_STATE: control_channel_2_state})
		message = bytes(message2)
		s = 'Message 0x53 validation.'
		result = True
		if payload:
			if len(payload)!=15:
				s += ' Wrong Message received: Expected length: 15, Received "{0}".'.format(len(payload))
				result = False			
			else:
				if payload[2]!=83:
					s += ' Wrong Message received: Expected: 0x53, Received "{:02X}".'.format(payload[2])
					result = False
				else:
					s += ' Message 0x53 received.'		
					if (message[1]!=payload[1]):
						s += ' Wrong ORM Number: Configured "{0}", received "{1}".'.format(message[1], payload[1])
						result = False
					if (message[12]!=payload[12]):
						s += ' Wrong TEST_MESSAGE_NUMBER: Configured "{0}", received "{1}".'.format(message[12], payload[12])
						result = False
					if (message[13]!=payload[13]):
						s += ' Wrong CONTROL_CHANNEL_1_STATE: Configured "{0}", received "{1}".'.format(message[13], payload[13])
						result = False
					if (message[14]!=payload[14]):
						s += ' Wrong CONTROL_CHANNEL_2_STATE: Configured "{0}", received "{1}".'.format(message[14], payload[14])
						result = False
		else:
			s += ' ERROR: No message received'
			result = False
		return result, s

class Config_Executor:

	def Values_Exec(self, message_row):
		# Ecexute message type and paarmeters from CDATA
		print ("::FOR LOGGING PURPOSE. SORM_CONFIG_MODULE. Start of parsing, raw data from file::",message_row)
		message_row_type = None
		mes_params = dict()
		if message_row:
			message_row = message_row.strip()
			row_comp = message_row.partition("(") 
			try:
				message_row_type = int(row_comp[0].strip())
			except:
				raise SORM_Error("Configuration data is not valid. Invalid command format")
			if (1<=message_row_type<=17) or (21<=message_row_type<=53):
				if row_comp[2] and row_comp[2] != ")": 
					temp_string = '' 	#temporary string for build new param value
					param = ''      	#temporary string for build new param
					flag_list1 = False  #true if list [ was opened
					list1_vc = 0        #sequence number of value in list
					for _val in row_comp[2]:
						if _val == "'" or _val == '"':
							pass
						elif _val == "(":
							raise SORM_Error("Configuration data is not valid. Symbol '(' in command")
						elif _val == "," or _val ==";":
							if param != '':
								fin_string = temp_string.strip()
								if fin_string:
									try:
										fin_string = int(temp_string.strip())
									except:
										pass
									if flag_list1:
										mes_params[param].append(fin_string)
										list1_vc += 1
										temp_string = ''	
									else:
										mes_params[param] = fin_string
										temp_string = ''
										param = ''
							else:
								pass
								#raise SORM_Error("Configuration data is not valid. Missed Parameter=Value definition")
						elif _val == ")":
							print ("::FOR LOGGING PURPOSE. SORM_CONFIG_MODULE.') handler'::", param, temp_string)
							fin_string = temp_string.strip()
							if (param and fin_string):
								try:
									fin_string = int(temp_string.strip())
								except:
									pass										
								mes_params[param] = fin_string
								temp_string = ''
								param = ''
								pass
							elif param:
								raise SORM_Error("Configuration data is not valid. Missed Parameter value")
							else:
								pass
						elif _val == "=":
							param = temp_string.strip().lower().replace(" ", "_")
							temp_string = ''
						elif _val == "[":
							if flag_list1:
								raise SORM_Error("Configuration data is not valid. Symbol [ in list")
							else:
								flag_list1 = True
								mes_params[param] = list()
						elif _val == "]":
							if flag_list1:
								fin_string = temp_string.strip()
								if fin_string:
									try:
										fin_string = int(temp_string.strip())										
									except:
										pass
									mes_params[param].append(fin_string)
									print ("::FOR LOGGING PURPOSE. SORM_CONFIG_MODULE.'] handler'::", param, fin_string, mes_params[param])
									param = ''
									temp_string = ''
									flag_list1 = False
									list1_vc = 0									
								else:
									raise SORM_Error("Configuration data is not valid. Missed Parameter value")										
							else:
								raise SORM_Error("Configuration data is not valid. List wasn't opened - missed [")
						else:
							temp_string +=_val
					print ("::FOR LOGGING PURPOSE. SORM_CONFIG_MODULE. End of parsing::",mes_params)
					return message_row_type, mes_params
				else: 
					raise SORM_Error("Configuration data is not valid. Missing header in command")
			else:
				raise SORM_Error("Configuration data is not valid. Invalid command number")
		else:
			return "NO_MESSAGE", mes_params #!!! check if needed

class SORM_Error(Exception):

    def __init__(self, description):
        self.description = description

