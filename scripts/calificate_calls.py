# Standar imports
import os
from io import BytesIO

# Third-party imports
import pandas as pd
import requests
from openai import OpenAI
from dotenv import load_dotenv

from auxiliar_fucntions import  absolute_path
# Load environment variables from .env file
load_dotenv(override=True)

## Define some functions
def calificate_call(call_transcript: str):

    promp_calificate_AI_path = absolute_path('../prompts/calificate_call_v2.prompt')
    # System promt to the AI
    with open(promp_calificate_AI_path, 'r') as file:
        promt_calificate_AI = file.read()  # read all content

    # Create the client for OpenAI
    client = OpenAI()

    completion = client.chat.completions.create(
    model="gpt-4o",
    temperature = 0,
    messages=[
        {"role": "system", "content": f"{promt_calificate_AI}"},
        {"role": "system", "content": f"{call_transcript}"},
    ]
    )

    return str(completion.choices[0].message.content)

def calificate_calls_from_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function takes a DataFrame with the leads report and adds a new two columns with the transcript of the calls,
    and the calification of the calls.

    Parameters:
    df (pd.DataFrame): The DataFrame with the leads report.

    Returns:
    pd.DataFrame: The DataFrame with the new columns.
    """
    # Create an empty list to store the transcripts
    transcripts = []

    for index, row in df.iterrows():
        recording_url = row['recording_location']
        
        try:
            # Step 1: Download the audio file (but don't save it to disk)
            response = requests.get(recording_url)
            if response.status_code == 200:
                audio_data = BytesIO(response.content)  # Store audio data in memory
                
                # Step 2: Send the audio data to the endpoint as a file
                DOMAIN_DIARIZATION_SERVER = os.getenv("DOMAIN_DIARIZATION_SERVER")
                files = {'audio_file': ('audio.mp3', audio_data, 'audio/mpeg')}
                process_audio_response = requests.post(f"{DOMAIN_DIARIZATION_SERVER}/process-audio", files=files)

                # Step 3: Check if the request was successful and extract the "messages" key from the JSON response
                if process_audio_response.status_code == 200:
                    response_json = process_audio_response.json()
                    transcript = str(response_json.get("messages"))  # Convert the list to a string

                else:
                    transcript = "Error: Failed to process audio"
            else:
                transcript = "Error: Failed to download audio"
        
        except Exception as e:
            transcript = f"Error: {str(e)}"
        
        # Add the transcript to the list
        transcripts.append(transcript if "Error" not in transcript else "")
    
    # Add the new "transcript" column to the DataFrame
    df['transcript'] = transcripts
    

    # Calificate the calls regarding of transcript
    califications = []
    for index, row in df.iterrows():
        califications.append(calificate_call(row['transcript']))

    # Add the new "calification" column to the DataFrame
    df['calification'] = califications

    return df