import os 
import asyncio
from agents import Agent, Runner, set_tracing_disabled, function_tool  # type: ignore
from agents.extensions.models.litellm_model import LitellmModel  # type: ignore
from agents import Agent, handoff # type: ignore

set_tracing_disabled(disabled=True)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set or empty.")

MODEL = "gemini/gemini-2.5-flash"

billing_agent = Agent(name="Billing agent")
refund_agent = Agent(name="Refund agent")

general_agent = Agent(name="General agent", handoffs=[billing_agent,refund_agent], model =LitellmModel(
    model=MODEL,
    api_key=GEMINI_API_KEY,
))


async def main():
    
    result = await Runner.run(
        general_agent,
        "I want to refund my order #12345. Can you help me with that?"
    )
    
    print(result.final_output)
    print("last agent", result.last_agent) 
    
    

if __name__ == "__main__":
    asyncio.run(main())    
    