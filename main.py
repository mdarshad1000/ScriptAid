from flask import Flask, render_template, request, session
from openai import OpenAI
import os
from flask_wtf.csrf import CSRFProtect

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))




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
    notes = request.json["notes"] if request.json["notes"] else ""
    content = request.json["content"] if request.json["content"] else ""
    content_type = request.json["type"] if request.json["type"] else "" 
    style = request.json["style"] if request.json["style"] else ""
    topic = request.json["topic"] if request.json["topic"] else ""

    # for verifying the input
    tweet = 'Tweet'
    blog = 'blog post'

    prompt = (
        f"Write a {'detailed, engaging, creative ' if request.json['type'] != tweet else '' }{style} {content_type} "
        f"{'on ' + topic if request.json['topic'] else 'about anything engaging, relevant, interesting'}"
        f"{' considering the following instructions/points:' + chr(10) + notes if request.json['notes'] else ' and add details and facts to make it interesting.'}"
        "\n"
        f"{'Use headings, bullet points, facts, lists if neccessary to make it easy to read and eloquent.' if request.json['type'] == blog else ''}"
        "\n\n"
        f"{content}."
    )
    prompt_trunc = " ".join(prompt.split(" ")[-1024:])

    print(prompt)

    response = client.completions.create(# engine = "text-chat-davinci-002-20221122",
    engine = "gpt-3.5-turbo",
    prompt = prompt_trunc,        
    max_tokens=25,
    temperature=0.9,
    top_p=1)
    completion_response = response.choices[0].text
    session['completion_response'] = completion_response

    return {"suggestion": completion_response}


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=1234))



# PROMPT - 2
# criteria = (
#     request.json["style"]
#     or request.json["topic"]
#     or request.json["notes"]
# )   # Returns a Boolean

# prompt = (
#     f"You are versatile, creative, and expert in writing {content_type}"
#     "You structure your text to be easy to read." 
#     "For example by using list, facts, figures, and headings while writing large contents.\n"
#     f"You are now writing a {content_type}"
#     f"{'with these criterias' if criteria else ''}:\n"
#     f"{'Topic: ' + topic + chr(10) if request.json['topic'] else '' }"
#     f"{'Style: ' + style + chr(10) if request.json['style'] else '' }"
#     f"{'Notes: ' + notes + chr(10) if request.json['notes'] else '' }"
#     "\n"
#     f"Here is your final version:"
#     "\n\n"
#     f"{content}."
# )


# PROMPT-3
# prompt = f"This is a {style} {content_type} about {topic}:\n\n{request.json['content']}",
