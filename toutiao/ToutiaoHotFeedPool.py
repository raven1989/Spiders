# -*- coding:utf-8 -*-
import sys,time,traceback,json
import urllib
import urllib2, cookielib
import re

class ToutiaoHotFeedPool:
  def __init__(self, url):
    self.urlTemplate_ = url
    self.cookie_ = cookielib.CookieJar()
    self.headers_ = {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
        }
    self.opener_ = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie_))
    self.next_ = 0
  
  def getSome(self):
    try:
      request = urllib2.Request(self.urlTemplate_ % (self.next_, self.next_), headers = self.headers_)
      response = self.opener_.open(request).read().decode('utf-8')
      feeds = self.getFeedListFromJson(response)
      # print len(feeds)
      for i in xrange(0, len(feeds)):
        self.getFeedArticle(feeds, i)
        log = '%s %s %s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), feeds[i]['title'], feeds[i]['url'])
        print log.encode('utf-8')
        time.sleep(2)
      return feeds
    except:
      traceback.print_exc()

  def getFeedListFromJson(self, jstr):
    jata = json.loads(jstr)
    self.next_ = jata['next']['max_behot_time']
    # print jata['data'] 
    feeds = []
    for jeed in jata['data']:
      # print type(jeed)
      # print jeed['article_genre']
      if jeed['is_feed_ad'] :
        continue
      else:
        # article类型
        if jeed['article_genre'].find('article')>=0:
          one = {
            'title':jeed['title'], 
            'url':'http://www.toutiao.com/a%s' % jeed['group_id'],
          }
          # print one
          feeds.append(one)
    return feeds

  def getFeedArticle(self, feeds, i):
    try:
      url = feeds[i]['url']
      request = urllib2.Request(url, headers = self.headers_)
      response = self.opener_.open(request).read().decode('utf-8')
      content = self.getArticleFromHtml(response)
      feeds[i]['content'] = content
      if content == '':
        feeds[i]['valid'] = False
      else:
        feeds[i]['valid'] = True
    except:
      traceback.print_exc()

  def getArticleFromHtml(self, html):
    try:
      pattern = re.compile('<div class="article-content">(.*?)</div>\s*<div class.*?>', re.S)
      matches = re.findall(pattern, html)
      return matches[0]
    except:
      traceback.print_exc()
    return ''

if __name__=='__main__':
  feedPool = ToutiaoHotFeedPool('http://www.toutiao.com/api/pc/feed/?category=news_hot&utm_source=toutiao&widen=1&max_behot_time=%d&max_behot_time_tmp=%d&tadrequire=true&as=A1C5187BD39FA36&cp=58B37F9A23369E1')
  feeds = feedPool.getSome()
  print len(feeds)
  for feed in feeds:
    print feed['title'], feed['url'], feed['content']

