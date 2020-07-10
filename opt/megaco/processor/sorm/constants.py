
import enum



@enum.unique
class CommandCode(enum.IntEnum):
    '''
    Control commands codes in accordance with order No.268 Appendix 6.
    '''
    SORM_START              = 0x01
    SORM_STOP               = 0x02
    PASSWORD_SET            = 0x03
    CONTROL_LINE_ADD        = 0x04 # To group
    OBJECT_ADD              = 0x05
    OBJECT_REMOVE           = 0x06
    CONTROL_LINE_CONNECT    = 0x07 # To voice channel
    CONTROL_LINE_DISCONNECT = 0x08 # From voice channel
    CONTROL_LINE_REMOVE     = 0x09 # From group
    OBJECT_GET_INFO         = 0x0A
    CONTROL_LINE_GET_INFO   = 0x0B
    SERVICES_GET_INFO       = 0x0C
    COMMAND_INTERRUPT       = 0x0D
    TEST_REQUEST            = 0x0E
    OBJECT_CHANGE           = 0x0F
    LINKSET_GET_INFO         = 0x10
    FIRMWARE_VERSION_GET    = 0x11


@enum.unique
class MessageCode1(enum.IntEnum):
    '''
    Messages codes in data transmission channel 1 (one) in accordance with order No.268 Appendix 9.
    '''
    STATION_FAILURE         = 0x21
    FIRMWARE_REBOOT         = 0x22
    OBJECT_INFO             = 0x23
    CONTROL_LINE_INFO       = 0x24
    SERVICES_INFO           = 0x25
    INTRUSION               = 0x26
    CONFIRM_RECEIPT         = 0x27
    CONFIRM_EXECUTION       = 0x28
    TEST_RESPONSE           = 0x29
    LINKSET_INFO            = 0x2A
    FIRMWARE_VERSION_INFO   = 0x2B
    MESSAGE_TRANSMISSION    = 0x2C


@enum.unique
class MessageCode2(enum.IntEnum):
    '''
    Messages codes in data transmission channel 2 (two) in accordance with order No.268 Appendix 11.
    '''
    CALL_SETUP              = 0x41
    CALL_ANSWER             = 0x42
    CALL_HANGUP             = 0x43
    VAS_ACTIVATION          = 0x44

    CONTROL_LINE_CONNECTED  = 0x51
    CONTROL_LINE_DISCONNECTED = 0x52
    TEST_RESPONSE           = 0x53


@enum.unique
class Header(enum.Enum):
    '''
    Names of command or message header fields.

    Usage:
        from sorm268 import Header

        opts = {
            Header.PASSWORD: '987654'
        }
        sormStartMsg = sorm268.CmdSORMStart(opts)
    '''
    PREAMBLE                = 'PREAMBLE'
    SORM_NUMBER             = 'SORM_NUMBER'
    PAYLOAD_LENGTH          = 'PAYLOAD_LENGTH'
    COMMAND_CODE            = 'COMMAND_CODE'
    # Unique for command
    PASSWORD                = 'PASSWORD'
    # Unique for messages 1 and 2
    MESSAGE_CODE            = 'MESSAGE_CODE'
    # Unique for message 1
    MESSAGES_COUNT          = 'MESSAGES_COUNT'
    MESSAGE_NUMBER          = 'MESSAGE_NUMBER'
    RESERVE                 = 'RESERVE'
    VERSION                 = 'VERSION'
    # Unique for message 2
    CALL_NUMBER             = 'CALL_NUMBER'
    OBJECT_TYPE             = 'OBJECT_TYPE'
    OBJECT_NUMBER           = 'OBJECT_NUMBER'
    SELECTION_SIGN          = 'SELECTION_SIGN'
    CALL_ATTRIBUTE          = 'CALL_ATTRIBUTE'
    VAS_PHASE               = 'VAS_PHASE'


@enum.unique
class DummyHeader(enum.IntEnum):
    PREAMBLE                = 0
    SORM_NUMBER             = 1
    COMMAND_CODE            = 2
    PAYLOAD_LENGTH          = 3


