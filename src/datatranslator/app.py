# -*- coding: utf-8 -*-
# pylint: disable=missing-function-docstring
"""
   API Interface for translator
.. moduleauthor:: Sandesh <sandesh2k18@gmail.com> (Sep 12, 2021)
"""

import json
import logging
from datatranslator import config
from flask import Flask, request, jsonify
from datatranslator.apierror import (BaseException, 
                                    BadRequest,
                                    TranslatorException,)
from datatranslator.translator import (get_translator_object,
                                      LOW_TOLERANCE, 
                                      HUMAN_READABLE)

logging.basicConfig(level = logging.INFO)
LOG = logging.getLogger('translator')

def create_translation_api():
    """Create a flask route for restaurant dates"""
    app = Flask(__name__)
    app.config.from_object(config)
    
    @app.errorhandler(BaseException)
    def handle_exception(ex):
        """Return error details in JSON for BaseException type"""
        response = {"error": ex.message}
        LOG.error("Error detected: {}".format(ex.message))
        return jsonify(response), ex.status_code
    
    @app.route('/restaurant/dates', methods=['POST'])
    def translate():
        """API Endpoint for receiving input data for translation
        :raises BaseException: For any client, application errors
        """
        tolerance = LOW_TOLERANCE
        type = HUMAN_READABLE
        working_hours_data = {}
        if request.json:
            working_hours_data = request.json
        elif request.files.get('file', {}):
            working_hours_data = json.load(request.files['file'])
        if not working_hours_data:
            raise BadRequest('Input data is empty.', code=400)
        if app.config.get('TOLERANCE'):
            tolerance = app.config.get('TOLERANCE')
        if app.config.get('TYPE'):
            type = app.config.get('TYPE')
        result = []
        translator_obj = get_translator_object(working_hours_data, tolerance=tolerance, type=type)
        result = translator_obj.traslate()
        return jsonify(result)
    
    return app

if __name__ == "__main__":
    app = create_translation_api()
    app.run(port=config.PORT)
