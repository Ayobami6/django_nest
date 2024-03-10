from django.http import JsonResponse
from django.views import View


def Controller(name):
    def decorator(cls):
        class Wrapper(View):

            def dispatch(self, request, *args, **kwargs):
                method = request.method.lower()
                print(method)
                handler = getattr(self, method, self.http_method_not_allowed)
                print(handler)
                print(Wrapper.__dict__)
                return handler(request, *args, **kwargs)

            def http_method_not_allowed(self, request, *args, **kwargs):
                return JsonResponse({"error": "Method not allowed"}, status=405)

        Wrapper.__name__ = cls.__name__
        Wrapper.__module__ = cls.__module__
        print(Wrapper.__name__)
        all_methods_dir = [
            method
            for method in dir(cls)
            if callable(getattr(cls, method)) and not method.startswith("__")
        ]
        print("Methods using dir():", all_methods_dir)
        for method in all_methods_dir:
            if method.startswith("get"):
                setattr(Wrapper, "get", getattr(cls, method))

        return type(name, (Wrapper,), dict(cls.__dict__))

    return decorator


def Get():
    def decorator(f):
        f.__name__ = "get"
        print(f.__name__)

        def get(self, request, *args, **kwargs):

            return JsonResponse({"data": f(self, request, *args, **kwargs)})

        return get

    return decorator


# TODO
# write methods for all the method necessary
