import imp
from nameko.testing.services import worker_factory
from temp_messenger.service import MessageService

# testing
def test_konichiwa():
    service = worker_factory(MessageService)
    result = service.konichiwa()
    assert result == 'konichiwa'