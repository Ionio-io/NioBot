# NioBot: A Smart WhatsApp Chatbot  

NioBot is a multitasking WhatsApp chatbot designed to make your conversations more productive and interactive. It combines YouTube video summarization with real-time information access using a Retrieval-Augmented Generation (RAG) pipeline. NioBot is built with Twilio’s WhatsApp API and leverages a Large Language Model (LLM) with internet access for seamless, intelligent responses.  

![Architecture Diagram](https://github.com/user-attachments/assets/07b3d52a-e51e-411d-8929-93bb9699691a)

## Features  

- **YouTube Video Summarization**  
  Share a YouTube link, and NioBot generates concise and relevant summaries. Perfect for finding key insights without watching the entire video.  

- **Real-Time Information Retrieval**  
  Ask questions or chat casually—NioBot’s LLM fetches up-to-date information from the internet for accurate responses.  

- **Chat Modes**  
  - **Summary Mode**: For video summarization tasks.  
  - **General Chat Mode**: For regular conversations and information queries.  

## Architecture  

```plaintext
[WhatsApp] <---> [Twilio API] <---> [NioBot Backend]
                             |--> [LLM with Internet Access (Perplexity)]
                             |--> [YouTube Summarizer (RAG Pipeline)]
```

## Tech Stack  

- **Backend**: Python (Flask/FastAPI)  
- **APIs**: Twilio WhatsApp API  
- **LLM**: Integrated with a Perplexity-based model for internet queries  
- **Video Summarization**: RAG pipeline for generating concise insights  
- **Deployment**: Hosted on a cloud server for 24/7 availability  

## Getting Started  

### Prerequisites  

- Twilio account with a WhatsApp Business API setup  
- Python 3.8 or higher  
- API keys for the LLM and YouTube data access  

### Installation  

1. Clone the repository:  
   ```bash  
   git clone https://github.com/yourusername/NioBot.git  
   cd NioBot  
   ```  

2. Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  

3. Add your configuration details in the `.env` file:  
   - Twilio credentials  
   - LLM API key  
   - YouTube API key  

4. Run the bot:  
   ```bash  
   python app.py  
   ```  

5. Connect it to WhatsApp via Twilio's sandbox or production environment.  

## Usage  

- Add the bot to your WhatsApp contacts.  
- To summarize a YouTube video: Send the video link to the bot.  
- For general queries: Just type your question and wait for the response.  

## Future Enhancements  

- Adding vision capabilities for image-based queries.  
- Improving scalability for handling concurrent users.  
- Integrating more video platforms for summarization.  

## Contributing  

Feel free to fork this repository and submit pull requests. Contributions are welcome to make NioBot smarter and more feature-rich!  

## License  

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.  

---  

> Have questions or ideas for improvements? Reach out or open an issue!  

