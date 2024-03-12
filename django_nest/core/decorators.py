from django.http import JsonResponse
from django.views import View


def Controller(name):
    def decorator(cls):
        class Wrapper(View):

            def dispatch(self, request, *args, **kwargs):
                method = request.method.lower()
                handler = getattr(self, method, self.http_method_not_allowed)
                return handler(request, *args, **kwargs)

            def http_method_not_allowed(self, request, *args, **kwargs):
                return JsonResponse({"error": "Method not allowed"}, status=405)

        Wrapper.__name__ = cls.__name__
        Wrapper.__module__ = cls.__module__
        all_methods_dir = [
            method
            for method in dir(cls)
            if callable(getattr(cls, method)) and not method.startswith("__")
        ]
        http_methods_mapping = {
            "get": "get",
            "create": "post",
            "update": "put",
            "delete": "delete",
        }
        for method in all_methods_dir:
            for prefix, http_method in http_methods_mapping.items():
                if method.startswith(prefix):
                    setattr(Wrapper, http_method, getattr(cls, method))

        return type(name, (Wrapper,), dict(cls.__dict__))

    return decorator


def Get():
    def decorator(f):
        def get(self, request, *args, **kwargs):
            response = f(self, request, *args, **kwargs)
            print(response)
            return JsonResponse({"data": response})

        return get

    return decorator


def Post():
    def decorator(f):
        def post(self, request, *args, **kwargs):
            return JsonResponse({"data": f(self, request, *args, **kwargs)})

        return post

    return decorator


# TODO
# write methods for all the method necessary
