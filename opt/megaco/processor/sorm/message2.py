
import struct

from processor.sorm.constants import (MessageCode2,
                               Header,
                               Payload,
                               Message2Header,
                               Message2_x,
                               #~ Message2_1_1,
                               #~ Message2_1_2,
                               #~ Message2_1_3,
                               #~ Message2_1_4,
                               #~ Message2_2_1,
                               #~ Message2_2_2,
                               Message2_2_3,
                               HeaderFormat,
                               PayloadFormat,
                               Const,
                              )
import processor.sorm.text as text
import processor.sorm.utils as utils



class _Message2():
    '''
    SORM message from data transmission channel 2 (two) in
    accordance with order No.268 Appendix 10.

    Dummy class with main functionality. Do not use it in you own code.
    Only way to use it - inherit new class from this.

    Inherited classes MUST implement these methods:
        _packPayload(self)
        _unpackPayload(self, b)
        __str__(self)
    '''
    def __init__(self, messageCode, *args):
        '''
        Arguments:
            messageCode: int()
            args*:       *dict()
        '''
        self.fields = dict()
        for arg in args:
            if not isinstance(arg, dict):
                raise TypeError('Argument {} must be dict, but {} given!'.format(arg, type(arg)))
            self.fields.update(arg)

        self.fields.setdefault(Header.PREAMBLE,         Const.PREAMBLE)
        self.fields.setdefault(Header.SORM_NUMBER,      Const.DEFAULT_SORM_NUMBER)
        self.fields[Header.MESSAGE_CODE]                = messageCode
        self.fields[Header.PAYLOAD_LENGTH]              = 0 # Real payload length calculated while payload packed to bytes
        self.fields.setdefault(Header.CALL_NUMBER,      Const.FILLBYTE_TWO)
        self.fields.setdefault(Header.OBJECT_TYPE,      Const.FILLBYTE)
        self.fields.setdefault(Header.OBJECT_NUMBER,    Const.FILLBYTE_TWO)
        self.fields.setdefault(Header.SELECTION_SIGN,   Const.FILLBYTE)
        self.fields.setdefault(Header.CALL_ATTRIBUTE,   Const.FILLBYTE)
        self.fields.setdefault(Header.VAS_PHASE,        Const.FILLBYTE)

    def _packHeader(self):
        '''
        Internal function.
        Pack header from class fields dictionary to binary.

        Return:
            bytes()
        '''
        return struct.pack(HeaderFormat.Message2,
                           self.fields.get(Header.PREAMBLE),
                           self.fields.get(Header.SORM_NUMBER),
                           self.fields.get(Header.MESSAGE_CODE),
                           self.fields.get(Header.PAYLOAD_LENGTH),
                           self.fields.get(Header.CALL_NUMBER),
                           self.fields.get(Header.OBJECT_TYPE),
                           self.fields.get(Header.OBJECT_NUMBER),
                           self.fields.get(Header.SELECTION_SIGN),
                           self.fields.get(Header.CALL_ATTRIBUTE),
                           self.fields.get(Header.VAS_PHASE),
                          )

    def _unpackHeader(self, b):
        '''
        Internal function.
        Unpack header from binary to class fields dictionary.

        Arguments:
            b: bytes()
        '''
        if len(b) < Const.MSG2_HDR_LENGTH:
            raise ValueError('Message 2 header too small.')
        t = struct.unpack(HeaderFormat.Message2, b[:Const.MSG2_HDR_LENGTH])
        self.fields[Header.PREAMBLE]        = t[Message2Header.PREAMBLE]
        self.fields[Header.SORM_NUMBER]     = t[Message2Header.SORM_NUMBER]
        self.fields[Header.MESSAGE_CODE]    = t[Message2Header.MESSAGE_CODE]
        self.fields[Header.PAYLOAD_LENGTH]  = t[Message2Header.PAYLOAD_LENGTH]
        self.fields[Header.CALL_NUMBER]     = t[Message2Header.CALL_NUMBER]
        self.fields[Header.OBJECT_TYPE]     = t[Message2Header.OBJECT_TYPE]
        self.fields[Header.OBJECT_NUMBER]   = t[Message2Header.OBJECT_NUMBER]
        self.fields[Header.SELECTION_SIGN]  = t[Message2Header.SELECTION_SIGN]
        self.fields[Header.CALL_ATTRIBUTE]  = t[Message2Header.CALL_ATTRIBUTE]
        self.fields[Header.VAS_PHASE]       = t[Message2Header.VAS_PHASE]

    def _packPayload(self):
        '''
        Internal function.
        Pack payload from class fields dictionary to binary.
        MUST be implemented in inherited classes.

        Return:
            bytes()
        '''
        raise NotImplementedError


    def _unpackPayload(self, b):
        '''
        Internal function.
        Unpack payload from binary to class fields dictionary.
        MUST be implemented in inherited classes.

        Arguments:
            b: bytes()
        '''
        raise NotImplementedError


    def _header2string(self):
        '''
        Internal function.
        Convert internal representation of header to human readable string.

        Return:
            str()
        '''
        s = '\n'.join(['- - - - - - -',
                       utils.printableBytes(bytes(self)),
                       text.preamble(       self.fields[Header.PREAMBLE]        ),
                       text.sormNumber(     self.fields[Header.SORM_NUMBER]     ),
                       text.messageCode2(   self.fields[Header.MESSAGE_CODE]    ),
                       text.payloadLength(  self.fields[Header.PAYLOAD_LENGTH]  ),
                       text.callNumber(     self.fields[Header.CALL_NUMBER]     ),
                       text.objectType(     self.fields[Header.OBJECT_TYPE]     ),
                       text.objectNumber(   self.fields[Header.OBJECT_NUMBER]   ),
                       text.selectionSign(  self.fields[Header.SELECTION_SIGN]  ),
                       text.callAttribute(  self.fields[Header.CALL_ATTRIBUTE]  ),
                       text.vasPhase(       self.fields[Header.VAS_PHASE]       ),
                       '- - -\n',
                     ])
        return s

    def _getPayload(self, b):
        '''
        Internal function.
        Extract payload from binary.

        Arguments:
            b: bytes()
        Return:
            bytes()
        '''
        payload = b[Const.MSG2_HDR_LENGTH:]
        if len(payload) != self.fields[Header.PAYLOAD_LENGTH]:
            raise ValueError('Wrong payload size, expected 0x{:02X}, but got 0x{:02X}.'.format(self.fields[Header.PAYLOAD_LENGTH],
                                                                                               len(payload)
                                                                                              ))
        return payload

    def __bytes__(self):
        '''
        Convert internal representation of message to bytes.

        Usage:
            It's used when you need send message via network:
                ``
                message = _Message2() # Replace _Message2() to message you needed
                sormAddr = ('192.0.2.1', 8888)
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(bytes(message), sormdAddr)
                ``

            or represent message as byte string:
                ``
                message = _Message2() # Replace _Message2() to message you needed
                hexRepr = ' '.join(['0x{:02X}'.format(x) for x in bytes(message)][1:])
                print(hexRepr)
                ``
        Return:
            bytes()
        '''
        payload = self._packPayload() # Payload before header because we need to calculate payload length
        header = self._packHeader()
        return header + payload

    def __str__(self):
        '''
        Convert class representation to human readable string.
        MUST be implemented in inherited classes.
        '''
        raise NotImplementedError

    def fromBytes(self, b):
        '''
        Set command class parameters from binary representation.

        Arguments:
            b: bytes()
        '''
        self._unpackHeader(b)
        self._unpackPayload(b)



