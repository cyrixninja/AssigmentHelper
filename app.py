import os
import openai
import streamlit as st
import easyocr as ocr
from PIL import Image
import numpy as np #Image Processing 
import json
from fpdf import FPDF
import base64

st.title("Assignment Helper")

openai.api_key =  ""

def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
       data = f.read()
    return base64.b64encode(data).decode()
def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
        <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
        ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('background.png')

def getanswers(txt):
    txtprompt= ["I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with \"Unknown\".\n\nQ: What is human life expectancy in the United States?\nA: Human life expectancy in the United States is 78 years.\n\nQ: Who was president of the United States in 1955?\nA: Dwight D. Eisenhower was president of the United States in 1955.\n\nQ: Which party did he belong to?\nA: He belonged to the Republican Party.\n\nQ: What is the square root of banana?\nA: Unknown\n\nQ: How does a telescope work?\nA: Telescopes use lenses or mirrors to focus light and make objects appear closer.\n\nQ: Where were the 1992 Olympics held?\nA: The 1992 Olympics were held in Barcelona, Spain.\n\nQ: How many squigs are in a bonk?\nA: Unknown\n\nQ:"+" "+txt+"?\nA:"]
    response = openai.Completion.create(
    engine="babbage",
    prompt=txtprompt,
    temperature=0,
    max_tokens=100,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=["\n"]
    )
    ans1=(response['choices'][0]['text']).split(".")
    ans2 = ans1[0:]
    sepans = "\n".join(ans2)
    st.subheader(sepans)
    answer = sepans
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 10)
    pdf.multi_cell(0,7, answer,'C')
    
    html = create_download_link(pdf.output(dest="S").encode("latin-1"), "test")

    st.markdown(html, unsafe_allow_html=True)

    
        # save FPDF() class into a 
    # variable pd
    

image = st.file_uploader(label = "Upload your image here",type=['png','jpg','jpeg'])


@st.cache
def load_model(): 
    reader = ocr.Reader(['en'],model_storage_directory='.')
    return reader 




if st.button('Click here'):
    reader = load_model() #load model
    if image is not None:

        input_image = Image.open(image) #read image
        st.image(input_image) #display image

        with st.spinner("🤖 Processing "):
            result = reader.readtext(np.array(input_image))
            result_text = []
            for text in result:
                result_text.append(text[1])
            result_text1=json.dumps(result_text)
            txt1=result_text1.replace('"', "")
            txt2=txt1.replace('[', "")
            txt3=txt2.replace(']', "")
            txt=txt3.replace(',', "")
            getanswers(txt)
    
    else:
        st.write("Upload an Image")

        

 
    


    
    
