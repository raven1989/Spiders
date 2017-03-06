# -*- coding:utf-8 -*-
import sys, time, traceback
import urllib
import urllib2
import re

dest = sys.argv[1]
page = int(sys.argv[2])
url = 'http://www.qiushibaike.com/text/page/' + str(page)
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }
seq = 1
for i in xrange(0, page):
  try:
    request = urllib2.Request(url,headers = headers)
    response = urllib2.urlopen(request)
    content = response.read().decode('utf-8')
    # print content
    pattern = re.compile('<a href.*?"/article/\d+".*?"_blank".*?contentHerf.*?"content".*?<span>(.*?)</span>.*?</a>',re.S)
    items = re.findall(pattern,content)
    for item in items:
      content = '%s\n' % (item.replace('<br/>', '\n') )
      title = '%s : %s ...' % ('天天糗事:'.decode('utf-8'), content[0:16].strip().replace('\n', ''))
      date = time.strftime("%Y-%m-%d", time.localtime())
      log = '%s %s %d' %(date, title, seq)
      print log.encode('utf-8')
      one = None
      try:
        one = file('%s/qiushi.%s.%d.txt' % (dest, date, seq), 'w')
        article = '<title>%s<title>\n%s' % (title, content)
        one.write(article.encode('utf-8'))
        seq = seq+1
      except:
        traceback.print_exc()
        continue
      finally:
        if one:
          one.close()
    time.sleep(2)
  except:
    traceback.print_exc()
print '.......%d articles Done.......' % seq
