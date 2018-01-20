#!/usr/bin/env python
# -*- coding: utf-8 -*-


beat_schedule = {
        'send-email-every-minute': {
            'task': 'app.schedules.schedule_send_emails',
            'schedule': 60.0,
            'args': ()
        },
    }

imports = ('app.schedules', 'app.email')

timezone = 'UTC'