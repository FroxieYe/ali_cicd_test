import json
import os
import requests
import tornado.auth
import tornado.ioloop
import tornado.options
import tornado.web
import urllib.parse
from tornado.options import define, options

define("port", default=8889, help="run on the given port", type=int)

settings = {
    'debug':True,
}

class AuthHandler(tornado.web.RequestHandler):
    def get(self):
        code = self.get_argument("code", False)
        if not code:
            return
        self._get_session_key(code)

    def _get_session_key(self, code):
        args = {
            "appid": "wx3924b6c24f183c70",
            "secret": "00762f90a9d808299575bea6c9a0205f",
            "js_code": code,
            "grant_type": "authorization_code"
        }
        response = requests.get(
            "https://api.weixin.qq.com/sns/jscode2session?" +
            urllib.parse.urlencode(args))
        print(response.json())
        self.write(
            response.json()
        )

class FroxieHandler(tornado.web.RequestHandler):
    def get(self):
        code = self.get_argument("code", False)
        if not code:
            self.write("Froxie is playing with k8s.")
            return
        else:
            self._get_access_token(code)

    def _get_access_token(self, code):
        idaas_server = "bhgmgfdhwe.api.aliyunidaas.com"
        client_id = "be1b4c9ec86f16e4b2d12c71423e13c7Ns4B7T94BYr"
        client_secret = "gQ0GmHvGhlNecIWpAYpSoTgoq0jw749vkW0tuQ5glX"
        grant_type = "authorization_code"

        args = {
            "grant_type": grant_type,
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": "http://121.41.75.12:8889"
        }

        response = requests.get(
            f"https://{idaas_server}/oauth/token?",
            urllib.parse.urlencode(args))
        print(response.json())
        

def make_app():
    print('Preparing data')
    return tornado.web.Application([
        (r"/auth", AuthHandler),
        (r"/", FroxieHandler),
    ], **settings)


def run_server():
    tornado.options.parse_command_line()
    app = make_app()
    print('Server starting on {}'.format(options.port))
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    run_server()
