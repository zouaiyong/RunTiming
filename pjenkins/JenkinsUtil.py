import socket
import jenkins
import os
from utils.FileUtil import FileUtil
from utils.ConfigParserUtils import ConfigParserUtils


class JenkinsUtil():
    def __init__(self):
        config = ConfigParserUtils()
        self.jenkins_url = config.get_config_value_by_key(
            'jenkins_config',

            'jenkins_url')
        self.username = config.get_config_value_by_key(
            'jenkins_config',

            'user_name')
        self.password = config.get_config_value_by_key(
            'jenkins_config', 'password')
        self.server = jenkins.Jenkins(self.jenkins_url,
                                      username=self.username,
                                      password=self.password)
        print('jenkins_url=%s username=%s password=%s' %
              (self.jenkins_url, self.username, self.password))

    def getjob_fullname_byview(self, view_name):
        '''
        返回某个视图下的所有job  fullname名字（JOB__NAME）
        :param view_name:
        :return:返回某个视图下的所有job名字
        '''
        url = self.jenkins_url + '/view/' + view_name
        server = jenkins.Jenkins(url,
                                 username=self.username,
                                 password=self.password)
        joblists = server.get_jobs(view_name)
        jobfullnameList = []
        for job in joblists:
            jobfullnameList.append(job['fullname'])
        return jobfullnameList

    def getjob_name_byview(self, view_name):
        '''
        返回某个视图下的所有job JOB_BASE_NAME
        :param view_name:
        :return:返回某个视图下的所有job名字
        '''
        url = self.jenkins_url + '/view/' + view_name
        server = jenkins.Jenkins(url,
                                 username=self.username,
                                 password=self.password)
        joblists = server.get_jobs(view_name)
        jobnameList = []
        for job in joblists:
            jobnameList.append(job['name'])
        return jobnameList

    def create_job(self, name, config):
        self.server.create_job(name, config)

    def job_save_config_byview(self, view_name):
        '''
        传入视视图字，返回该视图下所有的job的配置信息 （不包括文件夹类型）
        :param view_name:
        :return:
        '''

        jobnameList = self.getjob_fullname_byview(view_name)
        for job in jobnameList:
            f = FileUtil()
            filepath = 'JobConfig' + os.sep + job + ".xml"
            filecontent = self.server.get_job_config(job)
            f.create_file(filepath, filecontent)

    def createjob(self, jobname, config_file_path):
        f = FileUtil()
        config_xml = f.read_file(config_file_path)
        self.server.create_job(jobname, config_xml)
    def deleteJob(self,jobName):
        self.server.delete_job(jobName)

    def create_view(self, view_name):
        f = FileUtil()
        conig_xml = f.read_file("ConfigXML\\viewtemplate.xml")
        self.server.create_view(view_name, conig_xml)

    def batchCreateJob(self):
        self.createjob("template_deploy", "ConfigXML\\folder_job_config.xml")

    def stop_all_BuildNumber(self, jobName):
        '''

        :param jobName: 需要停止的job名字 ``str``
        '''
        server = jenkins.Jenkins(self.jenkins_url,
                                 username=self.username,
                                 password=self.password)
        listBuilds = server.get_job_info(jobName)['builds']
        if listBuilds is None:
            print('no builds')
        else:
            for build in listBuilds:
                print('stop number %s' % build['number'])
                self.stopJob(jobName, build['number'])

    def get_nodeStatus(self, nodeName):
        info = self.server.get_node_info(nodeName)
        if not info['offline']:
            return True
        else:
            return False

    def get_LastBuildNumber(self, jobName):
        '''

        :param jobName: job名字 ``str``
        :return:
        '''

        return self.server.get_job_info(jobName)['lastBuild']['number']

    def buildAJob(self, jobName, parameters, token):
        '''

        :param jobName: job名字 'str'
        :param parameters:  当前任务需要传入的参数 ``dict``
        :param token: 远程请求时job配置的token  ``str``

        '''

        if self.server.job_exists(jobName):
            self.server.build_job(
                name=jobName, parameters=parameters, token=token)
            print('job %s build success' % jobName)
        else:
            print('job %s is not exists build fail' % jobName)
    def isJob_exists(self,jobName):
        return self.server.job_exists(jobName)
    def stopJob(self, jobName, buildNumber):
        '''

        :param jobName:  job名字
        :param buildNumber:  需要停止的任务buildID

        '''

        if self.server.job_exists(jobName):
            self.server.stop_build(name=jobName, number=buildNumber)
        else:
            print("job %s is not exists" % jobName)

    def disable_job(self, jobName):
        if self.server.job_exists(jobName):
            self.server.disable_job(jobName)
        else:
            print("job %s is not exists" % jobName)

    def enable_job(self, jobName):
        self.server.enable_job(jobName)

    def rechangejob_config(self, name, configstr):
        if self.server.job_exists(name):
            self.server.reconfig_job(name, configstr)
        else:
            self.create_job(name,configstr)

    def cread_Launcher_SSH_Node(self,
                                nodeName,
                                numExecutors,
                                nodeDescription,
                                remoteFS,
                                labels,
                                exclusive,
                                launcher_params):
        '''

        :param nodeName:  节点名字
        :param numExecutors:  节点可并发数
        :param nodeDescription:  节点描述
        :param remoteFS:  工作目录
        :param labels:  标签
        :param exclusive:  Use this node for tied jobs only, ``bool``
        :param launcher_params: 启动参数 ``dict``

        '''

        if self.server.node_exists(nodeName):
            print("node is exist")
        else:
            self.server.create_node(
                nodeName,
                numExecutors=numExecutors,
                nodeDescription=nodeDescription,
                remoteFS=remoteFS,
                labels=labels,
                exclusive=exclusive,
                launcher=jenkins.LAUNCHER_SSH,
                launcher_params=launcher_params)

    def isNodeexists(self, nodeName):
        if self.server.node_exists(nodeName):
            print("node is exist")
            return True
        else:
            print("node is not exist")
            return False

    def enableNode(self, name):
        self.server.enable_node(name)

    def isJobRunning(self, jobName):
        builds = self.server.get_running_builds()
        print(builds)
        if jobName in str(builds):
            print(jobName, "is running")
            return True
        else:
            print(jobName, "is not running")
            return False

    def isJobNodeRunning(self, jobName, node):
        builds = self.server.get_running_builds()
        print(builds)
        if jobName in str(builds)and node in str(builds):
            print(node, "is running")
            return True
        else:
            print(node, "is not running")
            return False

    @classmethod
    def get_host_ip(cls):
        """
        查询本机ip地址
        :return: ip
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip


if __name__ == '__main__':
    jenkinsUtil = JenkinsUtil()
    jenkinsUtil.isJobNodeRunning("WebUiTest", '10.100.99.8')
    parameters = {
        "parameter": [
            {
                "name": "platform", "value": "Android"}, {
                "name": "isupdate", "value": "false"}, {
                    "name": "isautotest", "value": "true"}, {
                        "name": "testcase", "value": [
                            "case1", "case2", "case3", "case4", "case5", "case6", "case7"]}]}
    #parameters={'platform':'Android','isupdate':'true','isautotest':'true','testcase':'case1 case2 case3'}
    jenkinsUtil.buildAJob(
        'testproject',
        parameters=parameters,
        token="ATest")
    # jenkinsUtil.buildAJob(
    #     'AppUITest',
    #     parameters='case_1000',
    #     token='token1234')
