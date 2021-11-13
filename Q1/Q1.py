import tensorflow as tf
import numpy as np
from pickle import load

class Model:

    def __init__(self):
       
       self.model = tf.keras.models.load_model('Q1.h5')
       self.cond = ["normal","faulty"]
       self.scaler = load(open('scaler.pkl', 'rb'))

    def predict(self):

       CHP1Temp1 = input('CHP1Temp1(Deg C): ')
       CHP1Temp2 = input('CHP1Temp2(Deg C): ')
       CHP2Temp1 = input('CHP2Temp1(Deg C): ')
       CHP2Temp2 = input('CHP2Temp2(Deg C): ')
       CHP1Vib1 = input('CHP1Vib1(mm/s): ')
       CHP1Vib2 = input('CHP1Vib2(mm/s): ')
       CHP2Vib1 = input('CHP2Vib1(mm/s): ')
       CHP2Vib2 = input('CHP2Vib2(mm/s): ')

       X = np.array([CHP1Temp1,CHP1Temp2,CHP2Temp1,CHP2Temp2,CHP1Vib1 ,CHP1Vib2,CHP2Vib1,CHP2Vib2])
       X = X.reshape(1,-1)
       X = self.scaler.transform(X)

       y_pred = self.model.predict(X)
       y_pred = y_pred >= 0.5
       y_pred = y_pred.astype('int')

       cond  = self.cond[y_pred[0][0]]

       print("\nModel Prediction : {}".format(y_pred[0][0]))
       print("The pump is in {} condition".format(cond))
       print("\n--------------------------------------------------------------------\n")

model = Model()
print("The app has started, Press ctrl+c to exit\n")
while True:

    print("Press ctrl+c to exit\n")
    model.predict()