import logging
import pulsectl
from devicemanager import DeviceManager

logger = logging.getLogger('default')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

pulse_server = pulsectl.Pulse('sony_disconnect')

device_manager = DeviceManager()


def get_sink_by_index(sink_list, sink_index):
    for sink in sink_list:
        if sink.index == sink_index:
            return sink
    return False

# TODO: check that 'bt-device' installed


with pulsectl.Pulse('event-printer') as pulse:

    def print_events(ev):
        event_type = ev.t
        if ev.facility == pulsectl.PulseEventFacilityEnum.sink:
            sink = get_sink_by_index(pulse_server.sink_list(), ev.index)
            if event_type == pulsectl.PulseEventTypeEnum.new:
                logger.info(f'New sink found: {sink}')
                device_manager.add_device(sink)

            if event_type == pulsectl.PulseEventTypeEnum.change:
                logger.debug(f'Sink with index {sink.index} changed.')
                logger.debug(f'Sink state: {sink.state}')
                device_manager.update_device(sink)
            if event_type == pulsectl.PulseEventTypeEnum.remove:
                logger.debug(f'Sink with index {ev.index} was removed.')
                device_manager.remove_device(ev.index)

    pulse.event_mask_set('all')
    pulse.event_callback_set(print_events)
    pulse.event_listen()
