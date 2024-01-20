import streamlit as st
from Home import face_reco
from streamlit_webrtc import webrtc_streamer
import av

import time 


st.set_page_config(page_title='Real Time Prediction')
st.subheader('Real Time Prediction')

with st.spinner('Retrieving Data from Redis DB'):
    redis_face_db=face_reco.retrieve_data(name='academy:register')
    st.dataframe(redis_face_db)


st.success('Data successfully retrieved from Redis')


waitTime=30
setTime=time.time()
realtimepred=face_reco.RealTimePred()



#Real Time Prediction 




def video_frame_callback(frame):

    global setTime

    img = frame.to_ndarray(format="bgr24")


    pred_img=realtimepred.face_prediction(img,redis_face_db,'Facial Features',['Name','Role'],thresh=0.5)

    timenow=time.time()
    difftime=timenow-setTime

    if difftime >= waitTime:
        realtimepred.saveLogs_redis()
        setTime=time.time()

        print('Save data to redis database')

    return av.VideoFrame.from_ndarray(pred_img, format="bgr24")


webrtc_streamer(key="realTimePrediction", video_frame_callback=video_frame_callback)



