# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: my.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x08my.proto\"3\n\x12SetUserNameRequest\x12\x0f\n\x07session\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\"-\n\x10\x43onnectedPlayers\x12\n\n\x02id\x18\x01 \x01(\x05\x12\r\n\x05names\x18\x02 \x03(\t\"3\n\x14NotificationsRequest\x12\x0f\n\x07session\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\x05\"=\n\x15NotificationsResponse\x12\x11\n\tconnected\x18\x01 \x01(\x08\x12\x11\n\tuser_name\x18\x02 \x01(\t\"0\n\x11\x44isconnectRequest\x12\x0f\n\x07session\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\x05\"+\n\x0cReadyRequest\x12\x0f\n\x07session\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\x05\";\n\rReadyResponse\x12\x0c\n\x04role\x18\x01 \x01(\t\x12\x0f\n\x07players\x18\x02 \x03(\t\x12\x0b\n\x03ids\x18\x03 \x03(\x05\".\n\x0fKillVoteRequest\x12\x0f\n\x07session\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\x05\"5\n\x16KillPlayerMafiaRequest\x12\x0f\n\x07session\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\x05\"[\n\x10\x45ndNightResponse\x12\x14\n\x0c\x63hecked_role\x18\x01 \x01(\t\x12\x10\n\x08\x65nd_game\x18\x02 \x01(\x08\x12\x0e\n\x06killed\x18\x03 \x01(\x05\x12\x0f\n\x07\x63hecked\x18\x04 \x01(\x05\"1\n\x12\x43heckPlayerRequest\x12\x0f\n\x07session\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\x05\",\n\rEndDayRequest\x12\x0f\n\x07session\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\x05\"2\n\x0e\x45ndDayResponse\x12\x0e\n\x06killed\x18\x01 \x01(\x05\x12\x10\n\x08\x65nd_game\x18\x02 \x01(\x08\"#\n\x10SkipNightRequest\x12\x0f\n\x07session\x18\x01 \x01(\t\"\x07\n\x05\x45mpty2\xf6\x03\n\x0bMafiaServer\x12\x37\n\x0bSetUserName\x12\x13.SetUserNameRequest\x1a\x11.ConnectedPlayers\"\x00\x12\x45\n\x10GetNotifications\x12\x15.NotificationsRequest\x1a\x16.NotificationsResponse\"\x00\x30\x01\x12*\n\nDisconnect\x12\x12.DisconnectRequest\x1a\x06.Empty\"\x00\x12\x31\n\x0eSetReadyStatus\x12\r.ReadyRequest\x1a\x0e.ReadyResponse\"\x00\x12,\n\x0eKillPlayerVote\x12\x10.KillVoteRequest\x1a\x06.Empty\"\x00\x12?\n\x0fKillPlayerMafia\x12\x17.KillPlayerMafiaRequest\x1a\x11.EndNightResponse\"\x00\x12\x37\n\x0b\x43heckPlayer\x12\x13.CheckPlayerRequest\x1a\x11.EndNightResponse\"\x00\x12+\n\x06\x45ndDay\x12\x0e.EndDayRequest\x1a\x0f.EndDayResponse\"\x00\x12\x33\n\tSkipNight\x12\x11.SkipNightRequest\x1a\x11.EndNightResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'my_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SETUSERNAMEREQUEST._serialized_start=12
  _SETUSERNAMEREQUEST._serialized_end=63
  _CONNECTEDPLAYERS._serialized_start=65
  _CONNECTEDPLAYERS._serialized_end=110
  _NOTIFICATIONSREQUEST._serialized_start=112
  _NOTIFICATIONSREQUEST._serialized_end=163
  _NOTIFICATIONSRESPONSE._serialized_start=165
  _NOTIFICATIONSRESPONSE._serialized_end=226
  _DISCONNECTREQUEST._serialized_start=228
  _DISCONNECTREQUEST._serialized_end=276
  _READYREQUEST._serialized_start=278
  _READYREQUEST._serialized_end=321
  _READYRESPONSE._serialized_start=323
  _READYRESPONSE._serialized_end=382
  _KILLVOTEREQUEST._serialized_start=384
  _KILLVOTEREQUEST._serialized_end=430
  _KILLPLAYERMAFIAREQUEST._serialized_start=432
  _KILLPLAYERMAFIAREQUEST._serialized_end=485
  _ENDNIGHTRESPONSE._serialized_start=487
  _ENDNIGHTRESPONSE._serialized_end=578
  _CHECKPLAYERREQUEST._serialized_start=580
  _CHECKPLAYERREQUEST._serialized_end=629
  _ENDDAYREQUEST._serialized_start=631
  _ENDDAYREQUEST._serialized_end=675
  _ENDDAYRESPONSE._serialized_start=677
  _ENDDAYRESPONSE._serialized_end=727
  _SKIPNIGHTREQUEST._serialized_start=729
  _SKIPNIGHTREQUEST._serialized_end=764
  _EMPTY._serialized_start=766
  _EMPTY._serialized_end=773
  _MAFIASERVER._serialized_start=776
  _MAFIASERVER._serialized_end=1278
# @@protoc_insertion_point(module_scope)