class _Message2default(_Message2):
    '''
    SORM message from data transmission channel 2 (two) in
    accordance with order No.268 Appendix 10.

    Dummy class with main functionality. Do not use it in you own code.
    Only way to use it - inherit new class from this.

    This class implements these methods because many channel 2 messages have
    same payload structure:
        _packPayload(self)
        _unpackPayload(self, b)

    Inherited classes MUST implement these methods:
        __str__(self)
    '''
    def __init__(self, messageCode, *args):
        '''
        Arguments:
            messageCode: int()
            args*:       *dict()
        '''
        _Message2.__init__(self, messageCode, *args)
        self.fields.setdefault(Payload.CALLING_PHONE_TYPE,      Const.FILLBYTE)
        self.fields.setdefault(Payload.CALLING_PHONE_NUMBER,    '')
        if self.fields[Payload.CALLING_PHONE_NUMBER] == '':
            length = Const.FILLBYTE
        else:
            length = len(self.fields[Payload.CALLING_PHONE_NUMBER])
        self.fields.setdefault(Payload.CALLING_PHONE_LENGTH,    length)
        self.fields.setdefault(Payload.CALLED_PHONE_TYPE,       Const.FILLBYTE)
        self.fields.setdefault(Payload.CALLED_PHONE_NUMBER,     '')
        if self.fields[Payload.CALLED_PHONE_NUMBER] == '':
            length = Const.FILLBYTE
        else:
            length = len(self.fields[Payload.CALLED_PHONE_NUMBER])
        self.fields.setdefault(Payload.CALLED_PHONE_LENGTH,     length)
        self.fields.setdefault(Payload.LINKSET_NUMBER,          Const.FILLBYTE_TWO)
        self.fields.setdefault(Payload.LINE_A_NUMBER,           Const.FILLBYTE)
        self.fields.setdefault(Payload.LINE_A_STREAM_NUMBER,    Const.ZEROBYTE)
        self.fields.setdefault(Payload.LINE_B_NUMBER,           Const.FILLBYTE)
        self.fields.setdefault(Payload.LINE_B_STREAM_NUMBER,    Const.ZEROBYTE)
        self.fields.setdefault(Payload.LINE_B_NUMBER,           Const.FILLBYTE)
        self.fields.setdefault(Payload.CALL_DAY,                Const.FILLBYTE)
        self.fields.setdefault(Payload.CALL_HOUR,               Const.FILLBYTE)
        self.fields.setdefault(Payload.CALL_MINUTE,             Const.FILLBYTE)
        self.fields.setdefault(Payload.CALL_SECOND,             Const.FILLBYTE)
        self.fields.setdefault(Payload.PRIORITY,                Const.FILLBYTE)
        self.fields.setdefault(Payload.OPERATION_CODE,          Const.FILLBYTE)
        self.fields.setdefault(Payload.VAS_CODE,                Const.FILLBYTE_THREE)
        self.fields.setdefault(Payload.ADDITIONAL_CODE,         Const.FILLBYTE)

    def _packPayload(self):
        '''
        Internal function.
        Pack header from class fields dictionary to binary.

        Return:
            bytes()
        '''
        controlLineA = utils.mergeStreamAndLine(self.fields.get(Payload.LINE_A_STREAM_NUMBER),
                                                self.fields.get(Payload.LINE_A_NUMBER)
                                               )
        controlLineB = utils.mergeStreamAndLine(self.fields.get(Payload.LINE_B_STREAM_NUMBER),
                                                self.fields.get(Payload.LINE_B_NUMBER)
                                               )
        payload = struct.pack(PayloadFormat.Message2_x,
                              self.fields[Payload.CALLING_PHONE_TYPE],
                              self.fields[Payload.CALLING_PHONE_LENGTH],
                              utils.phone2bcd(self.fields[Payload.CALLING_PHONE_NUMBER]),
                              self.fields[Payload.CALLED_PHONE_TYPE],
                              self.fields[Payload.CALLED_PHONE_LENGTH],
                              utils.phone2bcd(self.fields[Payload.CALLED_PHONE_NUMBER]),
                              self.fields[Payload.LINKSET_NUMBER],
                              controlLineA,
                              controlLineB,
                              utils.int2bcd(self.fields[Payload.CALL_DAY]),
                              utils.int2bcd(self.fields[Payload.CALL_HOUR]),
                              utils.int2bcd(self.fields[Payload.CALL_MINUTE]),
                              utils.int2bcd(self.fields[Payload.CALL_SECOND]),
                              self.fields[Payload.PRIORITY],
                              self.fields[Payload.OPERATION_CODE],
                              self.fields[Payload.VAS_CODE],
                              self.fields[Payload.ADDITIONAL_CODE],
                             )
        self.fields[Header.PAYLOAD_LENGTH] = len(payload)
        return payload

    def _unpackPayload(self, b):
        '''
        Internal function.
        Unpack payload from binary to class fields dictionary.
        MUST be implemented in inherited classes.

        Arguments:
            b: bytes()
        '''
        payload = self._getPayload(b)
        t = struct.unpack(PayloadFormat.Message2_x, payload)
        self.fields[Payload.CALLING_PHONE_TYPE]     = t[Message2_x.CALLING_PHONE_TYPE]
        self.fields[Payload.CALLING_PHONE_LENGTH]   = t[Message2_x.CALLING_PHONE_LENGTH]
        self.fields[Payload.CALLING_PHONE_NUMBER]   = utils.bcd2phone(t[Message2_x.CALLING_PHONE_NUMBER])
        self.fields[Payload.CALLED_PHONE_TYPE]      = t[Message2_x.CALLED_PHONE_TYPE]
        self.fields[Payload.CALLED_PHONE_LENGTH]    = t[Message2_x.CALLED_PHONE_LENGTH]
        self.fields[Payload.CALLED_PHONE_NUMBER]    = utils.bcd2phone(t[Message2_x.CALLED_PHONE_NUMBER])
        self.fields[Payload.LINKSET_NUMBER]         = t[Message2_x.LINKSET_NUMBER]
        self.fields[Payload.LINE_A_STREAM_NUMBER], \
        self.fields[Payload.LINE_A_NUMBER] = utils.splitStreamAndLine(t[Message2_x.LINE_A_NUMBER])
        self.fields[Payload.LINE_B_STREAM_NUMBER], \
        self.fields[Payload.LINE_B_NUMBER] = utils.splitStreamAndLine(t[Message2_x.LINE_B_NUMBER])
        self.fields[Payload.CALL_DAY]               = utils.bcd2int(t[Message2_x.CALL_DAY])
        self.fields[Payload.CALL_HOUR]              = utils.bcd2int(t[Message2_x.CALL_HOUR])
        self.fields[Payload.CALL_MINUTE]            = utils.bcd2int(t[Message2_x.CALL_MINUTE])
        self.fields[Payload.CALL_SECOND]            = utils.bcd2int(t[Message2_x.CALL_SECOND])
        self.fields[Payload.PRIORITY]               = t[Message2_x.PRIORITY]
        self.fields[Payload.OPERATION_CODE]         = t[Message2_x.OPERATION_CODE]
        self.fields[Payload.VAS_CODE]               = t[Message2_x.VAS_CODE]
        self.fields[Payload.ADDITIONAL_CODE]        = t[Message2_x.ADDITIONAL_CODE]

    def __str__(self):
        '''
        Convert class representation to human readable string.
        MUST be implemented in inherited classes.
        '''
        s = self._header2string() + \
            '\n'.join([text.objectNumber(   self.fields[Payload.CALLING_PHONE_TYPE]     ),
                       text.objectType(     self.fields[Payload.CALLING_PHONE_LENGTH]   ),
                       text.objectType(     self.fields[Payload.CALLING_PHONE_NUMBER]   ),
                       text.phoneType(      self.fields[Payload.CALLED_PHONE_TYPE]      ),
                       text.phoneLength(    self.fields[Payload.CALLED_PHONE_LENGTH]    ),
                       text.phoneNumber(    self.fields[Payload.CALLED_PHONE_NUMBER]    ),
                       text.linksetNumber(  self.fields[Payload.LINKSET_NUMBER]         ),
                       text.eventDate(      self.fields[Payload.INTRUSION_DAY],
                                            self.fields[Payload.INTRUSION_HOUR],
                                            self.fields[Payload.INTRUSION_MINUTE],
                                            self.fields[Payload.INTRUSION_SECOND],      ),
                       text.priority(       self.fields[Payload.PRIORITY]               ),
                       self.__operationCode2String(),
                       text.vasCode(        self.fields[Payload.VAS_CODE]               ),
                       text.additionalCode( self.fields[Payload.ADDITIONAL_CODE]        ),
                     ])
        return s

    def __operationCode2String(self):
        '''
        Internal function.
        Represent string value of operation code.
        MUST be implemented in inherited classes.

        Return:
            str()
        '''
        raise NotImplementedError



