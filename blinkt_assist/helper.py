import abc
import blinkt
import colorsys
import logging
import numpy
from random import randint
import time
import threading
from google.assistant.library.event import EventType as google_EventType

"""Assist processing for the Blinkt Library"""

LOG_LEVEL = logging.DEBUG

logging.basicConfig(
    level=LOG_LEVEL,
    format="[%(asctime)s] %(levelname)s:%(name)s.%(funcName)s:%(message)s"
)


class GoogleAssistantColorHelper(object):
    RED = 0
    GREEN = 1
    BLUE = 2

    GOO_BLUE = [53, 25, 237]
    GOO_RED = [255, 25, 20]
    GOO_YELLOW = [255, 155, 0]
    GOO_GREEN = [30, 255, 15]
    GOO_PIXELS = [GOO_GREEN, GOO_GREEN, GOO_YELLOW, GOO_YELLOW, GOO_RED, GOO_RED, GOO_BLUE, GOO_BLUE]
    GOO_LIGHT = 0.05

    GOO_BLUE_H = 235
    GOO_RED_H = 352
    GOO_YELLOW_H = 55
    GOO_GREEN_H = 110
    GOO_PIXELS_H = [GOO_GREEN_H, GOO_GREEN_H, GOO_YELLOW_H, GOO_YELLOW_H, GOO_RED_H, GOO_RED_H, GOO_BLUE_H, GOO_BLUE_H]


