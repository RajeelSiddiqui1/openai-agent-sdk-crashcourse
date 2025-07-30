import os 
from agents import Agent, Runner, set_tracing_disabled, function_tool  # type: ignore
from agents.extensions.models.litellm_model import LitellmModel  # type: ignore


set_tracing_disabled(disabled=True)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set or empty.")

MODEL = "gemini/gemini-1.5-flash"

@function_tool
def weather(city: str) -> str:
    return f"The weather in {city} is sunny"

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model=LitellmModel(
        model=MODEL,
        api_key=GEMINI_API_KEY,
    ),
    tools=[weather]
)

result = Runner.run_sync(agent, "What is the weather of Tokyo?")
print(result.final_output)
