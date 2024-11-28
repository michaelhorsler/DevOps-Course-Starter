from flask import Flask, redirect, render_template, request
from todo_app.data.mongo_items import add_item, get_items, move_item_to_active, move_item_to_done

from todo_app.flask_config import Config
from todo_app.View_Model import ViewModel
from todo_app.oauth import blueprint
from flask_dance.contrib.github import github
from werkzeug.middleware.proxy_fix import ProxyFix
from loggly.handlers import HTTPSHandler
from logging import Formatter
import os

def create_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config.from_object(Config())
    app.logger.setLevel(app.config['LOGS_LEVEL'])
    app.logger.info("Log Level - %s", app.config['LOGS_LEVEL'])
#    app.logger.info("Loggly token - %s", app.config['LOGGLY_TOKEN'])

    if app.config['LOGGLY_TOKEN'] is not None:
        handler = HTTPSHandler(f'https://logs-01.loggly.com/inputs/{app.config["LOGGLY_TOKEN"]}/tag/todo-app')
        handler.setFormatter(
            Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
        )
        app.logger.addHandler(handler)
    app.logger.info("Logged in User - %s", os.getlogin())
    app.register_blueprint(blueprint, url_prefix="/login")

    @app.route('/')
    def index():
#        if not github.authorized:
#            app.logger.info("Login Failure - Unauthorised.")
#            return redirect('http://localhost:5000/login/github')
        items = get_items()
        item_view_model = ViewModel(items)
    #   return render_template('index.html', items = items)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/add-todo', methods=["POST"])
    def add_todo():
#        if not github.authorized:
#            app.logger.info("Login Failure - Unauthorised.")
#            return redirect('http://localhost:5000/login/github')
        new_todo_title = request.form.get('title')
        app.logger.info("Add Todo Item - %s", new_todo_title)
        add_item(new_todo_title)
        return redirect('/')

    @app.route('/active-item/<todo_id>', methods=["POST"])
    def active_item(todo_id):
    #    if not github.authorized:
    #        app.logger.info("Login Failure - Unauthorised.")
    #        return redirect('http://localhost:5000/login/github')
       app.logger.info("Add Active Item - %s", todo_id)
       move_item_to_active(todo_id)
       return redirect('/')

    @app.route('/complete-item/<active_id>', methods=["POST"])
    def complete_item(active_id):
    #    if not github.authorized:
    #        app.logger.info("Login Failure - Unauthorised.")
    #        return redirect('http://localhost:5000/login/github')
       app.logger.info("Complete Item - %s", active_id)
       move_item_to_done(active_id)
       return redirect('/')
    
    return app