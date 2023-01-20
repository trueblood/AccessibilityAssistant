class QuestionHelper:
    def checkIfQuestionIsInList(question):
        data = [ "what is the title of the article"
        ]
        if question in data:
            return True
        else:
            return False
