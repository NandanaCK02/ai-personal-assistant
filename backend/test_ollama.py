import ollama

response = ollama.chat(
    model="qwen2.5:3b",
    messages=[
        {
            "role": "user",
            "content": "Explain what an API is in simple English."
        }
    ]
)

print(response["message"]["content"])