class GoogleAssistantColorStrategy(metaclass=abc.ABCMeta):
    """
    Abstract strategy for all Blinkt animation strategy.
    """

    def __init__(self, event_type):
        """
        Constructor.
        :param event_type: The event registered
        :type event_type: google_EventType
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.log(logging.DEBUG, "Event Type:{!s}".format(event_type))
        self.google_event_type = event_type
        self.initialised = False
        self.wake_event = threading.Event()
        self.done_event = threading.Event()
        self.runner = threading.Thread(target=self.do, args=(self.wake_event, self.done_event,))
        self.runner.do_run = False

    def __is_eligible__(self, event_type):
        """
        Check if strategy can run for givbent event type.
        :param event_type: The event to check.
        :type event_type: google_EventType
        :return: bool
        """
        return self.google_event_type == event_type

    def activate(self):
        """
        Activate the strategy.
        :return: None
        """
        if not self.initialised:
            self.logger.log(logging.DEBUG, "Starting !")
            self.runner.start()
            self.initialised = True
            self.runner.do_stop = False
        self.logger.log(logging.DEBUG, "Activating !")
        self.runner.do_run = True
        self.wake_event.set()
        self.logger.log(logging.DEBUG, "Activated !")

    def deactivate(self):
        """
        Deactivate the strategy.
        :return: None
        """
        self.logger.log(logging.DEBUG, "Deactivating !")
        self.runner.do_run = False
        self.done_event.wait()
        self.clear()
        self.logger.log(logging.DEBUG, "Deactivated !")

    def terminate(self):
        """
        Deactivate the strategy.
        :return: None
        """
        self.logger.log(logging.DEBUG, "Terminating !")
        self.runner.do_stop = True
        self.runner.do_run = False
        self.wake_event.set()
        if self.runner.isAlive:
            try:
                self.runner.join()
            except RuntimeError:
                pass
        self.logger.log(logging.DEBUG, "Terminated !")

    def __str__(self):
        """
        Textual definition
        :return:
        """
        return "Strategy {!s}".format(self.__class__.__name__)

    def do(self, event, done):
        """
        Perform the strategy's business.
        :return: None
        """
        current_runner = threading.currentThread()
        while event.wait():
            event.clear()
            self.apply(current_runner)
            done.set()
            if getattr(current_runner, "do_stop", True):
                return

    @staticmethod
    def clear():
        """
        Clear the Blinkt!
        :return: None
        """
        blinkt.clear()
        blinkt.show()

    @abc.abstractmethod
    def apply(self, current_runner):
        """
        Perform the strategy's business.
        :param current_runner: The threading runner.
        :type current_runner: threading.Event
        :return: None
        """


class GoogleAssistantFullColorStrategy(GoogleAssistantColorStrategy):
    """
    Blinkt Strategy setting all LEDs to Google Assistant Colors.
    """
    def apply(self, current_runner):
        """
        Perform the strategy's business.
        :param current_runner: The threading runner.
        :type current_runner: threading.Event
        :return: None
        """
        while getattr(current_runner, "do_run", True):
            for pix in reversed(range(blinkt.NUM_PIXELS)):
                blinkt.clear()
                i = pix
                blinkt.set_pixel(i, GoogleAssistantColorHelper.GOO_PIXELS[i][GoogleAssistantColorHelper.RED],
                                 GoogleAssistantColorHelper.GOO_PIXELS[i][GoogleAssistantColorHelper.GREEN],
                                 GoogleAssistantColorHelper.GOO_PIXELS[i][GoogleAssistantColorHelper.BLUE],
                                 GoogleAssistantColorHelper.GOO_LIGHT)
                i = pix + 1
                if i == blinkt.NUM_PIXELS:
                    i = 0
                blinkt.set_pixel(i, GoogleAssistantColorHelper.GOO_PIXELS[i][GoogleAssistantColorHelper.RED],
                                 GoogleAssistantColorHelper.GOO_PIXELS[i][GoogleAssistantColorHelper.GREEN],
                                 GoogleAssistantColorHelper.GOO_PIXELS[i][GoogleAssistantColorHelper.BLUE],
                                 GoogleAssistantColorHelper.GOO_LIGHT)
                blinkt.show()
                time.sleep(0.075)
            time.sleep(0.1)


class GoogleAssistantFadingColorStrategy(GoogleAssistantColorStrategy):
    """
    Blinkt Strategy setting all LEDs to Google Assistant Colors with fading effect.
    """
    MAX = 0.4
    STEP = 0.02
    TEMPO = 0.04

    def apply(self, current_runner):
        """
        Perform the strategy's business.
        :param current_runner: The threading runner.
        :type current_runner: threading.Event
        :return: None
        """
        sat = 1.0
        while getattr(current_runner, "do_run", True):
            for bright in numpy.arange(0.0, GoogleAssistantFadingColorStrategy.MAX,
                                       GoogleAssistantFadingColorStrategy.STEP):
                for i in reversed(range(blinkt.NUM_PIXELS)):
                    hue = GoogleAssistantColorHelper.GOO_PIXELS_H[i]
                    h = (hue % 360) / 360.0
                    r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, sat, bright)]
                    blinkt.set_pixel(i, r, g, b)
                    blinkt.show()
                time.sleep(GoogleAssistantFadingColorStrategy.TEMPO)
            time.sleep(0.075)
            for bright in reversed(numpy.arange(0.0, GoogleAssistantFadingColorStrategy.MAX,
                                                GoogleAssistantFadingColorStrategy.STEP)):
                for i in reversed(range(blinkt.NUM_PIXELS)):
                    hue = GoogleAssistantColorHelper.GOO_PIXELS_H[i]
                    h = (hue % 360) / 360.0
                    r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, sat, bright)]
                    blinkt.set_pixel(i, r, g, b)
                    blinkt.show()
                time.sleep(GoogleAssistantFadingColorStrategy.TEMPO)
            time.sleep(0.075)


class GoogleAssistantRandomColorStrategy(GoogleAssistantColorStrategy):
    """
    Blinkt Strategy setting randomly groups of came coloured LEDs to Google Assistant Colors with fading effect.
    """
    MAX = 0.4
    STEP = 0.02
    TEMPO = 0.04

    def apply(self, current_runner):
        """
        Perform the strategy's business.
        :param current_runner: The threading runner.
        :type current_runner: threading.Event
        :return: None
        """
        last_hue = None
        sat = 1.0
        while getattr(current_runner, "do_run", True):
            i = randint(0, blinkt.NUM_PIXELS - 1)
            hue = GoogleAssistantColorHelper.GOO_PIXELS_H[i]
            if last_hue != hue:
                h = (hue % 360) / 360.0
                for bright in numpy.arange(0.0, GoogleAssistantRandomColorStrategy.MAX,
                                           GoogleAssistantRandomColorStrategy.STEP):
                    r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, sat, bright)]
                    blinkt.set_pixel(i, r, g, b)
                    if i + 1 < blinkt.NUM_PIXELS:
                        if GoogleAssistantColorHelper.GOO_PIXELS_H[i] == GoogleAssistantColorHelper.GOO_PIXELS_H[i + 1]:
                            blinkt.set_pixel(i + 1, r, g, b)
                        else:
                            blinkt.set_pixel(i - 1, r, g, b)
                    else:
                        blinkt.set_pixel(i - 1, r, g, b)
                    blinkt.show()
                    time.sleep(GoogleAssistantRandomColorStrategy.TEMPO)
                for bright in reversed(numpy.arange(0.0, GoogleAssistantRandomColorStrategy.MAX,
                                                    GoogleAssistantRandomColorStrategy.STEP)):
                    r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, sat, bright)]
                    blinkt.set_pixel(i, r, g, b)
                    if i + 1 < blinkt.NUM_PIXELS:
                        if GoogleAssistantColorHelper.GOO_PIXELS_H[i] == GoogleAssistantColorHelper.GOO_PIXELS_H[i + 1]:
                            blinkt.set_pixel(i + 1, r, g, b)
                        else:
                            blinkt.set_pixel(i - 1, r, g, b)
                    else:
                        blinkt.set_pixel(i - 1, r, g, b)
                    blinkt.show()
                    time.sleep(GoogleAssistantRandomColorStrategy.TEMPO)
                last_hue = hue
                time.sleep(1)


def main():
    print('Subclass:', issubclass(GoogleAssistantRandomColorStrategy,
                                  GoogleAssistantColorStrategy))
    example_black_strategy = GoogleAssistantRandomColorStrategy(google_EventType.ON_START_FINISHED)
    print('Instance:', isinstance(example_black_strategy,
                                  GoogleAssistantColorStrategy))
    print('Textual definition:', example_black_strategy)
    print('Check OK', example_black_strategy.__is_eligible__(google_EventType.ON_START_FINISHED))
    print('Check KO', example_black_strategy.__is_eligible__(google_EventType.ON_CONVERSATION_TURN_STARTED))
    example_full_strategy = GoogleAssistantFullColorStrategy(google_EventType.ON_START_FINISHED)
    example_full_strategy.activate()
    wait_show = 10
    wait_tempo = 2
    time.sleep(wait_show)
    example_full_strategy.deactivate()
    time.sleep(wait_tempo)

    example_random_strategy = GoogleAssistantRandomColorStrategy(google_EventType.ON_START_FINISHED)
    example_random_strategy.activate()
    time.sleep(wait_show)
    example_random_strategy.deactivate()
    time.sleep(wait_tempo)

    example_fading_strategy = GoogleAssistantFadingColorStrategy(google_EventType.ON_START_FINISHED)
    example_fading_strategy.activate()
    time.sleep(wait_show)
    example_fading_strategy.deactivate()
    time.sleep(wait_tempo)

    example_full_strategy.activate()
    time.sleep(wait_show)
    example_full_strategy.deactivate()
    time.sleep(wait_tempo)

    example_full_strategy.terminate()
    example_random_strategy.terminate()
    example_fading_strategy.terminate()


if __name__ == '__main__':
    main()
