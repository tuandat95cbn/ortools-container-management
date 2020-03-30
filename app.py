#!/usr/bin/env python
# coding:utf-8

import logging.config
from werkzeug.routing import Rule
import os
import uuid

from flask import Flask, request, json, jsonify
from flask import send_from_directory

from constant.const import LOG_CONFIG_FILE_PATH, LOG_DIR, UPLOAD_DIR

app = Flask(__name__)

_VERSION = 1  # API version


CONTEXT_PATH = '/optimize'
UPLOAD_FOLDER = UPLOAD_DIR



def create_app():
    ALLOWED_EXTENSIONS = set(['java', ])
    app = Flask(__name__, static_url_path=CONTEXT_PATH)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['APPLICATION_ROOT'] = CONTEXT_PATH
    app.url_rule_class = lambda path, **options: Rule(app.config['APPLICATION_ROOT'] + path, **options)

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route(CONTEXT_PATH + '/solve', methods=['POST'])
    def schedule():
        if request.method == 'POST':
            script = request.files['script']

            if not allowed_file(script.filename):
                res = {"status": "ERROR", "msg": "File do not accept"}
                response = app.response_class(
                    response=json.dumps(res, sort_keys=False),
                    status=400,
                    mimetype='application/json'
                )
            id = str(uuid.uuid1())
            logging.info(id)
            folder_path = os.path.join(app.config['UPLOAD_FOLDER'], id)
            os.makedirs(folder_path)
            script.save(os.path.join(folder_path, 'Main.java'))
            files = request.files.getlist('files[]')
            for file in files:
                file.save(os.path.join(folder_path, file.filename))

            response_status = "SUCCESS"

            res = {"status": response_status, "msg": "Job scheduled!", "id": id}
            response = app.response_class(
                response=json.dumps(res, sort_keys=False),
                status=200,
                mimetype='application/json'
            )
            return response


    @app.route(CONTEXT_PATH+'/files/<uuid:id>/<string:filename>',methods=['GET'])
    def get_file(id,filename):
        print(request.view_args['id'])
        file_path = os.path.join(app.config['UPLOAD_FOLDER'],str(id))
        return send_from_directory(
                                   file_path,filename)


    @app.errorhandler(500)
    def internal_error(error):
        print(str(error))  # ghetto logging
        return jsonify(status="ERROR", msg="Please try again later!!"), 500


    @app.errorhandler(404)
    def not_found_error(error):
        print(str(error))
        return jsonify(status="ERROR", msg="Please try again later!!"), 404


    @app.errorhandler(405)
    def not_allowed_error(error):
        print(str(error))
        return jsonify(status="ERROR", msg="Please try again later!!"), 405


        return app
if __name__ == '__main__':
    logging.config.fileConfig(LOG_CONFIG_FILE_PATH)
    app = create_app()
    app.run(host="0.0.0.0", port=int(8080))

