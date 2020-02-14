import os
import config
import click
from flask import Flask
from models.base_model import db
from flask_jwt_extended import JWTManager

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'ezpark_web')

app = Flask('EZPARK', root_path=web_dir)
jwt = JWTManager(app)
if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc

@click.command()
def pi():
    from util import run
    run()

app.cli.add_command(pi)