from flask import Flask, render_template, request
import openai
import os
from flask_wtf.csrf import CSRFProtect

openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

app.config.update(
    SECRET_KEY=os.environ.get("FLASK_SECRET"),
    SESSION_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Strict",
)

csrf = CSRFProtect() 
csrf.init_app(app)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/suggest', methods=['POST', 'GET'])
def suggest():

    style = request.json["style"] if request.json["style"] else ""
    topic = request.json["topic"] if request.json["topic"] else ""
    content_type = request.json["type"] if request.json["type"] else ""
    notes = request.json["notes"] if request.json["notes"] else ""
    print(notes)
    response = openai.Completion.create(
        engine = "text-davinci-003",
        # prompt = f"This is a {style} {content_type} about {topic}:\n\n{request.json['content']}",
        prompt = f"You are a versatile, creative, expert writer and can write amazing {content_type}.\
            Your content is properly structured.\nYou can use bullet points, headings, sub-headings, facts, figures if required.\
                \nYou are now writing a {content_type} with these criterias:\
                Topic: {topic}\
                Style: {style}\
                Notes: {notes}",        
        max_tokens=15,
        temperature=0.7,
        top_p=1, 
    )
    # print(response["choices"][0]["text"])
    return {"suggestion": response["choices"][0]["text"]}


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))