# -*- coding: utf-8 -*-
# @Time    : 2018/11/9 9:53
# @Author  : zouay
# @Email   : zouaiyong@tuandai.com
# @File    : timeTask.py
# @Software: PyCharm
import json
import os
import re

from pjenkins.JenkinsUtil import JenkinsUtil


class TimingTask():
    def __init__(self):
        path=os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))
        self.confPath=path+os.sep+'config'+os.sep+'config.xml'
        self.jekinsBean = JenkinsUtil()

    def changeconfig(self,config, params=None,name=None):
        regx = '<spec>(.*)</spec>'
        nameRegx='<description>定时任务</description>'
        timing_data=params.get('timing_data')
        timing_cycle=timing_data.get('timing_cycle')
        start_time=timing_data.get('start_time')
        print(json.dumps(params))
        timeReplace=''
        nameplace='<description>'+name+'</description>'
        if timing_cycle=='hour':
            time='*/'+start_time
            timeReplace = '<spec>' + 'H ' + time + " " + "* * *" + '</spec>'
        elif timing_cycle=='week':
            time=start_time
            timeReplace = '<spec>' +  "* * * * " +time+ '</spec>'
        elif timing_cycle=='day':
            time=start_time.split(':')
            timehour = time[0]
            timemin=time[1]
            timeReplace = '<spec>' + timemin +" "+timehour +" * * * "  + '</spec>'
        elif timing_cycle == 'minute':
            time = '*/'+start_time
            timeReplace = '<spec>' +time + " * * * *" + '</spec>'

        jsondataRegx= r'<defaultValue>{.*}</defaultValue>'
        jsondataReplase='<defaultValue>'+json.dumps(params)+'</defaultValue>'
        with open(config, 'r', encoding='utf-8') as f:
            configxml = f.read()
            if len(configxml) > 0:
                configxml=re.sub(re.compile(nameRegx), nameplace, configxml)
                configxml = re.sub(re.compile(regx), timeReplace, configxml)
                configxml=re.sub(re.compile(jsondataRegx),jsondataReplase,configxml)
        #print(configxml)
        return configxml
    def startTimingTask(self,jobName,params):
        try:
            config = self.changeconfig(self.confPath, params=params,name=jobName)
            #jekinsBean = JenkinsUtil()
            self.jekinsBean.rechangejob_config(jobName, config)
            self.jekinsBean.enable_job(jobName)
            return {'code': '200', 'data': '', 'message': '定时成功'}
        except Exception as e:
            return {'code': '202', 'data': str(e), 'message': 'jenkins异常'}

    def stopTimingTask(self,jobName):

        try:
            #jekinsBean = JenkinsUtil()
            self.jekinsBean.disable_job(jobName)
            return {'code': '200', 'data': '', 'message': '关闭成功'}
        except Exception as e:
            return {'code': '202', 'data': str(e), 'message': 'jenkins异常'}
    def deleteTimingTask(self,jobName):
        try:
            # jekinsBean = JenkinsUtil()
            if self.jekinsBean.isJob_exists(jobName):
                self.jekinsBean.deleteJob(jobName)
            else:
                return {'code': '202', 'data': '', 'message': '任务不存在'}
            return {'code': '200', 'data': '', 'message': '删除成功'}
        except Exception as e:
            return {'code': '202', 'data': str(e), 'message': 'jenkins异常'}

