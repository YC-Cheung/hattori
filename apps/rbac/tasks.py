from __future__ import absolute_import, unicode_literals

import time

from celery import shared_task


@shared_task
def add(x, y):
    time.sleep(3)
    return x + y
