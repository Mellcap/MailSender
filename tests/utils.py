#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arrow


def generate_timestamp(valid=True, shift_hours=1):
    now = arrow.utcnow().replace(second=0, microsecond=0)
    if valid:
        return now.shift(hours=shift_hours)
    else:
        return now.shift(hours=-shift_hours)
