"""
sentry.tasks.process_buffer
~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2010-2014 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from __future__ import absolute_import

import logging

from sentry.tasks.base import instrumented_task
from sentry.utils.locking import UnableToAcquireLock


logger = logging.getLogger(__name__)


@instrumented_task(
    name='sentry.tasks.process_buffer.process_pending')
def process_pending():
    """
    Process pending buffers.
    """
    from sentry import buffer
    from sentry.app import locks

    lock = locks.get('buffer:process_pending', duration=60)
    try:
        with lock.acquire():
            buffer.process_pending()
    except UnableToAcquireLock as error:
        logger.warning('process_pending.fail', extra={'error': error})


@instrumented_task(
    name='sentry.tasks.process_buffer.process_incr')
def process_incr(**kwargs):
    """
    Processes a buffer event.
    """
    from sentry import buffer

    buffer.process_incr(**kwargs)


@instrumented_task(
    name='sentry.tasks.process_buffer.process_cb')
def process_cb(**kwargs):
    from sentry import buffer

    buffer.process_cb(**kwargs)
