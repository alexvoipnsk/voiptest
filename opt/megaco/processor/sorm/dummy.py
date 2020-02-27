
import struct

from processor.sorm.constants import (Header,
                               Payload,
                               DummyHeader,
                               HeaderFormat,
                               Const,
                              )
import processor.sorm.text
import processor.sorm.utils



class Message():
    '''
    Dummy message class for not implemented messages.
    '''
    def __init__(self, *args):
        self.fields = dict()
        for arg in args:
            if not isinstance(arg, dict):
                raise TypeError('Argument {} must be dict, but {} given!'.format(arg, type(arg)))
            self.fields.update(arg)

        self.fields.setdefault(Header.PREAMBLE,     Const.PREAMBLE)
        self.fields.setdefault(Header.SORM_NUMBER,  Const.DEFAULT_SORM_NUMBER)
        self.fields[Header.COMMAND_CODE]            = 0x00 # Unknown code
        self.fields[Header.PAYLOAD_LENGTH]          = 0 # Real payload length calculated while payload packed to bytes
        self.fields[Payload.UNKNOWN_BYTES]          = 0 # Real payload length calculated while payload packed to bytes

    def _packHeader(self):
        '''
        '''
        return struct.pack(HeaderFormat.Dummy,
                           self.fields.get(Header.PREAMBLE),
                           self.fields.get(Header.SORM_NUMBER),
                           self.fields.get(Header.COMMAND_CODE),
                           self.fields.get(Header.PAYLOAD_LENGTH),
                          )

    def _unpackHeader(self, b):
        '''
        '''
        if len(b) < Const.DUMMY_HDR_LENGTH:
            raise ValueError('SORM header too small.')
        t = struct.unpack(HeaderFormat.Dummy, b[:Const.CMD_HDR_LENGTH])
        self.fields[Header.PREAMBLE]        = t[DummyHeader.PREAMBLE]
        self.fields[Header.SORM_NUMBER]     = t[DummyHeader.SORM_NUMBER]
        self.fields[Header.COMMAND_CODE]    = t[DummyHeader.COMMAND_CODE]
        self.fields[Header.PAYLOAD_LENGTH]  = t[DummyHeader.PAYLOAD_LENGTH]

    def _packPayload(self):
        '''
        '''
        packFormat = '<{}s'.format(len(self.fields.get(Payload.UNKNOWN_BYTES)))
        payload = struct.pack(packFormat,
                              self.fields.get(Payload.UNKNOWN_BYTES)
                             )
        self.fields[Header.PAYLOAD_LENGTH] = len(payload)
        return payload

    def _unpackPayload(self, b):
        '''
        '''
        self.fields[Payload.UNKNOWN_BYTES] = self._getPayload(b)

    def _header2string(self):
        '''
        Convert internal representation of header to human readable string.
        '''
        s = '\n'.join(['- - - - - - -',
                       utils.printableBytes(bytes(self)),
                       text.preamble(       self.fields[Header.PREAMBLE]        ),
                       text.sormNumber(     self.fields[Header.SORM_NUMBER]     ),
                       text.commandCode(    self.fields[Header.COMMAND_CODE]    ),
                       text.payloadLength(  self.fields[Header.PAYLOAD_LENGTH]  ),
                       '- - -\n',
                     ])
        return s

    def _getPayload(self, b):
        return b[Const.DUMMY_HDR_LENGTH:]

    def __bytes__(self):
        '''
        Convert internal representation of header to bytes.

        Usage:
            It's used when you need send message via network:
                ``
                message = Message()
                sormAddr = ('192.0.2.1', 8888)
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(bytes(message), sormdAddr)
                ``

            or represent message as byte string:
                ``
                message = Message()
                hexRepr = ' '.join(['0x{:02X}'.format(x) for x in bytes(message)][1:])
                print(hexRepr)
                ``
        '''
        payload = self._packPayload() # Payload before header because we need to calculate payload length
        header = self._packHeader()
        return header + payload

    def __str__(self):
        return self._header2string() +\
               text.unknownBytes(self.fields[Payload.UNKNOWN_BYTES]),

    def fromBytes(self, b):
        self._unpackHeader(b)
        self._unpackPayload(b)
