from flask import Flask, render_template, request
from deep_translator import GoogleTranslator
from collections import defaultdict
import re
import heapq

app = Flask(__name__)

sanskrit_stopwords = set([
    "अथ", "एव", "तथा", "च", "व", "न", "हि", "यथा", "स्म", "यः", "एष", "किम्", "अपि", "सर्वे",
    "तत्", "ते", "सः", "मम", "सर्वथा", "तस्मात्", "तत्र", "अस्ति", "भवति", "इत्थं", "इति", "अधि",
    "अस्मिन", "अत्र", "नहि", "तत्", "एष", "प्रति", "पुनः", "अपि", "तस्मिन", "अन्ते", "च", "आत्मन्",
    "स्व", "अथवा", "केवलम्", "चेत्", "विना", "तेन", "मूल", "यद्यपि", "यत्र", "कदा", "पश्चात्", "किञ्च",
    "यदा", "विषये", "उपयोग", "तस्य", "संबंध", "अर्थ", "प्रकार", "अधिक", "समान", "विशेष", "परंतु",
    "न", "नहि", "सन्दर्भ", "किं", "नूनम्", "विशेष", "प्रत्येक", "उक्त", "तत्त्व", "सिद्ध", "किंचित्", "अस्मिन",
    "गत्वा", "यथा", "दृष्ट", "कर्म", "प्रश्न", "अयम्", "अधिकार", "आवश्यक", "इतिहास", "पृष्ठ", "विश्लेषण",
    "समाधान", "अर्थात्", "स्वतः", "च", "अवधि", "यथार्थ"
])

def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text)
    sentences = re.split(r'[।?!]', text)
    sentences = [sentence.strip() for sentence in sentences if sentence]
    return sentences

def calculate_word_frequencies(sentences):
    word_frequencies = defaultdict(int)
    for sentence in sentences:
        words = re.findall(r'\b\w+\b', sentence)
        for word in words:
            word = word.lower()
            if word not in sanskrit_stopwords:
                word_frequencies[word] += 1
    return word_frequencies

def rank_sentences(sentences, word_frequencies):
    sentence_scores = defaultdict(int)
    for sentence in sentences:
        words = re.findall(r'\b\w+\b', sentence)
        for word in words:
            if word.lower() in word_frequencies:
                sentence_scores[sentence] += word_frequencies[word.lower()]
    return sentence_scores

def summarize_text(text, num_sentences):
    sentences = preprocess_text(text)
    word_frequencies = calculate_word_frequencies(sentences)
    sentence_scores = rank_sentences(sentences, word_frequencies)
    summary_sentences = heapq.nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    return ' '.join(summary_sentences)

@app.route('/', methods=['GET', 'POST'])
def summarize():
    output_text = ''
    if request.method == 'POST':
        input_text = request.form.get('inputText')
        summary_line = int(request.form.get('summary_line', 5))
        output_text = summarize_text(input_text, num_sentences=summary_line)
    return render_template('summerize.html', output_text=output_text)

@app.route('/translate', methods=['GET', 'POST'])
def translate():
    output_text2 = ''
    translated_text = ''
    if request.method == 'POST':
        # Translation functionality
        text_to_translate = request.form.get('inputText2', '')
        translator = GoogleTranslator(source='sa', target='en')
        translated_text = translator.translate(text_to_translate)
    return render_template('translate.html', output_text2=translated_text)

if __name__ == '__main__':
    app.run(debug=True)
