FROM python as base

# Perform common operations, dependency installation etc...
RUN pip install poetry
RUN pip uninstall -y setuptools
RUN pip install setuptools==39.1.0
WORKDIR /app
COPY pyproject.toml poetry.lock ./
# azRUN poetry update
RUN poetry install
ENV WEBSITES_PORT=5000
# ENV WEBAPP_PORT=8080
EXPOSE ${WEBSITES_PORT}
COPY . .

FROM base as test
#Configure for test
COPY .env.test .
ENTRYPOINT poetry run pytest

FROM base as production
# Configure for production
ENTRYPOINT poetry run flask run --host=0.0.0.0

FROM base as development
# Configure for local development
ENV FLASK_ENV=development
ENTRYPOINT poetry run flask run --host=0.0.0.0