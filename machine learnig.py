from pop import AI
import numpy as np
import cv2
from os import listdir
from os.path import isfile, join
from sklearn.model_selection import train_test_split
dir_path = "./train/"

X_data=[]
Y_data=[]

print("Loading image files")
count=0
count1=0
count2=0
count3=0
count4=0
count5=0
count6=0
count7=0
count8=0
count9=0


i=0
prev=0
total = 10000
for f in listdir(dir_path):
    file_path = join(dir_path,f)
    if isfile(file_path):
        img=cv2.imread(file_path)
        img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img=cv2.resize(img, (50,50), interpolation=cv2.INTER_AREA)
        X_data.append(img.reshape(50,50,1).astype(float))
        if "IU" in f:
            Y_data.append(0) # 0: DOG
            count+=1
        elif "LS" in f:
            Y_data.append(1) # 1: CAT
            count1+=1
        elif "jhope" in f:
            Y_data.append(2)
            count2+=1         
        elif "jimin" in f:
            Y_data.append(3)
            count3+=1            
        elif "jin" in f:
            Y_data.append(4)
            count4+=1 
        elif "jungkook" in f:
            Y_data.append(5)
            count5+=1 
        else:
            Y_data.append(6)
            count6+=1 
            
            

    i+=1
    progress = int( (i/total)*100 )
    if progress/10 != prev/10:
        print("progress {}%".format(progress))
        prev = progress
    if progress == 10:
        break;
from keras.utils import to_categorical
Y_data = to_categorical(Y_data)
print("X_data:{}".format(len(X_data)))
print("Y_data:{}".format(len(Y_data)))
X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data, random_state=0)
print("Training model")
CNN=AI.CNN(input_size=[50,50], output_size=7)
CNN.X_data=X_train
CNN.Y_data=y_train
CNN.train(times=5)
print("Testing model")
prediction = CNN.run(X_test)
correct = 0
i = 0
for answer in prediction:
    if answer[0] == y_test[i][0]:
        correct+=1
    i+=1
        
total = len(y_test)
accuracy = (correct/total)*100
print("total:{0}, correct:{1}, accuracy:{2}%".format(total, correct, accuracy))
