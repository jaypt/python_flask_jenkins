from flask import Flask
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(format='%(asctime)s||%(levelname)-8s||%(message)s||%(name)s',
                            filename='/tmp/flask.log',
                            filemode='w',
                            )


JENKINS = 'localhost'
JENKINS_PATH = 'http://'+ JENKINS + ':8080/job/'
JENKINS_PARAMS = ['TOPO_NAME', 'TRIGGER_TYPE']
JENKINS_PARAMS_FILE = 'myapp/jenkins/jenkins_params.yml'
JENKINS_TIME = 'H(0-59) H(22-23) * * *'
JENKINS_CMD = 'run_test.sh'
YAML_PATH =  'myapp/setups/'
TRIGGER_TYPES = ['trigger1', 'trigger2']
STATUS = ['enable', 'disable']


app = Flask(__name__)
app.secret_key = 'so many random stuff'
from myapp import views
