from __future__ import annotations

import os

from .voice import VoiceError


def run_elevenlabs_conversation(*, use_g1_speaker: bool = True) -> str:
    """Run a private ElevenLabs session with the PC microphone and G1 speaker."""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    agent_id = os.getenv("ELEVENLABS_AGENT_ID")
    if not api_key:
        raise VoiceError("ELEVENLABS_API_KEY is not configured")
    if not agent_id:
        raise VoiceError("ELEVENLABS_AGENT_ID is not configured")

    try:
        from elevenlabs.client import ElevenLabs
        from elevenlabs.conversational_ai.conversation import Conversation
        from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
    except ImportError as error:
        raise VoiceError(
            'conversation dependencies are missing; install with pip install -e ".[conversation]"'
        ) from error

    if use_g1_speaker:
        from .g1_live_audio import G1LiveAudioInterface

        audio_interface = G1LiveAudioInterface()
    else:
        audio_interface = DefaultAudioInterface()

    client = ElevenLabs(api_key=api_key)
    conversation = Conversation(
        client,
        agent_id,
        requires_auth=True,
        audio_interface=audio_interface,
        callback_agent_response=lambda response: print(f"Migo: {response}"),
        callback_agent_response_correction=lambda original, corrected: print(
            f"Migo (corrección): {original} -> {corrected}"
        ),
        callback_user_transcript=lambda transcript: print(f"Usuario: {transcript}"),
        callback_latency_measurement=lambda latency: print(f"Latencia: {latency} ms"),
    )
    conversation.start_session()
    try:
        return conversation.wait_for_session_end()
    except KeyboardInterrupt:
        conversation.end_session()
        return conversation.wait_for_session_end()
