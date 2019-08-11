from __future__ import absolute_import
from FreshShop.celery import app #在成功安装celery之后，django新生成的模块

@app.task
def taskExample():
   print('send email ok!')

@app.task
def add(x=1, y=2):
   return x+y

