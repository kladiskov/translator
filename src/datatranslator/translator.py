# -*- coding: utf-8 -*-
# pylint: disable=missing-function-docstring
"""
.. :module:: translator
   :platform: Linux
   :synopsis: Implement translation modile

.. moduleauthor:: Sandesh <sandesh2k18@gmail.com> (Sep 12, 2021)
"""

import abc
import logging

from datetime import datetime

from datatranslator.apierror import BadRequest, TranslatorException

# Tolerance levels - High and low tolerance to input JSON validation and errors
HIGH_TOLERANCE = 1
LOW_TOLERANCE = 2

# Supported translator, not to be choosen by the client for now. 
HUMAN_READABLE = 1

INPUT_DAYS = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']

GENERIC_TRANSLATION_ERROR_MSG = "Error has occured while performing the operation"

LOG = logging.getLogger('translator')

class Translator(metaclass=abc.ABCMeta):
    """Declare an interface for data translation"""
    
    @abc.abstractmethod    
    def traslate(self):
       """Perform aprpriate data translation based on type of data 
       and the nature of translation required.
       """

    
class HumanReadableTranslator(Translator):
    """Class to translate restaurant working hours into human readable format
       Based on tolerance set in the config, application behaves differently.
       For low tolerance, requests will not get processed. For some form of data
       validation errors are omitted in the case of high tolerance
    """

    def __init__(self, data, tolerance=LOW_TOLERANCE):
        self.data = data
        self.tolerance = tolerance
    
    def traslate(self):
        """This method translates the given input json containing restaurant working 
        hours into human readable format and prints it into the console. Based on the 
        tolerance level (HIGH or LOW) it skips the processing for that day (High tolerance)
        or do not process the request (Low tolerance).
        :returns result: (list) working hours in human readable format.
        :raises BaseException: for any data validation errors
        """
        LOG.info("Received request for translating dates")
        result = []
        for day in INPUT_DAYS:
            this_day = ''
            if day not in self.data:
                # Data not availble for that day
                continue
            hours = self.data.get(day,[])
            if len(hours) == 0:
                # Restaurant is closed for that day
                result.append("{}: Closed".format(day.capitalize()))
                continue
            # Do not process for the day if there are validation errors
            # In the case of high tolerance, skip the error data 
            if not self._validate_input(hours):
                if self.tolerance == LOW_TOLERANCE:
                    raise BadRequest('Input data is not valid')
                else:
                    this_day = ''
                    continue
            hours = sorted(hours, key=lambda item: item.get("value", 0))
            first_time = True
            for hour in hours:
                _time = hour.get('value')
                _time = datetime.utcfromtimestamp(_time).strftime('%-I:%M %p').replace(':00','')
                if hour.get('type','') == 'close' and first_time:
                    if len(result) > 0:
                        index = len(result) - 1
                        result[index] = "{} - {}".format(result[index],_time)
                    first_time = False
                    continue
                elif hour.get('type','') == 'open':
                    if first_time:
                        first_time = False
                    if not this_day:
                        this_day = '{}: {}'.format(day.capitalize(), _time)
                    else:
                        this_day += ', {}'.format(_time)
                elif hour.get('type','') == 'close':
                    this_day += ' - {}'.format(_time)
            if this_day:
                result.append(this_day)
        if not self._validate_output(result):
            raise TranslatorException('Error in processing the input data')
        result_str = "\x1B[3m{}".format("\n".join(result[:]))
        LOG.info('#  Output in Human readable Format  #')
        LOG.info("\n\n{}\n\n".format(result_str))
        return result
    
    def _validate_input(self, hours):
        """Validates input data for field correctness
        :returns result:(bool) returns the validation status
        """
        result = True
        for data in hours:
            if not result:
                break
            if not data.get('type') or not data.get('value'):
                result = False
            if result and data.get('type','') not in ['open','close']:
                result = False
            if result:
                try:
                    int(data.get('value'))
                except Exception:
                    result = False
        return result
    
    def _validate_output(self, result_list):
        """Validate output data if input json has wrong entries"""
        for item in result_list:
            item = item.lower()
            if not any(day in item for day in INPUT_DAYS):
                return False
        return True
    
def get_translator_object(data,tolerance=LOW_TOLERANCE,type=HUMAN_READABLE):
    """Select appropriate translation object based on type"""
    if type == HUMAN_READABLE:
        return HumanReadableTranslator(data,tolerance)
    else:
        raise TranslatorException("Invalid translator type")