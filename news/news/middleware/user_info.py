import time
import logging

def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file, encoding='utf-8')
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


logger = setup_logger('info', 'info.log')


class GetInfo:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        date = time.strftime("%d-%m-%Y %H:%M")
        url = request.build_absolute_uri()
        method = request.META.get('REQUEST_METHOD')
        logger.info(f"Time: {date}, request URL: {url}, HTTP method: {method}")

        response = self.get_response(request)
        return response
