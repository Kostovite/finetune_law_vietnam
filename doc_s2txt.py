import os
import subprocess

def convert_doc_to_txt(input_path, output_path):
    """
    Convert .doc and .docx files to .txt using LibreOffice in headless mode.
    """
    try:
        subprocess.run(
            [
                "libreoffice", 
                "--headless",   # Run LibreOffice without GUI
                "--convert-to", "txt:Text",   # Convert to .txt
                "--outdir", os.path.dirname(output_path),  # Specify output directory
                input_path
            ],
            check=True
        )
        print(f"Converted {input_path} to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {input_path} to TXT: {e}")

def convert_all_docs_to_txt(input_dir, output_dir):
    """
    Convert all .doc and .docx files in the input directory to .txt files in the output directory.
    Keeps the original filenames, just changes the extension to .txt.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_name in os.listdir(input_dir):
        input_path = os.path.join(input_dir, file_name)
        output_path = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.txt")

        if file_name.endswith((".doc", ".docx")):
            # Convert .doc or .docx to .txt using LibreOffice
            convert_doc_to_txt(input_path, output_path)

# Define input and output directories
input_directory = "./Vietnam-Law-Raw-Data/luat_bo_luat"
output_directory = "./Vietnam-Law-txt"

# Run the conversion
convert_all_docs_to_txt(input_directory, output_directory)