class Msg2CallSetup(_Message2default):
    '''
    Message No.1.1 in accordance with order No.268 Appendix 11 paragraph 1.

    RU: Сообщение №1.1 "Прием полного номера телефона вызываемого пользователя"
    '''
    def __init__(self, *args):
        _Message2default.__init__(self, MessageCode2.CALL_SETUP, *args)

    def __operationCode2String(self):
        return text.operationCode(self.fields[Payload.OPERATION_CODE])



class Msg2CallAnswer(_Message2default):
    '''
    Message No.1.2 in accordance with order No.268 Appendix 11 paragraph 2.

    RU: Сообщение №1.2 "Ответ вызываемого абонента"
    '''
    def __init__(self, *args):
        _Message2default.__init__(self, MessageCode2.CALL_ANSWER, *args)

    def __operationCode2String(self):
        return text.operationCode(self.fields[Payload.OPERATION_CODE])



class Msg2CallHangup(_Message2default):
    '''
    Message No.1.3 in accordance with order No.268 Appendix 11 paragraph 3.

    RU: Сообщение №1.3 "Разъединение"
    '''
    def __init__(self, *args):
        _Message2default.__init__(self, MessageCode2.CALL_HANGUP, *args)

    def __operationCode2String(self):
        return text.operationCodeDisconnect(self.fields[Payload.OPERATION_CODE])



