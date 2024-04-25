import math
import numpy as np
import pickle
import streamlit as st

def pred_array(team):
    prediction_array = []
    # Batting Team
    if team == 'Chennai Super Kings': prediction_array = prediction_array + [1,0,0,0,0,0,0,0]
    elif team == 'Delhi Daredevils': prediction_array = prediction_array + [0,1,0,0,0,0,0,0]
    elif team == 'Kings XI Punjab': prediction_array = prediction_array + [0,0,1,0,0,0,0,0]
    elif team == 'Kolkata Knight Riders': prediction_array = prediction_array + [0,0,0,1,0,0,0,0]
    elif team == 'Mumbai Indians': prediction_array = prediction_array + [0,0,0,0,1,0,0,0]
    elif team == 'Rajasthan Royals': prediction_array = prediction_array + [0,0,0,0,0,1,0,0]
    elif team == 'Royal Challengers Bangalore': prediction_array = prediction_array + [0,0,0,0,0,0,1,0]
    elif team == 'Sunrisers Hyderabad': prediction_array = prediction_array + [0,0,0,0,0,0,0,1]
    return prediction_array



#SET PAGE WIDE
st.set_page_config(page_title='Score Predictor',layout="centered")

#Get the ML model 

filename = 'rf_model.pkl'
model = pickle.load(open(filename,'rb'))

# Title
st.markdown("<h1 style='text-align: center; color: black;'> Score Predictor </h1>", unsafe_allow_html=True)

#Add background
st.markdown(
         f"""
         <style>
         .stApp {{
             background-color:grey;
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

#Add description

st.info("""A Simple ML Model to predict IPL Scores between teams in an ongoing match. 
 """)

col1, col2 = st.columns(2)

#BATTING TEAM

with col1: 
    batting_team= st.selectbox('Batting Team ',('Chennai Super Kings', 'Delhi Daredevils', 'Kings XI Punjab','Kolkata Knight Riders','Mumbai Indians','Rajasthan Royals','Royal Challengers Bangalore','Sunrisers Hyderabad'))

prediction_array = pred_array(batting_team)

with col2:
    bowling_team = st.selectbox('Bowling Team ',('Chennai Super Kings', 'Delhi Daredevils', 'Kings XI Punjab','Kolkata Knight Riders','Mumbai Indians','Rajasthan Royals','Royal Challengers Bangalore','Sunrisers Hyderabad'))
    


if bowling_team==batting_team:
    st.error('Bowling and Batting teams should be different')

prediction_array += pred_array(bowling_team)
  

col3, col4 = st.columns(2)

#Current Ongoing Over
with col3:
    overs = st.number_input('Current Over',min_value=5.1,max_value=19.5,value=5.1,step=0.1)
    if overs-math.floor(overs)>0.5:
        st.error('Please enter valid over input as one over only contains 6 balls')

with col4:
#Current Runs
    runs = st.number_input('Current runs',min_value=0,max_value=354,step=1,format='%i')


#Taken fallen now
wickets =st.slider('Wickets fallen till now',0,9)
wickets=int(wickets)

wickets_in_prev_5 = st.number_input('Wickets fallen in the last 5 overs',min_value=0,max_value=wickets,step=1,format='%i')

runs_in_prev_5 = st.number_input('Runs scored in the last 5 overs',min_value=0,max_value=runs,step=1,format='%i')

#Get all the data for predicting

prediction_array = prediction_array + [runs, wickets, overs, runs_in_prev_5,wickets_in_prev_5]
prediction_array = np.array([prediction_array])
predict = model.predict(prediction_array)


if st.button('Predict'):
    prediction = int(round(predict[0]))
    
    x=f'PREDICTED MATCH SCORE IS {prediction-5} To {prediction+5}' 
    st.success(x)
   