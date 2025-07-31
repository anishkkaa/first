#streamlit run calculator.py
import streamlit as st

st.title('Simple Calculator')
# st.subheader('This is basic streamlit application')
# st.markdown('This is basic streamlit application')

c1, c2 = st.columns(2)
fnum = c1.number_input('Enter First number', value=0)
snum = c2.number_input('Enter the second number',value =0)

st.subheader("Options")
choice = ['Add','Sub','Mul','Div']
options = st.radio('Select any one operation',choice)

button = st.button('Calculate')

result =0
if button:
    if options == 'Add':
        result = fnum+snum
    if options == 'Sub':
        result = fnum-snum
    if options == 'Mul':
        result = fnum*snum
    if options == 'Div':
        result = fnum / snum     

st.success(f"Result is{result}")
st.balloons()