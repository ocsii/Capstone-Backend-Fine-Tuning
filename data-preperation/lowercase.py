import re

def read_and_preprocess_file(input_file='data-preperation/datasets/text-sectioned/save.txt', 
                             output_file='lowercase_handbook.txt'):
    """Read, convert to lowercase, strip whitespace, and save the content to a new file."""
    with open(input_file, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    # Split text into sections using two or more newlines
    sections = re.split(r'\n{3,}', raw_text)

    # Process each section
    processed_sections = [process_section(section) for section in sections]

    # Save processed text into the output file
    with open(output_file, 'w', encoding='utf-8') as f_out:
        for section in processed_sections:
            f_out.write(section + "\n\n")

    print(f"Processed text saved to {output_file}")

def process_section(section):
    """Convert text to lowercase and strip whitespace while keeping sectioning intact."""
    lines = section.splitlines()
    processed = []
    
    for line in lines:
        line = line.strip().lower()  # Convert to lowercase and strip whitespace
        if line:  # Only add non-empty lines
            processed.append(line)
    
    # Join the processed lines with a full stop at the end of each line
    return '. '.join(processed) + ('.' if processed else '')

# Run the preprocessing function
if __name__ == "__main__":
    read_and_preprocess_file()
    print("Done")
