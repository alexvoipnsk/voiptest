#!/usr/bin/env python3

import logging
import socket
import sctp
import sys
import modules.m2ua.m2ua as m2ua

#Config parameters values
address0 = '192.168.118.46'
port0 = 2904
address1 = '192.168.118.88'
port1 = 2904
address2 = '192.168.118.46'
port2 = 2906
address3 = '192.168.118.215'
port3 = 2904
asp0 = 10
asp1 = 11
iid2 = 10
iid3 = 11

#Message builder and parser
builder = m2ua.Message_Builder()
parser = m2ua.Message_Parser()
validator = m2ua.Parameters_Validator()

#Create SCTP socket
recv_buf = 15000
sk0 = sctp.sctpsocket_tcp(socket.AF_INET)
sk0.settimeout(30)
sk0.bind((address0, port0))
sk0.connect((address1, port1))

message = builder.Build_ASP_UP_Message(asp_identifier=224, info_string="sigtran test")
sk0.sctp_send(message,ppid=0x02000000)

message = sk0.recv(15000)
obj_message = parser.Parse_Message(message)
validation_result = validator.Validate_Message_W_Params(obj_message, 'mgmt', 'ERR', [(12, 15)])

#Close SCTP socket
sk0.close()
