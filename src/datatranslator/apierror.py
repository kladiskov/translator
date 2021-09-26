# -*- coding: utf-8 -*-
# pylint: disable=missing-function-docstring
"""
.. :module:: translator
   :platform: Linux
   :synopsis: A Place for common API errors handling

.. moduleauthor:: Sandesh <sandesh2k18@gmail.com> (Sep 12, 2021)
"""

BAD_REQUEST = 'Bad request'
APP_ERROR = 'There was some problem in processing the request.'

class BaseException(Exception):
    """Base exception handler"""
    def __init__(self, message, code=None, payload=None):
        super().__init__()
        self.message = message
        self.status_code = code
        self.content_type = 'application/json'
        self.data = None
    
class BadRequest(BaseException):
    """Handling Client side errors"""
    def __init__(self, message=BAD_REQUEST, code=400, payload=None):
        super().__init__(message, code=code, payload=payload)
        
    
class TranslatorException(BaseException):
    """Handling application errors"""
    def __init__(self, message=APP_ERROR, code=500, payload=None):
        super().__init__(message, code=code, payload=payload)