import os
from openai_interface import CloudflareAI
import json

def get_weather(location):
    # Mock weather function
    return f"The weather in {location} is sunny and 22°C"

# Example function definitions
available_functions = {
    "get_weather": {
        "name": "get_weather",
        "description": "Get the weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The location to get weather for"
                }
            },
            "required": ["location"]
        }
    }
}

# Initialize the client
client = CloudflareAI(
    api_key="nFdjsQbscfaCHJj50FKcYL2-fm1vVcZG16iFndLq",
    account_id="7f8c9af9a8d66e3edac3fd127433e7eb"
)

# Initialize messages list with system prompt
messages = []
system_prompt = input("Enter system prompt: ")
messages.append({"role": "system", "content": system_prompt})

# Main chat loop
while True:
    try:
        # Get user input
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
            
        # Add user message to history
        messages.append({"role": "user", "content": user_input})
        
        # Get response from Cloudflare AI with function definitions
        completion = client.chat().create(
            model="@cf/meta/llama-2-70b-chat",  # Note: Using Llama 2 70B as it better supports tools
            messages=messages,
            tools=[available_functions["get_weather"]]
        )
        
        # Check if the model wants to call a function
        if (hasattr(completion.choices[0].message, 'tool_calls') and 
            completion.choices[0].message.tool_calls is not None):
            for tool_call in completion.choices[0].message.tool_calls:
                if tool_call.function.name == "get_weather":
                    # Parse the arguments
                    args = json.loads(tool_call.function.arguments)
                    # Call the function
                    function_response = get_weather(args["location"])
                    
                    # Add function response to messages
                    messages.append({
                        "role": "function",
                        "name": tool_call.function.name,
                        "content": function_response
                    })
                    
                    # Get a new response from the model
                    completion = client.chat().create(
                        model="@cf/meta/llama-2-70b-chat",
                        messages=messages,
                        tools=[available_functions["get_weather"]]
                    )
        
        # Extract and print assistant's response
        assistant_response = completion.choices[0].message.content
        print("\nAssistant:", assistant_response)
        
        # Add assistant's response to message history
        messages.append({"role": "assistant", "content": assistant_response})
            
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")