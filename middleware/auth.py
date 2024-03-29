from django.http import JsonResponse
import jwt
from authentication.models import Account

def auth_middleware(get_response):
    def middleware(req):
        if req.path.startswith("/api/auth") or req.path.startswith("/api/test"):
            pass;
        else:
            if not "Access-Token" in req.headers:
                return JsonResponse({"message" : "No Token Provided"}, status=400)
            try:
                token_decoded = jwt.decode(req.headers["Access-Token"], "secret", algorithms=["HS256"])
                if not 'id' in token_decoded:
                    return JsonResponse({"message" : "Malacious token"}, status=401)
                id = token_decoded["id"]
            except jwt.ExpiredSignatureError:
                return JsonResponse({"message" : "Token is expired"}, status=401)
            try:
                account = Account.objects.get(id=id)
            except Account.DoesNotExist:
                return JsonResponse({"message" : "Malacious token"}, status=401)
            req.account = account
        response = get_response(req)
        return response
    return middleware
