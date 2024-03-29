import json

def body_parser(get_response):
    def middleware(req):
        req.parsed_body = json.loads(req.body.decode('utf-8'))

        response = get_response(req)
        return response
    return middleware
