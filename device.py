import threading
import logging
import datetime
import pulsectl
from subprocess import Popen
import os


class Device:

    sink = None
    timeout = 420.0  # timeout in seconds
    timer = 5.0
    state = None
    logger = None
    remove = False
    mac = None

    def __init__(self, sink):
        self.logger = logging.getLogger('default')
        self.update_sink(sink)
        self.timeout_delta = datetime.timedelta(seconds=self.timeout)
        self.active_time = datetime.datetime.now()
        if 'device.string' in self.sink.proplist.keys():
            self.mac = self.sink.proplist['device.string']
        else:
            self.remove = True
            raise DeviceMacAddressUnknown
        self._tick()

    def _tick(self):
        if not self.remove:
            self.thread = RepeatedTimer(self.timer, self._tick_handler)
            self.thread.start()

    def _tick_handler(self):
        self.logger.debug('Tick event')
        self.logger.debug(f'Current State: {self.state}')
        self.logger.debug(f'Sink index: {self.sink.index}')
        self.logger.debug(f'Last active time + timeout delta: {self.active_time + self.timeout_delta}')
        self.logger.debug(f'Now: {datetime.datetime.now()}')
        if self.state in [pulsectl.PulseStateEnum.suspended, pulsectl.PulseStateEnum.idle]:
            if self.active_time + self.timeout_delta < datetime.datetime.now():
                self.logger.debug('!!!Disconnect EVENT!!!')
                self.remove = True
                self.thread.stop()
                fnull = open(os.devnull, 'w')
                proc = Popen(f'bt-device -d {self.mac}', shell=True, stdout=fnull,
                             stderr=fnull)
                proc.wait()
            else:
                pass
        elif self.state == pulsectl.PulseStateEnum.running:
            self.active_time = datetime.datetime.now()
        else:
            pass

    def update_sink(self, sink):
        self.sink = sink
        self.logger.debug(f'New sink state. Was {self.state} now {sink.state}')
        self.state = sink.state
        if self.state == pulsectl.PulseStateEnum.running:
            self.active_time = datetime.datetime.now()

    def __del__(self):
        self.logger.debug(f'Removing device instance for index {self.sink.index}')
        try:
            self.thread.stop()
        except AttributeError:
            pass
        self.remove = True


class RepeatedTimer:
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = threading.Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


class DeviceMacAddressUnknown(Exception):
    pass
