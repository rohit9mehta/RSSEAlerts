#!/usr/bin/env python
import cgi;
import cgitb;cgitb.enable()

from flask import Flask, url_for, render_template, redirect
from forms import ContactForm
import json

app = Flask(__name__, instance_relative_config=False)
app.config.from_object('config.Config')
app.config['SECRET_KEY'] = 'any secret string'

# allUsers = open("userPrefs.txt", "a+")
allUsers = open('userPrefsDict.json', 'a+')
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
    # print(data)
    with open('userPrefsDict.json', 'a+') as f:
        json.dump(data, f)
    # allUsers.write(str(userID) + " | " + data[userID] + " | ")
    # allUsers.write("\n")
    # allUsers.close()

if __name__ == "__main__":
    app.run()

