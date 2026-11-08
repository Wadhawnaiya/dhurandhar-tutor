"""Ask Questions capability — an explicit user-selected interview mode."""

from __future__ import annotations

from typing import cast

from dhurandhar.agents.chat.agentic_pipeline import AgenticChatPipeline
from dhurandhar.core.capability_protocol import (
    StreamBusProtocol,
    TurnCapability,
)
from dhurandhar.core.context import UnifiedContext
from dhurandhar.runtime.bootstrap.builtin_capabilities import builtin_capability_manifest
from dhurandhar.runtime.stream_bus import StreamBus


class AskQuestionsCapability(TurnCapability):
    """Start the selected turn with a context-aware question card."""

    manifest = builtin_capability_manifest("ask_questions")

    async def run(self, context: UnifiedContext, stream: StreamBusProtocol) -> None:
        context.metadata["ask_questions_mode"] = True
        # This is the first *agent-loop round of the selected turn*, not the
        # first turn in the conversation.  The prompt still receives the full
        # history, so a turn selected much later asks a new, contextual question.
        pipeline = AgenticChatPipeline(
            language=context.language,
            initial_tool_choice="ask_user",
        )
        await pipeline.run(context, cast(StreamBus, stream))


__all__ = ["AskQuestionsCapability"]
