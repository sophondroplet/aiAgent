import requests
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class FunctionCall:
    name: str
    arguments: str

@dataclass
class ToolCall:
    id: str
    function: FunctionCall
    type: str = "function"

@dataclass
class ChatCompletionMessage:
    role: str
    content: str
    tool_calls: Optional[List[ToolCall]] = None

@dataclass
class ChatCompletionChoice:
    message: ChatCompletionMessage
    index: int = 0

@dataclass
class ChatCompletion:
    choices: List[ChatCompletionChoice]

class CloudflareAI:
    def __init__(self, api_key: str, account_id: str):
        self.api_base_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/"
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    def chat(self):
        return ChatCompletionCreator(self)

class ChatCompletionCreator:
    def __init__(self, client: CloudflareAI):
        self.client = client
    
    def create(
        self, 
        model: str, 
        messages: List[Dict[str, str]], 
        tools: Optional[List[Dict]] = None
    ) -> ChatCompletion:
        input_data = {
            "messages": messages,
        }
        
        # Add tools if provided
        if tools:
            input_data["tools"] = tools

        response = requests.post(
            f"{self.client.api_base_url}{model}", 
            headers=self.client.headers, 
            json=input_data
        )
        result = response.json()
        
        if 'result' not in result:
            raise Exception(f"Unexpected response format: {result}")
            
        result_data = result['result']
        
        # Check for function calls in the response
        tool_calls = None
        if result_data.get('tool_calls'):
            for tc in result_data['tool_calls']:
                tool_calls = [
                    ToolCall(
                        id=tc.get('id', 'default_id'),
                        type=tc.get('type', 'function'),
                        function=FunctionCall(
                            name=tc['function']['name'],
                            arguments=tc['function']['arguments']
                        )
                    )
                ]

        message = ChatCompletionMessage(
            role="assistant",
            content=result_data.get('response', ''),
            tool_calls=tool_calls
        )
        
        choice = ChatCompletionChoice(
            message=message
        )
        
        return ChatCompletion(choices=[choice])