
# BiliBrowser
#
# Macast Metadata
# <macast.title>BiliBrowser</macast.title>
# <macast.renderer>BiliBrowserRenderer</macast.renderer>
# <macast.platform>darwin,linux,win32</macast.platform>
# <macast.version>0.2</macast.version>
# <macast.host_version>0.7</macast.host_version>
# <macast.author>Pasical</macast.author>
# <macast.desc>Open the stream source BV video in browser. Dependence on NVA Protocol</macast.desc>

import re
import time
import threading
import webbrowser
import subprocess
import sys
import cherrypy

from macast import gui, Setting
from macast.renderer import Renderer

class BiliBrowserRenderer(Renderer):
    # AV转BV常量
    XOR_CODE = 23442827791579
    MASK_CODE = 2251799813685247
    MAX_AID = 1 << 51
    ALPHABET = "FcwAPNKTMug3GV5Lj7EJnHpWsx4tb8haYeviqBz6rkCy12mUSDQX9RdoZf"
    ENCODE_MAP = (8, 7, 0, 5, 1, 3, 2, 4, 6)
    BASE = len(ALPHABET)
    PREFIX = "BV1"
    
    def __init__(self):
        super(BiliBrowserRenderer, self).__init__()
        self.start_position = 0
        self.position_thread_running = True
        self.position_thread = threading.Thread(target=self.position_tick, daemon=True)
        self.position_thread.start()
    
    def position_tick(self):
        while self.position_thread_running:
            time.sleep(1)
            self.start_position += 1
            sec = self.start_position
            position = '%d:%02d:%02d' % (sec // 3600, (sec % 3600) // 60, sec % 60)
            self.set_state_position(position)

    # 从NVA协议获取aid
    def get_video_info_from_nva(self, url=None):
        try:
            target_cid = None
            if url:
                match = re.search(r'upgcxcode/\d+/\d+/(\d+)', url)
                target_cid = match.group(1) if match else None
            
            protocols = cherrypy.engine.publish('get_protocol')
            if protocols and hasattr(protocols[0], 'clients'):
                for handler in protocols[0].clients.values():
                    if hasattr(handler, 'aid') and handler.aid:
                        if target_cid and hasattr(handler, 'cid') and str(handler.cid) == str(target_cid):
                            return handler.aid
                        elif not target_cid:
                            return handler.aid
        except:
            pass
        return None

    # AV号转BV号    
    def av2bv(self, aid):
        try:
            aid = int(aid)
            bvid = [""] * 9
            tmp = (self.MAX_AID | aid) ^ self.XOR_CODE
            for i in range(len(self.ENCODE_MAP)):
                bvid[self.ENCODE_MAP[i]] = self.ALPHABET[tmp % self.BASE]
                tmp //= self.BASE
            return self.PREFIX + "".join(bvid)
        except:
            return None

    # 在默认浏览器中打开URL    
    def open_browser(self, url):
        try:
            if sys.platform == 'darwin':
                subprocess.Popen(['open', url])
            elif sys.platform == 'win32':
                webbrowser.open(url)
            else:
                env = Setting.get_system_env()
                toDelete = []
                for (k, v) in env.items():
                    if k != 'PATH' and 'tmp' in v:
                        toDelete.append(k)
                for k in toDelete:
                    env.pop(k, None)
                subprocess.Popen(["xdg-open", url], env=env)
            return True
        except:
            return False
    
    def set_media_stop(self):
        self.set_state_transport('STOPPED')
        cherrypy.engine.publish('renderer_av_stop')
    
    def set_media_url(self, url, start=0):
        self.set_media_stop()
        self.start_position = 0
        
        aid = self.get_video_info_from_nva(url)
        if aid:
            bvid = self.av2bv(aid)
            video_url = f"https://www.bilibili.com/video/{bvid}" if bvid else f"https://www.bilibili.com/video/av{aid}"
            self.open_browser(video_url)
            self.set_state_transport("PLAYING")
            cherrypy.engine.publish('renderer_av_uri', video_url)
            return
        
        # 如果NVA协议无法获取信息，直接打开原始链接
        self.open_browser(url)
        self.set_state_transport("PLAYING")
        cherrypy.engine.publish('renderer_av_uri', url)
    
    def stop(self):
        super(BiliBrowserRenderer, self).stop()
        self.set_media_stop()
        self.position_thread_running = False


if __name__ == '__main__':
    gui(BiliBrowserRenderer())
