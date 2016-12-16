HEADER='''<?xml version='1.0' encoding='UTF-8'?>
<project>
  <actions/>
  <description></description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <hudson.model.ParametersDefinitionProperty>
      <parameterDefinitions>
'''

STR_PARAMS='''
        <hudson.model.StringParameterDefinition>
          <name>{0}</name>
          <description></description>
          <defaultValue>{1}</defaultValue>
        </hudson.model.StringParameterDefinition>
'''

SLAVE_PARAMS='''
        <org.jvnet.jenkins.plugins.nodelabelparameter.NodeParameterDefinition plugin="nodelabelparameter@1.7.2">
          <name></name>
          <description></description>
          <allowedSlaves>
            <string>{0}</string>
          </allowedSlaves>
          <defaultSlaves>
            <string>{0}</string>
          </defaultSlaves>
          <triggerIfResult>multiSelectionDisallowed</triggerIfResult>
          <allowMultiNodeSelection>false</allowMultiNodeSelection>
          <triggerConcurrentBuilds>false</triggerConcurrentBuilds>
          <ignoreOfflineNodes>false</ignoreOfflineNodes>
          <nodeEligibility class="org.jvnet.jenkins.plugins.nodelabelparameter.node.AllNodeEligibility"/>
        </org.jvnet.jenkins.plugins.nodelabelparameter.NodeParameterDefinition>
'''

BODY_1='''
      </parameterDefinitions>
    </hudson.model.ParametersDefinitionProperty>
  </properties>
  <scm class="hudson.scm.NullSCM"/>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
'''

TRIGGERS='''
  <triggers>
    <hudson.triggers.TimerTrigger>
      <spec>{0}</spec>
    </hudson.triggers.TimerTrigger>
  </triggers>
  <concurrentBuild>false</concurrentBuild>
'''

CMD='''
  <builders>
    <hudson.tasks.Shell>
      <command>{0}</command>
    </hudson.tasks.Shell>
  </builders>
  <publishers/>
'''

EMAIL='''
  <publishers>
    <hudson.tasks.Mailer plugin="mailer@1.18">
      <recipients>{0}</recipients>
      <dontNotifyEveryUnstableBuild>false</dontNotifyEveryUnstableBuild>
      <sendToIndividuals>false</sendToIndividuals>
    </hudson.tasks.Mailer>
  </publishers>
  <buildWrappers/>
</project>
'''

def get_job_xml(data, params, time, cmd):
    xml = HEADER
    for param in params:
        xml += STR_PARAMS.format(param, data[param])

    xml += SLAVE_PARAMS.format(data['node'])
    xml += BODY_1
    xml += TRIGGERS.format(time)
    xml += CMD.format(cmd)
    xml += EMAIL.format(data['email'])
    return xml
