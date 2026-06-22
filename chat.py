import anthropic
from dotenv import load_dotenv
load_dotenv()

# The client automatically reads ANTHROPIC_API_KEY from the environment
client = anthropic.Anthropic()

# This list list holds the full conversation history

conversation = []

print("Chat with Claude! (type 'quit' to exit)\n")

while True:
    user_question = input("You: ")

    if user_question.lower() == "quit":
        break

    # Add the user's messages to the conversation history
    conversation.append({"role": "user", "content": user_question})


# Sending the question to the model

response = client.messages.create(

    model = "claude-sonnet-4-6",
    max_tokens = 300,
    messages = conversation
)


reply = response.content[0].text
print(f"\nClaude: {reply}\n")

# Add Claud's reply to the history too so that it has context next time
conversation.append({"role": "assistant", "content": reply})