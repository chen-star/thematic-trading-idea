import logging

from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.plugins.base_plugin import BasePlugin


class CountModelCallPlugin(BasePlugin):

    def __init__(self) -> None:
        """Initialize the plugin with counters."""
        super().__init__(name="count_model_call")
        self.total_model_call_count: int = 0
        self.per_agent_model_call_count: dict = {}

    # Callback: Runs before a model is called.
    async def before_model_callback(
            self, *, callback_context: CallbackContext, llm_request: LlmRequest
    ) -> None:
        self.total_model_call_count += 1
        self.per_agent_model_call_count[callback_context.agent_name] = (
                self.per_agent_model_call_count.get(callback_context.agent_name, 0) + 1
        )
        logging.info(f"[Plugin] Total LLM request count: {self.total_model_call_count}")
        logging.info(
            f"[Plugin] Agent {callback_context.agent_name} LLM request count: {self.per_agent_model_call_count[callback_context.agent_name]}")
