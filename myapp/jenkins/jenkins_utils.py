import jenkins
import logging
import yaml
from myapp import  JENKINS_PARAMS, JENKINS_PARAMS_FILE, JENKINS_TIME, JENKINS_CMD
from jenkins_xml import *
import sys


logger = logging.getLogger(__name__)

class JenkinsUtils(object):
      def __init__(self, server='1.1.1.1', user='admin', password='pass'):
          server_url = 'http://'+server+':8080'
          self.connected = False
          try:
             self.server = jenkins.Jenkins(server_url, username=user, password=password)
             whoami = self.server.get_whoami()
             self.connected = True
             logger.info('logged into server:'+ server_url + ' as:' + str(whoami))
          except:  
             logger.error("couldn't log into jenkins" +  server_url)

      
      def check_node_present(self, node):
          nodes = self.server.get_nodes()
          if filter(lambda x: x['name'] == node, nodes):
             return True
          return False

      def add_node(self, node, **kwargs):
          with open(JENKINS_PARAMS_FILE, 'r') as f:
              def_val = yaml.load(f)
          launch_params=dict(host=node, port=def_val['port'], credentialsId=def_val['credentials'],
                             maxNumRetries=def_val['maxNumRetries'],
                             retryWaitTime=def_val['retryWaitTime'])
          self.server.create_node(node, numExecutors=def_val['numExecutors'],
                             nodeDescription=def_val['nodeDescription'],
                             remoteFS=def_val['remoteFS'],
                             labels=def_val['labels'], exclusive=def_val['exclusive'],
                             launcher=jenkins.LAUNCHER_SSH,
                             launcher_params=launch_params) 
          
          return self.check_node_present(node)

      def check_job_present(self, job):
          jobs = self.server.get_jobs()
          if filter(lambda x: x['name'] == job, jobs):
             return True
          return False

      def disable_enable_job(self, job, state='disable'):
          try:
            if state == 'disable':
               self.server.disable_job(job)
            else:
               self.server.enable_job(job)
            msg = job + ' status marked as:' + state + ' in jenkins'
            logger.info(msg)
            return True
          except:
            msg = 'ERROR' + job + ' status NOT marked as:' + state + ' in jenkins'
            logger.error(msg)
            return False
          

      def add_job(self, new_data):
          job_xml = get_job_xml(new_data, JENKINS_PARAMS, JENKINS_TIME, JENKINS_CMD)
          try:
             self.server.create_job(new_data['TOPO_NAME'], job_xml)
             msg = 'created job:' + new_data['TOPO_NAME'] + ' in jenkins'
             logger.info(msg)
             if not self.check_job_present(new_data['TOPO_NAME']):
                msg = 'though created, job %s not found on jenkins' % (new_data['TOPO_NAME'])
                logger.error(msg)
                return False
             if not self.disable_enable_job(new_data['TOPO_NAME'], new_data['status']):
                return False  
          except:
             print sys.exc_info()
             msg = "couldn't create job:" + new_data['TOPO_NAME'] + ' in jenkins'
             logger.error(msg)
             return False

          return True


      def update_job(self, new_data, old_data):
          job_xml = get_job_xml(new_data, JENKINS_PARAMS, JENKINS_TIME, JENKINS_CMD)
          try:
             self.server.reconfig_job(new_data['TOPO_NAME'], job_xml)
             msg = 'updated job:' + new_data['TOPO_NAME'] + ' in jenkins'
             logger.info(msg)
             if not self.disable_enable_job(new_data['TOPO_NAME'], new_data['status']):
                return False  
          except:
             msg = "couldn't update job:"+ new_data['TOPO_NAME'] + ' in jenkins'
             logger.error(msg)
             return False

          return True

      def delete_job(self, job):
          try:
            self.server.delete_job(job)
            msg = job + ' deleted'
            logger.info(msg)
            return True
          except:
            msg = 'ERROR' + job + ' NOT deleted in jenkins' 
            logger.error(msg)
            return False
