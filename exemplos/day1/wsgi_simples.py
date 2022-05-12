def application(environ, start_response):
    body = b"<strong>Hello world!</strong>"
    status = "200 OK"
    headers = [("Content-type", "text/html")]
    start_response(status, headers)
    return [body]


if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    server = make_server("0.0.0.0", 8000, application)
    server.serve_forever()