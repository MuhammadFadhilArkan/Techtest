from transformers import pipeline

class pipeLine:

    def __init__(self):

        print("Preparing the model...")
        self.model_name = "fadhilarkan/distilbert-base-uncased-finetuned-cola-3"
        self.model = pipeline('text-classification', model=self.model_name, tokenizer=self.model_name)
        self.label_dict = {"LABEL_0":"AIMX", "LABEL_1":"OWNX", "LABEL_2":"CONT", "LABEL_3":"BASE", "LABEL_4":"MISC"}

    def predict(self,sentence):
        
        print("predicting...")
        prediction = self.model(sentence)
        prediction = prediction[0]
        label = self.label_dict[prediction['label']]
        probability = prediction['score']

        return label,probability

model = pipeLine()
while True :
    sentence = input("Input sentence to be classified : ")
    prediction,probs = model.predict(sentence)
    print("Predicted Label :",prediction)
    print("With probability :",probs)