from django.http import  HttpResponseBadRequest

def ajax_required(f):
    def wrap(request, *args, **kwargs):
        is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        if not is_ajax:
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap
