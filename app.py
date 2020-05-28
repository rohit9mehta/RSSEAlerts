# from flask import Flask, render_template
# from main import chat
# app = Flask(__name__)

# @app.route("/")
# def home():    
#     return render_template("home.html")

# @app.route("/get")
# def get_bot_response():
#     return chat()

# if __name__ == "__main__":
#     app.run()

from flask import Flask, url_for, render_template, redirect
from forms import ContactForm
import json

app = Flask(__name__, instance_relative_config=False)
app.config.from_object('config.Config')
app.config['SECRET_KEY'] = 'any secret string'

allUsers = open("userPrefs.txt", "a")
data = {}
if not data:
    userID = 0
else:
    userID = max(data.keys())
# allUsers.write(data)

@app.route('/', methods=('GET', 'POST'))
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # name = form.name.data
        # email = form.email.data
        # body = form.body.data
        # print(name)
        # print(email)
        # print(body)
        save(form.body.data)
        return redirect(url_for('success'))
    return render_template('contact.html', form=form)

@app.route('/success', methods=('GET', 'POST'))
def success():
    return render_template('success.html',
                           template='success-template')

def save(message):
    # wordsList = message.split(",")
    data[userID] = message
    allUsers.write(data[userID])
    allUsers.write("\n")
    allUsers.close()

if __name__ == "__main__":
    app.run()

