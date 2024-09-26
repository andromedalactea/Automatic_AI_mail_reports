# Standar imports
import os
from io import BytesIO

# Third-party imports
import pandas as pd
import requests
from openai import OpenAI
from dotenv import load_dotenv

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
        
        # transcript = """[{'content': " Hi, my name is Ladina, and I'm calling with Adventist Pay. May I speak to the business owner, please? It's her. Okay, great. So I was just reaching out about a new federal policy, and it simply states that you no longer have to pay transaction fees. You are currently paying those fees for your business, correct? No, we don't take credit cards. Is there a reason why you don't take credit cards now? Yeah, bad experiences.  Okay. Well, you know, we do offer 0% processing, and I can really assure you that you won't have any bad experience with us, because it's only $25 a month, and we don't have contracts, so you won't be in a contract or anything. It'll just be a month-to-month type of thing. My manager could explain more to you, and she did just have them call. Okay, so what if the client defeats the charge after we did the work?", 'role': 'assistant'}, {'content': "Hi, this is Treasure, one of the managers here at Adventist Pay. How are you, ma'am?", 'role': 'user'}, {'content': " I'm fine.", 'role': 'assistant'}, {'content': "Great. So you were asking about disputes. So we take our disputes very seriously, and we do investigate. So if the client disputes the charge, you're still going to receive those funds. We do same-day processing. So you're still going to receive those funds, and we're going to gather information from you, and the bank is going to do their investigation.", 'role': 'user'}, {'content': "Yeah, and then the client's disputed again, and then  You guys send them a message, and then they dispute it again, and you guys end up giving in to them.", 'role': 'assistant'}, {'content': "No, we have very low chargebacks. We have very, very low chargebacks. So you don't have to worry about that with us, because we take that part of the business very, very seriously. And as the associate were stating, it's a 60-day free trial. And that's just for you to try out the services to see if it evaluates.  and for you to evaluate it and see if it works well with your company. But we have really low charge back rates here at Aventus Pay. We do not grant. We know customers like to dispute charges and try to get their money back, and that's considered as fraud. So we do not. We take it serious. We don't just give them a slap on the back and send them their funds. So if they made that purchase and we can prove it, they will not get that money back.", 'role': 'user'}, {'content': " They're going to have... How do you prove it when it's labor done?", 'role': 'assistant'}, {'content': "I'm sorry?", 'role': 'user'}, {'content': "When we go and do a job and it's labor, how do you prove that they got the merchandise?", 'role': 'assistant'}, {'content': "Well, we take, you know, we have you send over stuff on our end. We do our investigation, so we may ask you for documentation and we may, you know, the bank does things like,  they go into the customer's app and look at their location. If they're sharing their location with that app, they can see where were they at this time. I mean, it's not my field, so I can't really break it down exactly how it will work. But I do know here at Eventus Pay, our chargebacks are really, really low.  So we do not rent.", 'role': 'user'}, {'content': "We're mostly commercial, so we deal with management companies. And they don't use credit cards. So that's 95% of our business. So basically, I would be paying $25 a month and lucky if I do one transaction during that month.", 'role': 'assistant'}, {'content': "So do you accept? So you do accept debit and credit cards at the moment, but you just don't take many of them?", 'role': 'user'}, {'content': " Well, no, they pay through Intuit, our accounting program. So that's the way we do it. But we don't do actual credit cards through a machine anymore.", 'role': 'assistant'}, {'content': 'Yeah, you do it through invoice, correct?', 'role': 'user'}, {'content': 'Right. But we have to do it through Intuit, the accounting program. Yeah, so we have a virtual terminal.', 'role': 'assistant'}, {'content': 'We have a virtual terminal where you will be able to send those  invoices out via email or text message as well.', 'role': 'user'}, {'content': "But I already have that and I don't have to pay a high fee. So how much do you pay now? We had to pay, we were paying for a credit card machine and we were barely using it and paying all these fees. So we were losing money on it and then  We had a couple people dispute that we did the work. I then sent the text messages between the client and how they were happy and blah, blah, blah. And then they disputed it two times. They first sided with us, and then the customer kept disputing it, and the bank just gave up and said we would have to take them to small claims court.", 'role': 'assistant'}, {'content': "Oh, no. Yeah, no. We don't work like that.  We're not going to give, you know, if that work was done and you can prove it, we can prove it. We're not going to just give the customers their money no matter how many times they dispute it. You know, we don't operate that way. And as far as you, you're saying that you were paying fees and you wasn't using the credit card machine, with us, there's no processing fee. It's just a $25 monthly fee. And if you went all month and you haven't had not one credit or debit card transaction,  We will waive that $25 monthly payment from you. So you don't have to worry about that. All right.", 'role': 'user'}, {'content': 'Let me talk to my husband. Let me talk to my husband and see if he wants to try it again.', 'role': 'assistant'}, {'content': 'OK. And I just have one question. So when you do accept Deben credit cards, how much would you say that you do monthly?', 'role': 'user'}, {'content': "Hardly anything. Everything's done through track or electronic.", 'role': 'assistant'}, {'content': "OK. OK. So you're not, yeah. OK. All right. So yeah, just go ahead and check with your husband. What is your first name? April.  April, okay April, my name is Treasure. So you can go ahead and check with your husband and when would you like for me to follow up? Is Monday morning okay or maybe later today?", 'role': 'user'}, {'content': 'Monday morning is fine.', 'role': 'assistant'}, {'content': "Alrighty, perfect. Okay April, you'll be looking for McCaw for me, okay?", 'role': 'user'}, {'content': 'Thanks.', 'role': 'assistant'}, {'content': 'Okay, bye-bye.', 'role': 'user'}, {'content': 'Bye.', 'role': 'assistant'}]"""

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