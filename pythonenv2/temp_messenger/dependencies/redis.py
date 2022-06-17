from redis import StrictRedis
from nameko.extensions import DependencyProvider
from uuid import uuid4

import redis


class Redis(DependencyProvider):
    def setup(self):
        self.redis_url = self.container.config['REDIS_URL']
        self.client = RedisClient(self.redis_url)

    def stop(self):
        del self.client

    def get_dependency(self, worker_ctx):
        return self.client


class RedisClient:
    def __init__(self, url):
        self.redis = StrictRedis.from_url(url, decode_responses=True)

    def get_message(self, message_id):
        message = self.redis.get(message_id)

        if message is None:
            raise "Message not found {}".format(message_id)
        return message

    # save messages
    def save_message(self, message):
        message_id = uuid4().hex
        self.redis.set(message_id, message, ex=10)

        return message_id

    # get all message in redis
    def get_all_messages(self):
        message_ids = self.redis.keys()
        messages = []

        for message_id in message_ids:
            message = self.redis.get(message_id)
            messages.append(
                {'id': message_id, 'message': message,
                    'expires_in': self.redis.pttl(message_id)}
            )

        return messages

    # def get_all_messages(self):
    #     return [
    #         {
    #             'id': message_id,
    #             'message': self.redis.get(message_id)
    #         }
    #         for message_id in self.redis.keys()
    #     ]


class RedisError(Exception):
    pass
