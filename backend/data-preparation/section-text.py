import os
import re

def section_text(book_text):
    sections = []
    main_sections = re.split(r'\n(?=\s*Section \d+)', book_text)

    for section in main_sections:
        sub_sections = re.split(r'\n(?=\d+\.\d+)', section)

        sections.append({
            'main_section': clean_text(sub_sections[0].strip()),  # Clean main section too
            'sub_sections': [clean_text(s) for s in sub_sections[1:]]  # Clean sub-sections too
        })

    return sections

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces/newlines with a single space
    text = text.strip()  # Strip leading/trailing whitespace
    return text.lower()  # Convert to lowercase

def process_files(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(input_dir, filename)

            with open(file_path, 'r', encoding='utf-8') as f:
                book_text = f.read()

            sectioned_text = section_text(book_text)

            # Create a corresponding output file name
            output_file_name = f'sectioned_text-{filename}'
            output_file_path = os.path.join(output_dir, output_file_name)

            with open(output_file_path, 'w', encoding='utf-8') as f:
                for section in sectioned_text:
                    f.write(section['main_section'] + '\n\n\n\n')
                    for sub_section in section['sub_sections']:
                        f.write('    ' + sub_section + '\n\n\n\n')
                    f.write('\n\n\n\n')

if __name__ == "__main__":
    input_dir = 'data-preparation/datasets/text-extracted'
    output_dir = 'data-preparation/datasets/text-sectioned'

    # Make sure dir exists
    os.makedirs(output_dir, exist_ok=True)

    process_files(input_dir, output_dir)
    print("Done sectioning")
