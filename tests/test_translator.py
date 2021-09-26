import pytest
import copy

from datatranslator.traslator import *
from fixtures import *
from datatranslator.apierror import *

def test_translate():
    """successful case"""
    obj = HumanReadableTranslator(DATE_JSON, tolerance=LOW_TOLERANCE)
    res = obj.traslate()
    assert res == DATE_RESULT
    
def test_translate_invalid_input_type():
    """input type is not valid"""
    obj = HumanReadableTranslator(INVALID_JSON, tolerance=LOW_TOLERANCE)
    with pytest.raises(BadRequest):
        obj.traslate()
        
def test_translate_invalid_input_value():
    """value is not a number"""
    input = copy.deepcopy(DATE_JSON)
    input['tuesday'][0]['value'] = 'this is not an int'
    obj = HumanReadableTranslator(input, tolerance=LOW_TOLERANCE)
    with pytest.raises(BadRequest):
        obj.traslate()

def test_translate_invalid_input_value_high_tolerance():
    """value is not a number, returns partial result with high tolerance"""
    input = copy.deepcopy(DATE_JSON)
    input['tuesday'][0]['value'] = 'this is not an int'
    obj = HumanReadableTranslator(input, tolerance=HIGH_TOLERANCE)
    response = obj.traslate()
    assert 'Tuesday: 10 AM - 6 PM' not in response
        
def test_translate_invalid_fileds_missing():
    """mandatory type or value missing"""
    input = copy.deepcopy(DATE_JSON)
    input['tuesday'][0].pop('type')
    obj = HumanReadableTranslator(input, tolerance=LOW_TOLERANCE)
    with pytest.raises(BadRequest):
        obj.traslate()
        
def test_translate_invalid_data():
    input = copy.deepcopy(MISSING_TYPES_JSON)
    obj = HumanReadableTranslator(input, tolerance=LOW_TOLERANCE)
    with pytest.raises(TranslatorException):
        obj.traslate()
    