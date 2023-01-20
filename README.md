# Accessibility Assistant

## About
This web application analyzes the data on a website and then organizes the data based on html element type. Throws it onto a no sql database, mongo db, and allows me to run queries against the data. The machine learning comes in so that the user can ask questions about the information that is present, Summarize text, or check entities in a paragraph. Then reads the results to the user. 

## I used txtAI for the AI Framework and Pipelines 
* Pipelines are objects that abstract most of the complex code from the library, offering a simple API dedicated to several tasks, including Named Entity Recognition, Masked Language Modeling, Sentiment Analysis, Feature Extraction and Question Answering. 
* txtai executes machine-learning workflows to transform data and build AI-powered semantic search applications. 

To train a model I used the hugging face trainer object. I did this to fine tune my question answer model 

## Three different machine learning techniques 
* Question answering with custom question answering to fine tune the model 
    * Ask questions about the paragraph or article as a whole 
* Text summarization 
    * To summarize the article or paragraph so the user doesn't have to listen to the whole thing unless they want too 
* Entity recognition 
    * Pick names out of the article 

## I used pretrained models for this project 
* distilbert-base-uncased 
    * For my question answering this model does get trained with my dataset 
* google/pegasus-xsum 
    * For my text summarization 
*   Udslim/bert-base-NER 
    * For my named entity recognition 

## Technologies used 
* Visual Studio code 
* Linux 
* Python 
* Pip 
* Flask 
* Hugging Face 
* TextAI 

 ## How to install and run the program
