import os
from agents import Agent,Runner,set_tracing_disabled,function_tool
from agents.extensions.models.litellm_model import LitellmModel

set_tracing_disabled(disabled=True)

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
MODEL = 'gemini/gemini-2.5-flash'

agent = Agent(
    name="Crash course Assistant",
    instructions = "You are crash course make with youtube links and best website paid and free for pratice",
    model = LitellmModel(model=MODEL, api_key=GEMINI_API_KEY)
)


loop = True

try:
    while loop:
        user_input = input("Enter input about to generate crash courses any: ")
        result = Runner.run_sync(agent, user_input)
        
        print(result.final_output)
        
        exist = input("for exist write:(y)").lower()
        if exist == "y":
            loop = False
            print("Thanks for comming")

except:
   print(Exception)