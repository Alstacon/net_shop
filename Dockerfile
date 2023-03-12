FROM python:3.10-slim

WORKDIR /opt/

COPY poetry.lock pyproject.toml ./

RUN pip install poetry \
    && poetry config virtualenvs.create false\
    && poetry install --without dev --no-root

COPY . .

ENTRYPOINT ["bash", "entrypoint.sh"]

CMD python manage.py runserver 0.0.0.0:80
