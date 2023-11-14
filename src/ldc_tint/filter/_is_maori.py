import argparse
import re
from typing import List

from ldc.core import LOGGING_WARN, DOMAIN_PRETRAIN
from ldc.filter import Filter, FILTER_ACTIONS, FILTER_ACTION_KEEP, FILTER_ACTION_DISCARD
from ldc.pretrain import PretrainData
from reo_toolkit import is_maori


class IsMaori(Filter):
    """
    Detects whether text is Māori or not, either in strict or weak mode.
    """

    def __init__(self, min_maori: float = 0.0, strict: bool = False, action: str = FILTER_ACTION_KEEP,
                 logger_name: str = None, logging_level: str = LOGGING_WARN):
        """
        Initializes the filter.

        :param min_maori: the minimum required ratio of Māori words (0-1)
        :type min_maori: float
        :param strict: whether to use a strict evaluation
        :type strict: bool
        :param action: the action to apply to the data records
        :type action: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)

        if action not in FILTER_ACTIONS:
            raise Exception("Invalid action: %s" % action)

        self.min_maori = min_maori
        self.strict = strict
        self.action = action

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "is-maori"

    def description(self) -> str:
        """
        Returns a description of the reader.

        :return: the description
        :rtype: str
        """
        return "Determines whether text is Māori or not (weak or strict mode), using the supplied threshold. The filter action then determines what to do with the record."

    def domains(self) -> List[str]:
        """
        Returns the domains of the filter.

        :return: the domains
        :rtype: list
        """
        return [DOMAIN_PRETRAIN]

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [PretrainData]

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [PretrainData]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-m", "--min_maori", type=float, default=0.0, help="The minimum required ratio (0-1) of Māori words in the text.")
        parser.add_argument("-s", "--strict", action="store_true", help="Whether to use strict mode rather than weak one.")
        parser.add_argument("-a", "--action", choices=FILTER_ACTIONS, default=FILTER_ACTION_KEEP, help="How to react when the thresholds are met")
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.min_maori = ns.min_maori
        self.strict = ns.strict
        self.action = ns.action

    def _do_process(self, data):
        """
        Processes the data record.

        :param data: the record to process
        :return: the potentially updated record or None if to drop
        """
        result = data

        # evaluate all words
        text = data.content.strip()
        splitter = re.compile(r'[\s\n\-]+')
        if splitter.search(text):
            evals = []
            # Split the text and evaluate each piece
            for split in splitter.split(text):
                if len(split) > 0:
                    evals.append(is_maori(split, strict=self.strict))
        else:
            evals = [is_maori(data.content, strict=self.strict)]

        if len(evals) > 0:
            ratio = evals.count(True) / len(evals)
        else:
            ratio = 0.0

        if ratio >= self.min_maori:
            if self.action == FILTER_ACTION_DISCARD:
                result = None
        else:
            if self.action == FILTER_ACTION_KEEP:
                result = None

        self.logger().info("ratio=%0.3f, forward=%s" % (ratio, (result is not None)))

        return result
