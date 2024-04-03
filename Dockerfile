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
