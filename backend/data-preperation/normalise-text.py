import re

def read_and_preprocess_file(input_file='data-preperation/datasets/text-manually-updated/sunway-handbook-manual.txt', 
                             output_file='preprocessed_handbook.txt'):
    """Read, clean, and process the handbook content, saving it to a new file."""
    with open(input_file, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    # Split text into sections using two or more newlines
    sections = re.split(r'\n{3,}', raw_text)

    # Process each section: flatten tables, lists, clean text, and convert to lowercase
    processed_sections = [process_section(section) for section in sections]

    # Save processed text into the output file
    with open(output_file, 'w', encoding='utf-8') as f_out:
        for section in processed_sections:
            f_out.write(section + "\n\n")

    print(f"Preprocessed text saved to {output_file}")

def process_section(section):
    """Flatten structured content, clean text, and convert to lowercase while keeping sectioning intact."""
    lines = section.splitlines()
    processed = []
    current_row = []  # Store parts of the same table row

    for line in lines:
        line = line.strip().lower()  # Convert to lowercase and strip whitespace
        if "|" in line:  # Handle table-like rows
            # Split the row into fields and join them into a single readable sentence
            fields = [field.strip().replace(':', ' is') for field in line.split('|')]
            current_row.append(' | '.join(fields))
        elif current_row:  # If we encounter a new line after a table row, finalize the row
            processed.append('. '.join(current_row))
            current_row = []
        elif line.startswith("-"):  # Handle bullet points or lists
            processed.append(line.lstrip('- ').capitalize())
        elif line:  # Regular text lines
            processed.append(line)

    # Handle any leftover row
    if current_row:
        processed.append('. '.join(current_row))

    # Join all lines into a single paragraph
    return ' '.join(processed)

# Run the preprocessing function
if __name__ == "__main__":
    read_and_preprocess_file()
    print("Done")
