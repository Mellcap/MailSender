#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from flask import render_template

from app import create_app, db, admin
from app.models.email_event import EmailEvent
from app.models.email_group import EmailGroup, EmailAddress
from flask_script import Manager, Shell, Command
from flask_migrate import Migrate, MigrateCommand
from flask_admin.contrib.sqla import ModelView


# =============
# Initial app
# =============

app = create_app(os.getenv('JUBLIA_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

# add admin model view
admin.add_view(ModelView(EmailEvent, db.session))
admin.add_view(ModelView(EmailGroup, db.session))
admin.add_view(ModelView(EmailAddress, db.session))


# =====================================
# add shell_context & migrate command
# =====================================

def make_shell_context():
    return dict(app=app, db=db, EmailEvent=EmailEvent, EmailGroup=EmailGroup, EmailAddress=EmailAddress)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


# ==================================
# add celery worker & beat command
# ==================================

class CeleryWorker(Command):
    """Starts the celery worker."""
    name = 'celery_worker'
    capture_all_args = True

    def run(self, argv):
        ret = subprocess.call(
            ['celery', 'worker', '-A', 'app.celery'] + argv)
        sys.exit(ret)

manager.add_command("celery_worker", CeleryWorker())

class CeleryBeat(Command):
    """Starts the celery beat."""
    name = 'celery_beat'
    capture_all_args = True

    def run(self, argv):
        ret = subprocess.call(
            ['celery', 'beat', '-A', 'app.celery'] + argv)
        sys.exit(ret)

manager.add_command("celery_beat", CeleryWorker())


# ======================
# add unittest command
# ======================

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

# home page
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


if __name__ == '__main__':
    manager.run()
