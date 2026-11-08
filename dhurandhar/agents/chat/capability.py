"""Agentic chat capability."""

from __future__ import annotations

from dhurandhar.agents.chat.agentic_pipeline import AgenticChatPipeline
from dhurandhar.core.capability_protocol import TurnCapability
from dhurandhar.core.context import UnifiedContext
from dhurandhar.runtime.bootstrap.builtin_capabilities import builtin_capability_manifest
from dhurandhar.runtime.stream_bus import StreamBus


class ChatCapability(TurnCapability):
    manifest = builtin_capability_manifest("chat")

    async def run(self, context: UnifiedContext, stream: StreamBus) -> None:
        pipeline = AgenticChatPipeline(language=context.language)
        await pipeline.run(context, stream)
