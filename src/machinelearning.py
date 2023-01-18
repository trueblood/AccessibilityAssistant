from datasets import load_dataset
from txtai.pipeline import HFTrainer
import pandas as pd
from transformers import pipeline
from transformers import PegasusForConditionalGeneration
from transformers import PegasusTokenizer
from transformers import pipeline


class MachineLearning:
    def run_machine_learning(context, question):
        #questions = pipeline("question-answering", model="distilbert-base-uncased")
        questions = pipeline("question-answering", model="ml6team/distilbart-tos-summarizer-tosdr")
        result =questions(question, context)
        return result.get('answer')


    def run_machine_learning_tuned_model(context, question, data):
        trainer = HFTrainer() 
        model, tokenizer = trainer("distilbert-base-uncased", data, task="question-answering")
        questions = pipeline("question-answering", model="distilbert-base-uncased")
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
            value.append(x)
        return value

    def summarize_text(text):

        # Pick model
        model_name = "google/pegasus-xsum"

        # Load pretrained tokenizer
        pegasus_tokenizer = PegasusTokenizer.from_pretrained(model_name)

        example_text = text
        #example_text = """copyleft.org is a collaborative project to create and disseminate useful information, tutorial material, and new policy ideas regarding all forms of copyleft licensing. This site itself is licensed under a free and open license and has received contributions from experts around the world."""


        # Define PEGASUS model
        pegasus_model = PegasusForConditionalGeneration.from_pretrained(model_name)

        # Create tokens
        tokens = pegasus_tokenizer(example_text, truncation=True, padding="longest", return_tensors="pt")


        # Summarize text
        encoded_summary = pegasus_model.generate(**tokens)

        # Decode summarized text
        decoded_summary = pegasus_tokenizer.decode(
            encoded_summary[0],
            skip_special_tokens=True
        )

        # Define summarization pipeline 
        summarizer = pipeline(
            "summarization", 
            model=model_name, 
            tokenizer=pegasus_tokenizer, 
            framework="pt"
        )
        summary = summarizer(example_text, min_length=30, max_length=150)

        return summary[0]["summary_text"]
