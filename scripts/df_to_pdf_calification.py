import pandas as pd
import markdown2
import pdfkit

def df_to_pdf(df: pd.DataFrame, output_pdf_path: str) -> None:
    """
    Converts the DataFrame into a PDF using Markdown formatting.

    Parameters:
    df (pd.DataFrame): The DataFrame with the lead reports.
    output_pdf_path (str): The path where the PDF file will be saved.
    """
    # Initialize an empty string to store the entire markdown content
    markdown_content = ""

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        # Construct the markdown content for each row
        line_content = f"**Evaluation for {row['full_name']}**\n"
        line_content += f"{row['calification']}\n"
        line_content += f"{row['transcript']}\n"
        
        # Append this line to the overall markdown content
        markdown_content += line_content

    # Convert Markdown content to HTML
    html_content = markdown2.markdown(markdown_content)

    # Convert HTML to PDF
    pdfkit.from_string(html_content, output_pdf_path)

# Usage example:
# Assuming `df` is your DataFrame
# df_to_pdf(df, 'output.pdf')
