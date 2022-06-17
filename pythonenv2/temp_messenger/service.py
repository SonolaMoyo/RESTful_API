from nameko.rpc import rpc, RpcProxy
from nameko.web.handlers import http
import redis

from temp_messenger.dependencies.redis import Redis
from .dependencies.jinja2 import Jinja2
from werkzeug.wrappers import Response

# micro service
class MessageService:
    name = "message_service"
    redis = Redis()
    
    @rpc
    def get_message(self, message_id):
        return self.redis.get_message(message_id)
    
    @rpc
    def save_message(self, message):
        message_id = self.redis.save_message(message)
        return message_id
    
    @rpc
    def get_all_messages(self):
        messages = self.redis.get_all_messages()
        return messages
    
# http encryption
class webServer:
    name = 'webServer'
    message_service = RpcProxy('message_service')
    templates = Jinja2()
    
    @http('GET', '/')
    def home(self, request):
        messages= self.message_service.get_all_messages()
        rendered_template = self.templates.render_home(messages)
        html_response = create_html_response(rendered_template)
        return html_response


def create_html_response(content):
    headers = {'Content-Type': 'text/html'}
    return Response(content, headers=headers)