@enum.unique
class CommandHeader(enum.IntEnum):
    PREAMBLE                = 0
    SORM_NUMBER             = 1
    COMMAND_CODE            = 2
    PAYLOAD_LENGTH          = 3
    PASSWORD                = 4


@enum.unique
class Message1Header(enum.IntEnum):
    PREAMBLE                = 0
    SORM_NUMBER             = 1
    MESSAGE_CODE            = 2
    PAYLOAD_LENGTH          = 3
    MESSAGES_COUNT          = 4
    MESSAGE_NUMBER          = 5
    RESERVE                 = 6
    VERSION                 = 7


@enum.unique
class Message2Header(enum.IntEnum):
    PREAMBLE                = 0
    SORM_NUMBER             = 1
    MESSAGE_CODE            = 2
    PAYLOAD_LENGTH          = 3
    CALL_NUMBER             = 4
    OBJECT_TYPE             = 5
    OBJECT_NUMBER           = 6
    SELECTION_SIGN          = 7
    CALL_ATTRIBUTE          = 8
    VAS_PHASE               = 9


@enum.unique
class Payload(enum.Enum):
    '''
    Names of command or message payload fields.

    Usage:
        from sorm268 import Payload

        opts = {
            Payload.NEW_PASSWORD: '987654'
        }
        changePasswordMsg = sorm268.CmdPasswordSet(opts)
    '''
    UNKNOWN_BYTES           = 'UNKNOWN_BYTES'       # Used in dummy message
    NEW_PASSWORD            = 'NEW_PASSWORD'        # 3
    LINE_GROUP_NUMBER       = 'LINE_GROUP_NUMBER'   # 4, 5, 7, 9, 11, 15, 1.3, 1.4
    LINE_GROUP_TYPE         = 'LINE_GROUP_TYPE'     # 4, 11, 1.4
    LINE_A_NUMBER           = 'LINE_A_NUMBER'       # 4, 8, 9, 11, 1.4, 2.* except 2.2.3
    LINE_B_NUMBER           = 'LINE_B_NUMBER'       # 4, 8, 9, 11, 1.4, 2.* except 2.2.3
    FINAL_BYTE              = 'FINAL_BYTE'          # 1.4
    OBJECT_NUMBER           = 'OBJECT_NUMBER'       # 5, 6, 7, 8, 10, 15, 1.3, 1.12
    OBJECT_TYPE             = 'OBJECT_TYPE'         # 5, 6, 7, 8, 10, 1.3, 1.12
    PHONE_TYPE              = 'PHONE_TYPE'          # 5, 6, 10, 12, 1.3, 1.5
    PHONE_LENGTH            = 'PHONE_LENGTH'        # 5, 6, 10, 12, 1.3, 1.5
    PHONE_NUMBER            = 'PHONE_NUMBER'        # 5, 6, 10, 12, 1.3, 1.5
    LINKSET_NUMBER          = 'LINKSET_NUMBER'      # 5, 6, 10, 16, 1.3, 1.10, 2.* except 2.2.3
    CONTROL_CATEGORY        = 'CONTROL_CATEGORY'    # 5, 15, 1.3
    PRIORITY                = 'PRIORITY'            # 5, 15, 1.3, 2.* except 2.2.3
    CALL_NUMBER             = 'CALL_NUMBER'         # 7, 8
    TEST_MESSAGE_NUMBER     = 'TEST_MESSAGE_NUMBER' # 14, 1.9, 2.2.3
    FAILURE_TYPE            = 'FAILURE_TYPE'        # 1.1
    FAILURE_CODE            = 'FAILURE_CODE'        # 1.1
    SUBSCRIBER_SET_STATE    = 'SUBSCRIBER_SET_STATE' # 1.3
    VAS_COUNT               = 'VAS_COUNT'           # 1.5
    VAS_CODE                = 'VAS_CODE'            # 1.5, 2.* except 2.2.3
    VAS_CODE_FILLER         = 'VAS_CODE_FILLER'     # 2.* except 2.2.3    
    INTRUSION_CODE          = 'INTRUSION_CODE'      # 1.6
    INTRUSION_DAY           = 'INTRUSION_DAY'       # 1.6
    INTRUSION_HOUR          = 'INTRUSION_HOUR'      # 1.6
    INTRUSION_MINUTE        = 'INTRUSION_MINUTE'    # 1.6
    INTRUSION_SECOND        = 'INTRUSION_SECOND'    # 1.6
    INTRUSION_MESSAGE       = 'INTRUSION_MESSAGE'   # 1.6
    COMMAND_CODE            = 'COMMAND_CODE'        # 1.7, 1.8
    RECEIPT_STATUS          = 'RECEIPT_STATUS'      # 1.7
    EXECUTION_STATUS        = 'EXECUTION_STATUS'    # 1.8
    CONTROL_CHANNEL_1_STATE = 'CONTROL_CHANNEL_1_STATE' # 1.9, 2.2.3
    CONTROL_CHANNEL_2_STATE = 'CONTROL_CHANNEL_2_STATE' # 1.9, 2.2.3
    LINKSET_NAME            = 'LINKSET_NAME'        # 1.10
    FIRMWARE_VERSION        = 'FIRMWARE_VERSION' # 1.11
    STATION_TYPE            = 'STATION_TYPE'        # 1.11
    SENDER_PHONE_TYPE       = 'SENDER_PHONE_TYPE'   # 1.12
    SENDER_PHONE_LENGTH     = 'SENDER_PHONE_LENGTH' # 1.12
    SENDER_PHONE_NUMBER     = 'SENDER_PHONE_NUMBER' # 1.12
    DELIVERY_STATE          = 'DELIVERY_STATE'      # 1.12
    DELIVERY_CODE           = 'DELIVERY_CODE'       # 1.12
    TRANSMISSION_DATE       = 'TRANSMISSION_DATE'   # 1.12
    RECEIVER_PHONE_TYPE     = 'RECEIVER_PHONE_TYPE' # 1.12
    RECEIVER_PHONE_LENGTH   = 'RECEIVER_PHONE_LENGTH' # 1.12
    RECEIVER_PHONE_NUMBER   = 'RECEIVER_PHONE_NUMBER' # 1.12
    SENDER_IMSI_TYPE        = 'SENDER_IMSI_TYPE'    # 1.12
    SENDER_IMSI_LENGTH      = 'SENDER_IMSI_LENGTH'  # 1.12
    SENDER_IMSI_NUMBER      = 'SENDER_IMSI_NUMBER'  # 1.12
    RECEIVER_IMSI_TYPE      = 'RECEIVER_IMSI_TYPE'  # 1.12
    RECEIVER_IMSI_LENGTH    = 'RECEIVER_IMSI_LENGTH' # 1.12
    RECEIVER_IMSI_NUMBER    = 'RECEIVER_IMSI_NUMBER' # 1.12
    TRANSMITTED_MESSAGE     = 'TRANSMITTED_MESSAGE' # 1.12
    CALLING_PHONE_TYPE      = 'CALLING_PHONE_TYPE'  # 2.* except 2.2.3
    CALLING_PHONE_LENGTH    = 'CALLING_PHONE_LENGTH'# 2.* except 2.2.3
    CALLING_PHONE_NUMBER    = 'CALLING_PHONE_NUMBER'# 2.* except 2.2.3
    CALLED_PHONE_TYPE       = 'CALLED_PHONE_TYPE'   # 2.* except 2.2.3
    CALLED_PHONE_LENGTH     = 'CALLED_PHONE_LENGTH' # 2.* except 2.2.3
    CALLED_PHONE_NUMBER     = 'CALLED_PHONE_NUMBER' # 2.* except 2.2.3
    CALL_DAY                = 'CALL_DAY'            # 2.* except 2.2.3
    CALL_HOUR               = 'CALL_HOUR'           # 2.* except 2.2.3
    CALL_MINUTE             = 'CALL_MINUTE'         # 2.* except 2.2.3
    CALL_SECOND             = 'CALL_SECOND'         # 2.* except 2.2.3
    OPERATION_CODE          = 'OPERATION_CODE'      # 2.* except 2.2.3
    ADDITIONAL_CODE         = 'ADDITIONAL_CODE'     # 2.* except 2.2.3
    LINE_A_STREAM_NUMBER    = 'LINE_A_STREAM_NUMBER' # 4, 8, 9, 11, 1.4, 2.* except 2.2.3
    LINE_B_STREAM_NUMBER    = 'LINE_B_STREAM_NUMBER' # 4, 8, 9, 11, 1.4, 2.* except 2.2.3


