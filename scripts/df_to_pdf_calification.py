import pandas as pd
import markdown2
import pdfkit

from auxiliar_functions import transcripts_to_md

def df_to_pdf(df: pd.DataFrame, output_pdf_path: str, css_path: str) -> None:
    """
    Converts the DataFrame into a PDF using Markdown formatting and applies a CSS style.

    Parameters:
    df (pd.DataFrame): The DataFrame with the lead reports.
    output_pdf_path (str): The path where the PDF file will be saved.
    css_path (str): The path to the CSS file for styling the PDF.
    """
    # Initialize an empty string to store the entire markdown content
    markdown_content = ""

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        # Transfrom transcript to markdown
        try:
            print(row['transcript'])
            transcript = transcripts_to_md(row['transcript'])
        except:
            transcript = None

        if transcript:
            # Construct the markdown content for each row
            line_content = f"---\n\n\n# Evaluation for {row['full_name']}\n".upper()
            line_content += f"\n{row['calification'].replace('# ', '## ')}\n"
            line_content += f"\n{transcript}\n"
            
            # Append this line to the overall markdown content
            markdown_content += line_content
    
    if markdown_content != "":
        # Convert Markdown content to HTML
        html_content = markdown2.markdown(markdown_content)

        # Read and add CSS to HTML
        with open(css_path, 'r') as css_file:
            css_content = css_file.read()
        
        # Combine CSS and HTML
        html_content_with_style = f"<style>{css_content}</style>{html_content}"

        # Convert HTML to PDF with css
        pdfkit.from_string(html_content_with_style, output_pdf_path)

# Usage example:
# Assuming `df` is your DataFrame
# df_to_pdf(df, 'output.pdf', 'path/to/styles.css')
