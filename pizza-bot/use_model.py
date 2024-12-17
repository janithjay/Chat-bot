import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load the fine-tuned model and tokenizer
model_path = 'D:\Github\Chat-bot\pizza-bot\fine_tuned_gpt2'  # Path to your fine-tuned model
model = GPT2LMHeadModel.from_pretrained(model_path)
tokenizer = GPT2Tokenizer.from_pretrained(model_path)

def generate_text(prompt, max_length=50, temperature=0.7, top_k=50, top_p=0.95):
    input_ids = tokenizer.encode(prompt, return_tensors='pt').to(device)

    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_length=max_length,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            num_return_sequences=1
        )

    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

# Example usage for a PizzaBot
if __name__ == "__main__":
    user_query = "What can you tell me about our special pizzas?"
    prompt = f"In response to the user's query: '{user_query}', "
    generated_text = generate_text(prompt)
    print("PizzaBot says:", generated_text)