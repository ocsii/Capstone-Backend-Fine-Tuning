import pdfplumber
import os

# Use PDF plumber to extract everything (tables, graphs (most) and text) into plain text format


# Directory paths
input_dir = 'data-preperation/datasets/text-raw-datasets'
output_dir = 'data-preperation/datasets/text-extracted'


# Make sure dir exists
os.makedirs(output_dir, exist_ok = True)

# Separate the landscape pdfs into two sections because pdfplumber by default 
# reads from left to right, disregarding 
def extract_text_landscape(pdf):
    extracted_text = ''

    for page in pdf.pages:

        # Ensure is landscape
        if page.width > page.height:
            # Separate into two sections
            left_section = (0, 0, page.width / 2 , page.height)
            right_box = (page.width / 2, 0, page.width, page.height)

            # Extract text from each section
            left_text = page.within_bbox(left_section).extract_text() or ''
            right_text = page.within_bbox(right_box).extract_text() or ''

            extracted_text += left_text + '\n\n' + right_text + '\n\n'
        else:
            extracted_text += page.extract_text() or ''
    
    return extracted_text


# Extract text
def extract_text (input_dir, output_dir):

    for filename in os.listdir(input_dir):

        if filename.endswith('.pdf'):
            pdf_path = os.path.join(input_dir, filename)
            extracted_text = ''

            try: 
                # Open PDF file 
                with pdfplumber.open(pdf_path) as pdf:

                    # Check orientation of second page (first page / cover page might be different)
                    if len(pdf.pages) > 1:
                        random_page = pdf.pages[1]  
                        is_landscape = random_page.width > random_page.height
                    else: 
                        page = pdf.pages[0]
                        is_landscape = page.width > page.height

                    # Extract data based on portrait or landscape
                    if is_landscape:
                        extracted_text = extract_text_landscape(pdf)
                    else: 
                        # Open PDF file and extract text
                        for page in pdf.pages:
                            extracted_text += page.extract_text() or ''

                    # Set the output filename
                    output_filename = f"{os.path.splitext(filename)[0]}_extracted.txt"
                    output_path = os.path.join(output_dir, output_filename)
                    
                    # Store extract text in (.txt file)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(extracted_text.lower())

                    print(f"Succesfully processed {filename}")

            except Exception as e:
                print(f"Error procesing {filename}: {e}")


if __name__ == "__main__":
    extract_text(input_dir, output_dir)
    print("Done extraction")