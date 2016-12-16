import logging
from jenkins_utils import *

logger = logging.getLogger(__name__)


def update_jenkins_job(server_ip='localhost', user='admin', 
                   password='pass', new_data=None, old_data=None):
    
    server = JenkinsUtils(server=server_ip, user=user, password=password)

    if 'TOPO_NAME' not in new_data:
       new_data['TOPO_NAME'] = old_data['TOPO_NAME']

    if not server.connected:
       logger.error("couldn't log into jenkins" + server_ip)
       return (False, "couldn't log into jenkins:"+server_ip)

    if not server.check_node_present(new_data['node']):
       node = server.add_node(new_data['node'])        
       if not node:
          msg = "couldn't add node:" + new_data['node']
          logger.error(msg)
          return (False, msg) 
       msg = 'added node:' + new_data['node']
       logger.info(msg)


    if not server.check_job_present(new_data['TOPO_NAME']):
       state = server.add_job(new_data)
       msg = 'added new job:' + new_data['TOPO_NAME']
       if not state:
          msg = "couldn't add new job:" + new_data['TOPO_NAME']
    else:
       state = server.update_job(new_data, old_data)
       msg = 'edited job:' + new_data['TOPO_NAME']
       if not state:
          msg = "couldn't edit job:" + new_data['TOPO_NAME']
      
    if not state:
       logger.error(msg)
       return (False, msg)
    else:
       logger.info(msg)

    return (True, 'successfully updated:'+server_ip+'with:'+ str(new_data))


def delete_jenkins_job(server_ip='localhost', user='admin', password='pass', job=None):
    server = JenkinsUtils(server=server_ip, user=user, password=password)
    if not server.delete_job(job):
       msg = "couldn't delete job:" + job
       logger.error(msg)
       return (False, msg)
    msg = 'deleted job:' + job 
    logger.info(msg)
    return (True, msg)
    
    
