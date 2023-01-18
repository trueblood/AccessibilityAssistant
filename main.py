import src.scrapwebpage as sw
import src.jsonhelper as jh
import src.machinelearning as ml
import src.databasehelper as db
import src.questionhelper as q
import os
import test as sum
import testagain as sum2

from transformers import pipeline
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SurfForm(FlaskForm):
    website = StringField('What website would you like to surf?', validators=[DataRequired()])
    submit = SubmitField('Submit')
class QuestionForm(FlaskForm):
    question = StringField('What question would you like to ask?', validators=[DataRequired()])
    website = ''
    submit = SubmitField('Submit')
    text = "test"

app = Flask(__name__)
app.config['SECRET_KEY']="hard to guess string"
boostrap = Bootstrap(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET'])
def onGetIndex():
    form = SurfForm()
    return render_template('index.html', form=form)

def getFormattedURL(website):
    inputArray = website.split()
    url = "https://"
    for i in range(len(inputArray)):
        url += inputArray[i]
    return url.lower()

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

@app.route('/', methods=['POST'])
def onPostIndex():
    website = None
    form = SurfForm()
    if form.validate_on_submit():
        website = form.website.data
        form.website.data = ''
        form = QuestionForm()
    return redirect(url_for('question', website=website))

@app.route('/question/<website>', methods=['GET'])
def question(website):
    url = getFormattedURL(website)
    #drpSuccessful =  db.DatabaseHelper.dropDatabaseTable()
    #if drpSuccessful == True:
    #    sw.ScrapWebPage.scrap_web_page_title(url)
    #    sw.ScrapWebPage.scrap_web_page_paragraph(url)
    #   sw.ScrapWebPage.scrap_web_page_header(url)
     #   sw.ScrapWebPage.scrap_web_page_link(url)
     #   sw.ScrapWebPage.scrap_web_page_source(url)
    form = QuestionForm()
    return render_template('question.html', form=form, website=url)

@app.route('/question/<website>', methods=['POST'])
def OnPostQuestion(website):
    originalwebsite = website
    url = getFormattedURL(website)
    website = url
    form = QuestionForm()
    if form.validate_on_submit():
        originalQuestion = form.question.data
        question = originalQuestion.lower()
        splitString = originalQuestion.split(" ")
        lengthOfList = len(splitString)
        firstWord = splitString[0] #what
        if firstWord == "summarize":
            if "article" in splitString: 
                url = getFormattedURL(originalwebsite)
                question = "read the article"
                value = db.DatabaseHelper.findDataByQuestion_Cleaned(question, url)
                #ext = ml.MachineLearning.summarize_text(value)
            else:
                question = "read paragraph " + str(splitString[2])
                url = getFormattedURL(originalwebsite)
                value = db.DatabaseHelper.findDataByQuestion_Cleaned(question, url)
                text = ml.MachineLearning.summarize_text(value)
        elif firstWord == "read":
            if "article" in splitString: 
                url = getFormattedURL(originalwebsite)
                value = db.DatabaseHelper.findDataByQuestion_Cleaned(originalQuestion, url)
                text = value
            else:
                url = getFormattedURL(originalwebsite)
                value = db.DatabaseHelper.findDataByQuestion_Cleaned(originalQuestion, url)
                text = value
        elif firstWord == "entities":
            if "article" in splitString: 
                url = getFormattedURL(originalwebsite)
                question = "read the article"
                value = db.DatabaseHelper.findDataByQuestion_Cleaned(question, url)
                text = ml.MachineLearning.entity_recognition(value)
            else:
                question = "read paragraph " + str(splitString[3])
                text = question
                url = getFormattedURL(originalwebsite)
                value = db.DatabaseHelper.findDataByQuestion_Cleaned(question, url)
                text = ml.MachineLearning.entity_recognition(value)
        
                


      

    
    return render_template('question.html', form=form, website=website, question=question, text=text)
#if __name__=="__
# main__":
#  app.run(host="127.0.0.1", port=int(os.environ['CDSW_APP_PORT']))