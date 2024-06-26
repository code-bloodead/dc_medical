# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/heartbeat.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15proto/heartbeat.proto\"$\n\x08NodeInfo\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\t\"@\n\x05Stats\x12\x11\n\tcpu_usage\x18\x01 \x01(\t\x12\x12\n\ndisk_space\x18\x02 \x01(\t\x12\x10\n\x08used_mem\x18\x03 \x01(\t2*\n\x08HearBeat\x12\x1e\n\x07isAlive\x12\t.NodeInfo\x1a\x06.Stats\"\x00\x62\x06proto3')



_NODEINFO = DESCRIPTOR.message_types_by_name['NodeInfo']
_STATS = DESCRIPTOR.message_types_by_name['Stats']
NodeInfo = _reflection.GeneratedProtocolMessageType('NodeInfo', (_message.Message,), {
  'DESCRIPTOR' : _NODEINFO,
  '__module__' : 'proto.heartbeat_pb2'
  # @@protoc_insertion_point(class_scope:NodeInfo)
  })
_sym_db.RegisterMessage(NodeInfo)

Stats = _reflection.GeneratedProtocolMessageType('Stats', (_message.Message,), {
  'DESCRIPTOR' : _STATS,
  '__module__' : 'proto.heartbeat_pb2'
  # @@protoc_insertion_point(class_scope:Stats)
  })
_sym_db.RegisterMessage(Stats)

_HEARBEAT = DESCRIPTOR.services_by_name['HearBeat']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _NODEINFO._serialized_start=25
  _NODEINFO._serialized_end=61
  _STATS._serialized_start=63
  _STATS._serialized_end=127
  _HEARBEAT._serialized_start=129
  _HEARBEAT._serialized_end=171
# @@protoc_insertion_point(module_scope)
