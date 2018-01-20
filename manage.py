#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess

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


# ======================
# add unittest command
# ======================

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
