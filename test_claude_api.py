"""
Quick test to verify Claude API access
Minimal token usage - just a hello world
"""
import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables
load_dotenv()

# Initialize client
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Minimal test message
print("Testing Claude API connection...")
message = client.messages.create(
    model="claude-3-haiku-20240307",  # Using Haiku for minimal cost
    max_tokens=50,  # Keep it very short
    messages=[
        {"role": "user", "content": "Say 'API test successful' and nothing else."}
    ]
)

print(f"\n[SUCCESS] Response from Claude:")
print(f"  {message.content[0].text}")
print(f"\nToken usage: {message.usage.input_tokens} input, {message.usage.output_tokens} output")
