import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments
from datasets import load_dataset

# Load the dataset and split it into train and validation sets
dataset = load_dataset('text', data_files={'train': 'D:\Github\Chat-bot\pizzadata.txt'})
train_test = dataset['train'].train_test_split(test_size=0.2)  # 80% train, 20% validation

# Load the pre-trained GPT-2 model and tokenizer
model_name = 'gpt2'
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Set the padding token to be the same as the EOS token
tokenizer.pad_token = tokenizer.eos_token  # Set padding token to EOS token

# Tokenize the dataset
def tokenize_function(examples):
    # Tokenize the text and create labels
    return tokenizer(examples['text'], truncation=True, padding='max_length', max_length=512, return_tensors='pt')

# Apply the tokenization
tokenized_datasets = train_test.map(tokenize_function, batched=True)

# Set the labels to be the same as input_ids for language modeling
def set_labels(examples):
    examples['labels'] = examples['input_ids']  # Set labels to input_ids
    return examples

tokenized_datasets = tokenized_datasets.map(set_labels)

# Set training arguments
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy='epoch',  # Set to 'epoch' for evaluation
    learning_rate=2e-5,
    per_device_train_batch_size=2,
    num_train_epochs=3,
    weight_decay=0.01,
    remove_unused_columns=False,  # Set this to False to avoid the error
)

# Create a Trainer instance
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets['train'],
    eval_dataset=tokenized_datasets['test'],  # Pass the validation dataset here
)

# Fine-tune the model
trainer.train()

# Save the model
model.save_pretrained('./fine_tuned_gpt2')
tokenizer.save_pretrained('./fine_tuned_gpt2')