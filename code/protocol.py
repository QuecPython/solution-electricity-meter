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


import ustruct as struct
from usr.constant import (
    COSEM,
    DATAType,
    COSEM_ACK,
    CONSEM_COMMON_RFC1662_PARAM_ID
)
from usr.qframe.logging import getLogger


logger = getLogger(__name__)


class FCSUtil(object):
    """
        FCSUtil 工具解析crc16的FCS
    """
    CRC_INIT = 0xffff
    POLYNOMIAL = 0x1021
    DATA_VALUE = 0xA0
    BIT32 = 0x8000

    @classmethod
    def byte_mirror(cls, c):
        c = (c & 0xF0) >> 4 | (c & 0x0F) << 4
        c = (c & 0xCC) >> 2 | (c & 0x33) << 2
        c = (c & 0xAA) >> 1 | (c & 0x55) << 1
        return c

    @classmethod
    def calc_crc(cls, data):
        _len = len(data)
        crc = cls.CRC_INIT
        for i in range(_len):

            if (i != 0) and (i != (_len - 1)) and (i != (_len - 2)) and (i != (_len - 3)):
                c = cls.byte_mirror(data[i])
                c = c << 8

                for j in range(8):

                    if (crc ^ c) & 0x8000:
                        crc = (crc << 1) ^ cls.POLYNOMIAL
                    else:
                        crc = crc << 1

                    c = c << 1
                    crc = crc % 65536
                    c = c % 65536
        crc = 0xFFFF - crc
        crc_HI = cls.byte_mirror(crc // 256)
        crc_LO = cls.byte_mirror(crc % 256)
        crc = 256 * crc_HI + crc_LO
        return crc

    @classmethod
    def check(cls, check_sum, data):
        """

        @check_sum: int
        @data: origin full data
        @return: boolean check FCS result
        """
        logger.info("check_sum = {}".format(check_sum))
        logger.info("cls.calc_crc(data) = {}".format(cls.calc_crc(data)))
        return check_sum == cls.calc_crc(data)


class InfoEntity(object):
    def __init__(self):
        self.__param_id = None
        self.__param_len = None
        self.__request_id = None
        self.__request_type = None
        self.__request_data = None
        self.__request_data_len = None

    def set_param_id(self, p_param_id):
        self.__param_id = p_param_id

    def set_param_len(self, p_len):
        self.__param_len = p_len

    def set_request_id(self, p_req_id):
        self.__request_id = p_req_id

    def set_request_type(self, p_req_type):
        self.__request_type = p_req_type

    def set_request_data(self, p_req_data):
        self.__request_data = p_req_data

    def set_request_data_len(self, p_req_data_len):
        self.__request_data_len = p_req_data_len

    def param_id(self):
        return self.__param_id

    def param_len(self):
        return self.__param_len

    def request_id(self):
        return self.__request_id

    def request_type(self):
        return self.__request_type

    def request_data(self):
        return self.__request_data

    def get_request_data_len(self):
        return self.__request_data_len

    def set_data(self, d):
        self.__request_data = d

    @staticmethod
    def build(data, mode, image_len=None):
        info = InfoEntity()
        try:
            if mode == COSEM.SERIA_NET:
                info.set_request_data(data)
                return info
            info.set_param_id(struct.unpack("<H", data[:2])[0])
            if info.param_id() in [CONSEM_COMMON_RFC1662_PARAM_ID.LQI, 0x8005, 0x8007]:
                if len(data) > 2:
                    info.set_param_len(data[2])
                    info.set_request_data(struct.unpack("{}s".format(info.param_len()), data[3:])[0])
                    return info
            if info.param_id() in [0x3008, 0x3007, 0x3009, 0x300A]:
                if len(data) > 2:
                    info.set_param_len(image_len + 1 - 4)
                    info.set_request_data(struct.unpack("{}s".format(info.param_len()), data[3:])[0])
                    return info
            if mode == COSEM.GET_RESP:
                if info.param_id() in [0x280F, 0x2801, 0x2802, 0x2803, 0x2804, 0x2805, 0x2806, 0x2807, 0x2860, 0x2861]:
                    if len(data) > 2:
                        info.set_param_len(data[2])
                        info.set_request_data(struct.unpack("{}s".format(info.param_len()), data[3:])[0])
                        info.set_request_data_len(info.param_len() - 3)
                    else:
                        info.set_request_data_len(0)
            elif mode == COSEM.SET:
                info.set_param_len(data[2])
                info.set_request_id(struct.unpack(">H", data[3:5])[0])
                info.set_request_type(data[5])
                if info.request_type() == DATAType.CHAR or info.request_type() == DATAType.STR:
                    info.set_request_data(struct.unpack("{}s".format(info.param_len() - 4), data[7:])[0])
                elif info.request_type() == DATAType.INT8U:
                    info.set_request_data(struct.unpack("B", data[6:7])[0])
                elif info.request_type() == DATAType.INT16U:
                    info.set_request_data(struct.unpack(">H", data[6:8])[0])
                elif info.request_type() == DATAType.INT32U:
                    info.set_request_data(struct.unpack(">i", data[6:10])[0])
                else:
                    print("DATAType error,self.request_type: {}".format(info.request_type()))
            elif mode == COSEM.GET:
                info.set_request_id(struct.unpack(">H", data[2:])[0])
        except Exception as e:
            print("e {}".format(e))
        return info

    def clear(self):
        self.__param_id = None
        self.__param_len = None
        self.__request_id = None
        self.__request_type = None
        self.__request_data = None
        self.__request_data_len = None

    def replay(self, t, d):
        self.__request_type = t
        self.__request_data = d
        # 需要回复类型的数据
        if self.__request_type is not None:
            if self.__request_type == DATAType.CHAR or self.__request_type == DATAType.STR:
                self.__request_data_len = len(self.__request_data) & 0xff
                ret_data = struct.pack(">H", self.__request_id) + struct.pack("<BB{}s".format(len(self.__request_data)),
                                                                              self.__request_type,
                                                                              self.__request_data_len,
                                                                              self.__request_data)
            elif self.__request_type == DATAType.INT8U or self.__request_type == DATAType.INT16U:
                ret_data = struct.pack(">H", self.__request_id) + struct.pack("<B{}s".format(len(self.__request_data)),
                                                                              self.__request_type,
                                                                              self.__request_data)
            else:
                print("DATAType error,request_type: {}".format(self.__request_type))
                ret_data = b''

            self.__param_len = len(ret_data)
        else:
            # 类似8003这种数据，无类型
            ret_data = struct.pack("<B", self.__request_data)
            self.__param_len = len(ret_data)
        return struct.pack("<HB", self.__param_id, self.__param_len) + ret_data

    def replay_get(self, t, d):
        return self.replay(t, d)

    def image_replay_get(self, data):
        self.__param_len = len(data)
        ret_data = struct.pack("<HB", self.__param_id, self.__param_len) + data
        print("image_replay_get 2--------", ret_data)
        return ret_data

    def replay_set(self, d):
        self.__request_data = d
        self.__request_type = None
        self.__request_id = None
        ret_data = struct.pack("<HBB", self.__param_id, 0x01, self.__request_data)
        return ret_data

    def replay_event(self, d):
        self.clear()
        self.__request_data = d
        ret_data = struct.pack("B", self.__request_data)


class RFC1662Protocol(object):
    HEADER = 0x7e
    ADDRESS = 0xFF
    CONTROL = 0x03
    END = 0x7e

    def __init__(self):
        self.__protocol = None
        self.__positions = 0
        self.__info_len = None
        self.__info_cmd = None
        self.__csq = 0
        # self.__info_data: InfoEntity = None
        self.__info_data = None
        self.__fcs = None
        self.__replay_data = ""

    def protocol(self):
        return self.__protocol

    def cmd(self):
        return self.__info_cmd

    def set_fcs(self, fcs):
        self.__fcs = fcs

    def set_info_len(self, l):
        self.__info_len = l

    def set_info_data(self, info_data):
        self.__info_data = info_data

    def set_info_cmd(self, info_cmd):
        self.__info_cmd = info_cmd

    def set_protocol(self, param):
        self.__protocol = param

    def increment(self, n):
        self.__positions += n

    def position(self):
        return self.__positions

    def info(self) -> InfoEntity:
        return self.__info_data

    @classmethod
    def build(cls, data):
        rfc_proto = RFC1662Protocol()
        if data[0] == cls.HEADER and data[1] == cls.ADDRESS and data[2] == cls.CONTROL:
            # 读取protocol，从第三个字节往后读两个字节
            rfc_proto.increment(3)
            rfc_proto.set_protocol(struct.unpack_from("<H", data[rfc_proto.position():rfc_proto.position() + 2])[0])
            rfc_proto.increment(2)

            # 继续读取info区里面的长度
            info_len = struct.unpack(">H", data[rfc_proto.position():rfc_proto.position() + 2])[0]
            rfc_proto.set_info_len(info_len)
            rfc_proto.increment(2)

            # 继续读取info区里面的命令
            info_cmd = struct.unpack("B", data[rfc_proto.position():rfc_proto.position() + 1])[0]
            rfc_proto.set_info_cmd(info_cmd)
            rfc_proto.increment(1)

            # 继续读取info区里面的参数
            info_data_len = info_len - 1
            info_data = struct.unpack("{}s".format(info_data_len),
                                      data[rfc_proto.position():rfc_proto.position() + info_data_len])[0]
            rfc_proto.set_info_data(InfoEntity.build(info_data, info_cmd, info_data_len))
            rfc_proto.increment(info_data_len)

            # 读取fcs校验帧
            fcs = struct.unpack("<H", data[rfc_proto.position():rfc_proto.position() + 2])[0]
            rfc_proto.increment(2)
            # 校验帧检查
            # message = " ".join(["%02x" % x for x in data])
            # print("FCS_data:", message)
            # print("FCS_data_len:", len(data))
            if FCSUtil.check(fcs, data):
                rfc_proto.set_fcs(fcs)
            else:
                logger.error("check fcs fail")
                return None

            # 读取结束字节0x7e
            end = struct.unpack("B", data[rfc_proto.position():rfc_proto.position() + 1])[0]
            rfc_proto.increment(1)

            # 判断结束帧
            if end == cls.END:
                return rfc_proto
            else:
                print("build error")
                return None
        else:
            print("head error")
            return None

    @classmethod
    def build_rfc_0x2100(cls, data):
        if data:
            rfc_proto = RFC1662Protocol()
            rfc_proto.set_protocol(0x2100)
            rfc_proto.set_info_cmd(COSEM.SERIA_NET)
            rfc_proto.set_info_len(len(data) + 1)
            csq = 0
            protocol = (rfc_proto.protocol() >> 8) & 0xff
            replay_data = struct.pack("<BBBBB", rfc_proto.HEADER, rfc_proto.ADDRESS, rfc_proto.CONTROL, csq,
                                      protocol) + \
                          struct.pack(">H", rfc_proto.__info_len) + struct.pack("<B", rfc_proto.cmd()) + data + \
                          struct.pack("<H", 0x0000) + struct.pack("<B", rfc_proto.END)
            rfc_proto.__fcs = FCSUtil.calc_crc(replay_data)
            rfc_proto.__replay_data = replay_data[:-3] + struct.pack("<HB", rfc_proto.__fcs, rfc_proto.END)
            return rfc_proto.__replay_data
        else:
            return None

    @classmethod
    def build_rfc_0x2200(cls, r_data):
        """
        RFC 2200 数据帧组包
        data = [get/set, parame_id, data] // get时data为None
        """
        if len(r_data) != 3:
            print("RFC2200 parameter error")
            return
        protocol = 0x2200
        rfc_proto = RFC1662Protocol()
        mode, parame_id, data = r_data
        if mode == COSEM.GET:
            cmd = struct.pack("<B", mode)
            protocol = struct.pack("<H", protocol)
            parame_id = struct.pack("<H", parame_id)
            info_len = struct.pack(">H", len(cmd) + len(parame_id))
            replay_data = struct.pack("<BBB", rfc_proto.HEADER, rfc_proto.ADDRESS, rfc_proto.CONTROL, ) + protocol + \
                          info_len + cmd + parame_id + struct.pack("<H", 0x0000) + struct.pack("<B", rfc_proto.END)
        # elif mode == COSEM.SET:
        else:
            cmd = struct.pack("<B", mode)
            protocol = struct.pack("<H", protocol)
            parame_id = struct.pack("<H", parame_id)
            info_len = struct.pack(">H", len(cmd) + len(protocol) + len(data))
            replay_data = struct.pack("<BBB", rfc_proto.HEADER, rfc_proto.ADDRESS, rfc_proto.CONTROL, ) + protocol + \
                          info_len + cmd + parame_id + data + struct.pack("<H", 0x0000) + struct.pack("<B",
                                                                                                      rfc_proto.END)
        rfc_proto._fcs = FCSUtil.calc_crc(replay_data)
        rfc_proto._replay_data = replay_data[:-3] + struct.pack("<HB", rfc_proto._fcs, rfc_proto.END)
        return rfc_proto._replay_data

    def pack_replay_data(self, info_data):
        self.__info_len = len(info_data) + 1
        self.__csq = 0
        protocol = (self.__protocol >> 8) & 0xff
        if self.__csq is None:
            self.__csq = 0
        replay_data = struct.pack("<BBBBB", self.HEADER, self.ADDRESS, self.CONTROL, self.__csq, protocol) + \
                      struct.pack(">H", self.__info_len) + struct.pack("<B", self.cmd()) + info_data + \
                      struct.pack("<H", self.__fcs) + struct.pack("<B", self.END)
        self.__fcs = FCSUtil.calc_crc(replay_data)
        self.__replay_data = replay_data[:-3] + struct.pack("<HB", self.__fcs, self.END)

    def replay_get(self, t=None, d=None, success=True):
        """
        应答get指令, 判断成功失败
        @param success:  true获取成功 false 获取失败
        @param t:   对应回复的类型 采用枚举类型{@DATAType}枚举值
        @param d:
        @return:
        """
        if success:
            info_data = self.__info_data.replay_get(t, d)
            # 进行回复时转为GET
            self.__info_cmd = COSEM.GET_RESP
            # 计算长度是info_data + 1
        else:
            self.__info_cmd = COSEM.CET_ERROR_RESP
            data_info = COSEM_ACK.FAILED
            info_data = self.__info_data.replay_set(data_info)
        self.pack_replay_data(info_data)
        return self.__replay_data

    def image_replay_get(self, data):
        info_data = self.__info_data.image_replay_get(data)
        # 进行回复时转为GET
        self.__info_cmd = COSEM.GET_RESP
        # 计算长度是info_data + 1
        self.pack_replay_data(info_data)
        return self.__replay_data

    def image_replay_set(self, data):
        info_data = self.__info_data.image_replay_get(data)
        # 进行回复时转为GET
        self.__info_cmd = COSEM.SET_RESP
        # 计算长度是info_data + 1
        self.pack_replay_data(info_data)
        return self.__replay_data

    def replay_set(self, success=True):
        """
        应答set指令
        @param success: true设置成功 false 设置失败
        @return:
        """
        data_info = COSEM_ACK.SUCCESS if success else COSEM_ACK.FAILED
        info_data = self.__info_data.replay_set(data_info)
        self.__info_cmd = COSEM.SET_RESP
        self.pack_replay_data(info_data)
        return self.__replay_data

    def reply_event(self):
        """
        应答event信息
        @return:
        """
        data_info = COSEM_ACK.SUCCESS
        # info_data = self.__info_data.replay_set(data_info)
        info_data = struct.pack("<BB", 0x01, data_info)
        self.__info_cmd = COSEM.SERIA_NET
        self.pack_replay_data(info_data)
        return self.__replay_data

    def __str__(self):
        rv = "{\n"
        rv += "    header=0x7e\n"
        rv += "    address=0xff\n"
        rv += "    control=0x03\n"
        rv += "    protocol={}\n".format(hex(self.__protocol))
        rv += "    info_len={}\n".format(self.__info_len)
        rv += "    info_cmd={}\n".format(hex(self.__info_cmd))
        rv += "    info_data={\n"
        rv += "       InfoEntity={\n"
        rv += "            param_id     = {}\n".format(hex(self.info().param_id()) if self.info().param_id() else None)
        rv += "            param_len    = {}\n".format(self.info().param_len())
        rv += "            request_id   = {}\n".format(hex(self.info().request_id()) if self.info().request_id() else None)
        rv += "            request_type = {}\n".format(self.info().request_type())
        rv += "            request_data = {}\n".format(self.info().request_data())
        rv += "         }\n"
        rv += "    }\n"
        rv += "    fcs={}\n".format(self.__fcs)
        rv += "    end=0x7e\n"
        rv += "}\n"
        return rv

    def hex(self):
        return " ".join(["%02x" % x for x in self.__replay_data])


class RFC1662ProtocolResolver(object):
    support_protocol_handlers = {}

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.extensions['rfc1662resolver'] = self

    def register(self, protocol):
        def wrapper(fn):
            if protocol in self.support_protocol_handlers:
                raise ValueError('mode \"{}\" already registered!'.format(hex(protocol)))
            self.support_protocol_handlers[protocol] = fn
            return fn
        return wrapper

    def resolve(self, msg):
        logger.info('get msg:\n{}'.format(msg))
        for protocol, handler in self.support_protocol_handlers.items():
            if protocol == msg.protocol():
                handler(msg)
                break
        else:
            ValueError('protocol not supported for id: {}'.format(msg.protocol()))

    @staticmethod
    def tcp_to_meter_packet(data=None):
        # tcp send data, 2100 packet
        # data: bytes from tcp
        return RFC1662Protocol.build_rfc_0x2100(data)

    @staticmethod
    def module_to_meter_packet(data):
        # module send data, 2200 packet
        # data: [get/set, id, data]
        return RFC1662Protocol.build_rfc_0x2200(data)
