import spacy

# Load the SpaCy English model
nlp = spacy.load("en_core_web_sm")

# Path to the input and output files
input_file_path = 'data-preperation/datasets/text-sectioned/save.txt'
output_file_path = 'data-preperation/datasets/text-tokenised/tokenised.txt'

def tokenize_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        
    # Tokenize the text using SpaCy
    doc = nlp(text)
    tokens = [token.text for token in doc]

    return tokens

def save_tokens(tokens, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        for token in tokens:
            file.write(f"{token}\n")

if __name__ == "__main__":
    tokens = tokenize_text(input_file_path)
    save_tokens(tokens, output_file_path)
    print(f"Tokens have been saved to {output_file_path}.")
