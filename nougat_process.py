import os
import subprocess

# Directory containing the PDF files
pdf_directory = 'C:/Users/rohan/Documents/Quant Textbooks/notion'  # Replace with your directory path

# List all files in the directory
all_files = os.listdir(pdf_directory)

# Filter out only the PDF files
pdf_files = [f for f in all_files if f.endswith('.pdf')]

for pdf in pdf_files:
    pdf_path = os.path.join(pdf_directory, pdf)
    
    print("Running nougat on", pdf_path)
    # Run the nougat command
    cmd = f'nougat "{pdf_path}" -o ./nougat-textbook --no-skipping --recompute'
    print(cmd)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    


    if result.returncode != 0:
        print(f"Error processing {pdf}:")
        print(result.stderr)  # Print the error output
        continue
    else:
        print("Command executed successfully!")
        print(result.stdout)  # Print the standard output
    # Assuming the output file has the same name as the PDF but with a .mmd extension
    mmd_file = os.path.join('./nougat-textbook', pdf.replace('.pdf', '.mmd'))
    if os.path.exists(mmd_file):  # Check if the mmd file exists
        txt_file = mmd_file.replace('.mmd', '.txt')
        
        # Rename the .mmd file to .txt
        os.rename(mmd_file, txt_file)
        print("Final file renamed to .txt for", pdf_path)

print("Processing completed!")
