# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/fluffy.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12proto/fluffy.proto\x12\x06\x66luffy\"*\n\x08\x46ileData\x12\x10\n\x08\x66ileName\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c\"\x1c\n\x08\x46ileInfo\x12\x10\n\x08\x66ileName\x18\x01 \x01(\t\"#\n\x0fRequestFileList\x12\x10\n\x08isClient\x18\x01 \x01(\x08\" \n\x08\x46ileList\x12\x14\n\x0clstFileNames\x18\x01 \x03(\t2\xee\x01\n\x13\x44\x61taTransferService\x12\x32\n\nUploadFile\x12\x10.fluffy.FileData\x1a\x10.fluffy.FileInfo(\x01\x12\x34\n\x0c\x44ownloadFile\x12\x10.fluffy.FileInfo\x1a\x10.fluffy.FileData0\x01\x12\x35\n\rReplicateFile\x12\x10.fluffy.FileData\x1a\x10.fluffy.FileInfo(\x01\x12\x36\n\tListFiles\x12\x17.fluffy.RequestFileList\x1a\x10.fluffy.FileListB\x04H\x01P\x01\x62\x06proto3')



_FILEDATA = DESCRIPTOR.message_types_by_name['FileData']
_FILEINFO = DESCRIPTOR.message_types_by_name['FileInfo']
_REQUESTFILELIST = DESCRIPTOR.message_types_by_name['RequestFileList']
_FILELIST = DESCRIPTOR.message_types_by_name['FileList']
FileData = _reflection.GeneratedProtocolMessageType('FileData', (_message.Message,), {
  'DESCRIPTOR' : _FILEDATA,
  '__module__' : 'proto.fluffy_pb2'
  # @@protoc_insertion_point(class_scope:fluffy.FileData)
  })
_sym_db.RegisterMessage(FileData)

FileInfo = _reflection.GeneratedProtocolMessageType('FileInfo', (_message.Message,), {
  'DESCRIPTOR' : _FILEINFO,
  '__module__' : 'proto.fluffy_pb2'
  # @@protoc_insertion_point(class_scope:fluffy.FileInfo)
  })
_sym_db.RegisterMessage(FileInfo)

RequestFileList = _reflection.GeneratedProtocolMessageType('RequestFileList', (_message.Message,), {
  'DESCRIPTOR' : _REQUESTFILELIST,
  '__module__' : 'proto.fluffy_pb2'
  # @@protoc_insertion_point(class_scope:fluffy.RequestFileList)
  })
_sym_db.RegisterMessage(RequestFileList)

FileList = _reflection.GeneratedProtocolMessageType('FileList', (_message.Message,), {
  'DESCRIPTOR' : _FILELIST,
  '__module__' : 'proto.fluffy_pb2'
  # @@protoc_insertion_point(class_scope:fluffy.FileList)
  })
_sym_db.RegisterMessage(FileList)

_DATATRANSFERSERVICE = DESCRIPTOR.services_by_name['DataTransferService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'H\001P\001'
  _FILEDATA._serialized_start=30
  _FILEDATA._serialized_end=72
  _FILEINFO._serialized_start=74
  _FILEINFO._serialized_end=102
  _REQUESTFILELIST._serialized_start=104
  _REQUESTFILELIST._serialized_end=139
  _FILELIST._serialized_start=141
  _FILELIST._serialized_end=173
  _DATATRANSFERSERVICE._serialized_start=176
  _DATATRANSFERSERVICE._serialized_end=414
# @@protoc_insertion_point(module_scope)
