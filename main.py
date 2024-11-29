import re
import os
import requests
#from langchain_together import ChatTogether
from langchain_community.chat_models import ChatPerplexity
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import YoutubeLoader
from langchain import LLMChain
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from requests.auth import HTTPBasicAuth

app = Flask(__name__)
load_dotenv()

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

llm_chat = ChatPerplexity(api_key=os.getenv('PERPLEXITY_API'), temperature=0.2, model="llama-3.1-sonar-small-128k-online")



user_chat_mode = {}

def is_youtube_url(url):
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    return bool(youtube_regex.match(url))

def summarise(video_url):
    loader = YoutubeLoader.from_youtube_url(video_url, add_video_info=False)
    data = loader.load()
    product_description_template = PromptTemplate(
        input_variables=["video_transcript"],
        template="""
        Read through the entire transcript carefully.
        Provide a concise summary of the video's main topic and purpose.
        Extract and list the five most interesting or important points from the transcript. For each point: State the key idea clearly and concisely.
        
        Ensure your summary and key points capture the essence of the video without including unnecessary details.
        Use clear, engaging language that is accessible to a general audience.
        If the transcript includes any statistical data, expert opinions, or unique insights, prioritize including these in your summary or key points.
        
        video transcript: {video_transcript}"""
    )
    chain = LLMChain(llm=llm_chat, prompt=product_description_template)
    summary = chain.invoke({"video_transcript": data[0].page_content})
    return summary['text']

def chat_response(message):
    response_template = PromptTemplate(
        input_variables=["user_message"],
        template="""
        You are NioBot, a helpful and friendly AI assistant created by Ionio.ai. Your goal is to assist the user with their queries in a polite, conversational, and professional tone. 
        Guidelines for your response:
        1. Whenever the user asks a question, look up the query online to fetch the latest information. Use your online search capabilities to verify the data. Ensure to search from reliable sources.
        2. Use the verified data to generate a precise and accurate response.
        3. If the query cannot be verified online or is ambiguous, politely ask the user for clarification.
        4. Avoid unnecessary details or fluff while maintaining a polite and approachable tone.
        5. In your response avoid including "[1][2]" such reference numbers. Instead, provide the information in a clear manner.
        User says: {user_message}
        Generate a response that is clear, polite, and engaging.
        """
    )
    chain = LLMChain(llm=llm_chat, prompt=response_template)
    response = chain.invoke({"user_message": message})
    return response['text']

def respond(message):
    response = MessagingResponse()
    response.message(message)
    return Response(str(response), content_type="application/xml")


@app.route('/summary', methods=['POST'])
def summary():
    url = request.form.get('Body').strip()
    sender = request.form.get('From') 
    media_url = request.form.get('MediaUrl0')
    print(f"Received message from {sender}: {media_url or url}")

    
    if media_url: 
        try:
            r = requests.get(media_url, auth=HTTPBasicAuth(
                os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN')))
            content_type = r.headers['Content-Type']
            username = sender.split(':')[1] 
            user_dir = f'uploads/{username}'
            if not os.path.exists(user_dir):
                os.makedirs(user_dir)

            if content_type == 'image/jpeg':
                filename = f'{user_dir}/{username}.jpg'
            elif content_type == 'image/png':
                filename = f'{user_dir}/{username}.png'
            elif content_type == 'image/gif':
                filename = f'{user_dir}/{username}.gif'
            else:
                return respond('The file that you submitted is not a supported image type.')

            with open(filename, 'wb') as f:
                f.write(r.content)
                print(f"Image saved as: {filename}")
            return respond('Thank you! Your image was received.')
        except Exception as e:
            print(f"Error handling media: {e}")
            return respond("Sorry, I couldn't process your image. Please try again.")

    
    if sender not in user_chat_mode:
        user_chat_mode[sender] = False  
        response = ("Hello! I'm NioBot, created by the developers at Ionio.ai. "
                    "I can assist you with basic queries in /chat mode. "
                    "You can switch to Summary mode by typing /summary. In this mode, simply provide a valid YouTube link, and I'll generate a concise summary of the video for you!")
    elif url.lower() == "/chat":
        user_chat_mode[sender] = True
        response = ("You've entered /chat mode! Ask me anything, and I'll do my best to help you out. "
                    "If you want to switch back to /summary mode, just send me a YouTube link!")
    elif url.lower() == "/summary":
        user_chat_mode[sender] = False
        response = ("You've entered /summary mode! Please send a valid YouTube link, and I'll summarize the video for you!")
    else:
        try:
            if user_chat_mode[sender]:
                response = chat_response(url)
            elif is_youtube_url(url):
                response = summarise(url)
            else:
                response = "Please enter a valid YouTube video URL or type '/chat' to enter chat mode."
        except Exception as e:
            print(f"Error generating response: {e}")
            response = "Oops! Something went wrong. Please try again later."

    print(f"Generated response: {response}")
    return respond(response)

if __name__ == '__main__':
    app.run(port=4040)
