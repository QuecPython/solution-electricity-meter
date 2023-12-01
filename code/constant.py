# Copyright (c) Quectel Wireless Solution, Co., Ltd.All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class DEVICE_TYPE_ENUM(object):
    # ec200a
    EC200A_CAT4 = 0
    # ec600u
    EC600U_CAT1 = 1
    # bg95
    BG95_CATM = 2


class MSG_TYPE_ENUM(object):
    # at 消息
    AT_MODE = 0
    # RFC1662协议
    RFC1662 = 1
    # SMS 消息
    SMS = 2
    # 客户端消息
    TCP_CLI = 3
    # 服务端消息
    TCP_SER = 4


class CMD_MODE_ENUM(object):
    # 查询模式
    READ = "read"
    # 设置模式
    WRITE = "write"
    # 其他
    OTHER = "other"
    # active
    ACTIVE = "active"


class COSEM(object):
    GET = 0xC0
    GET_RESP = 0xC4
    CET_ERROR_RESP = 0xC8
    SET = 0xC1
    SET_RESP = 0xC5
    EVENT = 0xC2
    EVENT_RESP = 0xC6
    ACTION = 0xC3
    ACTION_RESP = 0xC7
    SERIA_NET = 0xBF
    SERIA_NET_RESP = 0xC6


class COSEM_ACK(object):
    """用于应答"""
    SUCCESS = 0x00
    FAILED = 0x0C


class DATAType(object):
    CHAR = 0x0A
    INT8U = 0x11
    INT16U = 0x12
    INT32U = 0x06
    STR = 0x09
    DATATIME = 0x19


class CommandType(object):
    """
    外部数据来源
    0 sms 短信
    1 uart 串口，暂只支持主串口 MAIN
    2 TCP 服务端
    3 TCP 客户端
    """
    SMS_MSG = 0
    MAIN_UART_MSG = 1
    TCP_SER_MSG = 2
    TCP_CLI_MSG = 3


class WORKMODE(object):
    """
    接入HES系统类型，涉及到注册帧和心跳帧格式
    """
    AMR_ABAKUS = 0
    AMR_WILLIS = 1
    AMR_AMETYS = 2
    AMR_HXMDMS = 3
    AMR_VHES = 4
    AMR_NARI = 5
    AMR_ATE = 6
    AMR_DLMSIP = 7
    AMR_FARAB = 8
    AMR_SHAHAB = 9
    AMR_MAX_TYPE = 10


class APPNETMODE(object):
    '''
    模块网络制式模式
    '''
    APP_NETMODE_AUTO = 0
    APP_NETMODE_LTE = 1
    APP_NETMODE_3G = 2
    APP_NETMODE_2G = 3
    APP_NETMODE_CATM = 4
    APP_NETMODE_NB = 5
    APP_NETMODE_MAX = 6


class QPYNETMODE(object):
    '''
    模组网络制式配置及优先级选择
    '''
    QPY_NETMODE_2G = 0
    QPY_NETMODE_LTE = 5
    QPY_NETMODE_GSM_LTE_AUTO = 6
    QPY_NETMODE_GSM_LTE_GSM = 7
    QPY_NETMODE_GSM_LTE_LTE = 8
    QPY_NETMODE_CATM = 19
    QPY_NETMODE_GSM_CATM = 20
    QPY_NETMODE_CATNB = 21
    QPY_NETMODE_GSM_CATNB = 22
    QPY_NETMODE_CATM_CATNB = 23
    QPY_NETMODE_GSM_CATM_CATNB = 24
    QPY_NETMODE_CATM_GSM = 25
    QPY_NETMODE_CATNB_GSM = 26
    QPY_NETMODE_CATNB_CATM = 27
    QPY_NETMODE_GSM_CATNB_CATM = 28
    QPY_NETMODE_CATM_GSM_CATNB = 29
    QPY_NETMODE_CATM_CATNB_GSM = 30
    QPY_NETMODE_CATNB_GSM_CATM = 31
    QPY_NETMODE_CATNB_CATM_GSM = 32
    QPY_NETMODE_MAX = 6


class TCPMODE(object):
    """
    模块TCP连接模式,客户端模式或服务端模式
    """
    CLIENT_MODE = 0
    SERVER_MODE = 1
    MIX_MODE = 2
    MAX_TCP_MODE = 3


class SOCKET_ERROR_ENUM(object):
    ERR_AGAIN = -1
    ERR_SUCCESS = 0
    ERR_NOMEM = 1
    ERR_PROTOCOL = 2
    ERR_INVAL = 3
    ERR_NO_CONN = 4
    ERR_CONN_REFUSED = 5
    ERR_NOT_FOUND = 6
    ERR_CONN_LOST = 7
    ERR_PAYLOAD_SIZE = 9
    ERR_NOT_SUPPORTED = 10
    ERR_UNKNOWN = 13
    ERR_ERRNO = 14


