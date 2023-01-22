from datasets import load_dataset
from txtai.pipeline import HFTrainer
import pandas as pd
from transformers import pipeline
from transformers import PegasusForConditionalGeneration
from transformers import PegasusTokenizer
from transformers import pipeline


class MachineLearning:
    def question_answering(context, question):
        questions = pipeline("question-answering", model="distilbert-base-uncased")
        #questions = pipeline("question-answering", model="ml6team/distilbart-tos-summarizer-tosdr")
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














    def summarize_text(text):

        # Pick model
        model_name = "google/pegasus-xsum"

        # Load pretrained tokenizer
        pegasus_tokenizer = PegasusTokenizer.from_pretrained(model_name)

        example_text = str(text)
        example_text = """ and/or other fora provided by copyleft.org may not necessarily reflect the views of the contributors' employers and/or organizations sponsoring the project and/or organizations republishing copyleft.org's materials. Generally speaking, unless stated otherwise, please assume that individuals contribute to copyleft.org in their personal capacity.  """


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
        )

       # result = summarizer(str(text))

        summary = summarizer(example_text, min_length=0, max_length=len(text))

        return summary[0]["summary_text"]
        #return "tesst"
