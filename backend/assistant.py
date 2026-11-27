
import ollama
import json
from web_search import search_web
from weather import get_weather


# Store conversations separately for each session
conversation_history = {}


# Define available tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather information for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Name of the city"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
    "type": "function",
    "function": {
        "name": "search_web",
        "description": "Search the internet for current information, latest news, recent updates, and information that may have changed.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                }
            },
            "required": ["query"]
        }
    }
}
]


def chat_with_ai(message: str, session_id: str):

    # Get existing conversation or create a new one
    if session_id not in conversation_history:
        conversation_history[session_id] = []

    messages = conversation_history[session_id]

    # Add the latest user message
    messages.append({
        "role": "user",
        "content": message
    })

    # Ask the AI whether it needs a tool
    response = ollama.chat(
        model="qwen2.5:3b",
        messages=messages,
        tools=tools
    )

    # Check whether the AI requested a tool
    if response.message.tool_calls:

        messages.append(response.message)

        for tool_call in response.message.tool_calls:

            tool_name = tool_call.function.name
            arguments = tool_call.function.arguments

            if tool_name == "get_weather":

                result = get_weather(arguments["city"])
            elif tool_name =='search_web':
                result= search_web(arguments['query'])

                messages.append({
                    "role": "tool",
                    "tool_name": "get_weather",
                    "content": json.dumps(result)
                })

        # Ask AI to generate the final answer
        final_response = ollama.chat(
            model="qwen2.5:3b",
            messages=messages
        )

        answer = final_response.message.content

    else:
        answer = response.message.content

    # Save AI response in conversation history
    messages.append({
        "role": "assistant",
        "content": answer
    })

    return answer
