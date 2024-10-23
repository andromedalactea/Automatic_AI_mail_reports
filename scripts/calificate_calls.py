# Standar imports
import os
import re
from io import BytesIO

# Third-party imports
import pandas as pd
import requests
from openai import OpenAI
from dotenv import load_dotenv
import base64


from auxiliar_functions import  absolute_path
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

def calificate_call_from_direct_audio(audio_url: str, context_call: str) -> tuple:
    # Fetch the audio file and convert it to a base64 encoded string
    response = requests.get(audio_url)
    response.raise_for_status()
    wav_data = response.content
    encoded_string = base64.b64encode(wav_data).decode('utf-8')
    promp_calificate_AI_path = absolute_path('../prompts/calificate_call_from_direct_audio_v2.prompt')
    with open(promp_calificate_AI_path, 'r') as file:
        promt_calificate_AI = file.read()  # read all content

    # Create the client for OpenAI
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-audio-preview",
        modalities=["text"],
        messages=[
            {
                "role": "user",
                "content": [
                    { 
                        "type": "text",
                        "text": promt_calificate_AI
                    },
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": encoded_string,
                            "format": "mp3"
                        }
                    },
                    {
                        "type": "text",
                        "text": context_call
                    }
                ]
            },
        ],
        max_tokens=7000,
        temperature=0
    )
    
    transcript_qualification = str(response.choices[0].message.content)
    transcript_qualification_1 = """<transcript>
Kathy (Customer Service): Thank you for calling [Business Name], this is Kathy. How can I help you?
Sarah (Fronter): Hi, good morning, Kathy. My name is Sarah. I was just reaching out with Aventus Pay. Is the business owner available?
Kathy (Customer Service): You can speak with me. How can I help you?
Sarah (Fronter): Okay, great. I was just reaching out regarding a new federal policy that no longer requires for business owners like yourself to pay those processing fees when accepting credit and debit cards as a form of payment. Are you currently paying those transaction fees when your business accepts credit and debit cards at the moment?
Kathy (Customer Service): Well, I guess my question for you is, so what is your company doing exactly?
Sarah (Fronter): Yes, we are a 0% processing company. We eliminate your processing fees down to a 0%. I do have my manager on the line, they did just join the call, and they can explain in detail how our 0% processing works. Just one moment.
Adam (Closer): Hi, this is Adam Pierce. I'm one of the sales managers here at Aventus Pay. How are you?
Kathy (Customer Service): I'm fine, how are you?
Adam (Closer): Good, good. I'm sorry, I came on kind of late there. I didn't catch your name. Who am I speaking with?
Kathy (Customer Service): My name's Kathy.
Adam (Closer): Kathy, alright. Well, Kathy, so just as you heard, we do have an option here now for folks if they want to stop paying the processing fees, we have a way to get that done. Have you heard of anything called a cash discount before?
Kathy (Customer Service): Mm-mm.
Adam (Closer): Right. So the way it works is our equipment, which we provide for free, is going to show the full true cost now for anyone using a credit card. Where your transaction is normally $100, it's going to show $104 for folks. And if they want to use a discount by paying in cash or check, you can deduct that amount...
Kathy (Customer Service): You know what, I am so sorry, but I have another call coming in, and I do have to take that.
Adam (Closer): Oh, is there a time I should call you back?
Kathy (Customer Service): You know, I don't think that's going to be something we're going to be interested in, but thank you very much. You have a good day.
Adam (Closer): Alright, you too.
Kathy (Customer Service): Bye.
Adam (Closer): Bye.
<transcript>

<qualification>
# Call Performance Evaluation Report

## Overall Performance Score
- **Fronter (Sarah)**: 20/30
- **Closer (Adam)**: 10/20
- **Conversation Difficulty Modifier**: +1 for both agents

## Detailed Performance Breakdown

### Fronter Evaluation (Sarah)
- **Engagement and Introduction**: 7/10
  - Sarah initiated the conversation with a polite and clear introduction, effectively identifying herself and the purpose of the call.
- **Value Proposition Communication**: 6/10
  - She communicated the value proposition of eliminating processing fees but could have provided more detailed information to engage Kathy further.
- **Transition to Closer**: 7/10
  - The transition to Adam was smooth, but it could have been more engaging to ensure Kathy was prepared for the detailed explanation.

### Closer Evaluation (Adam)
- **Objection Handling**: 5/10
  - Adam attempted to explain the cash discount concept but did not effectively address Kathy's implicit objection or disinterest.
- **Closing Attempt**: 5/10
  - He asked about a callback time but did not attempt to secure a commitment or explore further interest before the call ended.

## Conversation Difficulty
- **Difficulty Level**: 2/5
  - Kathy was polite but seemed disinterested and was quick to end the call. The agents faced a challenge in maintaining her interest and engagement.

## Strengths and Areas for Improvement

### Fronter Strengths
1. **Clear Introduction**: Sarah introduced herself and the company clearly.
2. **Polite Engagement**: Maintained a polite and professional tone throughout.
3. **Smooth Transition**: Transitioned to the closer without any awkward pauses.

### Closer Strengths
1. **Polite and Professional**: Maintained a professional demeanor.
2. **Attempted to Re-engage**: Tried to re-engage Kathy by asking for a callback time.

### Fronter Areas for Improvement
1. **Value Proposition Depth**: Provide more detailed information to capture interest.
2. **Engagement Techniques**: Use questions to engage the prospect more actively.
3. **Transition Preparation**: Ensure the prospect is ready and interested before transitioning.

### Closer Areas for Improvement
1. **Objection Handling**: Develop strategies to address disinterest or objections more effectively.
2. **Closing Techniques**: Work on securing a commitment or next steps even if the prospect seems disinterested.
3. **Adaptability**: Adapt the pitch based on the prospect's responses to maintain engagement.

## Recommendations
1. **Training on Engagement**: Both agents could benefit from training on techniques to maintain and increase prospect engagement.
2. **Objection Handling Workshops**: Conduct workshops to improve handling objections and disinterest.
3. **Role-Playing Sessions**: Practice role-playing to simulate difficult conversations and improve adaptability.
4. **Feedback Sessions**: Regular feedback sessions to discuss call recordings and identify areas for improvement.

## Final Comments
Both Sarah and Adam demonstrated professionalism and politeness during the call. While the conversation was challenging due to Kathy's disinterest, there are opportunities to enhance engagement and objection handling skills. By focusing on these areas, both agents can improve their effectiveness in future calls. Keep up the good work and continue to refine your techniques!
<qualification>"""
    print(transcript_qualification)
    # Definir los patrones de las etiquetas con expresiones regulares
    transcript_pattern = r"<transcript>\s*(.*?)\s*<transcript>"
    qualification_pattern = r"<qualification>\s*(.*?)\s*<qualification>"

    # Buscar la transcripción
    transcript_match = re.search(transcript_pattern, transcript_qualification, re.DOTALL)
    transcript = transcript_match.group(1) if transcript_match else None

    # Buscar la calificación
    qualification_match = re.search(qualification_pattern, transcript_qualification, re.DOTALL)
    qualification = qualification_match.group(1) if qualification_match else None

    return transcript, qualification

