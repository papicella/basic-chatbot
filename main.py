# main.py
# pas test

import json
from flask import Flask, request, jsonify
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import os

# --- Configuration ---
# DistilGPT2 is a small, distilled version of GPT-2, suitable for quick local inference.
MODEL_NAME = "distilgpt2"

# Initialize Flask App
app = Flask(__name__)

# --- Load Model and Tokenizer ---
try:
    print(f"🤖 Loading Model: {MODEL_NAME}...")
    # Load the pre-trained model and tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained(MODEL_NAME)
    model = GPT2LMHeadModel.from_pretrained(MODEL_NAME)
    # Set the model to evaluation mode
    model.eval()
    print("✅ Model loaded successfully.")

    # Set pad_token to eos_token for generation, which is common for GPT-style models
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

except Exception as e:
    print(f"❌ Error loading model: {e}")
    # Note: If the model fails to load, the API calls will likely fail later.
    # For a real application, you'd add more robust error handling here.

# --- Chatbot Logic ---

def generate_chatbot_response(prompt: str) -> str:
    """
    Generates a response from the LLM based on the user's prompt.
    FIXED: Uses 'max_new_tokens' instead of 'max_length' to prevent errors with long prompts.
    """
    try:
        # 1. Encode the input prompt
        input_ids = tokenizer.encode(prompt, return_tensors='pt')

        # 2. Generate response tokens
        with torch.no_grad():
            output = model.generate(
                input_ids,
                max_new_tokens=100,  # Max length of the NEWLY generated text (100 tokens)
                num_return_sequences=1,
                no_repeat_ngram_size=2, # Avoid repeating phrases
                temperature=0.7,
                do_sample=True, # Enable sampling for more creative responses
                top_k=50,
                pad_token_id=tokenizer.eos_token_id # Use EOS token for padding
            )

        # 3. Decode the generated tokens back to text
        response_text = tokenizer.decode(
            output[0],
            skip_special_tokens=True
        )

        # Simple cleanup to remove the original prompt from the start of the response
        if response_text.startswith(prompt):
            return response_text[len(prompt):].strip()

        return response_text.strip()

    except Exception as e:
        print(f"An error occurred during generation: {e}")
        return "Sorry, I encountered an error generating a response."

# --- Flask REST Endpoint (Updated to support GET and POST) ---

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    """
    REST endpoint to receive a prompt and return a chatbot response.

    If using POST: Expects a JSON body: {"prompt": "user message here"}
    If using GET: Expects a URL query parameter: ?prompt=user%20message%20here
    Returns a JSON body: {"message": "chatbot response here"}
    """
    user_prompt = None

    if request.method == 'POST':
        # Retrieve prompt from JSON body for POST requests
        if not request.json or 'prompt' not in request.json:
            return jsonify({"error": "Missing 'prompt' in JSON request body for POST."}), 400
        user_prompt = request.json.get('prompt')

    elif request.method == 'GET':
        # Retrieve prompt from URL query parameters for GET requests
        user_prompt = request.args.get('prompt')

        if not user_prompt:
            return jsonify({"error": "Missing 'prompt' query parameter for GET."}), 400

    if not user_prompt or not isinstance(user_prompt, str):
           return jsonify({"error": "Invalid or empty 'prompt' value."}), 400

    print(f"▶️ Received prompt ({request.method}): {user_prompt}")

    # Get the response from the LLM
    bot_message = generate_chatbot_response(user_prompt)

    print(f"◀️ Sending response: {bot_message}")

    # Return the response as JSON
    return jsonify({"message": bot_message})

# --- Run the Flask App ---

if __name__ == '__main__':
    # Flask will run on http://127.0.0.1:5000/ by default
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
