# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dns.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tdns.proto\"C\n\x07request\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x0b\n\x03url\x18\x02 \x01(\t\x12\n\n\x02ip\x18\x03 \x01(\t\x12\x11\n\ttimestamp\x18\x04 \x01(\t\"\x1c\n\x08response\x12\x10\n\x08response\x18\x01 \x01(\t\"8\n\x0b\x62roadcastid\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0f\n\x07\x63hannel\x18\x03 \x01(\t\"#\n\x05probe\x12\x0c\n\x04port\x18\x01 \x01(\t\x12\x0c\n\x04\x66lag\x18\x02 \x01(\t20\n\ndnsService\x12\"\n\x0bSendMessage\x12\x08.request\x1a\t.response23\n\tbroadcast\x12&\n\x0bSendMessage\x12\x0c.broadcastid\x1a\t.response2+\n\x07\x63onnect\x12 \n\x0bSendMessage\x12\x06.probe\x1a\t.responseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'dns_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_REQUEST']._serialized_start=13
  _globals['_REQUEST']._serialized_end=80
  _globals['_RESPONSE']._serialized_start=82
  _globals['_RESPONSE']._serialized_end=110
  _globals['_BROADCASTID']._serialized_start=112
  _globals['_BROADCASTID']._serialized_end=168
  _globals['_PROBE']._serialized_start=170
  _globals['_PROBE']._serialized_end=205
  _globals['_DNSSERVICE']._serialized_start=207
  _globals['_DNSSERVICE']._serialized_end=255
  _globals['_BROADCAST']._serialized_start=257
  _globals['_BROADCAST']._serialized_end=308
  _globals['_CONNECT']._serialized_start=310
  _globals['_CONNECT']._serialized_end=353
# @@protoc_insertion_point(module_scope)
