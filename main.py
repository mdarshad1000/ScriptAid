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

    # Get input from the user
    topic = request.json["topic"] if request.json["topic"] else ""
    style = request.json["style"] if request.json["style"] else ""
    notes = request.json["notes"] if request.json["notes"] else ""

    content = request.json["content"] if request.json["content"] else ""
    content_type = request.json["type"] if request.json["type"] else ""
    
    criteria = (
        request.json["style"]
        or request.json["topic"]
        or request.json["notes"]
    )   # Returns a Boolean


    prompt = (
        "You are a versatile, creative, expert in your field and an excellent writer. "
        "You structure your text to be easy to read." 
        "For example by using list, facts & figures, and headings while writing large contents.\n"
        f"You are now writing a {content_type} "
        f"{'with these criterias' if criteria else ''}:\n"
        f"{'Topic: ' + topic + chr(10) if request.json['topic'] else '' }"
        f"{'Style: ' + style + chr(10) if request.json['style'] else '' }"
        f"{'Notes: ' + notes + chr(10) if request.json['notes'] else '' }"
        "\n"
        f"Here is your final version:"
        "\n\n"
        f"{content}."
    )

    print(prompt)
    response = openai.Completion.create(
        engine = "text-davinci-003",
        # prompt = f"This is a {style} {content_type} about {topic}:\n\n{request.json['content']}",
        prompt = prompt[-1750:],        
        max_tokens=17,
        temperature=0.7,
        top_p=1, 
    )

    # print(response["choices"][0]["text"])
    return {"suggestion": response["choices"][0]["text"]}


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))