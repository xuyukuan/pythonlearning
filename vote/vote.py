# -*- coding: utf-8 -*-
import requests
import random
import time
import string
import threading

def _vote(id, openid, ip):
  url = 'http://XXX.submit.php' //匿了
  votes = {}
  payload = {'id': id, 'openid': openid, 'votes': votes}
  headers = {'x-forwarded-for': ip}
  r = requests.post(url, data=payload, headers=headers)
  return r

def pickOne(start, end):
  return random.choice(range(start, end))

def randomIP(ipdb):
  size = len(ipdb)
  area = ipdb[pickOne(0, size)]
  ip1 = area[0].split('.')
  ip2 = area[1].split('.')
  ip = []
  for i in range(4):
    if ip1[i] is ip2[i]:
      ip.append(ip1[i])
    else:
      n1 = int(ip1[i])
      n2 = int(ip2[i]) + 1
      if n2 <= n1:
        n2 = 256
      ip.append(str(pickOne(n1, n2)))
  return '.'.join(ip)

def randomOpenId():
  raw = '_' + ''.join(map(lambda x:str(x), range(10))) + string.ascii_lowercase + string.ascii_uppercase
  list = []
  for i in range(28):
    list.append(raw[pickOne(0,len(raw))])
  return ''.join(list)

def vote(ipdb, run_event):
  id = '202079'
  count = 0
  while run_event.is_set():
    openid = randomOpenId()
    ip = randomIP(ipdb)
    r = _vote(id, openid, ip)
    if r.text.strip() == '1':
      count += 1
      print('投票成功！' + str(count))
    else:
      print(r.text)
    time.sleep(.5)

def initIpData():
  ipdb = []
  for line in open('./jsip.txt'):
    arr = filter(None, line.rstrip().split(' '))
    ipdb.append(arr)
  return ipdb

class myThread (threading.Thread):   #继承父类threading.Thread
  def __init__(self, threadID, name, ipdb, run_event):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.name = name
    self.ipdb = ipdb
    self.run_event = run_event
  def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
    print "Starting " + self.name
    vote(self.ipdb, self.run_event)
    print "Exiting " + self.name

if __name__ == '__main__':
  # vote()
  run_event = threading.Event()
  run_event.set()
  ipdb = initIpData()
  threads = []
  for i in range(50):
    t = myThread(i, 'Thread-' + str(i), ipdb, run_event)
    threads.append(t)
    t.start()
  try:
    while 1:
      time.sleep(.1)
  except KeyboardInterrupt:
    print "attempting to close threads."
    run_event.clear()
    for t in threads:
      t.join()
    print "threads successfully closed"
