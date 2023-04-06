from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import openai
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    apiKey = data.get('apiKey')
    urls = data.get('urls')

    scrapedText = ''

    for url in urls:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.find_all('p')

            for p in paragraphs:
                scrapedText += p.get_text() + '\n\n'
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
        scrapedText +='---------------------'

    return jsonify({'scrapedText': scrapedText})

@app.route('/summarize', methods=['POST'])
def generate_summary():
    data = request.get_json()
    apiKey = data.get('apiKey')
    prompt = data.get('prompt')
    scrapedText = data.get('crawledText')

    input = prompt+':\n\n'+scrapedText
    print (input)

    #set environment key
    openai.api_key = apiKey

    try:
        print ('Calling API')
        response = openai.Completion.create(
                                                model="text-davinci-003",
                                                max_tokens=500,
                                                temperature=1,
                                                prompt = input,
                                                top_p=1)

        # print (response.choices[0].text)
    except Exception as e:
        print (e)
        return jsonify({'summary': str(e)}), 500

    return jsonify({'summary': response.choices[0].text})

if __name__ == '__main__':
    app.run(debug=True)
