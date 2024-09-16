import logging

from django.dispatch.dispatcher import Signal

logger = logging.getLogger(__name__)

set_accepted = Signal(providing_args=["instance", "explicit"])
set_rejected = Signal(providing_args=["instance", "explicit"])
