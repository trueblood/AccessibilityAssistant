import src.scrapwebpage as sw
import src.jsonhelper as jh
import src.machinelearning as ml
import src.databasehelper as db
import src.questionhelper as q
import os
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
    drpSuccessful =  db.DatabaseHelper.dropDatabaseTable()
    if drpSuccessful == True:
        sw.ScrapWebPage.scrap_web_page_title(url)
        sw.ScrapWebPage.scrap_web_page_paragraph(url)
        sw.ScrapWebPage.scrap_web_page_header(url)
        sw.ScrapWebPage.scrap_web_page_link(url)
        sw.ScrapWebPage.scrap_web_page_source(url)
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
        question = originalQuestion
        splitString = originalQuestion.split(" ")
        lengthOfList = len(splitString)
        firstWord = splitString[0] #what
        if firstWord == "what":
            hasNumbers = has_numbers(originalQuestion)
            lastWord = splitString[lengthOfList-2] + " " + splitString[lengthOfList-1]
            question = "read" + " " + lastWord
            if hasNumbers:
                url = getFormattedURL(originalwebsite)
                value = db.DatabaseHelper.findDataByQuestion_Cleaned(question, url)
                context = value
                text = ml.MachineLearning.run_machine_learning(context, originalQuestion)
            else:
                questionInList = q.QuestionHelper.checkIfQuestionIsInList(originalQuestion)
                if questionInList == True:
                    url = getFormattedURL(originalwebsite)
                    value = db.DatabaseHelper.findDataByQuestion_Json(originalQuestion, url)
                    jsonData = value
                    text = jsonData
                    data = []
                    sourceQuestion = "what is the source"
                    context = db.DatabaseHelper.findDataByQuestion_Json(sourceQuestion, url)
                    data.append({'question' : jsonData['question'], 'context' : context['element'], 'answers' : jsonData['cleaned']})
                    text = ml.MachineLearning.run_machine_learning_tuned_model(context['element'], originalQuestion, data)
                else:
                    url = getFormattedURL(originalwebsite)
                    sourceQuestion = "what is the source"
                    context = db.DatabaseHelper.findDataByQuestion_Cleaned(sourceQuestion, url)
                    text = ml.MachineLearning.run_machine_learning(context, originalQuestion)
        elif firstWord == "read":
            url = getFormattedURL(originalwebsite)
            value = db.DatabaseHelper.findDataByQuestion_Cleaned(originalQuestion, url)
            text = value
        else:
            originalQuestion = "what is the source"
            url = getFormattedURL(originalwebsite)
            context = db.DatabaseHelper.findDataByQuestion_Cleaned(originalQuestion, url)
            text = ml.MachineLearning.run_machine_learning(context, question)
            question = question
        
        

    
    return render_template('question.html', form=form, website=website, question=question, text=text)
#if __name__=="__main__":
#  app.run(host="127.0.0.1", port=int(os.environ['CDSW_APP_PORT']))