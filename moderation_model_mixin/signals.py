import logging

from django.dispatch.dispatcher import Signal

logger = logging.getLogger(__name__)

set_accepted = Signal()
set_rejected = Signal()
