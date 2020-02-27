
from sorm268.constants import CommandCode
from sorm268.constants import MessageCode1
from sorm268.constants import MessageCode2

from sorm268.constants import Header
from sorm268.constants import Payload

from sorm268.parser import parse



from sorm268.command import CmdSORMStart
from sorm268.command import CmdSORMStop
from sorm268.command import CmdPasswordSet
from sorm268.command import CmdControlLineAdd
from sorm268.command import CmdObjectAdd
from sorm268.command import CmdObjectRemove
from sorm268.command import CmdControlLineConnect
from sorm268.command import CmdControlLineDisconnect
from sorm268.command import CmdControlLineRemove
from sorm268.command import CmdObjectGetInfo
from sorm268.command import CmdControlLineGetInfo
from sorm268.command import CmdServicesGetInfo
from sorm268.command import CmdCommandInterrupt
from sorm268.command import CmdTestRequest
from sorm268.command import CmdObjectChange
from sorm268.command import CmdLinksetGetInfo
from sorm268.command import CmdFirmwareVersionGet

Command1 = CmdSORMStart
Command2 = CmdSORMStop
Command3 = CmdPasswordSet
Command4 = CmdControlLineAdd
Command5 = CmdObjectAdd
Command6 = CmdObjectRemove
Command7 = CmdControlLineConnect
Command8 = CmdControlLineDisconnect
Command9 = CmdControlLineRemove
Command10 = CmdObjectGetInfo
Command11 = CmdControlLineGetInfo
Command12 = CmdServicesGetInfo
Command13 = CmdCommandInterrupt
Command14 = CmdTestRequest
Command15 = CmdObjectChange
Command16 = CmdLinksetGetInfo
Command17 = CmdFirmwareVersionGet



from sorm268.message1 import Msg1StationFailure
from sorm268.message1 import Msg1FirmwareReboot
from sorm268.message1 import Msg1ObjectInfo
from sorm268.message1 import Msg1ControlLineInfo
from sorm268.message1 import Msg1ServicesInfo
from sorm268.message1 import Msg1Intrusion
from sorm268.message1 import Msg1ConfirmReceipt
from sorm268.message1 import Msg1ConfirmExecution
from sorm268.message1 import Msg1TestResponse
from sorm268.message1 import Msg1LinksetInfo
from sorm268.message1 import Msg1FirmwareVersionInfo
#~ from sorm268.message1 import Msg1MessageTransmission

Message1_1 = Msg1StationFailure
Message1_2 = Msg1FirmwareReboot
Message1_3 = Msg1ObjectInfo
Message1_4 = Msg1ControlLineInfo
Message1_5 = Msg1ServicesInfo
Message1_6 = Msg1Intrusion
Message1_7 = Msg1ConfirmReceipt
Message1_8 = Msg1ConfirmExecution
Message1_9 = Msg1TestResponse
Message1_10 = Msg1LinksetInfo
Message1_11 = Msg1FirmwareVersionInfo
#~ Message1_12 = Msg1MessageTransmission



from sorm268.message2 import Msg2CallSetup
from sorm268.message2 import Msg2CallAnswer
from sorm268.message2 import Msg2CallHangup
from sorm268.message2 import Msg2VASActivation

from sorm268.message2 import Msg2ControlLineConnected
from sorm268.message2 import Msg2ControlLineDisconnected
from sorm268.message2 import Msg2TestResponse

Message2_1_1 = Msg2CallSetup
Message2_1_2 = Msg2CallAnswer
Message2_1_3 = Msg2CallHangup
Message2_1_4 = Msg2VASActivation

Message2_2_1 = Msg2ControlLineConnected
Message2_2_2 = Msg2ControlLineDisconnected
Message2_2_3 = Msg2TestResponse
