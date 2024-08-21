# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: management_service.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18management_service.proto\x12\nmanagement\"\xb3\x01\n\x17\x45xecuteOpCommandRequest\x12\x12\n\nrequest_id\x18\x01 \x01(\x04\x12\x15\n\x0b\x63li_command\x18\x02 \x01(\tH\x00\x12\x15\n\x0bxml_command\x18\x03 \x01(\tH\x00\x12\x16\n\x0cjson_command\x18\x04 \x01(\tH\x00\x12\x33\n\nout_format\x18\x05 \x01(\x0e\x32\x1f.management.OperationFormatTypeB\t\n\x07\x63ommand\"\x80\x01\n\x18\x45xecuteOpCommandResponse\x12\x12\n\nrequest_id\x18\x01 \x01(\x04\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\t\x12\x31\n\x06status\x18\x03 \x01(\x0e\x32!.management.JunosRpcResponseTypes\x12\x0f\n\x07message\x18\x04 \x01(\t\":\n\x14\x45phConfigRequestList\x12\x14\n\x0coperation_id\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\"\xd3\x01\n\x19GetEphemeralConfigRequest\x12\x12\n\nrequest_id\x18\x01 \x01(\x04\x12\x34\n\x08\x65ncoding\x18\x02 \x01(\x0e\x32\".management.JunosDataEncodingTypes\x12=\n\x13\x65ph_config_requests\x18\x03 \x03(\x0b\x32 .management.EphConfigRequestList\x12\x19\n\x11\x65ph_instance_name\x18\x04 \x01(\t\x12\x12\n\nmerge_view\x18\x05 \x01(\x08\"\xff\x01\n\x1aGetEphemeralConfigResponse\x12\x12\n\nrequest_id\x18\x01 \x01(\x04\x12\x45\n\x08response\x18\x02 \x03(\x0b\x32\x33.management.GetEphemeralConfigResponse.ResponseList\x1a\x85\x01\n\x0cResponseList\x12\x14\n\x0coperation_id\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\t\x12\x31\n\x06status\x18\x04 \x01(\x0e\x32!.management.JunosRpcResponseTypes\x12\x0f\n\x07message\x18\x05 \x01(\t\"\xfc\x02\n\x1a\x45\x64itEphemeralConfigRequest\x12\x12\n\nrequest_id\x18\x01 \x01(\x04\x12Y\n\x15\x65ph_config_operations\x18\x03 \x03(\x0b\x32:.management.EditEphemeralConfigRequest.ConfigOperationList\x12\x19\n\x11\x65ph_instance_name\x18\x04 \x01(\t\x12 \n\x18\x65nable_config_validation\x18\x05 \x01(\x08\x12\x11\n\tload_only\x18\x06 \x01(\x08\x1a\x9e\x01\n\x13\x43onfigOperationList\x12\x14\n\x0coperation_id\x18\x01 \x01(\t\x12-\n\toperation\x18\x02 \x01(\x0e\x32\x1a.management.ConfigCommands\x12\x0c\n\x04path\x18\x03 \x01(\t\x12\x14\n\nxml_config\x18\x04 \x01(\tH\x00\x12\x15\n\x0bjson_config\x18\x05 \x01(\tH\x00\x42\x07\n\x05value\"\xe3\x01\n\x1b\x45\x64itEphemeralConfigResponse\x12\x12\n\nrequest_id\x18\x01 \x01(\x04\x12\x46\n\x08response\x18\x02 \x03(\x0b\x32\x34.management.EditEphemeralConfigResponse.ResponseList\x1ah\n\x0cResponseList\x12\x14\n\x0coperation_id\x18\x01 \x01(\t\x12\x31\n\x06status\x18\x02 \x01(\x0e\x32!.management.JunosRpcResponseTypes\x12\x0f\n\x07message\x18\x03 \x01(\t\"R\n\x0c\x43onfigCommit\x12\x31\n\x0b\x63ommit_type\x18\x01 \x01(\x0e\x32\x1c.management.ConfigCommitType\x12\x0f\n\x07\x63omment\x18\x02 \x01(\t\"\xd5\x01\n\x18\x45xecuteCfgCommandRequest\x12\x12\n\nrequest_id\x18\x01 \x01(\x04\x12\x14\n\nxml_config\x18\x02 \x01(\tH\x00\x12\x15\n\x0bjson_config\x18\x03 \x01(\tH\x00\x12\x15\n\x0btext_config\x18\x04 \x01(\tH\x00\x12-\n\tload_type\x18\x05 \x01(\x0e\x32\x1a.management.ConfigLoadType\x12(\n\x06\x63ommit\x18\x06 \x01(\x0b\x32\x18.management.ConfigCommitB\x08\n\x06\x63onfig\"s\n\x19\x45xecuteCfgCommandResponse\x12\x12\n\nrequest_id\x18\x01 \x01(\x04\x12\x31\n\x06status\x18\x02 \x01(\x0e\x32!.management.JunosRpcResponseTypes\x12\x0f\n\x07message\x18\x03 \x01(\t*d\n\x13OperationFormatType\x12\x19\n\x15OPERATION_FORMAT_JSON\x10\x00\x12\x18\n\x14OPERATION_FORMAT_XML\x10\x01\x12\x18\n\x14OPERATION_FORMAT_CLI\x10\x02*\x8a\x01\n\x15JunosRpcResponseTypes\x12\x0b\n\x07SUCCESS\x10\x00\x12\x07\n\x03NOK\x10\x01\x12\x14\n\x10UNSUPPORTED_PATH\x10\x02\x12\x10\n\x0cINVALID_PATH\x10\x03\x12\x19\n\x15INVALID_CONFIGURATION\x10\x04\x12\x18\n\x14UNSUPPORTED_ENCODING\x10\x05*=\n\x16JunosDataEncodingTypes\x12\x10\n\x0c\x45NCODING_XML\x10\x00\x12\x11\n\rENCODING_JSON\x10\x01*J\n\x0e\x43onfigCommands\x12\x11\n\rUPDATE_CONFIG\x10\x00\x12\x12\n\x0eREPLACE_CONFIG\x10\x01\x12\x11\n\rDELETE_CONFIG\x10\x02*\x87\x01\n\x0e\x43onfigLoadType\x12\x17\n\x13\x43ONFIG_LOAD_REPLACE\x10\x00\x12\x15\n\x11\x43ONFIG_LOAD_MERGE\x10\x01\x12\x18\n\x14\x43ONFIG_LOAD_OVERRIDE\x10\x02\x12\x16\n\x12\x43ONFIG_LOAD_UPDATE\x10\x03\x12\x13\n\x0f\x43ONFIG_LOAD_SET\x10\x04*D\n\x10\x43onfigCommitType\x12\x1d\n\x19\x43ONFIG_COMMIT_SYNCHRONIZE\x10\x00\x12\x11\n\rCONFIG_COMMIT\x10\x01\x32\xaa\x03\n\x10ManagementRpcApi\x12\x61\n\x10\x45xecuteOpCommand\x12#.management.ExecuteOpCommandRequest\x1a$.management.ExecuteOpCommandResponse\"\x00\x30\x01\x12\x62\n\x11\x45xecuteCfgCommand\x12$.management.ExecuteCfgCommandRequest\x1a%.management.ExecuteCfgCommandResponse\"\x00\x12\x65\n\x12GetEphemeralConfig\x12%.management.GetEphemeralConfigRequest\x1a&.management.GetEphemeralConfigResponse\"\x00\x12h\n\x13\x45\x64itEphemeralConfig\x12&.management.EditEphemeralConfigRequest\x1a\'.management.EditEphemeralConfigResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'management_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_OPERATIONFORMATTYPE']._serialized_start=1915
  _globals['_OPERATIONFORMATTYPE']._serialized_end=2015
  _globals['_JUNOSRPCRESPONSETYPES']._serialized_start=2018
  _globals['_JUNOSRPCRESPONSETYPES']._serialized_end=2156
  _globals['_JUNOSDATAENCODINGTYPES']._serialized_start=2158
  _globals['_JUNOSDATAENCODINGTYPES']._serialized_end=2219
  _globals['_CONFIGCOMMANDS']._serialized_start=2221
  _globals['_CONFIGCOMMANDS']._serialized_end=2295
  _globals['_CONFIGLOADTYPE']._serialized_start=2298
  _globals['_CONFIGLOADTYPE']._serialized_end=2433
  _globals['_CONFIGCOMMITTYPE']._serialized_start=2435
  _globals['_CONFIGCOMMITTYPE']._serialized_end=2503
  _globals['_EXECUTEOPCOMMANDREQUEST']._serialized_start=41
  _globals['_EXECUTEOPCOMMANDREQUEST']._serialized_end=220
  _globals['_EXECUTEOPCOMMANDRESPONSE']._serialized_start=223
  _globals['_EXECUTEOPCOMMANDRESPONSE']._serialized_end=351
  _globals['_EPHCONFIGREQUESTLIST']._serialized_start=353
  _globals['_EPHCONFIGREQUESTLIST']._serialized_end=411
  _globals['_GETEPHEMERALCONFIGREQUEST']._serialized_start=414
  _globals['_GETEPHEMERALCONFIGREQUEST']._serialized_end=625
  _globals['_GETEPHEMERALCONFIGRESPONSE']._serialized_start=628
  _globals['_GETEPHEMERALCONFIGRESPONSE']._serialized_end=883
  _globals['_GETEPHEMERALCONFIGRESPONSE_RESPONSELIST']._serialized_start=750
  _globals['_GETEPHEMERALCONFIGRESPONSE_RESPONSELIST']._serialized_end=883
  _globals['_EDITEPHEMERALCONFIGREQUEST']._serialized_start=886
  _globals['_EDITEPHEMERALCONFIGREQUEST']._serialized_end=1266
  _globals['_EDITEPHEMERALCONFIGREQUEST_CONFIGOPERATIONLIST']._serialized_start=1108
  _globals['_EDITEPHEMERALCONFIGREQUEST_CONFIGOPERATIONLIST']._serialized_end=1266
  _globals['_EDITEPHEMERALCONFIGRESPONSE']._serialized_start=1269
  _globals['_EDITEPHEMERALCONFIGRESPONSE']._serialized_end=1496
  _globals['_EDITEPHEMERALCONFIGRESPONSE_RESPONSELIST']._serialized_start=1392
  _globals['_EDITEPHEMERALCONFIGRESPONSE_RESPONSELIST']._serialized_end=1496
  _globals['_CONFIGCOMMIT']._serialized_start=1498
  _globals['_CONFIGCOMMIT']._serialized_end=1580
  _globals['_EXECUTECFGCOMMANDREQUEST']._serialized_start=1583
  _globals['_EXECUTECFGCOMMANDREQUEST']._serialized_end=1796
  _globals['_EXECUTECFGCOMMANDRESPONSE']._serialized_start=1798
  _globals['_EXECUTECFGCOMMANDRESPONSE']._serialized_end=1913
  _globals['_MANAGEMENTRPCAPI']._serialized_start=2506
  _globals['_MANAGEMENTRPCAPI']._serialized_end=2932
# @@protoc_insertion_point(module_scope)
