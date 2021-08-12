import tornado.ioloop
import tornado.web
import os
from os import listdir
from os.path import join
import json
import math
import sys

import config
import project_manage

no_cache_headers = {
    'Cache-Control': ('no-store, no-cache, must-revalidate, '
                      'post-check=0, pre-check=0, max-age=0'),
    'Pragma': 'no-cache',
    'Expires': '-1',
}

def make_app():

    route = [
        (r"/images/(.*)", tornado.web.StaticFileHandler, {'path': './vp/image'}),
        (r"/audio/(.*)", tornado.web.StaticFileHandler, {'path': './vp/audio'}),
        (r"/favicon.ico", tornado.web.StaticFileHandler),

        (r"/", chooseProjectHandler),
        (r"/project/(?P<odm_name>.*)", projectHandler),
        (r"/rc/(?P<p_id>.*)", rcHandler),
        (r"/da/vp/py/(?P<vp_file_name>.*)", daHandler),
        (r"/delete_project/(?P<p_id>.*)/(?P<mac_addr>.*)", deleteProjectHandler),
    ]

    settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    
    return tornado.web.Application(route, **settings)

'''
class choose_vp_handler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
    def post(self):
        self.write("hhhhh")
    def delete():
        self.write("hhhhh")
    def put():
        self.write("hhhhh")
    def option():
        self.write("hhhhh")
'''

class chooseProjectHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main_page.html", vp_list=vp_list)

class projectHandler(tornado.web.RequestHandler):
    def get(self, **kwargs):
        print(kwargs)
        odm_name = kwargs.get('odm_name')
        if odm_name in vp_list:
            cur_p_id = project_manage.create_project_handler(odm_name)
            project_info = project_manage.project_set[cur_p_id]
            self.render("da/vp_index.html", p_id=cur_p_id, odm_name=odm_name, odo_id=project_info['output_device_info']['do_id'])
        else:
            self.redirect('/')

class rcHandler(tornado.web.RequestHandler):
    def get(self, **kwargs):
        p_id = kwargs.get('p_id')
        if int(p_id) in project_manage.project_set:
            project_info = project_manage.project_set[int(p_id)]
            odm_name = project_info['output_device_info']['dm_name']
            odm_id = project_info['output_device_info']['dm_id']
            in_do_id = project_info['input_device_info']['do_id']
            idf_list = []
            idf_para_list = []
            odf_list = []
            for df in project_info['input_device_info']['df_list']:
                para = []
                for parameter in df['parameter']:
                    para.append([parameter[1],parameter[2],(parameter[1]+parameter[2])/2])
                idf_list.append(df['name'])
                idf_para_list.append(para)
            for df in project_info['output_device_info']['df_list']:
                odf_list.append(df['name'])
            for key, val in no_cache_headers.items():
                self.set_header(key, val)
            print('idf_list', idf_list)
            self.render("da/mobile_rc.html", odm_name=odm_name, p_id=p_id, in_do_id=in_do_id, idf_list=idf_list, odf_list=odf_list, idf_para_list=idf_para_list)
        else:
            self.write("Please rescan QRCode.")

class daHandler(tornado.web.RequestHandler):
    def get(self, **kwargs):
        vp_file_name = kwargs.get('vp_file_name')
        
        for key, val in no_cache_headers.items():
            self.set_header(key, val)

        f = open(os.path.join(os.getcwd(), "vp/py/"+vp_file_name), "r")
        self.write(f.read())

class deleteProjectHandler(tornado.web.RequestHandler):
    def delete(self, **kwargs):
        p_id = kwargs.get('p_id')
        mac_addr = kwargs.get('mac_addr')
        project_manage.delete_project_handler(p_id, mac_addr)
        self.write('ok')

if __name__ == "__main__":
    app = make_app()
    app.listen(config.port)
    print("======== server start ========")
    global vp_list
    print('working directory:',os.getcwd())
    vp_file_list = listdir(join(os.getcwd(), 'vp/py'))
    vp_list = list(map(lambda x: x[:-3],filter(lambda x: x != 'Ball-collision.py' and x != 'Ball-Slide.py' and x != 'Ball-Spring.py' 
        and x != 'Ball-Throw.py' and x != 'Snakepend2.py',vp_file_list)))
    vp_list.sort()
    print('vp_list:',vp_list)
    tornado.ioloop.IOLoop.current().start()
