import cgi
import json
import re
from wsgiref.simple_server import make_server

from jinja2 import Environment, FileSystemLoader


class Erik:
    def __init__(self):
        self.url_map = []
        self.template_folder = "templates"
        self.env = Environment(loader=FileSystemLoader("templates"))

    def route(self, rule, method="GET", template=None):
        def decorator(view):
            self.url_map.append((rule, method, view, template))
            return view

        return decorator

    def render_template(self, template_name, **context):
        template = self.env.get_template(template_name)
        return template.render(**context).encode("utf-8")

    def __call__(self, environ, start_response):
        path = environ["PATH_INFO"]
        request_method = environ["REQUEST_METHOD"]
        body = b"Content Not Found"
        status = "404 Not Found"
        ctype = "text/html"

        for rule, method, view, template in self.url_map:
            match = re.match(rule, path)
            if match:
                if method != request_method:
                    continue
                view_args = match.groupdict()
                if method == "POST":
                    view_args["form"] = cgi.FieldStorage(
                        fp=environ["wsgi.input"],
                        environ=environ,
                        keep_blank_values=1,
                    )
                view_result = view(**view_args)

                if isinstance(view_result, tuple):
                    view_result, status, ctype = view_result
                else:
                    status = "200 OK"

                if template:
                    body = self.render_template(template, **view_result)
                elif (
                    isinstance(view_result, dict)
                    and ctype == "application/json"
                ):
                    body = json.dumps(view_result).encode("utf-8")
                else:
                    body = str(view_result).encode("utf-8")

        start_response(status, [("Content-type", ctype)])
        return [body]

    def run(self, host="0.0.0.0", port=8000):
        server = make_server(host, port, self)
        server.serve_forever()


if __name__ == "__main__":

    app = Erik()

    @app.route("^/$")
    def foo():
        return "Hello"

    @app.route("^/(?P<id>\d{1,})$")
    def foo2(id):
        return f"Hello {id}", 400, "foo"

    print(
        app(
            {"PATH_INFO": "/1234", "REQUEST_METHOD": "GET"},
            lambda *args: print(args),
        )
    )
    print(
        app(
            {"PATH_INFO": "/", "REQUEST_METHOD": "GET"},
            lambda *args: print(args),
        )
    )