def calificate_calls_from_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function takes a DataFrame with the leads report and adds two new columns: one with the transcript of the calls,
    and the other with the qualification of the call.

    Parameters:
    df (pd.DataFrame): The DataFrame with the leads report.

    Returns:
    pd.DataFrame: The DataFrame with the transcript and qualification columns.
    """
    
    # Lists to store the results
    transcripts = []
    qualifications = []
    qualification_from_audio = []

    for index, row in df.iterrows():
        recording_url = row['recording_location']
        transcript, qualification = None, None

        # Step 1: Try the primary path (process call audio directly via OpenAI)
        try:
            # Extrcat infor from df to provide context for the qualification:
            first_name = row['first_name'] if pd.notna(row['first_name']) else "Unknown"
            lead_id = row['lead_id'] if pd.notna(row['lead_id']) else "Unknown"

            context_call = f"""This is some context for the call (For executive summary but is possible to use for other parts of the report as well):
            Date of the call: {row['call_date'] if pd.notna(row['call_date']) else 'Unavailable'}
            Duration of the call: {row['length_in_sec'] if pd.notna(row['length_in_sec']) else 'Unavailable'} seconds
            Lead Name/ID: {first_name} ({lead_id})\n\n"
            Company Name: {row['last_name'] if pd.notna(row['last_name']) else 'Unknown'}
            """

            transcript, qualification = calificate_call_from_direct_audio(recording_url, context_call)
            # transcript, qualification = None, None
        except Exception as e:
            print(f"Exception during OpenAI evaluation for URL {recording_url}: {str(e)}")
            transcript = None
            qualification = None

        # Step 2: If transcript or qualification failed, try alternative flow
        if not transcript or not qualification:
            try:
                # Try processing the audio manually via the diarization service server
                response = requests.get(recording_url)
                response.raise_for_status()  # Raises exception if status_code is not 200

                audio_data = BytesIO(response.content)  # Keep audio in-memory
                DOMAIN_DIARIZATION_SERVER = os.getenv("DOMAIN_DIARIZATION_SERVER")
                files = {'audio_file': ('audio.mp3', audio_data, 'audio/mpeg')}
                
                # Call to the diarization service endpoint
                process_audio_response = requests.post(
                    f"{DOMAIN_DIARIZATION_SERVER}/process-audio", files=files)

                # Check for success status; process the result if successful
                if process_audio_response.status_code == 200:
                    response_json = process_audio_response.json()
                    transcript = str(response_json.get("messages"))  # Extracting `messages` from response
                else:
                    transcript = "Error: Failed to process audio"
                    qualification = "Unavailable"

            except requests.exceptions.RequestException as req_err:
                # Catch network-related errors
                print(f"Error fetching audio from URL {recording_url}: {req_err}")
                transcript = "Error: Failed to download/process audio"
                qualification = "Unavailable"
            except Exception as err:
                # Catch all other errors
                print(f"Unexpected error processing audio: {err}")
                transcript = "Error: " + str(err)
                qualification = "Unavailable"

        # Append results to lists

        qualification_from_audio.append(True if qualification else False)
        transcripts.append(transcript.replace('\n', '\n\n') if transcript else "Transcript not available")
        qualifications.append(qualification.replace('\n', '\n\n') if qualification else calificate_call(transcript))
        print(qualifications)
    # Add the new columns for transcript and qualification
    df['transcript'] = transcripts
    df['qualification'] = qualifications
    df['qualification_from_audio'] = qualification_from_audio
    print(df)
    return df

# Example usage
if __name__ == "__main__":
    url = "http://38.107.174.254/9820/2024-10-14/20241014-114434_5166296266-all.mp3"
    transcript, qualification = calificate_call_from_direct_audio(url)
    print("-"*50,transcript, "-"*50)
    print("-"*50,qualification, "-"*50)