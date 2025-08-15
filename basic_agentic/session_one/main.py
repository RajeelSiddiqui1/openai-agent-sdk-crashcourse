import os
import re
import time
from agents import Agent,Runner,set_tracing_disabled,function_tool # type: ignore
from agents.extensions.models.litellm_model import LitellmModel # type: ignore

set_tracing_disabled(disabled=True)


OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

MODEL = 'gpt-4.1-mini'
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.") 
MODEL2 = 'gemini/gemini-2.5-flash'

agent = Agent(
    name="Crash course Assistant",
    instructions = "You are a crash course assistant. Provide YouTube links and the best websites (both paid and free) for practice.",
    model = LitellmModel(model=MODEL2, api_key=GEMINI_API_KEY)
)


def clean_output(output):
    cleaned_output = re.sub(r'\s+',' ',output).strip()
    
    return cleaned_output

def print_one_word_at_a_time(output, delay=0.1):
    words = output.split()
    for word in words:
        print(word, end=' ', flush=True)
        time.sleep(delay)
    
    print()    

loop = True

try:
    while loop:
        user_input = input("Enter input about to generate crash courses any: ")
        result = Runner.run_sync(agent, user_input)
        
        cleaned_output = clean_output(result.final_output)
        print_one_word_at_a_time(cleaned_output)
        
        
        exist = input("for exist write:(y)").lower()
        if exist == "y":
            loop = False
            print("Thanks for comming")

except Exception as e:
   print(f"An error occurred: {e}")