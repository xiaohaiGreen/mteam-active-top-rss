from flask import Flask,make_response,request,jsonify,abort
from mteam.m_team import MTeam
from mteam.m_team_config import MTeamConfig
from mteam.util import *
from mteam.const import *
from mteam.param import Param
import os
import logging
from util.log import log

logger = log()

app = Flask(__name__)
x_api_key = os.environ.get("X-API-KEY")
if x_api_key is None:
    logger.error("X-API-KEY can not be null")
    exit(1)
    
config = MTeamConfig(x_api_key)
m_team = MTeam(config)

@app.route('/rss')
def get_mteam_acrive_top_rss():
    param = Param()
    success, desc, code = param.parse(request)
    if(not success):
        abort(code, description=desc)
    rss_str = m_team.generate_rss(param)
    response = make_response(rss_str)
    response.headers['Content-Type'] = "text/xml;charset=UTF-8"
    response.content_encoding
    return response


@app.errorhandler(400)
def handle_400_error(error):
    response = jsonify({"error": error.description})
    response.status_code = 400
    return response

@app.errorhandler(500)
def handle_500_error(error):
    response = jsonify({"error": error.description})
    response.status_code = 500
    return response

if __name__ == '__main__':
   app.config['JSON_AS_ASCII'] = False
   app.run()