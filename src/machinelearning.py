from datasets import load_dataset
from txtai.pipeline import HFTrainer
import pandas as pd
from transformers import pipeline



class MachineLearning:
    def run_machine_learning(context, question):
        trainer = HFTrainer() 
        questions = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
        result =questions(question, context)
        return result.get('answer')


    def run_machine_learning_tuned_model(context, question, data):
        trainer = HFTrainer() 
        model, tokenizer = trainer("distilbert-base-cased-distilled-squad", data, task="question-answering")
        questions = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
        result =questions(question, context)
        return result.get('answer')