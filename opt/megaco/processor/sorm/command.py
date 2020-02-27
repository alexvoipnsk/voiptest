
import struct

from processor.sorm.constants import (CommandCode,
                               Header,
                               Payload,
                               CommandHeader,
                               Command3,
                               Command4,
                               Command5,
                               Command6,
                               Command7,
                               Command8,
                               Command9,
                               Command10,
                               Command11,
                               Command12,
                               Command14,
                               Command15,
                               Command16,
                               HeaderFormat,
                               PayloadFormat,
                               Const,
                              )
import processor.sorm.text as text
import processor.sorm.utils as utils



class _Command():
    '''
    SORM command in accordance with order No.268 Appendix 5.

    Dummy class with main functionality. Please do not use it in you own code.
    Only way to use it - inherit new class from this.

    Inherited classes MUST implement these methods:
        _packPayload(self)
        _unpackPayload(self, b)
        __str__(self)
    '''
    def __init__(self, commandCode, *args):
        '''
        Arguments:
            commandCode: int()
            args*:       *dict()
        '''
        self.fields = dict()
        for arg in args:
            if not isinstance(arg, dict):
                raise TypeError('Argument {} must be dict, but {} given!'.format(arg, type(arg)))
            self.fields.update(arg)
        self.fields.setdefault(Header.PREAMBLE,     Const.PREAMBLE)
        self.fields.setdefault(Header.SORM_NUMBER,  Const.DEFAULT_SORM_NUMBER)
        self.fields[Header.COMMAND_CODE]            = commandCode
        self.fields[Header.PAYLOAD_LENGTH]          = 0 # Real payload length calculated while payload packed to bytes
        self.fields.setdefault(Header.PASSWORD,     Const.DEFAULT_SORM_PASSWORD)

    def _packHeader(self):
        '''
        Internal function.
        Pack header from class fields dictionary to binary.

        Return:
            bytes()
        '''
        return struct.pack(HeaderFormat.Command,
                           self.fields.get(Header.PREAMBLE),
                           self.fields.get(Header.SORM_NUMBER),
                           self.fields.get(Header.COMMAND_CODE),
                           self.fields.get(Header.PAYLOAD_LENGTH),
                           self.fields.get(Header.PASSWORD).encode(Const.DEFAULT_CODEC)
                          )

    def _unpackHeader(self, b):
        '''
        Internal function.
        Unpack header from binary to class fields dictionary.

        Arguments:
            b: bytes()
        '''
        if len(b) < Const.CMD_HDR_LENGTH:
            raise ValueError('Command header too small.')
        t = struct.unpack(HeaderFormat.Command, b[:Const.CMD_HDR_LENGTH])
        self.fields[Header.PREAMBLE]        = t[CommandHeader.PREAMBLE]
        self.fields[Header.SORM_NUMBER]     = t[CommandHeader.SORM_NUMBER]
        self.fields[Header.COMMAND_CODE]    = t[CommandHeader.COMMAND_CODE]
        self.fields[Header.PAYLOAD_LENGTH]  = t[CommandHeader.PAYLOAD_LENGTH]
        self.fields[Header.PASSWORD]        = t[CommandHeader.PASSWORD].decode(Const.DEFAULT_CODEC)

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
                       text.commandCode(    self.fields[Header.COMMAND_CODE]    ),
                       text.payloadLength(  self.fields[Header.PAYLOAD_LENGTH]  ),
                       text.password(       self.fields[Header.PASSWORD]        ),
                       '- - -\n',
                     ])
        return s

    def _header2strBytes(self):
        return utils.strBytes(bytes(self))

    def _getPayload(self, b):
        '''
        Internal function.
        Extract payload from binary.

        Arguments:
            b: bytes()
        Return:
            bytes()
        '''
        payload = b[Const.CMD_HDR_LENGTH:]
        if len(payload) != self.fields[Header.PAYLOAD_LENGTH]:
            raise ValueError('Wrong payload size, expected 0x{:02X}, but got 0x{:02X}.'.format(self.fields[Header.PAYLOAD_LENGTH],
                                                                                               len(payload)
                                                                                              ))
        return payload

    def __bytes__(self):
        '''
        Convert internal representation of command to bytes.

        Usage:
            It's used when you need send command via network:
                command = Command() # Replace Command() to command you needed
                sormAddr = ('192.0.2.1', 8888)
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(bytes(command), sormdAddr)

            or represent command as byte string:
                command = Command() # Replace Command() to command you needed
                hexRepr = ' '.join(['0x{:02X}'.format(x) for x in bytes(command)][1:])
                print(hexRepr)

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



class CmdSORMStart(_Command):
    '''
    Command No.1 in accordance with order No.268 Appendix 6 paragraph 1.

    RU: Команда №1 "Запуск технических средств ОРМ"
    '''
    def __init__(self, *args):
        _Command.__init__(self, CommandCode.SORM_START, *args)

    def _packPayload(self):
        return b'' # No payload in this message

    def _unpackPayload(self, b):
        pass # No payload in this message

    def __str__(self):
        return self._header2string()


class CmdSORMStop(_Command):
    '''
    Command No.2 in accordance with order No.268 Appendix 6 paragraph 2.

    RU: Команда №2 "Останов технических средств ОРМ"
    '''
    def __init__(self, *args):
        _Command.__init__(self, CommandCode.SORM_STOP, *args)

    def _packPayload(self):
        return b'' # No payload in this message

    def _unpackPayload(self, b):
        pass # No payload in this message

    def __str__(self):
        return self._header2string()



class CmdPasswordSet(_Command):
    '''
    Command No.3 in accordance with order No.268 Appendix 6 paragraph 3.

    RU: Команда №3 "Задание пароля"
    '''
    def __init__(self, *args):
        _Command.__init__(self, CommandCode.PASSWORD_SET, *args)
        self.fields.setdefault(Payload.NEW_PASSWORD, Const.DEFAULT_SORM_PASSWORD)

    def _packPayload(self):
        payload = struct.pack(PayloadFormat.Command3,
                              self.fields.get(Payload.NEW_PASSWORD).encode(Const.DEFAULT_CODEC)
                             )
        self.fields[Header.PAYLOAD_LENGTH] = len(payload)
        return payload

    def _unpackPayload(self, b):
        payload = self._getPayload(b)
        t = struct.unpack(PayloadFormat.Command3, payload)
        self.fields[Payload.NEW_PASSWORD] = t[Command3.NEW_PASSWORD].decode(Const.DEFAULT_CODEC)

    def __str__(self):
        s = self._header2string() + \
            '\n'.join([text.newPassword(self.fields[Payload.NEW_PASSWORD]), ])
        return s



class CmdControlLineAdd(_Command):
    '''
    Command No.4 in accordance with order No.268 Appendix 6 paragraph 4.

    RU: Команда №4 "Закрепление контрольной соединительной линии за группой"
    '''
    def __init__(self, *args):
        _Command.__init__(self, CommandCode.CONTROL_LINE_ADD, *args)
        self.fields.setdefault(Payload.LINE_A_NUMBER, Const.FILLBYTE)
        self.fields.setdefault(Payload.LINE_B_NUMBER, Const.FILLBYTE)
        self.fields.setdefault(Payload.LINE_A_STREAM_NUMBER, Const.ZEROBYTE)
        self.fields.setdefault(Payload.LINE_B_STREAM_NUMBER, Const.ZEROBYTE)

    def _packPayload(self):
        controlLineA = utils.mergeStreamAndLine(self.fields.get(Payload.LINE_A_STREAM_NUMBER),
                                                self.fields.get(Payload.LINE_A_NUMBER)
                                               )
        controlLineB = utils.mergeStreamAndLine(self.fields.get(Payload.LINE_B_STREAM_NUMBER),
                                                self.fields.get(Payload.LINE_B_NUMBER)
                                               )
        payload = struct.pack(PayloadFormat.Command4,
                              self.fields.get(Payload.LINE_GROUP_NUMBER),
                              self.fields.get(Payload.LINE_GROUP_TYPE),
                              controlLineA,
                              controlLineB,
                             )
        self.fields[Header.PAYLOAD_LENGTH] = len(payload)
        return payload

    def _unpackPayload(self, b):
        payload = self._getPayload(b)
        t = struct.unpack(PayloadFormat.Command4, payload)
        self.fields[Payload.LINE_GROUP_NUMBER]  = t[Command4.LINE_GROUP_NUMBER]
        self.fields[Payload.LINE_GROUP_TYPE]    = t[Command4.LINE_GROUP_TYPE]
        self.fields[Payload.LINE_A_STREAM_NUMBER], \
        self.fields[Payload.LINE_A_NUMBER] = utils.splitStreamAndLine(t[Command4.LINE_A_NUMBER])
        self.fields[Payload.LINE_B_STREAM_NUMBER], \
        self.fields[Payload.LINE_B_NUMBER] = utils.splitStreamAndLine(t[Command4.LINE_B_NUMBER])

    def __str__(self):
        s = self._header2string() + \
            '\n'.join([text.lineGroupNumber(self.fields[Payload.LINE_GROUP_NUMBER]      ),
                       text.lineGroupType(  self.fields[Payload.LINE_GROUP_TYPE]        ),
                       text.lineANumber(    self.fields[Payload.LINE_A_STREAM_NUMBER],
                                            self.fields[Payload.LINE_A_NUMBER]          ),
                       text.lineBNumber(    self.fields[Payload.LINE_B_STREAM_NUMBER],
                                            self.fields[Payload.LINE_B_NUMBER]          ),
                     ])
        return s



class CmdObjectAdd(_Command):
    '''
    Command No.5 in accordance with order No.268 Appendix 6 paragraph 5.

    RU: Команда №5 "Постановка объекта на контроль"
    '''
    def __init__(self, *args):
        _Command.__init__(self, CommandCode.OBJECT_ADD, *args)
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

    def _packPayload(self):
        payload = struct.pack(PayloadFormat.Command5,
                              self.fields[Payload.OBJECT_NUMBER],
                              self.fields[Payload.OBJECT_TYPE],
                              self.fields[Payload.PHONE_TYPE],
                              self.fields[Payload.PHONE_LENGTH],
                              utils.phone2bcd(self.fields[Payload.PHONE_NUMBER]),
                              self.fields[Payload.LINKSET_NUMBER],
                              self.fields[Payload.CONTROL_CATEGORY],
                              self.fields[Payload.LINE_GROUP_NUMBER],
                              self.fields[Payload.PRIORITY],
                             )
        self.fields[Header.PAYLOAD_LENGTH] = len(payload)
        return payload

    def _unpackPayload(self, b):
        payload = self._getPayload(b)
        t = struct.unpack(PayloadFormat.Command5, payload)
        self.fields[Payload.OBJECT_NUMBER]      = t[Command5.OBJECT_NUMBER]
        self.fields[Payload.OBJECT_TYPE]        = t[Command5.OBJECT_TYPE]
        self.fields[Payload.PHONE_TYPE]         = t[Command5.PHONE_TYPE]
        self.fields[Payload.PHONE_LENGTH]       = t[Command5.PHONE_LENGTH]
        self.fields[Payload.PHONE_NUMBER]       = utils.bcd2phone(t[Command5.PHONE_NUMBER])
        self.fields[Payload.LINKSET_NUMBER]     = t[Command5.LINKSET_NUMBER]
        self.fields[Payload.CONTROL_CATEGORY]   = t[Command5.CONTROL_CATEGORY]
        self.fields[Payload.LINE_GROUP_NUMBER]  = t[Command5.LINE_GROUP_NUMBER]
        self.fields[Payload.PRIORITY]           = t[Command5.PRIORITY]

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
                     ])
        return s



class CmdObjectRemove(_Command):
    '''
    Command No.6 in accordance with order No.268 Appendix 6 paragraph 6.

    RU: Команда №6 "Снятие объекта с контроля"
    '''
    def __init__(self, *args):
        _Command.__init__(self, CommandCode.OBJECT_REMOVE, *args)
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

    def _packPayload(self):
        payload = struct.pack(PayloadFormat.Command6,
                              self.fields[Payload.OBJECT_NUMBER],
                              self.fields[Payload.OBJECT_TYPE],
                              self.fields[Payload.PHONE_TYPE],
                              self.fields[Payload.PHONE_LENGTH],
                              utils.phone2bcd(self.fields[Payload.PHONE_NUMBER]),
                              self.fields[Payload.LINKSET_NUMBER],
                             )
        self.fields[Header.PAYLOAD_LENGTH] = len(payload)
        return payload

    def _unpackPayload(self, b):
        payload = self._getPayload(b)
        t = struct.unpack(PayloadFormat.Command6, payload)
        self.fields[Payload.OBJECT_NUMBER]      = t[Command6.OBJECT_NUMBER]
        self.fields[Payload.OBJECT_TYPE]        = t[Command6.OBJECT_TYPE]
        self.fields[Payload.PHONE_TYPE]         = t[Command6.PHONE_TYPE]
        self.fields[Payload.PHONE_LENGTH]       = t[Command6.PHONE_LENGTH]
        self.fields[Payload.PHONE_NUMBER]       = utils.bcd2phone(t[Command6.PHONE_NUMBER])
        self.fields[Payload.LINKSET_NUMBER]     = t[Command6.LINKSET_NUMBER]

    def __str__(self):
        s = self._header2string() + \
            '\n'.join([text.objectNumber(   self.fields[Payload.OBJECT_NUMBER]  ),
                       text.objectType(     self.fields[Payload.OBJECT_TYPE]    ),
                       text.phoneType(      self.fields[Payload.PHONE_TYPE]     ),
                       text.phoneLength(    self.fields[Payload.PHONE_LENGTH]   ),
                       text.phoneNumber(    self.fields[Payload.PHONE_NUMBER]   ),
                       text.linksetNumber(  self.fields[Payload.LINKSET_NUMBER] ),
                     ])
        return s



class CmdControlLineConnect(_Command):
    '''
    Command No.7 in accordance with order No.268 Appendix 6 paragraph 7.

    RU: Команда №7 "Подключение к разговорному тракту"
    '''
    def __init__(self, *args):
        _Command.__init__(self, CommandCode.CONTROL_LINE_CONNECT, *args)
        self.fields.setdefault(Payload.CALL_NUMBER,         Const.FILLBYTE_TWO)
        self.fields.setdefault(Payload.OBJECT_TYPE,         Const.FILLBYTE)
        self.fields.setdefault(Payload.OBJECT_NUMBER,       Const.FILLBYTE_TWO)
        self.fields.setdefault(Payload.LINE_GROUP_NUMBER,   Const.FILLBYTE)

    def _packPayload(self):
        payload = struct.pack(PayloadFormat.Command7,
                              self.fields.get(Payload.CALL_NUMBER),
                              self.fields.get(Payload.OBJECT_TYPE),
                              self.fields.get(Payload.OBJECT_NUMBER),
                              self.fields.get(Payload.LINE_GROUP_NUMBER),
                             )
        self.fields[Header.PAYLOAD_LENGTH] = len(payload)
        return payload

    def _unpackPayload(self, b):
        payload = self._getPayload(b)
        t = struct.unpack(PayloadFormat.Command7, payload)
        self.fields[Payload.CALL_NUMBER]        = t[Command7.CALL_NUMBER]
        self.fields[Payload.OBJECT_TYPE]        = t[Command7.OBJECT_TYPE]
        self.fields[Payload.OBJECT_NUMBER]      = t[Command7.OBJECT_NUMBER]
        self.fields[Payload.LINE_GROUP_NUMBER]  = t[Command7.LINE_GROUP_NUMBER]

    def __str__(self):
        s = self._header2string() + \
            '\n'.join([text.callNumber(     self.fields[Payload.CALL_NUMBER]        ),
                       text.objectType(     self.fields[Payload.OBJECT_TYPE]        ),
                       text.objectNumber(   self.fields[Payload.OBJECT_NUMBER]      ),
                       text.lineGroupNumber(self.fields[Payload.LINE_GROUP_NUMBER]  ),
                     ])
        return s



class CmdControlLineDisconnect(_Command):
    '''
    Command No.8 in accordance with order No.268 Appendix 6 paragraph 8.

    RU: Команда №8 "Освобождение контрольной соединительной линии"
    '''
    def __init__(self, *args):
        _Command.__init__(self, CommandCode.CONTROL_LINE_DISCONNECT, *args)
        self.fields.setdefault(Payload.CALL_NUMBER,         Const.FILLBYTE_TWO)
        self.fields.setdefault(Payload.OBJECT_TYPE,         Const.FILLBYTE)
        self.fields.setdefault(Payload.OBJECT_NUMBER,       Const.FILLBYTE_TWO)
        self.fields.setdefault(Payload.LINE_A_NUMBER,       Const.FILLBYTE)
        self.fields.setdefault(Payload.LINE_B_NUMBER,       Const.FILLBYTE)
        self.fields.setdefault(Payload.LINE_A_STREAM_NUMBER, Const.ZEROBYTE)
        self.fields.setdefault(Payload.LINE_B_STREAM_NUMBER, Const.ZEROBYTE)

    def _packPayload(self):
        controlLineA = utils.mergeStreamAndLine(self.fields.get(Payload.LINE_A_STREAM_NUMBER),
                                                self.fields.get(Payload.LINE_A_NUMBER)
                                               )
        controlLineB = utils.mergeStreamAndLine(self.fields.get(Payload.LINE_B_STREAM_NUMBER),
                                                self.fields.get(Payload.LINE_B_NUMBER)
                                               )
        payload = struct.pack(PayloadFormat.Command8,
                              self.fields.get(Payload.CALL_NUMBER),
                              self.fields.get(Payload.OBJECT_TYPE),
                              self.fields.get(Payload.OBJECT_NUMBER), 
                              controlLineA,
                              controlLineB,
                              #self.fields.get(controlLineA),
                              #self.fields.get(controlLineB),
                             )
        self.fields[Header.PAYLOAD_LENGTH] = len(payload)
        return payload

    def _unpackPayload(self, b):
        payload = self._getPayload(b)
        t = struct.unpack(PayloadFormat.Command8, payload)
        self.fields[Payload.CALL_NUMBER]        = t[Command8.CALL_NUMBER]
        self.fields[Payload.OBJECT_TYPE]        = t[Command8.OBJECT_TYPE]
        self.fields[Payload.OBJECT_NUMBER]      = t[Command8.OBJECT_NUMBER]
        self.fields[Payload.LINE_A_STREAM_NUMBER], \
        self.fields[Payload.LINE_A_NUMBER] = utils.splitStreamAndLine(t[Command8.LINE_A_NUMBER])
        self.fields[Payload.LINE_B_STREAM_NUMBER], \
        self.fields[Payload.LINE_B_NUMBER] = utils.splitStreamAndLine(t[Command8.LINE_B_NUMBER])

    def __str__(self):
        s = self._header2string() + \
            '\n'.join([text.callNumber(     self.fields[Payload.CALL_NUMBER]            ),
                       text.objectType(     self.fields[Payload.OBJECT_TYPE]            ),
                       text.objectNumber(   self.fields[Payload.OBJECT_NUMBER]          ),
                       text.lineANumber(    self.fields[Payload.LINE_A_STREAM_NUMBER],
                                            self.fields[Payload.LINE_A_NUMBER]          ),
                       text.lineBNumber(    self.fields[Payload.LINE_B_STREAM_NUMBER],
                                            self.fields[Payload.LINE_B_NUMBER]          ),
                     ])
        return s



class CmdControlLineRemove(_Command):
    '''
    Command No.9 in accordance with order No.268 Appendix 6 paragraph 9.

    RU: Команда №9 "Исключение контрольной соединительной линии из группы"
    '''
    def __init__(self, *args):
        _Command.__init__(self, CommandCode.CONTROL_LINE_REMOVE, *args)
        self.fields.setdefault(Payload.LINE_GROUP_NUMBER,       Const.FILLBYTE)
        self.fields.setdefault(Payload.LINE_A_NUMBER,           Const.FILLBYTE)
        self.fields.setdefault(Payload.LINE_A_STREAM_NUMBER,    Const.ZEROBYTE)
        self.fields.setdefault(Payload.LINE_B_NUMBER,           Const.FILLBYTE)
        self.fields.setdefault(Payload.LINE_B_STREAM_NUMBER,    Const.ZEROBYTE)

    def _packPayload(self):
        controlLineA = utils.mergeStreamAndLine(self.fields.get(Payload.LINE_A_STREAM_NUMBER),
                                                self.fields.get(Payload.LINE_A_NUMBER)
                                               )
        controlLineB = utils.mergeStreamAndLine(self.fields.get(Payload.LINE_B_STREAM_NUMBER),
                                                self.fields.get(Payload.LINE_B_NUMBER)
                                               )
        payload = struct.pack(PayloadFormat.Command9,
                              self.fields.get(Payload.LINE_GROUP_NUMBER),
                              controlLineA,
                              controlLineB,
                             )
        self.fields[Header.PAYLOAD_LENGTH] = len(payload)
        return payload

    def _unpackPayload(self, b):
        payload = self._getPayload(b)
        t = struct.unpack(PayloadFormat.Command9, payload)
        self.fields[Payload.LINE_GROUP_NUMBER]  = t[Command9.LINE_GROUP_NUMBER]
        self.fields[Payload.LINE_A_STREAM_NUMBER], \
        self.fields[Payload.LINE_A_NUMBER] = utils.splitStreamAndLine(t[Command9.LINE_A_NUMBER])
        self.fields[Payload.LINE_B_STREAM_NUMBER], \
        self.fields[Payload.LINE_B_NUMBER] = utils.splitStreamAndLine(t[Command9.LINE_B_NUMBER])

    def __str__(self):
        s = self._header2string() + \
            '\n'.join([text.lineGroupNumber(self.fields[Payload.LINE_GROUP_NUMBER]      ),
                       text.lineANumber(    self.fields[Payload.LINE_A_STREAM_NUMBER],
                                            self.fields[Payload.LINE_A_NUMBER]          ),
                       text.lineBNumber(    self.fields[Payload.LINE_B_STREAM_NUMBER],
                                            self.fields[Payload.LINE_B_NUMBER]          ),
                     ])
        return s



class CmdObjectGetInfo(_Command):
    '''
    Command No.10 in accordance with order No.268 Appendix 6 paragraph 10.

    RU: Команда №10 "Запрос на передачу данных об объектах контроля"
    '''
    def __init__(self, *args):
        _Command.__init__(self, CommandCode.OBJECT_GET_INFO, *args)
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

    def _packPayload(self):
        payload = struct.pack(PayloadFormat.Command10,
                              self.fields[Payload.OBJECT_NUMBER],
                              self.fields[Payload.OBJECT_TYPE],
                              self.fields[Payload.PHONE_TYPE],
                              self.fields[Payload.PHONE_LENGTH],
                              utils.phone2bcd(self.fields[Payload.PHONE_NUMBER]),
                              self.fields[Payload.LINKSET_NUMBER],
                             )
        self.fields[Header.PAYLOAD_LENGTH] = len(payload)
        return payload

    def _unpackPayload(self, b):
        payload = self._getPayload(b)
        t = struct.unpack(PayloadFormat.Command10, payload)
        self.fields[Payload.OBJECT_NUMBER]      = t[Command10.OBJECT_NUMBER]
        self.fields[Payload.OBJECT_TYPE]        = t[Command10.OBJECT_TYPE]
        self.fields[Payload.PHONE_TYPE]         = t[Command10.PHONE_TYPE]
        self.fields[Payload.PHONE_LENGTH]       = t[Command10.PHONE_LENGTH]
        self.fields[Payload.PHONE_NUMBER]       = utils.bcd2phone(t[Command10.PHONE_NUMBER])
        self.fields[Payload.LINKSET_NUMBER]     = t[Command10.LINKSET_NUMBER]

    def __str__(self):
        s = self._header2string() + \
            '\n'.join([text.objectNumber(   self.fields[Payload.OBJECT_NUMBER]  ),
                       text.objectType(     self.fields[Payload.OBJECT_TYPE]    ),
                       text.phoneType(      self.fields[Payload.PHONE_TYPE]     ),
                       text.phoneLength(    self.fields[Payload.PHONE_LENGTH]   ),
                       text.phoneNumber(    self.fields[Payload.PHONE_NUMBER]   ),
                       text.linksetNumber(  self.fields[Payload.LINKSET_NUMBER] ),
                     ])
        return s



class CmdControlLineGetInfo(_Command):
    '''
    Command No.11 in accordance with order No.268 Appendix 6 paragraph 11.

    RU: Команда №11 "Запрос на передачу информации о соответствии между КСЛ и группами"
    '''
    def __init__(self, *args):
        _Command.__init__(self, CommandCode.CONTROL_LINE_GET_INFO, *args)
        self.fields.setdefault(Payload.LINE_GROUP_NUMBER,       Const.FILLBYTE)
        self.fields.setdefault(Payload.LINE_GROUP_TYPE,         Const.FILLBYTE)
        self.fields.setdefault(Payload.LINE_A_NUMBER,           Const.FILLBYTE)
        self.fields.setdefault(Payload.LINE_B_NUMBER,           Const.FILLBYTE)
        self.fields.setdefault(Payload.LINE_A_STREAM_NUMBER,    Const.ZEROBYTE)
        self.fields.setdefault(Payload.LINE_B_STREAM_NUMBER,    Const.ZEROBYTE)

    def _packPayload(self):
        controlLineA = utils.mergeStreamAndLine(self.fields.get(Payload.LINE_A_STREAM_NUMBER),
                                                self.fields.get(Payload.LINE_A_NUMBER)
                                               )
        controlLineB = utils.mergeStreamAndLine(self.fields.get(Payload.LINE_B_STREAM_NUMBER),
                                                self.fields.get(Payload.LINE_B_NUMBER)
                                               )
        payload = struct.pack(PayloadFormat.Command11,
                              self.fields.get(Payload.LINE_GROUP_NUMBER),
                              self.fields.get(Payload.LINE_GROUP_TYPE),
                              controlLineA,
                              controlLineB,
                             )
        self.fields[Header.PAYLOAD_LENGTH] = len(payload)
        return payload

    def _unpackPayload(self, b):
        payload = self._getPayload(b)
        t = struct.unpack(PayloadFormat.Command11, payload)
        self.fields[Payload.LINE_GROUP_NUMBER]  = t[Command11.LINE_GROUP_NUMBER]
        self.fields[Payload.LINE_GROUP_TYPE]    = t[Command11.LINE_GROUP_TYPE]
        self.fields[Payload.LINE_A_STREAM_NUMBER], \
        self.fields[Payload.LINE_A_NUMBER] = utils.splitStreamAndLine(t[Command11.LINE_A_NUMBER])
        self.fields[Payload.LINE_B_STREAM_NUMBER], \
        self.fields[Payload.LINE_B_NUMBER] = utils.splitStreamAndLine(t[Command11.LINE_B_NUMBER])

    def __str__(self):
        s = self._header2string() + \
            '\n'.join([text.lineGroupNumber(self.fields[Payload.LINE_GROUP_NUMBER]      ),
                       text.lineGroupType(  self.fields[Payload.LINE_GROUP_TYPE]        ),
                       text.lineANumber(    self.fields[Payload.LINE_A_STREAM_NUMBER],
                                            self.fields[Payload.LINE_A_NUMBER]          ),
                       text.lineBNumber(    self.fields[Payload.LINE_B_STREAM_NUMBER],
                                            self.fields[Payload.LINE_B_NUMBER]          ),
                     ])
        return s



class CmdServicesGetInfo(_Command):
    '''
    Command No.12 in accordance with order No.268 Appendix 6 paragraph 12.

    RU: Команда №12 "Запрос на передачу списка услуг связи"
    '''
    def __init__(self, *args):
        _Command.__init__(self, CommandCode.SERVICES_GET_INFO, *args)
        self.fields.setdefault(Payload.PHONE_TYPE,      Const.FILLBYTE)
        self.fields.setdefault(Payload.PHONE_NUMBER,    '')
        if self.fields[Payload.PHONE_NUMBER] == '':
            length = Const.FILLBYTE
        else:
            length = len(self.fields[Payload.PHONE_NUMBER])
        self.fields.setdefault(Payload.PHONE_LENGTH,        length)

    def _packPayload(self):
        print("1111", self.fields)
        payload = struct.pack(PayloadFormat.Command12,
                              self.fields.get(Payload.PHONE_TYPE),
                              self.fields.get(Payload.PHONE_LENGTH),
                              utils.phone2bcd(self.fields[Payload.PHONE_NUMBER]),
                              #self.fields.get(Payload.PHONE_NUMBER),
                             )
        self.fields[Header.PAYLOAD_LENGTH] = len(payload)
        return payload

    def _unpackPayload(self, b):
        payload = self._getPayload(b)
        t = struct.unpack(PayloadFormat.Command12, payload)
        self.fields[Payload.PHONE_TYPE]     = t[Command12.PHONE_TYPE]
        self.fields[Payload.PHONE_LENGTH]   = t[Command12.PHONE_LENGTH]
        self.fields[Payload.PHONE_NUMBER]   = t[Command12.PHONE_NUMBER]

    def __str__(self):
        s = self._header2string() + \
            '\n'.join([text.phoneType(  self.fields[Payload.PHONE_TYPE]     ),
                       text.phoneLength(self.fields[Payload.PHONE_LENGTH]   ),
                       text.phoneNumber(self.fields[Payload.PHONE_NUMBER]   ),
                     ])
        return s



class CmdCommandInterrupt(_Command):
    '''
    Command No.13 in accordance with order No.268 Appendix 6 paragraph 13.

    RU: Команда №13 "Прерывание выдачи сообщений на запросы содержимого таблиц"
    '''
    def __init__(self, *args):
        _Command.__init__(self, CommandCode.COMMAND_INTERRUPT, *args)

    def _packPayload(self):
        return b'' # No payload in this message

    def _unpackPayload(self, b):
        pass # No payload in this message

    def __str__(self):
        return self._header2string()



class CmdTestRequest(_Command):
    '''
    Command No.14 in accordance with order No.268 Appendix 9 paragraph 14.

    RU: Команда №14 "Тестирование каналов передачи данных"
    '''
    def __init__(self, *args):
        _Command.__init__(self, CommandCode.TEST_REQUEST, *args)
        self.fields.setdefault(Payload.TEST_MESSAGE_NUMBER, Const.ZEROBYTE)

    def _packPayload(self):
        payload = struct.pack(PayloadFormat.Command14,
                              self.fields.get(Payload.TEST_MESSAGE_NUMBER)
                             )
        self.fields[Header.PAYLOAD_LENGTH] = len(payload)
        return payload

    def _unpackPayload(self, b):
        payload = self._getPayload(b)
        t = struct.unpack(PayloadFormat.Command14, payload)
        self.fields[Payload.TEST_MESSAGE_NUMBER]  = t[Command14.TEST_MESSAGE_NUMBER]

    def __str__(self):
        s = self._header2string() + \
            '\n'.join([text.testMessageNumber(self.fields[Payload.TEST_MESSAGE_NUMBER]), ])
        return s



class CmdObjectChange(_Command):
    '''
    Command No.15 in accordance with order No.268 Appendix 9 paragraph 15.

    RU: Команда №15 "Изменение параметров объекта контроля"
    '''
    def __init__(self, *args):
        _Command.__init__(self, CommandCode.OBJECT_CHANGE, *args)
        self.fields.setdefault(Payload.OBJECT_NUMBER,       Const.FILLBYTE_TWO)
        self.fields.setdefault(Payload.CONTROL_CATEGORY,    Const.FILLBYTE)
        self.fields.setdefault(Payload.LINE_GROUP_NUMBER,   Const.FILLBYTE)
        self.fields.setdefault(Payload.PRIORITY,            Const.FILLBYTE)

    def _packPayload(self):
        payload = struct.pack(PayloadFormat.Command15,
                              self.fields.get(Payload.OBJECT_NUMBER),
                              self.fields.get(Payload.CONTROL_CATEGORY),
                              self.fields.get(Payload.LINE_GROUP_NUMBER),
                              self.fields.get(Payload.PRIORITY),
                             )
        self.fields[Header.PAYLOAD_LENGTH] = len(payload)
        return payload

    def _unpackPayload(self, b):
        payload = self._getPayload(b)
        t = struct.unpack(PayloadFormat.Command15, payload)
        self.fields[Payload.OBJECT_NUMBER]      = t[Command15.OBJECT_NUMBER]
        self.fields[Payload.CONTROL_CATEGORY]   = t[Command15.CONTROL_CATEGORY]
        self.fields[Payload.LINE_GROUP_NUMBER]  = t[Command15.LINE_GROUP_NUMBER]
        self.fields[Payload.PRIORITY]           = t[Command15.PRIORITY]

    def __str__(self):
        s = self._header2string() + \
            '\n'.join([text.objectNumber(   self.fields[Payload.OBJECT_NUMBER]      ),
                       text.controlCategory(self.fields[Payload.CONTROL_CATEGORY]   ),
                       text.lineGroupNumber(self.fields[Payload.LINE_GROUP_NUMBER]  ),
                       text.priority(       self.fields[Payload.PRIORITY]           ),
                     ])
        return s



class CmdLinksetGetInfo(_Command):
    '''
    Command No.16 in accordance with order No.268 Appendix 9 paragraph 16.

    RU: Команда №16 "Запрос на передачу информации о соответствии имени пучка каналов и его условного номера"
    '''
    def __init__(self, *args):
        _Command.__init__(self, CommandCode.LINKSET_GET_INFO, *args)
        self.fields.setdefault(Payload.LINKSET_NUMBER, Const.FILLBYTE_TWO)

    def _packPayload(self):
        payload = struct.pack(PayloadFormat.Command16,
                              self.fields.get(Payload.LINKSET_NUMBER),
                             )
        self.fields[Header.PAYLOAD_LENGTH] = len(payload)
        return payload

    def _unpackPayload(self, b):
        payload = self._getPayload(b)
        t = struct.unpack(PayloadFormat.Command16, payload)
        self.fields[Payload.OBJECT_NUMBER]      = t[Command16.LINKSET_NUMBER]

    def __str__(self):
        s = self._header2string() + \
            '\n'.join([text.linksetNumber(self.fields[Payload.LINKSET_NUMBER]), ])
        return s



class CmdFirmwareVersionGet(_Command):
    '''
    Command No.17 in accordance with order No.268 Appendix 6 paragraph 17.

    RU: Команда №17 "Запрос версии ПО узла связи"
    '''
    def __init__(self, *args):
        _Command.__init__(self, CommandCode.FIRMWARE_VERSION_GET, *args)

    def _packPayload(self):
        return b'' # No payload in this message

    def _unpackPayload(self, b):
        pass # No payload in this message

    def __str__(self):
        return self._header2string()