class SOCKET_STATE(object):
    STA_ERROR = -1
    STA_CLOSED = 0
    STA_LISTEN = 1
    STA_SYN_SENT = 2
    STA_SYN_RCVD = 3
    STA_ESTABLISHED = 4
    STA_FIN_WAIT_1 = 5
    STA_FIN_WAIT_2 = 6
    STA_CLOSE_WAIT = 7
    STA_CLOSING = 8
    STA_LAST_ACK = 9
    STA_TIME_WAIT = 10


class CONSEM_COMMON_RFC1662_PARAM_ID:
    LQI = 0x8003
    MODULE_STATE = 0x8002
    METER_SN = 0x8005
    DEVICE_NAME = 0x8007


class CLASS18_IMAGE_STATE(object):
    IMAGE_TRANSFER_NOT_INITIATED = 0
    IMAGE_TRANSFER_INITIATED = 1
    IMAGE_VERIFICATION_INITIATED = 2
    IMAGE_VERIFICATION_SUCCESSFUL = 3
    IMAGE_VERIFICATION_FAILED = 4
    IMAGE_ACTIVATION_INITIATED = 5
    IMAGE_ACTIVATION_SUCCESS = 6
    IMAGE_ACTIVATION_FAILED = 7


class CLASS18_IMAGE_RESULT(object):
    Action_Result_success = 0
    Action_Result_hardware_fault = 1
    Action_Result_temporary_failure = 2
    Action_Result_read_write_denied = 3
    Action_Result_object_undefined = 4
    Action_Result_object_class_inconsistent = 9
    Action_Result_object_unavailable = 11
    Action_Result_type_unmatched = 12
    Action_Result_scope_of_access_violated = 13
    Action_Result_data_block_unavailable = 14
    Action_Result_long_action_aborted = 15
    Action_Result_no_long_action_in_progress = 17
    Action_Result_backup_next = 18
    Action_Result_other_reason = 250


class CLASS18_EVENT_FLAG(object):
    STANDARD_EVENT_0 = 0
    FINISH_OLDEST_FIRMWARE_1 = 1
    NOVERIFY_HASACTIVATE_2 = 2
    INITIATED_FAILED_STATE_3 = 3
    TRANSFER_FAILED_STATE_4 = 4
    VERIFICATION_FAILED_STATE_5 = 5
    ACTIVATION_FAILED_STATE_6 = 6
    FINISH_BACKUP_7 = 7
    FALLBACK_WHICH_8 = 8
    NONLEGAL_FIRMWARE_SIGNATURE_CRC32_12 = 12
    NONLEGAL_MODE_BYTE_16 = 16
    LEGAL_MODE_BYTE_17 = 17
    ACTIVE_MODE_BYTE_18 = 18
    EVENT_FLAG_MAX = 20


class IMAGE_HEAD_OFFSET(object):
    FIRMWARE_SIGNATURE_OFFSET = 0x00
    FIRMWARE_MCUADDRESS_OFFSET = 0x60
    FIRMWARE_SIZE_OFFSET = 0x64
    FIRMWARE_MANUFACTURER_OFFSET = 0x68
    FIRMWARE_HARDWARE_TYPE_OFFSET = 0x70
    FIRMWARE_SOFTWAREVERSION_OFFSET = 0x80
    FIRMWARE_BUILD_DATE_OFFSET = 0x94
    FIRMWARE_ALGORITHM_FLAG_OFFSET = 0x9A
    FIRMWARE_IMAGE_MODE_BYTE = 0x9B
    FIRMWARE_SOFTWARE_TYPE = 0xA0
    FIRMWARE_SOFTWARE_X50 = 0xB0


class ALGORITHM_FLAG(object):
    FIRMWARE_UPGRADE_CRC32 = 0
    FIRMWARE_UPGRADE_P256_DIGITAL_SIGNATURE = 1
    FIRMWARE_UPGRADE_P384_DIGITAL_SIGNATURE = 2
    FIRMWARE_UPGRADE_MD5 = 3


class TIMER_MODE(object):
    ONE_SHOT = 0  # 单次 TIMER_MODE.ONE_SHOT
    PERIODIC = 1  # 周期 TIMER_MODE.PERIODIC


# 预留是socket的  具体作用pawn填充
EAGAIN = 11
FAIL = 0X01
SUC = 0X00

HANDLER = "handler"
