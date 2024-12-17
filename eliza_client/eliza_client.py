import gradio as gr
import requests
import tweepy

# Function to send messages to API
def send_message(input_text):
    url = "http://localhost:3000/stephenA/message"
    headers = {"Content-Type": "application/json"}
    data = {
        "text": input_text,
        "userId": "user",
        "userName": "User"
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        if isinstance(response_json, list) and len(response_json) > 0:
            character_file = response_json[1].get('customeCharacter', {})
            providerData = response_json[1].get('customProvider', {})
            data_fetched = response_json[0].get('text', "No response text found")
            return data_fetched, providerData, character_file
        else:
            return "Invalid response format", "", ""
    else:
        return f"Error: {response.status_code}", "", ""

# Function to post to Twitter
def post_to_twitter(message):
    api_key = "your_api_key"
    api_secret_key = "your_api_secret_key"
    access_token = "your_access_token"
    access_token_secret = "your_access_token_secret"
    try:
        auth = tweepy.OAuth1UserHandler(api_key, api_secret_key, access_token, access_token_secret)
        api = tweepy.API(auth)
        api.update_status(message)
        return "Tweet posted successfully!"
    except Exception as e:
        return f"Error posting to Twitter: {str(e)}"

# Interface with updated background and reduced image size
with gr.Blocks(css="""
body {
    background: url('https://t4.ftcdn.net/jpg/04/55/65/69/360_F_455656949_lOgZhle5nMrzDJdoUMpZU0CH3CHWGprt.jpg') no-repeat center center fixed;
    background-size: 80%;
    font-family: 'Arial', sans-serif;
    margin: 0;
    padding: 0;
    color: #ffffff;
}

#title {
    text-align: center;
    font-size: 2.8rem;
    font-weight: bold;
    color: #ffffff;
    text-shadow: 2px 2px 4px #000000;
    margin-top: 30px;
}

#submit-btn, #tweet-btn {
    background-color: #4a90e2;
    color: white;
    border: none;
    padding: 12px 25px;
    margin-top: 10px;
    border-radius: 5px;
    font-size: 1rem;
    cursor: pointer;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    transition: background-color 0.3s;
}

#submit-btn:hover, #tweet-btn:hover {
    background-color: #357ab7;
}

.gradio-container label {
    color: #ffffff !important;
    font-weight: bold;
    text-shadow: 1px 1px 2px #000000;
}

.textbox {
    border-radius: 10px;
    background-color: rgba(255, 255, 255, 0.8); 
    color: #000000;
    padding: 15px;
    border: none;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.gradio-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
}

.center-box {
    background-color: rgba(0, 0, 0, 0.6);
    border-radius: 10px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
}

.center-image {
    display: block;
    margin: 0 auto;
    width: 15%;  
    height: auto;  
    border-radius: 50%;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
}

#user-input {
    margin-top: 20px;
}

.row-item {
    padding: 10px;
    margin: 10px 0;
}

@media only screen and (max-width: 768px) {
    .gradio-container {
        width: 100%;
        padding: 10px;
    }

    .center-image {
        width: 20%;  /* Smaller for smaller screens */
    }

    #title {
        font-size: 2rem;
    }

    #submit-btn, #tweet-btn {
        padding: 10px 20px;
    }
}
""") as iface:
    # Title
    gr.Markdown("""
    <div id="title">SPORTS ASSISTANT</div>
    """)

    # Image
    gr.HTML('<img src="https://cdn-icons-png.flaticon.com/512/733/733579.png" class="center-image">')

    # Main UI container
    with gr.Row(elem_classes="center-box"):
        with gr.Column(scale=1):
            character_file_display = gr.Textbox(label="Character Defined", interactive=False, elem_classes="textbox")
        with gr.Column(scale=1):
            data_fetched_display = gr.Textbox(label="Data File", interactive=False, elem_classes="textbox")

    # Input box
    gr.Markdown("<p style='text-align: center; font-size: 1.3rem; font-weight: bold;'>What do you want to know?</p>")
    user_input = gr.Textbox(label="Your Question", placeholder="Ask your sports-related question here...", elem_classes="textbox", elem_id="user-input")

    # Buttons and response
    with gr.Row():
        send_button = gr.Button("Submit", elem_id="submit-btn")

    # API Response
    api_response = gr.Textbox(label="Here's the Tweet We Generated for You!", interactive=False, elem_classes="textbox")
    
    # Twitter Integration
    with gr.Row():
        tweet_button = gr.Button("Your Tweet is All Set! Ready to Share?", elem_id="tweet-btn")
        tweet_status = gr.Textbox(label="Twitter Post Status", interactive=False, elem_classes="textbox", elem_id="tweet-status")

    # Linking Functions
    send_button.click(fn=send_message, inputs=user_input, outputs=[api_response, data_fetched_display, character_file_display])
    tweet_button.click(fn=post_to_twitter, inputs=api_response, outputs=tweet_status)

iface.launch(share=True)