import json
import re

from flask import Flask, render_template, request
import enchant

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        # print(request)
        # print(request.data)
        # print(request.headers)
        # data = json.loads(request.data.decode())
        data = request.data.decode()

        # Check if the data is in a valid text format (simple validation)
        if not is_valid_format(data):
            return json.dumps({'error': 'Invalid file format'}), 400
        return json.dumps(calculate_scores(parse_data(data)))

    except Exception as e:
        # Return an error message in case of exceptions
        print(f'Error: {e}')
    return json.dumps({'error': 'An error occurred processing your file'}), 500


def is_valid_format(data):
    # Check if the data starts with a typical Zoom chat line format
    # A typical line starts with a timestamp (e.g., "21:34:38"), followed by "From"
    pattern = r'^\d{2}:\d{2}:\d{2} From .+ To .+:'
    return bool(re.search(pattern, data, re.MULTILINE))


def parse_data(data: str):
    data = data.replace('\r\n\t', ' ')
    dataset = re.split(r'\r?\n', data)

    return dataset[:-2]


def calculate_scores(dataset):
    '''Algorithm to calulate the participation score of the students based on messages that are sent.

        Arguments: dataset - Zoom chat transcript
        Return: dictionary with the grades
    '''

    checker = enchant.Dict(
        "en_UK")  # a pyenchant dictionary object used to check if the words are valid. The base language is the UK English
    grades = dict()  # dictionary data structure used to

    for message in dataset:
        message_details = message.split(" To ")
        message_text = message_details[1].split(":")[1].split(" ")[1:]
        message_sender = message_details[0][14:].strip()

        pct_valid_words = 0
        valid_words = 0
        n_words = 0

        # print(message_text)
        for word in message_text:
            n_words += 1
            if (checker.check(word)):
                valid_words += 1

            # print(word, " :", checker.check(word))

        pct_valid_words = (valid_words / n_words) * 100

        if pct_valid_words > 70:
            if message_sender not in grades and message_sender != "":
                grades[message_sender] = 1  # assignment of first mark
            elif message_sender != "":
                grades[message_sender] += 1  # marks implement be

    return grades


if __name__ == '__main__':
    app.run()
