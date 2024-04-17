FROM python as base

# Perform common operations, dependency installation etc...
RUN pip install poetry
RUN pip install flask
COPY pyproject.toml poetry.lock ./
RUN poetry update
RUN poetry install
ENV WEBAPP_PORT=5000
EXPOSE ${WEBAPP_PORT}
COPY . .

FROM base as production

# Configure for production
ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0", "todo_app/app:create_app()"]

FROM base as development

# Configure for local development
ENV FLASK_ENV=development
ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0", "todo_app/app:create_app()"]







FROM python
RUN pip install poetry
RUN pip install flask
ENV FLASK_APP="todo_app/app:create_app()"
COPY pyproject.toml poetry.lock ./
RUN poetry update
RUN poetry install
ENV WEBAPP_PORT=5000
EXPOSE ${WEBAPP_PORT}
COPY . .

ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0"]
