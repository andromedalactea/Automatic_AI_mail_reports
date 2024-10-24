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
    promp_calificate_AI_path = absolute_path('../prompts/calificate_call_from_direct_audio_v3.prompt')
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
        max_tokens=8000,
        temperature=0
    )
    
    transcript_qualification = str(response.choices[0].message.content)
    transcript_qualification_ = """<transcript>
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
## **Call Performance Evaluation Report**

---

### **Manager's Report**

#### **Executive Summary**

On **October 22, 2024**, a 5-minute call was conducted with lead **Roger G. (ID: 964518)** from **Glenwood Springs**. Agents **Nadine** (Fronter) and **Adam** (Closer) demonstrated strong performance. This report incorporates advanced audio analysis to provide deeper insights into the call dynamics, including emotional tone, speech patterns, and customer engagement levels. Opportunities were identified to enhance engagement and objection handling by providing agents with tailored feedback based on specific observations from the call.

#### **Overall Performance Score** 🌟

- **Conversation Difficulty:** [██░░░░░░░░░] **2/5 (Moderate)**
- **Estimated Lead Quality:** [██████████░░] **80%**
- **Estimated Probability of Deal Closing:** [█████████░░░░] **70%**

---

#### **Agent Performance Summary**

##### **Fronter (Nadine)** 😊

**Total Score:** [██████████░░░] **24/30**

- **Engagement & Introduction:** [████████░░░] **8/10**
- **Value Proposition Communication:** [████████░░░] **8/10**
- **Transition to Closer:** [████████░░░] **8/10**

**Next Steps to Close the Lead:**

1. **Personalized Follow-Up Email** ✉️
   - Send Roger an email summarizing the key benefits discussed.
   - Include a success story relevant to his business.

2. **Schedule Confirmation** 📆
   - Ensure the follow-up call with Adam is confirmed for 11:00 AM as agreed.

##### **Closer (Adam)** 👍

**Total Score:** [███████████░░] **16/20**

- **Objection Handling:** [████████░░░] **8/10**
- **Closing Attempt:** [████████░░░] **8/10**

**Next Steps to Close the Lead:**

1. **Prepare Tailored Rebuttals** 🛠️
   - Review the specific objections raised by Roger and refine responses.

2. **Prepare for the Follow-Up Call** 📞
   - Address Roger's concerns with personalized solutions.

---

#### **Key Metrics Overview** 📊

<table border="1" cellspacing="0" cellpadding="10">
  <thead>
    <tr>
      <th>Metric</th>
      <th>Fronter (Nadine)</th>
      <th>Closer (Adam)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Engagement Rate</strong></td>
      <td>[██████████░░░] <strong>75%</strong></td>
      <td>[███████████░░] <strong>80%</strong></td>
    </tr>
    <tr>
      <td><strong>Average Response Time</strong></td>
      <td>[███░░░░░░░░░░░] <strong>3s</strong></td>
      <td>[██░░░░░░░░░░░░] <strong>2s</strong></td>
    </tr>
    <tr>
      <td><strong>Objection Frequency</strong></td>
      <td>N/A</td>
      <td>2 objections</td>
    </tr>
    <tr>
      <td><strong>Emotional Tone Consistency</strong></td>
      <td>[█████████░░░░] <strong>70%</strong></td>
      <td>[██████████░░] <strong>80%</strong></td>
    </tr>
    <tr>
      <td><strong>Customer Sentiment Score</strong></td>
      <td>[████████░░░] <strong>60%</strong></td>
      <td>[█████████░░░] <strong>70%</strong></td>
    </tr>
  </tbody>
</table>
---

#### **Advanced Audio Analysis** 🎧

##### **Emotional Tone Analysis** 🎭

- **Nadine:**
  - Maintained a **warm and friendly** tone throughout the call.
  - Expressed enthusiasm, especially during the introduction.

- **Adam:**
  - Adopted a **reassuring and confident** tone when handling objections.
  - Mirrored the customer's concern to build rapport.

##### **Speech Rate and Pauses** 🗣️

- **Nadine:**
  - Spoke at a moderate pace (~150 words per minute).
  - Utilized pauses effectively, allowing Roger to process information.

- **Adam:**
  - Slightly slower speech rate (~140 words per minute) when explaining complex points.
  - Paused after addressing objections, encouraging Roger to engage.

##### **Voice Stress Analysis** 📈

- **Customer (Roger):**
  - Slight increase in vocal stress when discussing potential customer reactions to the cash discount program.
  - Stress levels decreased after Adam provided reassurance.

- **Agents:**
  - Both maintained low stress levels, indicating confidence and control.

##### **Sentiment Over Time Graph** 📈

- **Start of Call:** Neutral sentiment.
- **Mid-Call:** Slightly negative when objections were raised.
- **End of Call:** Shifted to positive after effective objection handling.

##### **Emotional Keyword Spotting** 📝

- **Customer:**
  - Used words like "concerned," "not sure," and "customers might not like."

- **Agents:**
  - Used reassuring words like "understand," "benefit," "appreciate," and "opportunity."

##### **Silence and Overlap Detection** ⏱️

- **Interruptions:** None detected; agents allowed Roger to express his thoughts fully.
- **Overlaps:** Minimal, indicating active listening and respect for speaking turns.

##### **Tone Matching and Mirroring** 🎭

- **Agents:**
  - Matched Roger's tone by adopting a calm and considerate demeanor during concerns.
  - Increased energy levels when highlighting benefits to re-engage interest.

##### **Confidence Scoring** 💪

- **Nadine:**
  - High confidence score (**85%**) based on steady pitch and clear articulation.

- **Adam:**
  - Very high confidence score (**90%**), especially during objection handling.

##### **Background Noise and Clarity Assessment** 🔇

- **Call Quality:**
  - Excellent audio clarity from both agents and the customer.
  - No significant background noise detected.

---

#### **Recommendations for Management** 💡

##### **Training Focus Areas**

**For Nadine:**

1. **Incorporate Storytelling** 📖
   - **Action:** Share success stories to enhance emotional connection.
   - **Benefit:** May increase customer engagement levels.

2. **Enhance Value Proposition Clarity** 🔍
   - **Action:** Use relatable analogies.
   - **Benefit:** Simplifies complex concepts, aiding customer understanding.

**For Adam:**

1. **Tailored Objection Handling** 💪
   - **Action:** Utilize the provided rebuttals to address specific concerns.
   - **Benefit:** Addresses customer objections more effectively, improving sentiment.

2. **Introduce a Sense of Urgency** ⏰
   - **Action:** Offer limited-time incentives.
   - **Benefit:** Encourages prompt decision-making.

---

#### **Next Steps** 🚀

- **Implement Advanced Audio Training:**
  - Train agents on vocal techniques to enhance emotional engagement.

- **Develop Tailored Rebuttal Guide:**
  - Create resources based on common objections and effective responses.

- **Schedule Coaching Sessions:**
  - Review call recordings with agents to highlight strengths and areas for improvement.

---

### **Part 2: Agent's Report**

#### **Agent Performance Feedback**

##### **To: Nadine**

**Subject: Performance Evaluation and Personalized Feedback**

---

**Hi Nadine,**

Great job on your call with **Roger G.** on **October 22, 2024**! Your friendly introduction and clear explanation of the call's purpose were excellent.

**Total Score:** [██████████░░░] **24/30**

- **Engagement & Introduction:** [████████░░░] **8/10**
- **Value Proposition Communication:** [████████░░░] **8/10**
- **Transition to Closer:** [████████░░░] **8/10**

**Emotional Tone Analysis:**

- Maintained a warm and enthusiastic tone.
- Your positivity set a welcoming atmosphere for the call.

**Next Steps to Help Close the Lead:**

1. **Send a Friendly Follow-Up Email** ✉️
   - Reinforce the benefits discussed.
   - Share a relatable success story to strengthen the connection.

2. **Confirm the Follow-Up Call** 📆
   - Ensure Roger is prepared and answer any preliminary questions.

3. **Be Available for Questions** ❓
   - Encourage Roger to reach out with any immediate concerns.

**Opportunities to Shine Even Brighter:**

1. **Sprinkle in Some Stories** 📖

   - **Why:** Emotional stories can increase customer engagement.
   - **Tip:** Share experiences of similar businesses benefiting from our services.

2. **Make It Relatable** 🤗

   - **Why:** Analogies help simplify complex ideas.
   - **Example:** "Think of processing fees as tiny leaks—we help you seal them so you keep more earnings."

3. **Monitor Emotional Cues**

   - **Action:** Pay attention to changes in the customer's tone for better responsiveness.

**Keep up the fantastic work!** Your positive energy makes a difference.

---

##### **To: Adam**

**Subject: Performance Evaluation and Tailored Objection Handling**

---

**Hi Adam,**

Excellent job on your call with **Roger G.** on **October 22, 2024**! Your professional demeanor and clear explanations were commendable.

**Total Score:** [███████████░░] **16/20**

- **Objection Handling:** [████████░░░] **8/10**
- **Closing Attempt:** [████████░░░] **8/10**

**Emotional Tone Analysis:**

- Adopted a reassuring tone when addressing Roger's concerns.
- Mirrored Roger's hesitation to build empathy.

**Next Steps to Help Close the Lead:**

1. **Prepare Tailored Rebuttals**

   - Review Roger's specific objections and practice your responses using the examples below.

2. **Customize Your Approach**

   - Focus on addressing his concerns about customer reactions and unfamiliarity with the program.

3. **Highlight a Special Offer**

   - Consider introducing a limited-time incentive to encourage prompt action.

**Tailored Rebuttals for This Call's Objections:**

1. **Objection:** *"I'm not familiar with the cash discount program."*

   **Enhanced Rebuttal:**

   > "I understand it might be new to you, Roger. The cash discount program allows businesses to eliminate processing fees by offering a small discount to customers who pay with cash. This has helped many businesses like yours increase their profits. Would you like to hear how one of our clients benefited from this?"

2. **Objection:** *"I'm concerned my customers might not like this change."*

   **Enhanced Rebuttal:**

   > "That's a valid concern. Interestingly, many customers appreciate the transparency and the option to save by paying with cash. Businesses we've worked with have seen minimal impact on customer satisfaction but significant improvements in their bottom line."

**Tips for Effective Objection Handling:**

- **Listen Actively:** Confirm understanding by summarizing his concerns.
- **Empathize:** Acknowledge his feelings to build trust.
- **Provide Evidence:** Use data or testimonials to support your points.
- **Ask Open-Ended Questions:** Encourage dialogue to uncover deeper concerns.

**Ideas to Boost Your Impact:**

1. **Share Success Stories** 🌟

   - **Example:** "One of our clients saw a 15% increase in monthly revenue after adopting the program."

2. **Create a Friendly Nudge**

   - **Example:** "We have a special offer this month that could maximize your savings right away."

3. **Monitor Emotional Cues**

   - **Action:** Pay attention to changes in Roger's tone to adjust your approach accordingly.

**Keep up the great work!** These strategies will enhance your effectiveness.

---

#### **Final Thoughts for Both of You**

You're both doing an **excellent** job! By incorporating these insights from the audio analysis and making slight adjustments to your approach, you'll make your calls even more engaging and effective. Remember, understanding not just what is said but how it's said can significantly impact the customer's response.

**Let's close this deal and keep those success stories coming!**

If you have any questions or would like to discuss these points further, feel free to reach out. Let's make the next call even better!

**Enjoy your day and happy selling!** 🎉
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