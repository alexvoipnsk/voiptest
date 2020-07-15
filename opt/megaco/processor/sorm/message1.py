
import struct

from processor.sorm.constants import (MessageCode1,
                               Header,
                               Payload,
                               Message1Header,
                               Message1_1,
                               Message1_3,
                               Message1_4,
                               Message1_5,
                               Message1_6,
                               Message1_7,
                               Message1_8,
                               Message1_9,
                               Message1_10,
                               Message1_11,
                               Message1_12_head,
                               Message1_12_tail,
                               HeaderFormat,
                               PayloadFormat,
                               Const,
                              )
import processor.sorm.text as text
import processor.sorm.utils as utils



class _Message1():
    '''
    SORM message from data transmission channel 1 (one) in
    accordance with order No.268 Appendix 8.

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
        self.fields.setdefault(Header.MESSAGES_COUNT,   Const.ZEROBYTE)
        self.fields.setdefault(Header.MESSAGE_NUMBER,   Const.ZEROBYTE)
        self.fields.setdefault(Header.RESERVE,          Const.MSG1_RESERVE_BYTE)
        self.fields.setdefault(Header.VERSION,          Const.MSG1_SORM_VERSION)

    def _packHeader(self):
        '''
        Internal function.
        Pack header from class fields dictionary to binary.

        Return:
            bytes()
        '''
        return struct.pack(HeaderFormat.Message1,
                           self.fields.get(Header.PREAMBLE),
                           self.fields.get(Header.SORM_NUMBER),
                           self.fields.get(Header.MESSAGE_CODE),
                           self.fields.get(Header.PAYLOAD_LENGTH),
                           self.fields.get(Header.MESSAGES_COUNT),
                           self.fields.get(Header.MESSAGE_NUMBER),
                           self.fields.get(Header.RESERVE),
                           self.fields.get(Header.VERSION),
                          )

    def _unpackHeader(self, b):
        '''
        Internal function.
        Unpack header from binary to class fields dictionary.

        Arguments:
            b: bytes()
        '''
        if len(b) < Const.MSG1_HDR_LENGTH:
            raise ValueError('Message 1 header too small.')
        t = struct.unpack(HeaderFormat.Message1, b[:Const.MSG1_HDR_LENGTH])
        self.fields[Header.PREAMBLE]        = t[Message1Header.PREAMBLE]
        self.fields[Header.SORM_NUMBER]     = t[Message1Header.SORM_NUMBER]
        self.fields[Header.MESSAGE_CODE]    = t[Message1Header.MESSAGE_CODE]
        self.fields[Header.PAYLOAD_LENGTH]  = t[Message1Header.PAYLOAD_LENGTH]
        self.fields[Header.MESSAGES_COUNT]  = t[Message1Header.MESSAGES_COUNT]
        self.fields[Header.MESSAGE_NUMBER]  = t[Message1Header.MESSAGE_NUMBER]
        self.fields[Header.RESERVE]         = t[Message1Header.RESERVE]
        self.fields[Header.VERSION]         = t[Message1Header.VERSION]

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
                       text.messageCode1(   self.fields[Header.MESSAGE_CODE]    ),
                       text.payloadLength(  self.fields[Header.PAYLOAD_LENGTH]  ),
                       text.messagesCount(  self.fields[Header.MESSAGES_COUNT]  ),
                       text.messagesNumber( self.fields[Header.MESSAGE_NUMBER]  ),
                       text.reserve(        self.fields[Header.RESERVE]         ),
                       text.version(        self.fields[Header.VERSION]         ),
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
        payload = b[Const.MSG1_HDR_LENGTH:]
        print("OOOO", payload)
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
                message = _Message1() # Replace _Message1() to message you needed
                sormAddr = ('192.0.2.1', 8888)
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(bytes(message), sormdAddr)
                ``

            or represent message as byte string:
                ``
                message = _Message1() # Replace _Message1() to message you needed
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



class Msg1StationFailure(_Message1):
    '''
    Message No.1 in accordance with order No.268 Appendix 9 paragraph 1.

    RU: Сообщение №1 "Авария"
    '''
    def __init__(self, *args):
        _Message1.__init__(self, MessageCode1.STATION_FAILURE, *args)
        self.fields.setdefault(Payload.FAILURE_TYPE, Const.ZEROBYTE)
        self.fields.setdefault(Payload.FAILURE_CODE, Const.ZEROBYTE)

    def _packPayload(self):
        payload = struct.pack(PayloadFormat.Message1_1,
                              self.fields.get(Payload.FAILURE_TYPE),
                              self.fields.get(Payload.FAILURE_CODE),
                             )
        self.fields[Header.PAYLOAD_LENGTH] = len(payload)
        return payload

    def _unpackPayload(self, b):
        payload = self._getPayload(b)
        t = struct.unpack(PayloadFormat.Message1_1, payload)
        self.fields[Payload.FAILURE_TYPE] = t[Message1_1.FAILURE_TYPE]
        self.fields[Payload.FAILURE_CODE] = t[Message1_1.FAILURE_CODE]

    def __str__(self):
        s = self._header2string() + \
            '\n'.join([text.failureType(self.fields[Payload.FAILURE_TYPE]),
                       text.failureCode(self.fields[Payload.FAILURE_CODE]),
                     ])
        return s



class Msg1FirmwareReboot(_Message1):
    '''
    Message No.2 in accordance with order No.268 Appendix 9 paragraph 2.

    RU: Сообщение №2 "Перезапуск ПО станции"
    '''
    def __init__(self, *args):
        _Message1.__init__(self, MessageCode1.FIRMWARE_REBOOT, *args)

    def _packPayload(self):
        return b'' # No payload in this message

    def _unpackPayload(self, b):
        pass # No payload in this message

    def __str__(self):
        return self._header2string()



class Msg1ObjectInfo(_Message1):
    '''
    Message No.3 in accordance with order No.268 Appendix 9 paragraph 3.

    RU: Сообщение №3 "Данные об объектах контроля"
    '''
    def __init__(self, *args):
        _Message1.__init__(self, MessageCode1.OBJECT_INFO, *args)
        self.fields.setdefault(Payload.OBJECT_NUMBER,       Const.FILLBYTE_TWO)
        self.fields.setdefault(Payload.OBJECT_TYPE,         Const.FILLBYTE)
        self.fields.setdefault(Payload.PHONE_TYPE,          Const.FILLBYTE)
        self.fields.setdefault(Payload.PHONE_NUMBER,        '')
        if self.fields[Payload.PHONE_NUMBER] == '':
            length = Const.FILLBYTE
        else:
            length = len(self.fields[Payload.PHONE_NUMBER])
        self.fields.setdefault(Payload.PHONE_LENGTH,        length)
        self.fields.setdefault(Payload.LINKSET_NUMBER,      Const.FILLBYTE_TWO)
        self.fields.setdefault(Payload.CONTROL_CATEGORY,    Const.FILLBYTE)
        self.fields.setdefault(Payload.LINE_GROUP_NUMBER,   Const.FILLBYTE)
        self.fields.setdefault(Payload.PRIORITY,            Const.FILLBYTE)
        self.fields.setdefault(Payload.SUBSCRIBER_SET_STATE, Const.FILLBYTE)

    def _packPayload(self):
        payload = struct.pack(PayloadFormat.Message1_3,
                              self.fields[Payload.OBJECT_NUMBER],
                              self.fields[Payload.OBJECT_TYPE],
                              self.fields[Payload.PHONE_TYPE],
                              self.fields[Payload.PHONE_LENGTH],
                              utils.phone2bcd(self.fields[Payload.PHONE_NUMBER]),
                              self.fields[Payload.LINKSET_NUMBER],
                              self.fields[Payload.CONTROL_CATEGORY],
                              self.fields[Payload.LINE_GROUP_NUMBER],
                              self.fields[Payload.PRIORITY],
                              self.fields[Payload.SUBSCRIBER_SET_STATE],
                             )
        self.fields[Header.PAYLOAD_LENGTH] = len(payload)
        return payload

    def _unpackPayload(self, b):
        payload = self._getPayload(b)
        t = struct.unpack(PayloadFormat.Message1_3, payload)
        self.fields[Payload.OBJECT_NUMBER]      = t[Message1_3.OBJECT_NUMBER]
        self.fields[Payload.OBJECT_TYPE]        = t[Message1_3.OBJECT_TYPE]
        self.fields[Payload.PHONE_TYPE]         = t[Message1_3.PHONE_TYPE]
        self.fields[Payload.PHONE_LENGTH]       = t[Message1_3.PHONE_LENGTH]
        self.fields[Payload.PHONE_NUMBER]       = utils.bcd2phone(t[Message1_3.PHONE_NUMBER])
        self.fields[Payload.LINKSET_NUMBER]     = t[Message1_3.LINKSET_NUMBER]
        self.fields[Payload.CONTROL_CATEGORY]   = t[Message1_3.CONTROL_CATEGORY]
        self.fields[Payload.LINE_GROUP_NUMBER]  = t[Message1_3.LINE_GROUP_NUMBER]
        self.fields[Payload.PRIORITY]           = t[Message1_3.PRIORITY]
        self.fields[Payload.SUBSCRIBER_SET_STATE] = t[Message1_3.SUBSCRIBER_SET_STATE]

    def __str__(self):
        s = self._header2string() + \
            '\n'.join([text.objectNumber(   self.fields[Payload.OBJECT_NUMBER]      ),
                       text.objectType(     self.fields[Payload.OBJECT_TYPE]        ),
                       text.phoneType(      self.fields[Payload.PHONE_TYPE]         ),
                       text.phoneLength(    self.fields[Payload.PHONE_LENGTH]       ),
                       text.phoneNumber(    self.fields[Payload.PHONE_NUMBER]       ),
                       text.linksetNumber(  self.fields[Payload.LINKSET_NUMBER]     ),
                       text.controlCategory(self.fields[Payload.CONTROL_CATEGORY]   ),
                       text.lineGroupNumber(self.fields[Payload.LINE_GROUP_NUMBER]  ),
                       text.priority(       self.fields[Payload.PRIORITY]           ),
                       text.subscriberSetState(self.fields[Payload.SUBSCRIBER_SET_STATE]),
                     ])
        return s



class Msg1ControlLineInfo(_Message1):
    '''
    Message No.4 in accordance with order No.268 Appendix 9 paragraph 4.

    RU: Сообщение №4 "Информация о соответствии между КСЛ и группами"
    '''
    def __init__(self, *args):
        _Message1.__init__(self, MessageCode1.CONTROL_LINE_INFO, *args)
        fillBytesList = [Const.FILLBYTE, ] * Const.MSG1_4_GROUP_COUNT
        zeroBytesList = [Const.ZEROBYTE, ] * Const.MSG1_4_GROUP_COUNT
        self.fields.setdefault(Payload.LINE_GROUP_NUMBER,       fillBytesList)
        self.fields.setdefault(Payload.LINE_GROUP_TYPE,         fillBytesList)
        self.fields.setdefault(Payload.LINE_A_NUMBER,           fillBytesList)
        self.fields.setdefault(Payload.LINE_A_STREAM_NUMBER,    zeroBytesList)
        self.fields.setdefault(Payload.LINE_B_NUMBER,           fillBytesList)
        self.fields.setdefault(Payload.LINE_B_STREAM_NUMBER,    zeroBytesList)
        self.fields.setdefault(Payload.FINAL_BYTE,              Const.FILLBYTE)
        self.__extendKeys()

    def __extendKeys(self):
        for key, default in ((Payload.LINE_GROUP_NUMBER,    Const.FILLBYTE),
                             (Payload.LINE_GROUP_TYPE,      Const.FILLBYTE),
                             (Payload.LINE_A_NUMBER,        Const.FILLBYTE),
                             (Payload.LINE_A_STREAM_NUMBER, Const.ZEROBYTE),
                             (Payload.LINE_B_NUMBER,        Const.FILLBYTE),
                             (Payload.LINE_B_STREAM_NUMBER, Const.ZEROBYTE),
                            ):
            t = self.fields[key]
            if not isinstance(t, list):
                self.fields[key] = [t, ] + [default, ] * (Const.MSG1_4_GROUP_COUNT - 1)
            else:
                self.fields[key] = t + [default, ] * (Const.MSG1_4_GROUP_COUNT - len(t))

    def _packPayload(self):
        t = list()
        for i in range(Const.MSG1_4_GROUP_COUNT):
            controlLineA = utils.mergeStreamAndLine(self.fields.get(Payload.LINE_A_STREAM_NUMBER)[i],
                                                    self.fields.get(Payload.LINE_A_NUMBER)[i]
                                                   )
            controlLineB = utils.mergeStreamAndLine(self.fields.get(Payload.LINE_B_STREAM_NUMBER)[i],
                                                    self.fields.get(Payload.LINE_B_NUMBER)[i]
                                                   )
            t.extend([self.fields.get(Payload.LINE_GROUP_NUMBER)[i],
                     self.fields.get(Payload.LINE_GROUP_TYPE)[i],
                     controlLineA,
                     controlLineB,
                    ])
        payload = struct.pack(PayloadFormat.Message1_4,
                              *t,
                              self.fields.get(Payload.FINAL_BYTE),
                             )
        self.fields[Header.PAYLOAD_LENGTH] = len(payload)
        return payload

    def _unpackPayload(self, b):
        payload = self._getPayload(b)
        t = struct.unpack(PayloadFormat.Message1_4, payload)
        if t[Message1_4.FINAL_BYTE] != Const.FILLBYTE:
            raise('Final byte 0x{:02X} in Message 1.4 wrong, expect {}'.format(t[Message1_4.FINAL_BYTE],
                                                                               Const.FILLBYTE
                                                                              ))
        for i in range(Const.MSG1_4_GROUP_COUNT):
            shift = Const.MSG1_4_GROUP_SIZE * i
            self.fields[Payload.LINE_GROUP_NUMBER][i]   = t[Message1_4.LINE_GROUP_NUMBER + shift]
            self.fields[Payload.LINE_GROUP_TYPE][i]     = t[Message1_4.LINE_GROUP_TYPE + shift]
            self.fields[Payload.LINE_A_STREAM_NUMBER][i], \
            self.fields[Payload.LINE_A_NUMBER][i] = utils.splitStreamAndLine(t[Message1_4.LINE_A_NUMBER + shift])
            self.fields[Payload.LINE_B_STREAM_NUMBER][i], \
            self.fields[Payload.LINE_B_NUMBER][i] = utils.splitStreamAndLine(t[Message1_4.LINE_B_NUMBER + shift])
        self.__extendKeys()

    def __str__(self):
        s = self._header2string()
        for i in range(Const.MSG1_4_GROUP_COUNT):
            s += '\n'
            s += '\n'.join(['- Запись {} -'.format(i+1),
                            text.lineGroupNumber(   self.fields[Payload.LINE_GROUP_NUMBER][i]       ),
                            text.lineGroupType(     self.fields[Payload.LINE_GROUP_TYPE][i]         ),
                            text.lineANumber(       self.fields[Payload.LINE_A_STREAM_NUMBER][i],
                                                    self.fields[Payload.LINE_A_NUMBER][i],          ),
                            text.lineBNumber(       self.fields[Payload.LINE_B_STREAM_NUMBER][i],
                                                    self.fields[Payload.LINE_B_NUMBER][i],          ),
                         ])
        return s



class Msg1ServicesInfo(_Message1):
    '''
    Message No.5 in accordance with order No.268 Appendix 9 paragraph 5.

    RU: Сообщение №5 "Список услуг связи"
    '''
    def __init__(self, *args):
        _Message1.__init__(self, MessageCode1.SERVICES_INFO, *args)        
        self.fields.setdefault(Payload.PHONE_TYPE,      Const.FILLBYTE)
        self.fields.setdefault(Payload.PHONE_NUMBER,    '')
        if self.fields[Payload.PHONE_NUMBER] == '':
            length = Const.FILLBYTE
        else:
            length = len(self.fields[Payload.PHONE_NUMBER])
        self.fields.setdefault(Payload.PHONE_LENGTH,        length)
        self.fields.setdefault(Payload.VAS_COUNT,       Const.ZEROBYTE)
        if self.fields[Payload.VAS_COUNT]:
            fillBytesList = [Const.FILLBYTE_THREE, ] * self.fields[Payload.VAS_COUNT]
        else:
            fillBytesList = [Const.FILLBYTE_THREE, ] * Const.MSG1_5_GROUP_COUNT
        self.fields.setdefault(Payload.VAS_CODE,        fillBytesList)
        self.__extendKeys()

    def __extendKeys(self):
        key = Payload.VAS_CODE
        default = Const.FILLBYTE_THREE
        t = self.fields[key]
        if not isinstance(t, list):
            self.fields[key] = [t, ] + [default, ] * (Const.MSG1_5_GROUP_COUNT - 1)
        else:
            self.fields[key] = t + [default, ] * (Const.MSG1_5_GROUP_COUNT - len(t))

    def _packPayload(self):
        t = bytes()
        if self.fields[Payload.VAS_COUNT]:
            for i in range(self.fields[Payload.VAS_COUNT]):
                t += bytes([255, 255, self.fields.get(Payload.VAS_CODE)[i]])
        else:
            #t = [16777215, 16777215, 16777215, 16777215, 16777215, 16777215, 16777215, 16777215, 16777215, 16777215, 16777215]
            t = bytes([255,255,255, 255,255,255, 255,255,255, 255,255,255, 255,255,255, 255,255,255, 255,255,255, 255,255,255, 255,255,255, 255,255,255, 255,255,255])
        payload = struct.pack('<2B9s1B%ds' % len(t),
                              self.fields[Payload.PHONE_TYPE],
                              self.fields[Payload.PHONE_LENGTH],
                              utils.phone2bcd(self.fields[Payload.PHONE_NUMBER]),
                              self.fields[Payload.VAS_COUNT],
                              t,
                             )
        self.fields[Header.PAYLOAD_LENGTH] = len(payload)
        return payload

    def _unpackPayload(self, b):
        payload = self._getPayload(b)
        t = struct.unpack(PayloadFormat.Message1_5, payload)
        self.fields[Payload.PHONE_TYPE]         = t[Message1_5.PHONE_TYPE]
        self.fields[Payload.PHONE_LENGTH]       = t[Message1_5.PHONE_LENGTH]
        self.fields[Payload.PHONE_NUMBER]       = utils.bcd2phone(t[Message1_5.PHONE_NUMBER])
        self.fields[Payload.VAS_COUNT]          = t[Message1_5.VAS_COUNT]
        for i in range(Const.MSG1_5_GROUP_COUNT):
            # FIXME: Potential issue with 3-bytes values after unpacking
            shift = Const.MSG1_5_GROUP_SIZE * i
            self.fields[Payload.VAS_CODE][i]   = t[Message1_5.VAS_CODE + shift]
        self.__extendKeys()

    def __str__(self):
        s = self._header2string() + \
            '\n'.join([text.phoneType(  self.fields[Payload.PHONE_TYPE]     ),
                       text.phoneLength(self.fields[Payload.PHONE_LENGTH]   ),
                       text.phoneNumber(self.fields[Payload.PHONE_NUMBER]   ),
                       text.vasCount(   self.fields[Payload.VAS_COUNT]      ),
                     ])
        for i in range(Const.MSG1_5_GROUP_COUNT):
            s += '- Запись {} -\n'.format(i+1) + text.vasCode(self.fields[Payload.VAS_CODE][i])
        return s



class Msg1Intrusion(_Message1):
    '''
    Message No.6 in accordance with order No.268 Appendix 9 paragraph 6.

    RU: Сообщение №6 "Несанкционированный доступ к программным средствам технических средств ОРМ"
    '''
    def __init__(self, *args):
        _Message1.__init__(self, MessageCode1.INTRUSION, *args)
        self.fields.setdefault(Payload.INTRUSION_CODE,      Const.FILLBYTE)
        self.fields.setdefault(Payload.INTRUSION_DAY,       Const.FILLBYTE)
        self.fields.setdefault(Payload.INTRUSION_HOUR,      Const.FILLBYTE)
        self.fields.setdefault(Payload.INTRUSION_MINUTE,    Const.FILLBYTE)
        self.fields.setdefault(Payload.INTRUSION_SECOND,    Const.FILLBYTE)
        self.fields.setdefault(Payload.INTRUSION_MESSAGE,   str(Const.FILLBYTE_CHAR * Const.MSG1_6_MESSAGE_LENGTH))

    def _packPayload(self):
        t = self.fields.get(Payload.INTRUSION_MESSAGE)
        message = t.encode(Const.DEFAULT_CODEC) + \
                  Const.FILLBYTE_CHAR * (Const.MSG1_6_MESSAGE_LENGTH - len(t))
        payload = struct.pack(PayloadFormat.Message1_6,
                              self.fields[Payload.INTRUSION_CODE],
                              utils.int2bcd(self.fields[Payload.INTRUSION_DAY]),
                              utils.int2bcd(self.fields[Payload.INTRUSION_HOUR]),
                              utils.int2bcd(self.fields[Payload.INTRUSION_MINUTE]),
                              utils.int2bcd(self.fields[Payload.INTRUSION_SECOND]),
                              message,
                             )
        self.fields[Header.PAYLOAD_LENGTH] = len(payload)
        return payload

    def _unpackPayload(self, b):
        payload = self._getPayload(b)
        t = struct.unpack(PayloadFormat.Message1_6, payload)
        self.fields[Payload.INTRUSION_CODE]     = t[Message1_6.INTRUSION_CODE]
        self.fields[Payload.INTRUSION_DAY]      = utils.bcd2int(t[Message1_6.INTRUSION_DAY])
        self.fields[Payload.INTRUSION_HOUR]     = utils.bcd2int(t[Message1_6.INTRUSION_HOUR])
        self.fields[Payload.INTRUSION_MINUTE]   = utils.bcd2int(t[Message1_6.INTRUSION_MINUTE])
        self.fields[Payload.INTRUSION_SECOND]   = utils.bcd2int(t[Message1_6.INTRUSION_SECOND])
        self.fields[Payload.INTRUSION_MESSAGE]  = t[Message1_6.INTRUSION_MESSAGE].decode(Const.DEFAULT_CODEC)

    def __str__(self):
        s = self._header2string() + \
            '\n'.join([text.intrusionCode(      self.fields[Payload.INTRUSION_CODE]     ),
                       text.eventDate(          self.fields[Payload.INTRUSION_DAY],
                                                self.fields[Payload.INTRUSION_HOUR],
                                                self.fields[Payload.INTRUSION_MINUTE],
                                                self.fields[Payload.INTRUSION_SECOND],  ),
                       text.intrusionMessage(   self.fields[Payload.INTRUSION_MESSAGE]  ),
                     ])
        return s



class Msg1ConfirmReceipt(_Message1):
    '''
    Message No.7 in accordance with order No.268 Appendix 9 paragraph 7.

    RU: Сообщение №7 "Подтверждение приёма команды из пункта управления ОРМ"
    '''
    def __init__(self, *args):
        _Message1.__init__(self, MessageCode1.CONFIRM_RECEIPT, *args)
        self.fields.setdefault(Header.PAYLOAD_LENGTH,   2)
        self.fields.setdefault(Payload.COMMAND_CODE,    Const.FILLBYTE)
        self.fields.setdefault(Payload.RECEIPT_STATUS,  Const.FILLBYTE)

    def _packPayload(self):
        payload = struct.pack(PayloadFormat.Message1_7,
                              self.fields[Payload.COMMAND_CODE],
                              self.fields[Payload.RECEIPT_STATUS],
                             )
        self.fields[Header.PAYLOAD_LENGTH] = len(payload)
        return payload

    def _unpackPayload(self, b):
        print ("LLL", b)
        payload = self._getPayload(b)
        t = struct.unpack(PayloadFormat.Message1_7, payload)
        self.fields[Payload.COMMAND_CODE]   = t[Message1_7.COMMAND_CODE]
        self.fields[Payload.RECEIPT_STATUS] = t[Message1_7.RECEIPT_STATUS]

    def __str__(self):
        s = self._header2string() + \
            '\n'.join([text.commandCode(    self.fields[Payload.COMMAND_CODE]   ),
                       text.receiptStatus(  self.fields[Payload.RECEIPT_STATUS] ),
                     ])
        return s



class Msg1ConfirmExecution(_Message1):
    '''
    Message No.8 in accordance with order No.268 Appendix 9 paragraph 8.

    RU: Сообщение №8 "Подтверждение о выполнении команды из пункта управления ОРМ"
    '''

    def __init__(self, *args):
        _Message1.__init__(self, MessageCode1.CONFIRM_RECEIPT, *args)
        self.fields.setdefault(Payload.COMMAND_CODE,        Const.FILLBYTE)
        self.fields.setdefault(Payload.EXECUTION_STATUS,    Const.FILLBYTE)

    def _packPayload(self):
        payload = struct.pack(PayloadFormat.Message1_8,
                              self.fields[Payload.COMMAND_CODE],
                              self.fields[Payload.EXECUTION_STATUS],
                             )
        self.fields[Header.PAYLOAD_LENGTH] = len(payload)
        return payload

    def _unpackPayload(self, b):
        payload = self._getPayload(b)
        t = struct.unpack(PayloadFormat.Message1_8, payload)
        self.fields[Payload.COMMAND_CODE]       = t[Message1_8.COMMAND_CODE]
        self.fields[Payload.EXECUTION_STATUS]   = t[Message1_8.EXECUTION_STATUS]

    def __str__(self):
        s = self._header2string() + \
            '\n'.join([text.commandCode(    self.fields[Payload.COMMAND_CODE]       ),
                       text.executionStatus(self.fields[Payload.EXECUTION_STATUS]   ),
                     ])
        return s



class Msg1TestResponse(_Message1):
    '''
    Message No.9 in accordance with order No.268 Appendix 9 paragraph 9.

    RU: Сообщение №9 "Ответное тестовое сообщение"
    '''
    def __init__(self, *args):
        _Message1.__init__(self, MessageCode1.TEST_RESPONSE, *args)
        self.fields.setdefault(Payload.TEST_MESSAGE_NUMBER,     Const.FILLBYTE)
        self.fields.setdefault(Payload.CONTROL_CHANNEL_1_STATE, Const.FILLBYTE)
        self.fields.setdefault(Payload.CONTROL_CHANNEL_2_STATE, Const.FILLBYTE)

    def _packPayload(self):
        payload = struct.pack(PayloadFormat.Message1_9,
                              self.fields[Payload.TEST_MESSAGE_NUMBER],
                              self.fields[Payload.CONTROL_CHANNEL_1_STATE],
                              self.fields[Payload.CONTROL_CHANNEL_2_STATE],
                             )
        self.fields[Header.PAYLOAD_LENGTH] = len(payload)
        return payload

    def _unpackPayload(self, b):
        payload = self._getPayload(b)
        t = struct.unpack(PayloadFormat.Message1_9, payload)
        self.fields[Payload.TEST_MESSAGE_NUMBER]        = t[Message1_9.TEST_MESSAGE_NUMBER]
        self.fields[Payload.CONTROL_CHANNEL_1_STATE]    = t[Message1_9.CONTROL_CHANNEL_1_STATE]
        self.fields[Payload.CONTROL_CHANNEL_2_STATE]    = t[Message1_9.CONTROL_CHANNEL_2_STATE]

    def __str__(self):
        s = self._header2string() + \
            '\n'.join([text.testMessageNumber(      self.fields[Payload.TEST_MESSAGE_NUMBER]        ),
                       text.controlChannelStatus(   self.fields[Payload.CONTROL_CHANNEL_1_STATE],
                                                    self.fields[Payload.CONTROL_CHANNEL_2_STATE]    ),
                     ])
        return s



class Msg1LinksetInfo(_Message1):
    '''
    Message No.10 in accordance with order No.268 Appendix 9 paragraph 10.

    RU: Сообщение №10 "Данные о соответствии условных номеров пучков каналов и их реальных станционных имён"
    '''
    def __init__(self, *args):
        _Message1.__init__(self, MessageCode1.LINKSET_INFO, *args)
        self.fields.setdefault(Payload.LINKSET_NUMBER,  Const.FILLBYTE_TWO)
        self.fields.setdefault(Payload.LINKSET_NAME,    Const.FILLBYTE_CHAR * Const.MSG1_10_NAME_LENGTH)

    def _packPayload(self):
        t = self.fields.get(Payload.LINKSET_NAME)
        name = t.encode(Const.DEFAULT_CODEC) + \
                        Const.FILLBYTE_CHAR * (Const.MSG1_10_NAME_LENGTH - len(t))
        payload = struct.pack(PayloadFormat.Message1_10,
                              self.fields[Payload.LINKSET_NUMBER],
                              name,
                             )
        self.fields[Header.PAYLOAD_LENGTH] = len(payload)
        return payload

    def _unpackPayload(self, b):
        payload = self._getPayload(b)
        t = struct.unpack(PayloadFormat.Message1_10, payload)
        self.fields[Payload.LINKSET_NUMBER] = t[Message1_10.LINKSET_NUMBER]
        self.fields[Payload.LINKSET_NAME]   = t[Message1_10.LINKSET_NAME].decode(Const.DEFAULT_CODEC)

    def __str__(self):
        s = self._header2string() + \
            '\n'.join([text.linksetNumber(  self.fields[Payload.LINKSET_NUMBER] ),
                       text.linksetName(    self.fields[Payload.LINKSET_NAME]  ),
                     ])
        return s



class Msg1FirmwareVersionInfo(_Message1):
    '''
    Message No.11 in accordance with order No.268 Appendix 9 paragraph 11.

    RU: Сообщение №11 "Версия ПО станции"
    '''
    def __init__(self, *args):
        _Message1.__init__(self, MessageCode1.FIRMWARE_VERSION_INFO, *args)
        self.fields.setdefault(Payload.FIRMWARE_VERSION,    Const.FILLBYTE_CHAR * Const.MSG1_11_VERSION_LENGTH)
        self.fields.setdefault(Payload.STATION_TYPE,        Const.FILLBYTE)

    def _packPayload(self):
        t = self.fields.get(Payload.FIRMWARE_VERSION)
        version = t.encode(Const.DEFAULT_CODEC) + \
                           Const.FILLBYTE_CHAR * (Const.MSG1_11_VERSION_LENGTH - len(t))
        payload = struct.pack(PayloadFormat.Message1_11,
                              version,
                              self.fields[Payload.STATION_TYPE],
                             )
        self.fields[Header.PAYLOAD_LENGTH] = len(payload)
        return payload

    def _unpackPayload(self, b):
        payload = self._getPayload(b)
        t = struct.unpack(PayloadFormat.Message1_11, payload)
        self.fields[Payload.FIRMWARE_VERSION] = t[Message1_11.FIRMWARE_VERSION].decode(Const.DEFAULT_CODEC)
        self.fields[Payload.STATION_TYPE]     = t[Message1_11.STATION_TYPE]

    def __str__(self):
        s = self._header2string() + \
            '\n'.join([text.firmwareVersion(self.fields[Payload.FIRMWARE_VERSION]   ),
                       text.stationType(    self.fields[Payload.STATION_TYPE]       ),
                     ])
        return s



# TODO: Implement when SMG supports it
# class Msg1MessageTransmission(_Message1):