# class Command1() not needed - no payload


# class Command2() not needed - no payload


@enum.unique
class Command3(enum.IntEnum):
    NEW_PASSWORD            = 0


@enum.unique
class Command4(enum.IntEnum):
    LINE_GROUP_NUMBER       = 0
    LINE_GROUP_TYPE         = 1
    LINE_A_NUMBER           = 2
    LINE_B_NUMBER           = 3


@enum.unique
class Command5(enum.IntEnum):
    OBJECT_NUMBER           = 0
    OBJECT_TYPE             = 1
    PHONE_TYPE              = 2
    PHONE_LENGTH            = 3
    PHONE_NUMBER            = 4
    LINKSET_NUMBER          = 5
    CONTROL_CATEGORY        = 6
    LINE_GROUP_NUMBER       = 7
    PRIORITY                = 8


@enum.unique
class Command6(enum.IntEnum):
    OBJECT_NUMBER           = 0
    OBJECT_TYPE             = 1
    PHONE_TYPE              = 2
    PHONE_LENGTH            = 3
    PHONE_NUMBER            = 4
    LINKSET_NUMBER          = 5


@enum.unique
class Command7(enum.IntEnum):
    CALL_NUMBER             = 0
    OBJECT_TYPE             = 1
    OBJECT_NUMBER           = 2
    LINE_GROUP_NUMBER       = 3


