
from processor.sorm.constants import (CommandCode,
                               MessageCode1,
                               MessageCode2,
                               Const,
                              )
import processor.sorm.command
import processor.sorm.message1
import processor.sorm.message2
import processor.sorm.dummy

def parse(b):
    msgLength = len(b)
    if msgLength < Const.DUMMY_HDR_LENGTH:
        raise ValueError('Bytes object too short, need at leads {} bytes, got {}!'.format(Const.DUMMY_HDR_LENGTH, msgLength))
    code = b[2]
    parser = {
        CommandCode.SORM_START              : command.CmdSORMStart,
        CommandCode.SORM_STOP               : command.CmdSORMStop,
        CommandCode.PASSWORD_SET            : command.CmdPasswordSet,
        CommandCode.CONTROL_LINE_ADD        : command.CmdControlLineAdd,
        CommandCode.OBJECT_ADD              : command.CmdObjectAdd,
        CommandCode.OBJECT_REMOVE           : command.CmdObjectRemove,
        CommandCode.CONTROL_LINE_CONNECT    : command.CmdControlLineConnect,
        CommandCode.CONTROL_LINE_DISCONNECT : command.CmdControlLineDisconnect,
        CommandCode.CONTROL_LINE_REMOVE     : command.CmdControlLineRemove,
        CommandCode.OBJECT_GET_INFO         : command.CmdObjectGetInfo,
        CommandCode.CONTROL_LINE_GET_INFO   : command.CmdControlLineGetInfo,
        CommandCode.SERVICES_GET_INFO       : command.CmdServicesGetInfo,
        CommandCode.COMMAND_INTERRUPT       : command.CmdCommandInterrupt,
        CommandCode.TEST_REQUEST            : command.CmdTestRequest,
        CommandCode.OBJECT_CHANGE           : command.CmdObjectChange,
        CommandCode.LINKSET_GET_INFO        : command.CmdLinksetGetInfo,
        CommandCode.FIRMWARE_VERSION_GET    : command.CmdFirmwareVersionGet,

        MessageCode1.STATION_FAILURE        : message1.Msg1StationFailure,
        MessageCode1.FIRMWARE_REBOOT        : message1.Msg1FirmwareReboot,
        MessageCode1.OBJECT_INFO            : message1.Msg1ObjectInfo,
        MessageCode1.CONTROL_LINE_INFO      : message1.Msg1ControlLineInfo,
        MessageCode1.SERVICES_INFO          : message1.Msg1ServicesInfo,
        MessageCode1.INTRUSION              : message1.Msg1Intrusion,
        MessageCode1.CONFIRM_RECEIPT        : message1.Msg1ConfirmReceipt,
        MessageCode1.CONFIRM_EXECUTION      : message1.Msg1ConfirmExecution,
        MessageCode1.TEST_RESPONSE          : message1.Msg1TestResponse,
        MessageCode1.LINKSET_INFO           : message1.Msg1LinksetInfo,
        MessageCode1.FIRMWARE_VERSION_INFO  : message1.Msg1FirmwareVersionInfo,
        #~ MessageCode1.MESSAGE_TRANSMISSION   : message1.Msg1MessageTransmission,

        MessageCode2.CALL_SETUP             : message2.Msg2CallSetup,
        MessageCode2.CALL_ANSWER            : message2.Msg2CallAnswer,
        MessageCode2.CALL_HANGUP            : message2.Msg2CallHangup,
        MessageCode2.VAS_ACTIVATION         : message2.Msg2VASActivation,

        MessageCode2.CONTROL_LINE_CONNECTED : message2.Msg2ControlLineConnected,
        MessageCode2.CONTROL_LINE_DISCONNECTED : message2.Msg2ControlLineDisconnected,
        MessageCode2.TEST_RESPONSE          : message2.Msg2TestResponse,
        }.get(code, dummy.Message)
    if parser is None:
        raise ValueError('Unknown command or message with code 0x{:02X}.'.format(code))
    parsed = parser()
    parsed.fromBytes(b)
    return parsed
