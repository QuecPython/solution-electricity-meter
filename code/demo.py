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
import checkNet
from usr.qframe import Application
from usr.business import rfc1662resolver, client, uart

PROJECT_NAME = "QuecPython_Framework_DEMO"
PROJECT_VERSION = "1.0.0"


def poweron_print_once():
    checknet = checkNet.CheckNetwork(
        PROJECT_NAME,
        PROJECT_VERSION,
    )
    checknet.poweron_print_once()


def create_app(name='DTU', config_path='/usr/dev.json'):
    _app = Application(name)
    _app.config.from_json(config_path)

    rfc1662resolver.init_app(_app)
    uart.init_app(_app)
    client.init_app(_app)

    return _app


app = create_app()


if __name__ == '__main__':
    poweron_print_once()
    app.mainloop()
