# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: goras_message.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='goras_message.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\x13goras_message.proto\"\xcf\x01\n\rGorasSentence\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0f\n\x07speaker\x18\x02 \x01(\t\x12\x0c\n\x04when\x18\x03 \x01(\x01\x12\x0e\n\x06to_who\x18\x04 \x01(\t\x12\x1c\n\x05query\x18\x05 \x01(\x0b\x32\x0b.GorasQueryH\x00\x12\x18\n\x03\x61\x63k\x18\x06 \x01(\x0b\x32\t.GorasAckH\x00\x12\x1e\n\x06inform\x18\x07 \x01(\x0b\x32\x0c.GorasInformH\x00\x12 \n\x07\x63ommand\x18\x08 \x01(\x0b\x32\r.GorasCommandH\x00\x42\t\n\x07\x63ontent\"\x1e\n\nGorasQuery\x12\x10\n\x08question\x18\x01 \x01(\t\"+\n\x08GorasAck\x12\x0e\n\x06ref_id\x18\x01 \x01(\x05\x12\x0f\n\x07\x63omment\x18\x02 \x01(\t\"O\n\x0bGorasInform\x12\x0f\n\x07subject\x18\x01 \x01(\t\x12\x0c\n\x04verb\x18\x02 \x01(\t\x12\x0e\n\x06object\x18\x03 \x01(\t\x12\x11\n\tadjective\x18\x04 \x01(\t\"/\n\x0cGorasCommand\x12\x0f\n\x07subject\x18\x01 \x01(\t\x12\x0e\n\x06\x61\x63tion\x18\x02 \x01(\tb\x06proto3')
)




_GORASSENTENCE = _descriptor.Descriptor(
  name='GorasSentence',
  full_name='GorasSentence',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='GorasSentence.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='speaker', full_name='GorasSentence.speaker', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='when', full_name='GorasSentence.when', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='to_who', full_name='GorasSentence.to_who', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='query', full_name='GorasSentence.query', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ack', full_name='GorasSentence.ack', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='inform', full_name='GorasSentence.inform', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='command', full_name='GorasSentence.command', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='content', full_name='GorasSentence.content',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=24,
  serialized_end=231,
)


_GORASQUERY = _descriptor.Descriptor(
  name='GorasQuery',
  full_name='GorasQuery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='question', full_name='GorasQuery.question', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=233,
  serialized_end=263,
)


_GORASACK = _descriptor.Descriptor(
  name='GorasAck',
  full_name='GorasAck',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ref_id', full_name='GorasAck.ref_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='comment', full_name='GorasAck.comment', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=265,
  serialized_end=308,
)


_GORASINFORM = _descriptor.Descriptor(
  name='GorasInform',
  full_name='GorasInform',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='subject', full_name='GorasInform.subject', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='verb', full_name='GorasInform.verb', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='object', full_name='GorasInform.object', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='adjective', full_name='GorasInform.adjective', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=310,
  serialized_end=389,
)


_GORASCOMMAND = _descriptor.Descriptor(
  name='GorasCommand',
  full_name='GorasCommand',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='subject', full_name='GorasCommand.subject', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='action', full_name='GorasCommand.action', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=391,
  serialized_end=438,
)

_GORASSENTENCE.fields_by_name['query'].message_type = _GORASQUERY
_GORASSENTENCE.fields_by_name['ack'].message_type = _GORASACK
_GORASSENTENCE.fields_by_name['inform'].message_type = _GORASINFORM
_GORASSENTENCE.fields_by_name['command'].message_type = _GORASCOMMAND
_GORASSENTENCE.oneofs_by_name['content'].fields.append(
  _GORASSENTENCE.fields_by_name['query'])
_GORASSENTENCE.fields_by_name['query'].containing_oneof = _GORASSENTENCE.oneofs_by_name['content']
_GORASSENTENCE.oneofs_by_name['content'].fields.append(
  _GORASSENTENCE.fields_by_name['ack'])
_GORASSENTENCE.fields_by_name['ack'].containing_oneof = _GORASSENTENCE.oneofs_by_name['content']
_GORASSENTENCE.oneofs_by_name['content'].fields.append(
  _GORASSENTENCE.fields_by_name['inform'])
_GORASSENTENCE.fields_by_name['inform'].containing_oneof = _GORASSENTENCE.oneofs_by_name['content']
_GORASSENTENCE.oneofs_by_name['content'].fields.append(
  _GORASSENTENCE.fields_by_name['command'])
_GORASSENTENCE.fields_by_name['command'].containing_oneof = _GORASSENTENCE.oneofs_by_name['content']
DESCRIPTOR.message_types_by_name['GorasSentence'] = _GORASSENTENCE
DESCRIPTOR.message_types_by_name['GorasQuery'] = _GORASQUERY
DESCRIPTOR.message_types_by_name['GorasAck'] = _GORASACK
DESCRIPTOR.message_types_by_name['GorasInform'] = _GORASINFORM
DESCRIPTOR.message_types_by_name['GorasCommand'] = _GORASCOMMAND
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GorasSentence = _reflection.GeneratedProtocolMessageType('GorasSentence', (_message.Message,), dict(
  DESCRIPTOR = _GORASSENTENCE,
  __module__ = 'goras_message_pb2'
  # @@protoc_insertion_point(class_scope:GorasSentence)
  ))
_sym_db.RegisterMessage(GorasSentence)

GorasQuery = _reflection.GeneratedProtocolMessageType('GorasQuery', (_message.Message,), dict(
  DESCRIPTOR = _GORASQUERY,
  __module__ = 'goras_message_pb2'
  # @@protoc_insertion_point(class_scope:GorasQuery)
  ))
_sym_db.RegisterMessage(GorasQuery)

GorasAck = _reflection.GeneratedProtocolMessageType('GorasAck', (_message.Message,), dict(
  DESCRIPTOR = _GORASACK,
  __module__ = 'goras_message_pb2'
  # @@protoc_insertion_point(class_scope:GorasAck)
  ))
_sym_db.RegisterMessage(GorasAck)

GorasInform = _reflection.GeneratedProtocolMessageType('GorasInform', (_message.Message,), dict(
  DESCRIPTOR = _GORASINFORM,
  __module__ = 'goras_message_pb2'
  # @@protoc_insertion_point(class_scope:GorasInform)
  ))
_sym_db.RegisterMessage(GorasInform)

GorasCommand = _reflection.GeneratedProtocolMessageType('GorasCommand', (_message.Message,), dict(
  DESCRIPTOR = _GORASCOMMAND,
  __module__ = 'goras_message_pb2'
  # @@protoc_insertion_point(class_scope:GorasCommand)
  ))
_sym_db.RegisterMessage(GorasCommand)


# @@protoc_insertion_point(module_scope)