@enum.unique
class Command8(enum.IntEnum):
    CALL_NUMBER             = 0
    OBJECT_TYPE             = 1
    OBJECT_NUMBER           = 2
    LINE_A_NUMBER           = 3
    LINE_B_NUMBER           = 4


@enum.unique
class Command9(enum.IntEnum):
    LINE_GROUP_NUMBER       = 0
    LINE_A_NUMBER           = 1
    LINE_B_NUMBER           = 2


@enum.unique
class Command10(enum.IntEnum):
    OBJECT_NUMBER           = 0
    OBJECT_TYPE             = 1
    PHONE_TYPE              = 2
    PHONE_LENGTH            = 3
    PHONE_NUMBER            = 4
    LINKSET_NUMBER          = 5


@enum.unique
class Command11(enum.IntEnum):
    LINE_GROUP_NUMBER       = 0
    LINE_GROUP_TYPE         = 1
    LINE_A_NUMBER           = 2
    LINE_B_NUMBER           = 3


@enum.unique
class Command12(enum.IntEnum):
    PHONE_TYPE              = 0
    PHONE_LENGTH            = 1
    PHONE_NUMBER            = 2


# class Command13() not needed - no payload


@enum.unique
class Command14(enum.IntEnum):
    TEST_MESSAGE_NUMBER     = 0


@enum.unique
class Command15(enum.IntEnum):
    OBJECT_NUMBER           = 0
    CONTROL_CATEGORY        = 1
    LINE_GROUP_NUMBER       = 2
    PRIORITY                = 3


@enum.unique
class Command16(enum.IntEnum):
    LINKSET_NUMBER          = 0


# class Command17() not needed - no payload


@enum.unique
class Message1_1(enum.IntEnum):
    FAILURE_TYPE            = 0
    FAILURE_CODE            = 1


# class Message1_2() not needed - no payload


@enum.unique
class Message1_3(enum.IntEnum):
    OBJECT_NUMBER           = 0
    OBJECT_TYPE             = 1
    PHONE_TYPE              = 2
    PHONE_LENGTH            = 3
    PHONE_NUMBER            = 4
    LINKSET_NUMBER          = 5
    CONTROL_CATEGORY        = 6
    LINE_GROUP_NUMBER       = 7
    PRIORITY                = 8
    SUBSCRIBER_SET_STATE    = 9


