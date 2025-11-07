FROM python:3.12.7-slim AS build_app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip && pip install poetry==1.8.2
RUN poetry config virtualenvs.create false

WORKDIR /proj/backend/

COPY poetry.lock pyproject.toml /proj/backend/

FROM build_app AS prod

ENV MODE='PROD'

RUN poetry install --without dev

COPY . /proj/backend/

CMD ["sh", "-c", "alembic upgrade head && uvicorn src.asgi:app --host 0.0.0.0 --port 8000"]


FROM build_app AS dev

ENV MODE='DEV'

RUN poetry install --with dev

COPY . /proj/backend/

CMD ["sh", "-c", "alembic upgrade head && uvicorn src.asgi:app --host 0.0.0.0 --port 8000 --reload"]
