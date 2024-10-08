import pdfplumber
import os

# Use PDF plumber to extract everything (tables, graphs (most) and text) into plain text format


# Directory paths
input_dir = 'datasets/raw-datasets'
output_dir = 'datasets/text-extracted'


# Make sure dir exists
os.makedirs(output_dir, exist_ok = True)


for filename in os.listdir(input_dir):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(input_dir, filename)
        extracted_text = ''

        try: 
            # Open PDF file and extract text
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    extracted_text += page.extract_text() or ''


            # Set the output filename
            output_filename = f"{os.path.splitext(filename)[0]}_extracted.txt"
            output_path = os.path.join(output_dir, output_filename)

            
            # Store extract text in (.txt file)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(extracted_text)

        except Exception as e:
            print(f"Error procesing {filename}: {e}")

print("Text extraction complete")