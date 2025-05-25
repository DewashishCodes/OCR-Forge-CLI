# We need the Groq client instance and the model name from main/config
# So functions will accept groq_client as an argument.
# Model name can also be passed or used directly from config.
import voiceout as vo

import os
global voice_mode

def load_voice_mode():
    # Path to the config file
    config_file = "voicemodeconfig.txt"

    # Default voice mode is False (voice_off)
    voice_mode = False

    try:
        with open(config_file, "r") as file:
            content = file.read().strip()
            if content == "voice_on":
                voice_mode = True
            elif content == "voice_off":
                voice_mode = False
    except FileNotFoundError:
        print(f"{config_file} not found. Defaulting to voice_off.")

    return voice_mode

# Example usage
voice_mode = load_voice_mode()



def clean_text_with_llm(groq_client, text, model_name):
    """Sends raw text to LLM for cleaning and summarization."""
    if not text or not text.strip():
         print("\n⚠️ No text provided to the LLM for cleanup.")
         return "[No text provided for LLM cleanup]"

    prompt = f"Extract only the important information from the following screen text. Remove all irrelevant or repeated content, UI elements descriptions, and noise:\n\n{text}\n\nImportant Info:"
    cleaned_text_buffer = ""
    print("\n🧠 Sending to LLM for cleanup...")
    print("----------------------")
    try:
        chat_completion = groq_client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are an assistant that cleans and summarizes screen-captured OCR text. You prioritize actual content over UI noise."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500, # Adjusted max tokens
            top_p=1,
            stream=True # Enable streaming
        )

        # Iterate over the stream of chunks and print directly
        for chunk in chat_completion:
            # Check if the chunk contains content (text)
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end='', flush=True) # Print the content immediately
                cleaned_text_buffer += content # Add to the buffer

        print("\n----------------------") # Separator after streaming
        print("✅ LLM cleanup complete.")

        cleaned = cleaned_text_buffer.strip()
        if not cleaned:
             return "[LLM returned empty output after processing]"
        return cleaned

    except Exception as e:
        print(f"\n❌ Error contacting Groq API during cleanup: {e}")
        return f"[Error contacting Groq API]: {e}"


def follow_up_prompt(groq_client, context, model_name):
    """Allows the user to ask follow-up questions about the last processed context."""
    if not context or not context.strip() or context.startswith("["): # Don't allow follow-up on empty or error context
         print("\n💬 No valid context available from the last capture for follow-up.")
         return

    while True:
        user_input = input("\n💬 Ask a follow-up about the context (or type 'exit' to stop):\n> ")

        if user_input.strip().lower() in ['exit', 'quit', 'q']:
            if voice_mode==True:
                vo.speak("Exiting followup mode")
            break

        if not user_input.strip():
             continue # Skip empty input

        # Include the context and the user's question in the prompt
        prompt = f"Here is the previous screen content context:\n\n---\n{context}\n---\n\nBased on this context, please respond to the following request. If the context is insufficient, use your general knowledge. Be concise and respond only necessary information: {user_input.strip()}"

        try:
            print("\n🤖 Groq is thinking...")
            print("----------------------")
            response = groq_client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant working with screen-captured text. You can elaborate or use general knowledge if the provided context is limited."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5, # Slightly higher temp for follow-up creativity
                max_tokens=600, # More tokens for responses
                stream=True
            )

            response_buffer = "" # Buffer to store the full response (optional, could be used for logging later)
            # Iterate over the stream of chunks and print directly
            
            for chunk in response:
                 if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(content, end='', flush=True) # Print immediately
                    response_buffer += content
            
            if voice_mode==True:
                vo.speak(response_buffer)

            print("\n----------------------")

        except Exception as e:
            print(f"\n❌ [Error from Groq]: {e}")
            # Optionally log the error