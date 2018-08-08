from swift.common.swob import Request, Response
from swift.common.constraints import MAX_META_VALUE_LENGTH
from tinytag import TinyTag

class MetaExtractor(object):
    def __init__(self, stream):
        self.stream = stream
        self.tinytag = TinyTag

    def read(self, size=None):
        try:
            data = self.tinytag.get(size, image=True)
        except Exception as e:
            print 'Caught an exception: ', e
        return data

    def get_tags():
        return {k: v for k, v in tag.__dict__.items() if not k.startswith('_')}


class MusicMeta(object):
    def __init__(self, app, conf):
        self.app = app
        self.conf = conf
        self.logger = get_logger(conf, log_route='jpeg_extract')

    def __call__(self, env, start_response):
        if env['REQUEST_METHOD'] != 'PUT':
            return self.app(env, start_response)
        req = Request(env)
        version, account, container, obj = split_path(env['PATH_INFO'], 1, 4, True)
        if not obj:
            return self.app(env, start_response)
        if not obj.lower().endswith('.mp3') and \
                not obj.lower().endswith('.oga') and \
                not obj.lower().endswith('.ogg') and \
                not obj.lower().endswith('.opus') and \
                not obj.lower().endswith('.wav') and \
                not obj.lower().endswith('.flac') and \
                not obj.lower().endswith('.wma') and \
                not obj.lower().endswith('.m4a') and \
                not obj.lower().endswith('.mp4'):
            return self.app(env, start_response)
        headers = {}
        extractor = MetaExtractor(env['wsgi.input'])
        for tag, value in extractor.get_tags().items():
            #skip empty tag items
            if not tags[name]:
                continue
            if len(tags[name] > MAX_META_VALUE_LENGTH:
                continue
            header = f'X-Object-Meta-{tag.replace(" ", "-").replace("_", "-")}'
            headers[header] = value if value else ""
            req.headers[header] = headers[header]
        self.logger.info(headers)
        try:
            resp = self._app_call(env)
        except Exception:
            resp = HTTPServerError(request=Request(env), body="error")
            return resp(env, start_response)
        start_response(self._response_status, self._response_headers,
                       self._response_exc_info)
        return resp

def filter_factory(global_conf, **local_conf):
    """Returns the WSGI filter for use with paste.deploy."""
     conf = global_conf.copy()
    conf.update(local_conf)
    register_swift_info('music_meta')

    def music_meta(app):
        return MusicMeta(app, conf)
    return music_meta
