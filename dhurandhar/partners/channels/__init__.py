"""Chat channels module with plugin architecture."""

from dhurandhar.partners.channels.base import BaseChannel
from dhurandhar.partners.channels.manager import ChannelManager

__all__ = ["BaseChannel", "ChannelManager"]
