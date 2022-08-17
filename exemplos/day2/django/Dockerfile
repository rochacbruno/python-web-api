FROM python:3.10.6-slim-bullseye AS app

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential curl libpq-dev \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean \
  && useradd --create-home python \
  && chown python:python -R /app \
  && mkdir /static \
  && chown python:python -R /static

USER python

# Copy local django/ contents to container /app (WORKDIR)
COPY --chown=python:python . .

ARG DEBUG="false"
ENV DEBUG="${DEBUG}" \
    PYTHONUNBUFFERED="true" \
    PYTHONPATH="/app" \
    PATH="${PATH}:/home/python/.local/bin" \
    USER="python" \
    BLOG_STATIC_ROOT="/static/" \
    BLOG_STATIC_URL="/static/" \
    BLOG_DEBUG="${DEBUG}" \
    BLOG_ALLOWED_HOSTS='["*"]' \
    BLOG_DATABASES__default__ENGINE="django.db.backends.postgresql" \
    BLOG_DATABASES__default__NAME="blog" \
    BLOG_DATABASES__default__USER="blog" \
    BLOG_DATABASES__default__HOST="blog_postgres" \
    DJANGO_SETTINGS_MODULE="djblog.settings"

RUN python -m pip install install /app gunicorn psycopg2

RUN if [ "${DEBUG}" = "false" ]; then \
  SECRET_KEY=dummyvalue python manage.py collectstatic --no-input; \
  fi

ENTRYPOINT [ "/app/docker/entrypoint.sh" ]

EXPOSE 8000

CMD ["python -m gunicorn", "-c", "python:djblog.gunicorn", "djblog.wsgi"]
