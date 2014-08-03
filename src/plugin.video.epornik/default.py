import urllib,urllib2,re,os,sys
import xbmc,xbmcplugin,xbmcgui,xbmcaddon
import HTMLParser

homepage = 'http://www.epornik.com'

__settings__ = xbmcaddon.Addon(id='plugin.video.epornik')
home = __settings__.getAddonInfo('path')
imagedir = xbmc.translatePath( os.path.join( home, 'images' ) )

def GET_HTML(url):
  req = urllib2.Request(url)
  req.add_header('User-Agent','Mozilla/5.0 (Windows NT 5.1; rv:18.0) Gecko/20100101 Firefox/18.0')
  response = urllib2.urlopen(req)
  html=response.read()
  response.close()
  return html

def HOME():
  addDir('  New Videos',homepage +'/pornos/1/newest/alltime/all/',2,'')
  addDir('  Most Watched',homepage +'/porn/most-watched',2,'')
  addDir('  Top-Rated',homepage +'/porn/top-rated',2,'')
  addDir('-Categories-','',0,'')
  LIST_SECTIONS(homepage)

def LIST_SECTIONS(url):
  html = GET_HTML(url)
  match=re.compile('<li class="list-group-item">.+?<span class="badge">(.+?)</span>.+?<a href="(.+?)">(.+?)</a>', re.DOTALL | re.MULTILINE).findall(html)
  for num,url,title in match:
    url = homepage + url
    title = title + ' (' + num + ')'
    addDir(title,url,2,'')

def LIST_ITEMS(url):
  html = GET_HTML(url)
  match=re.compile('<div class="item">.+?<img data-thumb=.+?src="(.+?)".+?<span class="duration">(.+?)</span>.+?<div class="videoTitle">.+?<a href="(.+?)">(.+?)</a>', re.DOTALL | re.MULTILINE).findall(html)
  next=re.compile("<li><a href='(.+?)'>Next").findall(html)

  for img,time,part_url,title in match:
    url = homepage + part_url
    time = '  (' + time + ')'
    addDownLink(title + time,url,3,img)

  for next_page in next:
    url = homepage + next_page
    thumb = xbmc.translatePath( os.path.join( imagedir, "next.png") )
    addDir('--> Next Page',url,2,thumb)

def VIDEOLINKS(url,title):
  html = GET_HTML(url)
  stream=re.compile('file: "(.+?)",').findall(html)
  for link in stream:
    print 'Link: ' + str(link)
    listitem = xbmcgui.ListItem(title)
    listitem.setInfo(type="video", infoLabels={ "Title": title } )
    xbmc.Player( xbmc.PLAYER_CORE_DVDPLAYER ).play(link, listitem)

def get_params():
  param=[]
  paramstring=sys.argv[2]
  if len(paramstring)>=2:
    params=sys.argv[2]
    cleanedparams=params.replace('?','')
    if (params[len(params)-1]=='/'):
      params=params[0:len(params)-2]
    pairsofparams=cleanedparams.split('&')
    param={}
    for i in range(len(pairsofparams)):
      splitparams={}
      splitparams=pairsofparams[i].split('=')
      if (len(splitparams))==2:
        param[splitparams[0]]=splitparams[1]
  return param

def addDir(name,url,mode,iconimage):
  u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
  ok=True
  liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png",thumbnailImage=iconimage)
  liz.setInfo( type="Video", infoLabels={ "Title": name })
  ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
  return ok

def addDownLink(name,url,mode,iconimage):
  u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
  ok=True
  liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
  liz.setInfo( type="Video", infoLabels={ "Title": name } )
  ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
  return ok

params=get_params()
url=None
name=None
mode=None

try:
  url=urllib.unquote_plus(params["url"])
except:
  pass
try:
  name=urllib.unquote_plus(params["name"])
except:
  pass
try:
  mode=int(params["mode"])
except:
  pass

print 'Mode: ' + str(mode)
print 'URL : ' + str(url)
print 'Name: ' + str(name)

if mode==None or url==None or len(url)<1:
  HOME()
elif mode==1:
  LIST_SECTIONS(url)
elif mode==2:
  LIST_ITEMS(url)
elif mode==3:
  VIDEOLINKS(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
