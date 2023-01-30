from datasets import load_dataset
from txtai.pipeline import HFTrainer
import pandas as pd
from transformers import pipeline


class MachineLearning:
    def question_answering(context, question):
        questions = pipeline("question-answering", model="distilbert-base-uncased")
        result =questions(question, context)
        return result.get('answer')


    def question_answering__tuned_model(context, question, data):
        trainer = HFTrainer() 
        model, tokenizer = trainer("distilbert-base-uncased", data, task="question-answering")
        questions = pipeline("question-answering", model=model, tokenizer=tokenizer)
        result =questions(question, context)
        return result.get('answer')

    def entity_recognition(text):
        pipe = pipeline("ner", model="dslim/bert-base-NER")
        result = pipe(str(text))
        value = []
        for x in result:
            value.append(x['word'])
        return value

    def summarize_paragraph(text):
        pipe = pipeline("summarization", model="google/pegasus-xsum")
        result = pipe(str(text))
        value = []
        for x in result:
            value.append(x['summary_text'])
        return value