#!/usr/bin/env python
# -*- coding: utf-8 -*-

from blinkt_assist.helper import GoogleAssistantColorHelper, GoogleAssistantFullColorStrategy, \
    GoogleAssistantFadingColorStrategy, GoogleAssistantRandomColorStrategy

import unittest
import mock


class RunnerTestCase(unittest.TestCase):
    """
    Unit Test case for the class assisting processing for the Blinkt Library.
    """

    def test_color_helper(self):
        """

        :return:
        """
        color_helper = GoogleAssistantColorHelper()
        self.assertIsNotNone(color_helper, "Unable to create the test class!")
        self.assertIsNotNone(color_helper.RED, "Missing Property RED!")
        self.assertIsNotNone(color_helper.GREEN, "Missing Property GREEN!")
        self.assertIsNotNone(color_helper.BLUE, "Missing Property BLUE!")

        self.assertIsNotNone(color_helper.GOO_BLUE, "Missing Property GOO_BLUE!")
        self.assertIsNotNone(color_helper.GOO_RED, "Missing Property GOO_RED!")
        self.assertIsNotNone(color_helper.GOO_YELLOW, "Missing Property GOO_YELLOW!")
        self.assertIsNotNone(color_helper.GOO_GREEN, "Missing Property GOO_GREEN!")
        self.assertIsNotNone(color_helper.GOO_PIXELS, "Missing Property GOO_PIXELS!")
        self.assertIsNotNone(color_helper.GOO_LIGHT, "Missing Property GOO_LIGHT!")

        self.assertIsNotNone(color_helper.GOO_BLUE_H, "Missing Property GOO_BLUE_H!")
        self.assertIsNotNone(color_helper.GOO_RED_H, "Missing Property GOO_RED_H!")
        self.assertIsNotNone(color_helper.GOO_YELLOW_H, "Missing Property GOO_YELLOW_H!")
        self.assertIsNotNone(color_helper.GOO_GREEN_H, "Missing Property GOO_GREEN_H!")
        self.assertIsNotNone(color_helper.GOO_PIXELS_H, "Missing Property GOO_PIXELS_H!")

    @mock.patch("blinkt.clear")
    @mock.patch("blinkt.set_pixel")
    @mock.patch("blinkt.show")
    def test_full_color_strategy(self, mock_show, mock_set, mock_clear):
        """
        TODO
        :param mock_show:
        :param mock_set:
        :param mock_clear:
        :return:
        """
        strategy = GoogleAssistantFullColorStrategy(None)
        self.assertIsNotNone(strategy)

    @mock.patch("blinkt.clear")
    @mock.patch("blinkt.set_pixel")
    @mock.patch("blinkt.show")
    def test_random_strategy(self, mock_show, mock_set, mock_clear):
        """
        TODO
        :param mock_show:
        :param mock_set:
        :param mock_clear:
        :return:
        """
        strategy = GoogleAssistantRandomColorStrategy(None)
        self.assertIsNotNone(strategy)

    @mock.patch("blinkt.clear")
    @mock.patch("blinkt.set_pixel")
    @mock.patch("blinkt.show")
    def test_fading_strategy(self, mock_show, mock_set, mock_clear):
        """
        TODO
        :param mock_show:
        :param mock_set:
        :param mock_clear:
        :return:
        """
        strategy = GoogleAssistantFadingColorStrategy(None)
        self.assertIsNotNone(strategy)
