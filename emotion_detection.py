# -*- coding: utf-8 -*-

import cv2
import numpy as np
from keras.models import load_model
import sys
from csv import writer


##Satart Section
''' Keras took all GPU memory so to limit GPU usage, I have add those lines'''

import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
import os

config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.1
set_session(tf.Session(config=config))
''' Keras took all GPU memory so to limit GPU usage, I have add those lines'''
## End section


faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
model = load_model('keras_model/model_5-49-0.62.hdf5')



def test_image(file):
    emotion_counter = {'angry': 0, 'disgust': 0, 'fear': 0, 'happy': 0, 'sad': 0, 'surprise': 0, 'neutral': 0}
    target = ['angry','disgust','fear','happy','sad','surprise','neutral']
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    im = cv2.imread(file)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1)
    
    for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x+w, y+h), (0, 255, 0), 2,5)
            face_crop = im[y:y+h,x:x+w]
            face_crop = cv2.resize(face_crop,(48,48))
            face_crop = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
            face_crop = face_crop.astype('float32')/255
            face_crop = np.asarray(face_crop)
            face_crop = face_crop.reshape(1, 1,face_crop.shape[0],face_crop.shape[1])
            result = target[np.argmax(model.predict(face_crop))]
            print(result)
            emotion_counter[result] = emotion_counter.get(result, 0) + 1
            #cv2.putText(im,result,(x,y), font, 1, (200,0,0), 3, cv2.LINE_AA)

    return emotion_counter

    #cv2.imshow('result', im)
    #cv2.imwrite('result_emotion_detection_app.jpg',im)
    #cv2.waitKey(0)
    
if __name__=='__main__':

    with open('emotions.csv', 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)


        counter = 0
        for filename in os.listdir('thumbnails'):
            if filename.endswith(".png"):
                print(os.path.join('thumbnails\\', filename))
                e = test_image(os.path.join('thumbnails\\', filename))

                row_contents = [os.path.splitext(os.path.basename(filename))[0], e['angry'], e['disgust'], e['fear'], e['happy'], e['sad'], e['surprise'], e['neutral']]

                # Append a list as new line to an old csv file
                csv_writer.writerow(row_contents)


                counter += 1
            #if counter > 5:
            #    break

        print(counter)