class Msg2VASActivation(_Message2default):
    '''
    Message No.1.4 in accordance with order No.268 Appendix 11 paragraph 4.

    RU: Сообщение №1.4 "Использование услуг связи"
    '''
    def __init__(self, *args):
        _Message2default.__init__(self, MessageCode2.VAS_ACTIVATION, *args)

    def __operationCode2String(self):
        return text.operationCode(self.fields[Payload.OPERATION_CODE])



class Msg2ControlLineConnected(_Message2default):
    '''
    Message No.2.1 in accordance with order No.268 Appendix 11 paragraph 5.

    RU: Сообщение №2.1 "Подключение контрольной соединительной линии"
    '''
    def __init__(self, *args):
        _Message2default.__init__(self, MessageCode2.CONTROL_LINE_CONNECTED, *args)

    def __operationCode2String(self):
        return text.operationCodeControlLineConnect(self.fields[Payload.OPERATION_CODE])



class Msg2ControlLineDisconnected(_Message2default):
    '''
    Message No.2.2 in accordance with order No.268 Appendix 11 paragraph 6.

    RU: Сообщение №2.2 "Освобождение контрольной соединительной линии"
    '''
    def __init__(self, *args):
        _Message2default.__init__(self, MessageCode2.CONTROL_LINE_DISCONNECTED, *args)

    def __operationCode2String(self):
        return text.operationCodeControlLineDisconnect(self.fields[Payload.OPERATION_CODE])



