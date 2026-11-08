"""Voice adapter registry.

Adapters are stateless singletons keyed by the ``adapter`` field on the
resolved config. The OpenAI-compatible pair covers OpenAI, Groq, SiliconFlow,
OpenRouter, Azure OpenAI and local vLLM/LM Studio; add bespoke providers
(DashScope native, ElevenLabs, Gemini, Deepgram) by registering new keys here.
"""

from __future__ import annotations

from dhurandhar.services.voice.adapters.dashscope import (
    DashScopeSTTAdapter,
    DashScopeTTSAdapter,
)
from dhurandhar.services.voice.adapters.edge import EdgeTTSAdapter
from dhurandhar.services.voice.adapters.gemini import GeminiTTSAdapter
from dhurandhar.services.voice.adapters.mimo import MiMoTTSAdapter
from dhurandhar.services.voice.adapters.minimax import MiniMaxTTSAdapter
from dhurandhar.services.voice.adapters.mistral import MistralSTTAdapter, MistralTTSAdapter
from dhurandhar.services.voice.adapters.openai_compat import (
    OpenAICompatSTTAdapter,
    OpenAICompatTTSAdapter,
    OpenRouterTTSAdapter,
)
from dhurandhar.services.voice.adapters.volcengine import VolcengineSTTAdapter, VolcengineTTSAdapter
from dhurandhar.services.voice.adapters.xai import XaiSTTAdapter, XaiTTSAdapter
from dhurandhar.services.voice.base import BaseSTTAdapter, BaseTTSAdapter, VoiceProviderError

TTS_ADAPTERS: dict[str, BaseTTSAdapter] = {
    "mimo_tts": MiMoTTSAdapter(),
    "minimax": MiniMaxTTSAdapter(),
    "volcengine": VolcengineTTSAdapter(),
    "openai_compat": OpenAICompatTTSAdapter(),
    "openrouter_tts": OpenRouterTTSAdapter(),
    "dashscope": DashScopeTTSAdapter(),
    "gemini": GeminiTTSAdapter(),
    "edge": EdgeTTSAdapter(),
    "mistral_tts": MistralTTSAdapter(),
    "xai_tts": XaiTTSAdapter(),
}

STT_ADAPTERS: dict[str, BaseSTTAdapter] = {
    "volcengine": VolcengineSTTAdapter(),
    "openai_compat": OpenAICompatSTTAdapter(),
    "dashscope": DashScopeSTTAdapter(),
    "mistral_stt": MistralSTTAdapter(),
    "xai_stt": XaiSTTAdapter(),
}


def get_tts_adapter(name: str) -> BaseTTSAdapter:
    adapter = TTS_ADAPTERS.get(name or "openai_compat")
    if adapter is None:
        raise VoiceProviderError(f"Unsupported TTS adapter: {name!r}")
    return adapter


def get_stt_adapter(name: str) -> BaseSTTAdapter:
    adapter = STT_ADAPTERS.get(name or "openai_compat")
    if adapter is None:
        raise VoiceProviderError(f"Unsupported STT adapter: {name!r}")
    return adapter


__all__ = [
    "TTS_ADAPTERS",
    "STT_ADAPTERS",
    "get_tts_adapter",
    "get_stt_adapter",
    "DashScopeSTTAdapter",
    "DashScopeTTSAdapter",
]
