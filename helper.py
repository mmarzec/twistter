import json
import functools
import uuid
import datetime
import calendar
from twisted.python import log

from error import ApiError, BadRequest


def get_json(request):
    try:
        return json.loads(request.content.getvalue())
    except ValueError:
        raise BadRequest('supplied data is not a valid JSON object')


def get_json_arg(json_data, element, default=None):
    try:
        return json_data[element]
    except KeyError:
        if default is None:
            raise BadRequest('missing required parameter: "{}"'.format(element))
        else:
            return default


def content_type(mime_type):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(request, *args, **kwargs):
            request.responseHeaders.addRawHeader('content-type', mime_type)
            return f(request, *args, **kwargs)
        return wrapper
    return decorator


def json_convert(obj):
    if isinstance(obj, datetime.datetime):
        if obj.utcoffset() is not None:
            obj = obj - obj.utcoffset()
        millis = int(calendar.timegm(obj.timetuple()) * 1000 +
                     obj.microsecond / 1000)
        return {"$date": millis}
    if isinstance(obj, uuid.UUID):
        return {"$uuid": obj.hex}
    raise TypeError("%r is not JSON serializable" % obj)


def returns_json(f):
    @functools.wraps(f)
    @content_type('application/json')
    def wrapper(request, *args, **kwargs):
        ret = f(request, *args, **kwargs)
        return json.dumps(ret, indent=4, separators=(',', ': '), default=json_convert)
    return wrapper


def rest_api(f):
    '''Decorate REST API function.'''
    @functools.wraps(f)
    @returns_json
    def wrapper(request, *args, **kwargs):
        try:
            return f(request, *args, **kwargs)
        except ApiError as e:
            log.err('Error while processing request to {}: {}'.format(request.uri, str(e.message)))
            request.setResponseCode(e.STATUS_CODE)
            return e.json
    return wrapper


def rest_api_json(f):
    '''Decorate REST API function.'''
    @functools.wraps(f)
    @rest_api
    def wrapper(request, *args, **kwargs):
        json = get_json(request)
        return f(json, *args, **kwargs)
    return wrapper

