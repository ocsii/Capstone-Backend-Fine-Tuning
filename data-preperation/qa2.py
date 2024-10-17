from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
import json

# Load the T5 model and tokenizer
model_name = "t5-small"
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

# Path to the input file containing tokenized text
input_file_path = 'data-preperation/datasets/text-tokenised/tokenised.txt'
output_file_path = 'data-preperation/datasets/qa_pairs.json'

def create_qa_pairs(file_path, num_questions=5):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Prepare input for T5 model (e.g., "generate questions: [context]")
    input_text = f"generate questions: {text}"
    
    # Tokenize input text
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    # List to hold all generated questions
    questions = []

    # Generate the specified number of questions
    for i in range(num_questions):
        print(f"Generating question {i + 1}/{num_questions}...")  # Debugging output
        with torch.no_grad():
            outputs = model.generate(input_ids, max_length=50)

        question = tokenizer.decode(outputs[0], skip_special_tokens=True)
        questions.append(question)

        # Print the generated question for debugging
        print(f"Generated question: {question}")

    # Create QA pairs (assuming text as the answer)
    qa_pairs = [{"question": question, "answer": text} for question in questions]

    return qa_pairs

def save_qa_pairs(qa_pairs, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(qa_pairs, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    qa_pairs = create_qa_pairs(input_file_path, num_questions=5)
    save_qa_pairs(qa_pairs, output_file_path)
    print(f"QA pairs have been saved to {output_file_path}.")
