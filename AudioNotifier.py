# Notify user via audio
# Author: Tyler Gamvrelis

import beepy
import logging
from queue import Queue
from threading import Thread, Event


class AudioNotifier(Thread):
    """Notifies user of a drop using an audio track."""

    def __init__(self):
        super(AudioNotifier, self).__init__(name='audio_thread')
        self._cmd_queue = Queue() # Infinite queue
        self._stop_event = Event()
        self._play_audio = False
        self._logger = logging.getLogger(__name__)

    def stop(self):
        """
        Prevents any more stock checks from executing, and causes the thread to
        exit when the current request (if any) is done executing.
        """
        self._stop_event.set()
        self.stop_audio() # To ensure thread is not blocked
        self._logger.info('Stop requested for audio_thread')

    def _has_stopped(self):
        """Check whether this thread has been stopped."""
        return self._stop_event.is_set()

    def start_audio(self):
        """Start audio playback."""
        self._cmd_queue.put(True)

    def stop_audio(self):
        """Stop audio playback."""
        self._cmd_queue.put(False)

    def run(self):
        while True:
            if self._has_stopped():
                break
            if not self._play_audio:
                # If we aren't playing audio, then block until we get a command
                self._play_audio = self._cmd_queue.get()
            else:
                # Play sound, then apply new commands
                beepy.beep(sound='ready') # Blocking call
                while not self._cmd_queue.empty():
                    self._play_audio = self._cmd_queue.get()
        self._logger.info('Exiting thread audio_thread')
