from transformers import T5Tokenizer, T5ForConditionalGeneration, pipeline
import json


model_name = "valhalla/t5-small-qg-hl"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# def generate_question(context):
#     input_text = "Generate two to five relevant questions about this context:  "+ context
#     input_ids = tokenizer.encode(input_text, return_tensors="pt")
#     outputs = model.generate(input_ids)
#     question = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # return question


def generate_question(context):
    input_text = f"Generate specific and relevant questions from the following context:\n\n{context}\n\n"
    input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(input_ids, max_length=50, num_return_sequences=1)
    question = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return question


qa_pipeline = pipeline("question-answering")

def read_sectioned_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        sections = f.read().split('\n\n\n\n')
    return sections


def generate_answer(question, context):
    answer = qa_pipeline(question = question, context = context)
    return answer['answer']

def save_qa_pairs(qa_pairs, output_file):
    with open(output_file, 'w', encoding='utf-8')as f:
        json.dump(qa_pairs, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":

    # Store QA Pairs
    qa_pairs = []

    # Section out text into array
    sections = read_sectioned_text('data-preperation/datasets/text-sectioned/save.txt')

    for section in sections:

        if not section.strip():
            continue

        question = generate_question(section)
        answer = generate_answer(question, section)

        qa_pairs.append({'question': question, 'answer': answer, "context": section})

    save_qa_pairs(qa_pairs, 'qa_pairs.json')









