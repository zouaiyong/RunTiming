# -*- coding: utf-8 -*-
# @Time    : 2018/11/12 11:11
# @Author  : zouay
# @Email   : zouaiyong@tuandai.com
# @File    : runTiming.py
# @Software: PyCharm
import argparse
import json

from flask import Flask, request

from pjenkins.timeTask import TimingTask

app = Flask(__name__)
timeTask=TimingTask()
@app.route('/timing_task',methods=['POST'])
def timeingTask():
    data=request.get_data().decode()
    params = json.loads(data)
    print('params=',params)
    is_run=params.get('is_run')
    task_id=params.get('time_id')
    if is_run!=1:
        msg=timeTask.stopTimingTask(task_id)
        return json.dumps(msg,ensure_ascii=False)
    else:
        msg=timeTask.startTimingTask(task_id,params)
        return json.dumps(msg,ensure_ascii=False)
@app.route('/timing_task/<path:id>',methods=['GET','POST'])
def timingTaskParams(id):
    method=request.method
    if method=='GET' and str(id).lower()=='delete':
        params=request.values.to_dict()
        jobName=params.get('jobName')
        msg=timeTask.deleteTimingTask(jobName)
        return json.dumps(msg, ensure_ascii=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=7802)
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=args.port,debug=True)

