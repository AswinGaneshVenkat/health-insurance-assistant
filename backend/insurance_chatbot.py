from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from peft import PeftModel, PeftConfig

# Step 1: Load the base model (google/flan-t5-small)
base_model_id = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(base_model_id)
base_model = AutoModelForSeq2SeqLM.from_pretrained(base_model_id)

# Step 2: Load your LoRA adapter
adapter_model_id = "AswinGanesh07/insurance-flan-bot"
model = PeftModel.from_pretrained(base_model, adapter_model_id)

# Step 3: Now you can use the model!
def get_bot_response(user_input):
    inputs = tokenizer(user_input, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_new_tokens=100,
        no_repeat_ngram_size=3,
        early_stopping=True,
        repetition_penalty=1.5,
        temperature=0.7
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

if __name__ == "__main__":
    print("💬 Health Insurance Chatbot 💬")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Bot: Goodbye!")
            break
        bot_reply = get_bot_response(user_input)
        print(f"Bot: {bot_reply}")
