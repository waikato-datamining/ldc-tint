import argparse
import copy
from typing import List

from ldc.core import LOGGING_WARN, DOMAIN_PAIRS, DOMAIN_PRETRAIN, DOMAIN_TRANSLATION
from ldc.core import LOCATION_ANY, LOCATION_INSTRUCTION, LOCATION_INPUT, LOCATION_OUTPUT, LOCATION_CONTENT, \
    LOCATIONS, LOCATIONS_PAIRS, LOCATIONS_PRETRAIN
from ldc.filter import Filter
from ldc.pretrain import PretrainData
from ldc.supervised.pairs import PairData
from ldc.translation import TranslationData


class Demacronize(Filter):
    """
    Removes macrons from text.
    """

    def __init__(self, location: str = LOCATION_ANY, languages: List[str] = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARN):
        """
        Initializes the filter.

        :param location: in which part of the data to look for the macrons
        :type location: str
        :param languages: the languages to restrict the check to, None to check all
        :type languages: list
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)

        if location not in LOCATIONS:
            raise Exception("Invalid location: %s" % location)

        self.location = location
        self.languages = languages

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "de-macronize"

    def description(self) -> str:
        """
        Returns a description of the reader.

        :return: the description
        :rtype: str
        """
        return "Removes macrons from text, e.g., Ā -> Aa and ā -> aa"

    def domains(self) -> List[str]:
        """
        Returns the domains of the filter.

        :return: the domains
        :rtype: list
        """
        return [DOMAIN_PAIRS, DOMAIN_PRETRAIN, DOMAIN_TRANSLATION]

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [PairData, PretrainData, TranslationData]

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [PairData, PretrainData, TranslationData]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-L", "--location", choices=LOCATIONS, default=LOCATION_ANY, help="Where to look for the macons; pairs: " + ",".join(LOCATIONS_PAIRS) + ", pretrain: " + ",".join(LOCATIONS_PRETRAIN) + ", translation: " + ",".join(LOCATIONS_PRETRAIN))
        parser.add_argument("-g", "--language", type=str, help="The languages to inspect; inspects all if not specified", required=False, nargs="*")
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.location = ns.location
        self.languages = ns.language

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()

        if self.languages is not None:
            self.languages = [x.lower() for x in self.languages]

    def _get_lengths(self, data) -> List[int]:
        """
        Turns the record into list of lengths.

        :return: the compiled list of lengths
        :rtype: list
        """
        lengths = list()

        if isinstance(data, PairData):
            if self.location in [LOCATION_INSTRUCTION, LOCATION_ANY]:
                lengths.append(len(data.instruction))
            if self.location in [LOCATION_INPUT, LOCATION_ANY]:
                lengths.append(len(data.input))
            if self.location in [LOCATION_OUTPUT, LOCATION_ANY]:
                lengths.append(len(data.output))
        elif isinstance(data, PretrainData):
            if self.location in [LOCATION_CONTENT, LOCATION_ANY]:
                lengths.append(len(data.content))
        elif isinstance(data, TranslationData):
            if self.languages is None:
                for k in data.translations:
                    lengths.append(len(data.translations[k]))
            else:
                for lang in self.languages:
                    if lang in data.translations:
                        lengths.append(len(data.translations[lang]))
                    else:
                        # missing language gets length 0
                        lengths.append(0)
        else:
            raise Exception("Unhandled data type: %s" % str(type(data)))

        return lengths

    def _remove(self, s: str) -> str:
        """
        Removes the macrons from the string.

        :param s: the string to process
        :type s: str
        :return: the processed string
        :rtype: str
        """
        s = s.replace("Ā", "Aa")
        s = s.replace("ā", "aa")
        s = s.replace("Ē", "Ee")
        s = s.replace("ē", "ee")
        s = s.replace("Ī", "Ii")
        s = s.replace("ī", "ii")
        s = s.replace("Ō", "Oo")
        s = s.replace("ō", "oo")
        s = s.replace("Ū", "Uu")
        s = s.replace("ū", "uu")
        return s

    def process(self, data):
        """
        Processes the data record.

        :param data: the record to process
        :return: the potentially updated record or None if to drop
        """
        result = copy.deepcopy(data)

        if isinstance(result, PairData):
            if self.location in [LOCATION_INSTRUCTION, LOCATION_ANY]:
                result.instruction = self._remove(result.instruction)
            if self.location in [LOCATION_INPUT, LOCATION_ANY]:
                result.input = self._remove(result.input)
            if self.location in [LOCATION_OUTPUT, LOCATION_ANY]:
                result.output = self._remove(result.output)
        elif isinstance(result, PretrainData):
            if self.location in [LOCATION_CONTENT, LOCATION_ANY]:
                result.content = self._remove(result.content)
        elif isinstance(result, TranslationData):
            if self.languages is None:
                for k in result.translations:
                    result.translations[k] = self._remove(result.translations[k])
            else:
                for lang in self.languages:
                    if lang in result.translations:
                        result.translations[lang] = self._remove(result.translations[lang])
        else:
            raise Exception("Unhandled data type: %s" % str(type(result)))

        return result
