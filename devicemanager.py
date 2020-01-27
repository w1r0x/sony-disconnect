from device import Device
from device import DeviceMacAddressUnknown
import logging
import pulsectl


class DeviceManager:
    device_list = {}
    logger = logging.getLogger('default')

    def add_device(self, sink):
        if sink.index in self.device_list.keys():
            del self.device_list[sink.index]
        try:
            self.device_list[sink.index] = Device(sink)
            self.logger.info(f'Added new Device \
\'{self.device_list[sink.index].sink.description}\' with mac \
\'{self.device_list[sink.index].mac}\'')

        except DeviceMacAddressUnknown:
            pass

    def remove_device(self, sink_index):
        if sink_index in self.device_list.keys():
            self.logger.info(f'Removed Device \
\'{self.device_list[sink_index].sink.description}\' with mac \
\'{self.device_list[sink_index].mac}\'')
            del self.device_list[sink_index]

    def update_device(self, sink):
        if sink.index not in self.device_list.keys():
            if sink.state not in [pulsectl.PulseStateEnum.suspended,
                                  pulsectl.PulseStateEnum.idle]:
                self.add_device(sink)
        elif sink.index in self.device_list.keys():
            self.device_list[sink.index].update_sink(sink)
