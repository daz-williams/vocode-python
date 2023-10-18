import logging
from fastapi import FastAPI

from vocode.streaming.models.agent import ChatGPTAgentConfig

from vocode.streaming.models.synthesizer import AzureSynthesizerConfig
from vocode.streaming.synthesizer.azure_synthesizer import AzureSynthesizer

from vocode.streaming.models.synthesizer import ElevenLabsSynthesizerConfig
from vocode.streaming.synthesizer.eleven_labs_synthesizer import ElevenLabsSynthesizer

from vocode.streaming.synthesizer.rime_synthesizer import RimeSynthesizer

from vocode.streaming.models.transcriber import DeepgramTranscriberConfig
from vocode.streaming.transcriber.deepgram_transcriber import DeepgramTranscriber

from vocode.streaming.agent.chat_gpt_agent import ChatGPTAgent
from vocode.streaming.client_backend.conversation import ConversationRouter
from vocode.streaming.models.message import BaseMessage

from dotenv import load_dotenv

load_dotenv()

app = FastAPI(docs_url=None)

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def create_synthesizer(ws_synthesizer_config):
    logger.debug(f"output_audio_config: {ws_synthesizer_config}")
    # synthesizer_config = ElevenLabsSynthesizerConfig.from_output_audio_config(
    #     ws_synthesizer_config
    # )
    # logger.debug(f"Synthesizer Config: {synthesizer_config}")
    return AzureSynthesizer(ws_synthesizer_config)

def create_transcriber(ws_transcriber_config):
    logger.debug(f"input_audio_config: {ws_transcriber_config}")
    transcriber_config = DeepgramTranscriberConfig.from_input_audio_config(
        ws_transcriber_config
    )
    logger.debug(f"Synthesizer Config: {transcriber_config}")
    return DeepgramTranscriber(transcriber_config)

conversation_router = ConversationRouter(
    agent_thunk=lambda agent_config: ChatGPTAgent(agent_config),
    synthesizer_thunk=create_synthesizer,
    transcriber_thunk=create_transcriber,
    logger=logger,
)

app.include_router(conversation_router.get_router())
