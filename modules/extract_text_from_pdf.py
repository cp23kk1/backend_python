import fitz  # PyMuPDF
import os

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text()

    doc.close()
    return text

def extract_text_from_pdf(source_path: str, destination_path: str, extension: str):
    if not os.path.exists(destination_path):
        raise FileNotFoundError(f"Directory does not exist: {destination_path}")

    file_names: [] = os.listdir(source_path)
    print(file_names)

    for i in range(len(file_names)):
        file_path = f"{source_path}/{file_names[i]}"
        file_name = os.path.splitext(file_names[i])[0]

        print("--------------------------------------------------")
        print(file_path)
        print(file_name)

        output_file_path = f"{destination_path}/{file_name}.{extension}"
        print(output_file_path)

        extracted_text = extract_text(file_path)

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(extracted_text)