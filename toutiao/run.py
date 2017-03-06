from ToutiaoHotFeedPool import ToutiaoHotFeedPool
import sys, traceback, time

feedPool = ToutiaoHotFeedPool('http://www.toutiao.com/api/pc/feed/?category=news_hot&utm_source=toutiao&widen=1&max_behot_time=%d&max_behot_time_tmp=%d&tadrequire=true&as=A1C5187BD39FA36&cp=58B37F9A23369E1')

dest = sys.argv[1]
pages = int(sys.argv[2])
cnt = 0

for i in xrange(0, pages):
  feeds = feedPool.getSome()
  for feed in feeds:
    if not feed['valid']:
      continue
    article = None
    try:
      date = time.strftime("%Y-%m-%d", time.localtime())
      article = file('%s/toutiao_hot.%s.%d.txt' %(dest, date, cnt), 'w')
      one = '<title>%s<title>\n%s' % (feed['title'], feed['content'])
      article.write(one.encode('utf-8'))
      cnt = cnt+1
    except:
      traceback.print_exc()
    finally:
      if article:
        article.close()
