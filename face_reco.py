import numpy as np 
import pandas as pd 
import cv2 

import redis

#insightface
from insightface.app import FaceAnalysis
from sklearn.metrics import pairwise



#Connecting to redis database 
hostname='redis-17790.c281.us-east-1-2.ec2.cloud.redislabs.com'
portnumber=17790  
password='GLZP9gx3pWKk9NrVc00YjsRnhsOb3yEz'
r=redis.StrictRedis(host=hostname,port=portnumber,password=password)

#Configure Face Analysis 
faceapp=FaceAnalysis(name='buffalo_l',root='insightface_models',providers=['CPUExecutionProvider'])
faceapp.prepare(ctx_id=0,det_size=(640,640))

def ml_search_algorithm(dataframe,feature_column,test_vector,name_role=['Name','Role'],thresh=0.5):
    
    
    
    dataframe=dataframe.copy()
    
    
    X_list=dataframe[feature_column].tolist()
    x=np.asarray(X_list)
    
    
    similar=pairwise.cosine_similarity(x,test_vector.reshape(1,-1))
    similar_arr=np.array(similar).flatten()
    dataframe['cosine']=similar_arr
    
    
    data_filter=dataframe.query(f'cosine >= {thresh}')
    if(len(data_filter)>0):
        data_filter.reset_index(drop=True,inplace=True)
        argmax=data_filter['cosine'].argmax()
        person_name,person_role=data_filter.loc[argmax][name_role]
        
    else:
        person_name='Unknown'
        person_role='Unknown'
    
    
    return person_name,person_role
    

def face_prediction(test_image,dataframe,feature_column,name_role=['Name','Role'],thresh=0.5):
    results=faceapp.get(test_image)
    test_copy=test_image.copy()   
    for res in results:
        x1,y1,x2,y2=res['bbox'].astype(int)
        embeddings=res['embedding']
        person_name,person_role=ml_search_algorithm(dataframe,
                                                    feature_column,test_vector=embeddings,
                                                    name_role=name_role,thresh=thresh) 




        if person_name == 'Unknown':
            color=(0,0,255)

        else:
            color=(0,255,0)


        cv2.rectangle(test_copy,(x1,y1),(x2,y2),color)


        text_gen=person_name
        cv2.putText(test_copy,text_gen,(x1,y1),cv2.FONT_HERSHEY_DUPLEX,0.7,color,1)
        
    return test_copy




