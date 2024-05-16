FROM python as base

# Perform common operations, dependency installation etc...
RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry update
RUN poetry install
ENV WEBAPP_PORT=5000
EXPOSE ${WEBAPP_PORT}
COPY . .

FROM base as test

ENTRYPOINT [ "poetry", "run", "pytest" ]

FROM base as production

# Configure for production
ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0"]

FROM base as development

# Configure for local development
ENV FLASK_ENV=development
ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0"]