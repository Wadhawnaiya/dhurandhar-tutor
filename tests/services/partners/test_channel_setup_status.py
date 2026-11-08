from __future__ import annotations

from typing import Any

import pytest

from dhurandhar.partners.bus.queue import MessageBus
from dhurandhar.partners.channels.discord import DiscordChannel, DiscordConfig
from dhurandhar.partners.channels.email import EmailChannel, EmailConfig
from dhurandhar.partners.channels.mattermost import MattermostChannel, MattermostConfig
from dhurandhar.partners.channels.slack import SlackChannel, SlackConfig
from dhurandhar.partners.channels.telegram import TelegramChannel, TelegramConfig
from dhurandhar.partners.channels.zulip import ZulipChannel, ZulipConfig


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("channel_cls", "config"),
    [
        (DiscordChannel, DiscordConfig(enabled=True, allow_from=["*"])),
        (MattermostChannel, MattermostConfig(enabled=True, allow_from=["*"])),
        (SlackChannel, SlackConfig(enabled=True, allow_from=["*"])),
        (TelegramChannel, TelegramConfig(enabled=True, allow_from=["*"])),
        (ZulipChannel, ZulipConfig(enabled=True, allow_from=["*"])),
    ],
)
async def test_missing_credentials_are_visible_in_webui_status(
    channel_cls: type[Any], config: Any
) -> None:
    channel = channel_cls(config, MessageBus())

    await channel.start()

    assert channel.is_running is False
    assert channel.setup_state == {
        "status": "action_required",
        "message": (
            "Required fields are missing. Complete the channel configuration and save again."
        ),
    }


@pytest.mark.asyncio
async def test_email_consent_requirement_is_visible_in_webui_status() -> None:
    channel = EmailChannel(
        EmailConfig(enabled=True, allow_from=["*"], consent_granted=False),
        MessageBus(),
    )

    await channel.start()

    assert channel.setup_state == {
        "status": "action_required",
        "message": "Explicit consent is required before email polling can start.",
    }