class Msg2TestResponse(_Message2):
    '''
    Message No.2.3 in accordance with order No.268 Appendix 11 paragraph 7.

    RU: Сообщение №2.3 "Ответное тестовое сообщение"
    '''
    def __init__(self, *args):
        _Message2.__init__(self, MessageCode2.TEST_RESPONSE, *args)
        self.fields.setdefault(Payload.TEST_MESSAGE_NUMBER,     Const.FILLBYTE)
        self.fields.setdefault(Payload.CONTROL_CHANNEL_1_STATE, Const.FILLBYTE)
        self.fields.setdefault(Payload.CONTROL_CHANNEL_2_STATE, Const.FILLBYTE)

    def _packPayload(self):
        payload = struct.pack(PayloadFormat.Message2_2_3,
                              self.fields[Payload.TEST_MESSAGE_NUMBER],
                              self.fields[Payload.CONTROL_CHANNEL_1_STATE],
                              self.fields[Payload.CONTROL_CHANNEL_2_STATE],
                             )
        self.fields[Header.PAYLOAD_LENGTH] = len(payload)
        return payload

    def _unpackPayload(self, b):
        payload = self._getPayload(b)
        t = struct.unpack(PayloadFormat.Message2_2_3, payload)
        self.fields[Payload.TEST_MESSAGE_NUMBER]        = t[Message2_2_3.TEST_MESSAGE_NUMBER]
        self.fields[Payload.CONTROL_CHANNEL_1_STATE]    = t[Message2_2_3.CONTROL_CHANNEL_1_STATE]
        self.fields[Payload.CONTROL_CHANNEL_2_STATE]    = t[Message2_2_3.CONTROL_CHANNEL_2_STATE]

    def __str__(self):
        s = self._header2string() + \
            '\n'.join([text.testMessageNumber(      self.fields[Payload.TEST_MESSAGE_NUMBER]        ),
                       text.controlChannelStatus(   self.fields[Payload.CONTROL_CHANNEL_1_STATE],
                                                    self.fields[Payload.CONTROL_CHANNEL_2_STATE]    ),
                     ])
        return s
