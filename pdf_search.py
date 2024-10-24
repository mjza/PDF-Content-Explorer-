import os
import re
from PyPDF2 import PdfReader
import argparse
from tqdm import tqdm  # For the progress bar

def search_keyword_in_pdf(pdf_file, regex_pattern):
    """Search for the regex pattern in the text extracted from the PDF."""
    try:
        with open(pdf_file, 'rb') as f:
            reader = PdfReader(f)
            pdf_text = ""

            # Extract text from all pages
            for page_num in range(len(reader.pages)):
                page_text = reader.pages[page_num].extract_text()
                if page_text:
                    pdf_text += "\n" + page_text

            # Search for the regex pattern in the extracted text
            matches = set(re.findall(regex_pattern, pdf_text, re.IGNORECASE | re.DOTALL))

            # If matches found, return them
            if matches:
                return matches
    except Exception as e:
        print(f"Error reading {pdf_file}: {e}")
    return None

def search_in_folder(source_folder, regex_pattern, output_file):
    # Clean the output file (open it in 'w' mode to clear the content)
    with open(output_file, 'w') as out_file:
        out_file.write('')  # This clears the file
        out_file.flush()

    """Search for the regex pattern in all PDF files in the source folder and write the results to the output file."""
    # Get list of PDF files
    pdf_files = [f for f in os.listdir(source_folder) if f.endswith(".pdf")]

    # Open the output file in append mode
    with open(output_file, 'a') as out_file:
        # Initialize progress bar with tqdm
        with tqdm(total=len(pdf_files), desc="Processing PDFs") as pbar:
            for filename in pdf_files:
                # Update the progress bar description with the current file name
                pbar.set_description(f"Processing {filename}")

                pdf_path = os.path.join(source_folder, filename)
                matches = search_keyword_in_pdf(pdf_path, regex_pattern)

                if matches:
                    # Write the unique matches to the output file
                    out_file.write(f"{filename} => {', '.join(matches)}\n")
                    out_file.flush()  # Ensure the file is written to immediately after processing the PDF

                # Update the progress bar
                pbar.update(1)

    print(f"Search complete. Matches saved to {output_file}")

def main():
    """Main function to handle argument parsing and initiating the search."""
    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(description="Search for a regex pattern in multiple PDFs.")
    
    # Add arguments for source folder, regex, and output file
    parser.add_argument('-s', '--source', type=str, required=True, help='Source folder containing PDFs')
    parser.add_argument('-r', '--regex', type=str, required=True, help='Regex pattern to search for in the PDFs')
    parser.add_argument('-d', '--destination', type=str, required=True, help='Destination output text file for results')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the search function
    search_in_folder(args.source, args.regex, args.destination)

if __name__ == "__main__":
    main()
