import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request
from requests_html import HTMLSession
from twilio.rest import Client


load_dotenv(find_dotenv())
app = Flask(__name__)

# Helper function to send WhatsApp messages
def send_message(to, body):
    # Initialize client
    client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    client.messages.create(
        body=body,
        from_=os.getenv('WHATSAPP_FROM_NUMBER'),
        to=to
    )

# Helper function to get an emoji's description
def get_emojipedia_description(character):
    # Get the Emojipedia page for this emoji
    session = HTMLSession()
    response = session.get('https://emojipedia.org/' + character)

    # If we didn't find an emoji, say so
    if not response.ok:
        return "Hmm - I couldn't find that emoji. Try sending me a single emoji ☝️"

    # Extract the title and description using Requests-HTML and format it a bit
    title = response.html.find('h1', first=True).text
    description = response.html.find('.description', first=True)
    description = '\n\n'.join(description.text.splitlines()[:-1])

    # And template it
    return render_template(
        'response.txt',
        title=title,
        description=description,
        url=response.url
    )

@app.route('/whatsapp', methods=['GET', 'POST'])
def receive_message():
    # Get the description for this character
    character = request.values.get('Body')
    description = get_emojipedia_description(character)

    send_message(to=request.values['From'], body=description)

    return ('', 204)

if __name__ == "__main__":
    app.run(debug=True)