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

import usys
from usr.protocol import RFC1662ProtocolResolver
from usr.qframe.logging import getLogger
import ustruct as struct
from usr.qframe.threading import Thread
from usr.protocol import RFC1662Protocol
from usr.qframe import CurrentApp
from usr.qframe import Uart, TcpClient


logger = getLogger(__name__)


class BusinessClient(TcpClient):

    def recv_callback(self, data):
        # recv tcp data and send to uart
        data = RFC1662Protocol.build_rfc_0x2100(data)
        CurrentApp().uart.write(data)


# tcp client, recv/send tcp data
client = BusinessClient('client')


class UartBusiness(Uart):

    def __init__(self, name, app=None):
        self.buffer = b''
        super().__init__(name, app)

    def check(self, data):
        return (data[0] == RFC1662Protocol.HEADER
                and data[1] == RFC1662Protocol.ADDRESS
                and data[2] == RFC1662Protocol.CONTROL
                and data[-1] == RFC1662Protocol.END)

    def parse(self, data):
        # HEADER/1b ADDRESS/1b CONTROL/1b RFC_PROTO/2b INFO_LEN/2b
        _i = 0
        if len(data) < 7:
            # 不满足头部协议7字节
            return False, _i
        if self.check(data):
            # 这里直接跳过协议 占2字节
            _i += 7
            info_len = struct.unpack(">H", data[5:7])[0]
            # 包大小等于头部7字节 + 长度 + (fcs/2b + 0x7e)
            _i = _i + info_len + 3
            # 判断包数据大小小于整包的大小,包不完整
            if len(data) < _i:
                return False, 0
            else:
                return True, _i
        else:
            return False, _i

    def recv_callback(self, data):
        if not data:
            return
        self.buffer += data
        if len(self.buffer) < 3:
            logger.warn("recv data len lt 3 while continue")
            return
        if not self.check(self.buffer):
            logger.error("drop rubbish data {}".format(data))
            self.buffer = b''
            return
        while True:
            flag = False
            if not self.buffer:
                break
            state, _i = self.parse(self.buffer)
            if state:
                if not flag:
                    flag = True
                try:
                    rfs = RFC1662Protocol.build(self.buffer)
                    if rfs:
                        Thread(target=CurrentApp().rfc1662resolver.resolve, args=(rfs, )).start()
                    self.buffer = b''
                except Exception as e:
                    usys.print_exception(e)
                    self.buffer = b''
            if not flag:
                self.buffer = b''
                print("incomplete serial data sets = {}".format(data))
                break


# uart business, read/write uart data
uart = UartBusiness('uart')


# rfc1662 protocol data resovler
rfc1662resolver = RFC1662ProtocolResolver()


# >>>>>>>>>> handle rfc1662 message received from uart <<<<<<<<<<

@rfc1662resolver.register(0x2100)
def handle2100(msg):
    """post data received to cloud"""
    data = msg.info().request_data()
    if data:
        CurrentApp().client.send(data)
