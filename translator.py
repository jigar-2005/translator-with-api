from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, url_for, flash, redirect, request, abort
import requests
import os
from gtts import gTTS
from playsound import playsound


app = Flask(__name__)
app.secret_key = "Secret Key"


@app.route('/')
def home():
    return render_template('translator_design.html')


@app.route('/update_api', methods=['GET', 'POST'])
def update_api():
    output_data_list=[]
    if request.method == 'POST':
        default_language=request.form.get('default_language')
        convert_language=request.form.get('convert_language')
        user_text = request.form.get('user_text').replace('?', '')
        if user_text != "":
            url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=" + default_language + "&tl=" + convert_language + "&dt=t&q=" + user_text
            url_request = requests.get(url)
            url_json = url_request.json()
            output_data = url_json[0]
            for data in output_data:
                output_data_list.append(data[0])
            output_data=(' '.join([str(elem) for elem in output_data_list]))
            return render_template('translator_design.html', output_data=output_data, user_text=user_text, default_language=default_language, convert_language=convert_language)
        else:
            flash('please write some data to convert', 'danger')
    return redirect(url_for('home'))


@app.route('/english_to_hindi+<user_text>+to+<output_data>/default_language=<default_language>/convert language=<convert_language>', methods=['GET', 'POST'])
def english_to_hindi(user_text, output_data, default_language, convert_language):
    default_language = default_language
    convert_language = convert_language
    return render_template('translator_design.html', user_text=user_text, output_data=output_data, default_language=default_language, convert_language=convert_language)


@app.route('/play_output_data<user_text>to<output_data>/default_language=<default_language>/convert language=<convert_language>', methods=['GET', 'POST'])
def play_output_data(user_text, output_data, default_language, convert_language):
    default_language = default_language
    convert_language = convert_language
    myobj = gTTS(text=output_data, lang='hi', slow=False)
    myobj.save("C:/Users/Ram Sharma/Desktop/python/static/voice/voice.mp3")
    playsound('C:/Users/Ram Sharma/Desktop/python/static/voice/voice.mp3')
    os.remove('C:/Users/Ram Sharma/Desktop/python/static/voice/voice.mp3')
    return redirect(url_for('english_to_hindi', user_text=user_text, output_data=output_data, default_language=default_language, convert_language=convert_language))


if __name__ == '__main__':
    app.run(debug=True)