@enum.unique
class Message1_4(enum.IntEnum): # Fields repeats 11 times (29.10.2019)
    LINE_GROUP_NUMBER       = 0
    LINE_GROUP_TYPE         = 1
    LINE_A_NUMBER           = 2
    LINE_B_NUMBER           = 3
    FINAL_BYTE              = 44

@enum.unique
class Message1_5(enum.IntEnum):
    PHONE_TYPE              = 0
    PHONE_LENGTH            = 1
    PHONE_NUMBER            = 2
    VAS_COUNT               = 3
    VAS_CODE                = 4


@enum.unique
class Message1_6(enum.IntEnum):
    INTRUSION_CODE          = 0
    INTRUSION_DAY           = 1
    INTRUSION_HOUR          = 2
    INTRUSION_MINUTE        = 3
    INTRUSION_SECOND        = 4
    INTRUSION_MESSAGE       = 5


@enum.unique
class Message1_7(enum.IntEnum):
    COMMAND_CODE            = 0
    RECEIPT_STATUS          = 1


@enum.unique
class Message1_8(enum.IntEnum):
    COMMAND_CODE            = 0
    EXECUTION_STATUS        = 1


@enum.unique
class Message1_9(enum.IntEnum):
    TEST_MESSAGE_NUMBER     = 0
    CONTROL_CHANNEL_1_STATE = 1
    CONTROL_CHANNEL_2_STATE = 2


@enum.unique
class Message1_10(enum.IntEnum):
    LINKSET_NUMBER          = 0
    LINKSET_NAME            = 1


@enum.unique
class Message1_11(enum.IntEnum):
    FIRMWARE_VERSION        = 0
    STATION_TYPE            = 1


@enum.unique
class Message1_12_head(enum.IntEnum):
    OBJECT_NUMBER           = 0
    OBJECT_TYPE             = 1
    SENDER_PHONE_TYPE       = 2
    SENDER_PHONE_LENGTH     = 3
    SENDER_PHONE_NUMBER     = 4
    DELIVERY_STATE          = 5
    DELIVERY_CODE           = 6
    TRANSMISSION_DATE       = 7
    RECEIVER_PHONE_TYPE     = 8
    RECEIVER_PHONE_LENGTH   = 9
    RECEIVER_PHONE_NUMBER   = 10
    SENDER_IMSI_TYPE        = 11
    SENDER_IMSI_LENGTH      = 12
    SENDER_IMSI_NUMBER      = 13
    RECEIVER_IMSI_TYPE      = 14
    RECEIVER_IMSI_LENGTH    = 15
    RECEIVER_IMSI_NUMBER    = 16


@enum.unique
class Message1_12_tail(enum.IntEnum):
    TRANSMITTED_MESSAGE     = 0


@enum.unique
class Message2_x(enum.IntEnum):
    CALLING_PHONE_TYPE      = 0
    CALLING_PHONE_LENGTH    = 1
    CALLING_PHONE_NUMBER    = 2
    CALLED_PHONE_TYPE       = 3
    CALLED_PHONE_LENGTH     = 4
    CALLED_PHONE_NUMBER     = 5
    LINKSET_NUMBER          = 6
    LINE_A_NUMBER           = 7
    LINE_B_NUMBER           = 8
    CALL_DAY                = 9
    CALL_HOUR               = 10
    CALL_MINUTE             = 11
    CALL_SECOND             = 12
    PRIORITY                = 13
    OPERATION_CODE          = 14
    VAS_CODE                = 15
    VAS_CODE_FILLER         = 16
    ADDITIONAL_CODE         = 17


#~ Message2_1_1 = Message2_x # Same payload structure in accordance order 268 appendix 10


#~ Message2_1_2 = Message2_x # Same payload structure in accordance order 268 appendix 10


#~ Message2_1_3 = Message2_x # Same payload structure in accordance order 268 appendix 10


#~ Message2_1_4 = Message2_x # Same payload structure in accordance order 268 appendix 10


#~ Message2_2_1 = Message2_x # Same payload structure in accordance order 268 appendix 10


#~ Message2_2_2 = Message2_x # Same payload structure in accordance order 268 appendix 10


