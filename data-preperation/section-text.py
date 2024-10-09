import os
import re

def section_text (book_text):

    sections = []
    main_sections = re.split(r'\n(?=/s*Section \d+)', book_text)

    for section in main_sections:
        
        sub_sections = re.split(r'\n(?=\d+\.\d+)', section)
        sections.append({'main_section': sub_sections[0].strip(), 'sub_sections': [s.strip() for s in sub_sections[1:]] })
    
    return sections

def process_files (input_dir, output_dir):

    combined_sections = []
    
    for filename in os.listdir(input_dir):

        sectioned_text = ''

        if filename.endswith('.txt'):
            file_path = os.path.join(input_dir, filename)
        
            with open (file_path, 'r', encoding='utf-8') as f:
                book_text = f.read()

            sectioned_text = section_text(book_text)

            combined_sections.append(sectioned_text)
    

    output_file_path = os.path.join(output_dir, 'sectioned_text.txt')

    with open(output_file_path, 'w', encoding='utf-8') as f:
        for sections in combined_sections:
            for section in sections:
                f.write(section['main_section'] + '\n\n\n\n')
                for sub_section in section['sub_sections']:
                    f.write('    ' + sub_section + '\n\n\n\n')  # Indent sub-sections for clarity
                f.write('\n\n\n\n')  # Add an extra newline for better separation

if __name__ == "__main__":

    input_dir = 'data-preperation/datasets/text-extracted'
    output_dir = 'data-preperation/datasets/text-sectioned'

    # Make sure dir exists
    os.makedirs(output_dir, exist_ok = True)

    process_files(input_dir, output_dir)
    print("Done sectioning")




