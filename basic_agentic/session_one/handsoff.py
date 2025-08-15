import os
from agents import Agent, Runner, set_tracing_disabled,handoff, function_tool #type: ignore
from agents.extensions.models.litellm_model import LitellmModel #type: ignore

set_tracing_disabled(disabled=True)

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set or empty.")

MODEL = "gemini/gemini-2.5-flash"
gemini_model = LitellmModel(model=MODEL, api_key=GEMINI_API_KEY)


@function_tool
def get_weather(city:str)->str:
    f"the weather of {city} is sunny"

refund_agent = Agent(name="refund agent")

general_agent = Agent(
    name="General agent",
    tools = [get_weather],
    handoffs=[
        handoff(
            agent = refund_agent,
            tool_name_override = "refuned_order",
            tool_description_override = "handles a refund request",
            is_enabled=True
        )
        ],
    model=gemini_model
)

result = Runner.run_sync(
    general_agent,
    "I want to refund my order . Can you help me with that?"
)

print(result.final_output)
