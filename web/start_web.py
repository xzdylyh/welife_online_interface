#coding=utf-8
from flask import Flask, render_template
import os

app = Flask(__name__)


@app.route('/report/<report_dir>/<report_name>')
def  report(report_dir, report_name):
    return render_template(r'/report/{}/{}'.format(report_dir, report_name))


@app.route('/')
@app.route('/report/')
def report_dir():
    all_list = []
    folder_list = []

    #report路径
    webpath = os.path.abspath(os.path.dirname("__file__"))
    templatesReportPath = os.path.join(webpath, 'templates')
    redir = os.path.join(templatesReportPath, 'report')

    #遍历路径,取文件夹名称和html文件存入list
    for root, subdirs, _ in os.walk(redir):
        for sdirs in subdirs:
            folder_list.append(sdirs)
            for subroot, dirs, files in os.walk(os.path.join(root,sdirs)):
                for fi in files:
                    folder_list.append(fi)
                all_list.append(folder_list)
            folder_list = []


    return render_template('directory.html', all_list = all_list)



if __name__ == "__main__":
    # app.debug = True
    app.run(host='172.17.240.230',port=5001)
    # app.run(host='172.17.240.230')