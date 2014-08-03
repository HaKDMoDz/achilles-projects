#!/usr/bin/python

import urllib,urllib2,re
import xbmc,xbmcplugin,xbmcgui,sys

def GET_HTTP(url):
  req = urllib2.Request(url)
  req.add_header('User-Agent','Mozilla/5.0 (Windows NT 5.1; rv:8.0) Gecko/20100101 Firefox/8.0')
  response = urllib2.urlopen(req)
  html=response.read()
  response.close()
  return html

def LIST_CHANNELS():
  home = 'http://www.mekongtv.net/channels/'
  chans = 'http://www.mekongtv.net/channels/tvk'
  html = GET_HTTP(chans)
  matchchans = re.compile('<a id="ctl00_cphMain_gvChannels_.+?_linkLogo" class="panel2" href="(.+?)"><img id="ctl00_cphMain_gvChannels_.+?_imgLogo" src="(.+?)" alt="(.+?)" style="border-width:0px;" /></a>').findall(html)

  for link,image,name in matchchans:
    chan_url = home + link
    chan_img = home + image
    addDownLink(name,chan_url,1,chan_img)

def STREAMLINK(url,name):
  home = 'http://www.mekongtv.net'
  html = GET_HTTP(url)
  match=re.compile('param name="InitParams" value="ch=.+?,m=(.+?)">').findall(html)
  asx_url = match[0]

  if 'playlists/-' in asx_url:
    print "Channel: " + name + " is not available in your area."
  else:
    asxhtml = GET_HTTP(asx_url)
    mmsmatch=re.compile('<ref href="(.+?)"').findall(asxhtml)
    asx = mmsmatch[0]
    listitem = xbmcgui.ListItem(name)
    listitem.setInfo('video', {'Title': name})
    xbmc.Player( xbmc.PLAYER_CORE_DVDPLAYER ).play(asx, listitem)

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

#print 'Mode: ' + str(mode)
#print 'URL : ' + str(url)
#print 'Name: ' + str(name)

if mode==None or url==None or len(url)<1:
  LIST_CHANNELS()
elif mode==1:
  STREAMLINK(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
