
import glob
import yaml
import logging
import os
from collections import defaultdict

from myapp import app, JENKINS_PATH, YAML_PATH, logger


logger = logging.getLogger(__name__)

def dict_values_convert(var, f=str):
    return { k: f(v) for k, v in var.iteritems()}

class SetupDatabase(object):
   
     def get_setup(self, files=None):
         info = []
         if files:
            files = [YAML_PATH+files]
         else:
            files = glob.glob(YAML_PATH+'*.yml')
         for file in files:
             with open(file, 'r') as f:
                 setup = yaml.load(f)
                 info.append(setup)    
         return info

     def add_setup(self, setup):
         filename = setup['TOPO_NAME']
         with open(YAML_PATH+filename+'.yml', 'w') as f:
             yaml.dump(dict_values_convert(setup), f, default_flow_style=False)

     def del_setup(self, setup):
         filename = YAML_PATH+ setup + '.yml'
         if os.path.exists(filename):
            os.remove(filename)


class DatabaseInterface(SetupDatabase):

      def get_all(self):
          logger.debug('reading all yml info')
          data = super(DatabaseInterface, self).get_setup() 
          return data

      def get_setup(self, setup):
          setup = str(setup) + '.yml'
          logger.debug('reading all yml info for' + setup)
          data = super(DatabaseInterface, self).get_setup(setup)
          return data


      def add(self, setup):
          logger.info('writing yml info for setup'+ setup['TOPO_NAME'])
          super(DatabaseInterface, self).add_setup(setup)

      def delete(self, setup):
          logger.info('deleting yml info for setup')
          super(DatabaseInterface, self).del_setup(setup)

      def update(self, setup, newinfo):
          currentinfo = self.get_setup(setup)[0]
          updateinfo = {}
          if currentinfo:
             updateinfo =  defaultdict(**currentinfo)
          updateinfo.update(newinfo)
          self.add(updateinfo)
          
          
          
 