@enum.unique
class Message2_2_3(enum.IntEnum):
    TEST_MESSAGE_NUMBER     = 0
    CONTROL_CHANNEL_1_STATE = 1
    CONTROL_CHANNEL_2_STATE = 2


class HeaderFormat():
    Dummy       = '<4B' # Only preamble, SORM number, message/command code and message length
    Command     = '<4B6s'
    Message1    = '<4B2H2B'
    Message2    = '<4B1H1B1H3B'


class PayloadFormat():
    # Command1 has no payload
    # Command2 has no payload
    Command3    = '<6s'
    Command4    = '<4B'
    Command5    = '<1H3B9s1H3B'
    Command6    = '<1H3B9s1H'
    #Command7    = '<2s1B1H1B'
    Command7    = '<1H1B1H1B'
    #Command8    = '<2s1B1H2B'
    Command8    = '<1H1B1H2B'
    Command9    = '<3B'
    Command10   = '<1H3B9s1H'
    Command11   = '<4B'
    Command12   = '<2B9s'
    # Command13 has no payload
    Command14   = '<1B'
    Command15   = '<1H3B'
    Command16   = '<1H'
    # Command17 has no payload

    Message1_1  = '<2B'
    # Message1_2 has no payload
    Message1_3  = '<1H3B9s1H4B'
    Message1_4  = '<45B'
    Message1_5  = '<2B9s1B33s'
    Message1_6  = '<5B40s'
    Message1_7  = '<2B'
    Message1_8  = '<2B'
    Message1_9  = '<3B'
    Message1_10 = '<1H43s'
    Message1_11 = '<44s1B'
    Message1_12_head = '<1H3B9s2B'  # Unique case - message 1.12 have mandatory 53 bytes
    Message1_12_tail = '<{}s'       # and X bytes for message content (calculate from payload length)

    Message2_x = '<2B9s2B9s1H9B1H1B'
    Message2_1_1 = Message2_x
    Message2_1_2 = Message2_x
    Message2_1_3 = Message2_x
    Message2_1_4 = Message2_x
    Message2_2_1 = Message2_x
    Message2_2_2 = Message2_x
    Message2_2_3 = '<3B'


class Const():
    # Usable byte constants
    ZEROBYTE                = 0x00
    FILLBYTE                = 0xFF # Used for fill unused messages fields
    FILLBYTE_CHAR           = FILLBYTE.to_bytes(1, 'big')
    FILLBYTE_TWO            = 0xFFFF
    FILLBYTE_THREE          = 0xFFFFFF

    # Headers length
    CMD_HDR_LENGTH          = 10 # 10 bytes according to order 268 Appendix 5
    MSG1_HDR_LENGTH         = 10 # 10 bytes according to order 268 Appendix 8
    MSG2_HDR_LENGTH         = 12 # 12 bytes according to order 268 Appendix 10
    DUMMY_HDR_LENGTH        = 4 # Only preamble, SORM number, message/command code and message length

    # Headers defaults
    PREAMBLE                = 0xCC # Mandatory from order 268 Appendixes 5, 8, 10
    SORM_VERSION            = 0x02 # SORM version according to order 268 Appendixes 8, 10
    DEFAULT_SORM_NUMBER     = 0
    DEFAULT_SORM_PASSWORD   = '123456' # SORM password

    # Messages payload
    MSG1_RESERVE_BYTE       = 0xFF # Mandatory from order 268 Appendix 8 paragraph 2.1.7
    MSG1_SORM_VERSION       = 0x02 # Mandatory from order 268 Appendix 8 paragraph 2.1.8
    MSG1_4_GROUP_COUNT      = 11 # 44 bytes in blocks of 4 bytes
    MSG1_4_GROUP_SIZE       = 4
    MSG1_5_GROUP_COUNT      = 11 # 33 bytes in blocks of 3 bytes
    MSG1_5_GROUP_SIZE       = 3
    MSG1_6_MESSAGE_LENGTH   = 40
    MSG1_10_NAME_LENGTH     = 43
    MSG1_11_VERSION_LENGTH  = 44

    # For utils and text
    PHONE_LENGTH_IN_BYTES   = 9 # BCD bytes encoded 18 digits phone number length
    DEFAULT_CODEC           = 'latin-1'
