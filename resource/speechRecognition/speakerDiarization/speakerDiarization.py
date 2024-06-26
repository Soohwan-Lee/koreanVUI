#
#    Copyright 2022-2023 Picovoice Inc.
#
#    You may not use this file except in compliance with the license. A copy of the license is located in the "LICENSE"
#    file accompanying this source.
#
#    Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
#    an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
#    specific language governing permissions and limitations under the License.
#

import signal
import sys
import time
from argparse import ArgumentParser
from threading import Thread

from pvfalcon import create, FalconActivationLimitError
from pvrecorder import PvRecorder
from tabulate import tabulate


class Recorder(Thread):
    def __init__(self, audio_device_index):
        super().__init__()
        self._pcm = list()
        self._is_recording = False
        self._stop = False
        self._audio_device_index = audio_device_index

    def is_recording(self):
        return self._is_recording

    def run(self):
        self._is_recording = True

        recorder = PvRecorder(frame_length=160, device_index=self._audio_device_index)
        recorder.start()

        while not self._stop:
            self._pcm.extend(recorder.read())
        recorder.stop()

        self._is_recording = False

    def stop(self):
        self._stop = True
        while self._is_recording:
            pass

        return self._pcm


def main():
    parser = ArgumentParser()
    parser.add_argument(
        '--access_key',
        help='AccessKey obtained from Picovoice Console (https://console.picovoice.ai/)')
    parser.add_argument(
        '--library_path',
        help='Absolute path to dynamic library. Default: using the library provided by `pvfalcon`')
    parser.add_argument(
        '--model_path',
        help='Absolute path to Falcon model. Default: using the model provided by `pvfalcon`')
    parser.add_argument(
        '--show_audio_devices',
        action='store_true',
        help='Only list available devices and exit')
    parser.add_argument(
        '--audio_device_index',
        default=-1,
        type=int,
        help='Audio device index to use from --show_audio_devices')
    args = parser.parse_args()

    args.access_key = "YOUR_API_KEY"

    if args.show_audio_devices:
        for index, name in enumerate(PvRecorder.get_available_devices()):
            print('Device #%d: %s' % (index, name))
        return

    if args.audio_device_index != -1:
        devices_length = len(PvRecorder.get_available_devices())
        if args.audio_device_index < 0 or args.audio_device_index >= devices_length:
            print('Invalid audio device index provided.')
            sys.exit(1)

    if not args.access_key:
        print('--access_key is required.')
        return

    falcon = create(
        access_key=args.access_key,
        model_path=args.model_path,
        library_path=args.library_path)

    recorder = None

    def on_exit(_, __):
        falcon.delete()

        if recorder is not None:
            recorder.stop()

        print()
        sys.exit(0)

    signal.signal(signal.SIGINT, on_exit)

    print('>>> Press `CTRL+C` to exit: ')

    while True:
        if recorder is not None:
            input('>>> Recording ... Press `ENTER` to stop: ')
            try:
                segments = falcon.process(recorder.stop())
                print(tabulate(segments, headers=['start_sec', 'end_sec', 'speaker_tag'], floatfmt='.2f'))
            except FalconActivationLimitError:
                print('AccessKey has reached its processing limit.')
            print()
            recorder = None
        else:
            input('>>> Press `ENTER` to start: ')
            recorder = Recorder(args.audio_device_index)
            recorder.start()
            time.sleep(.25)


if __name__ == '__main__':
    main()