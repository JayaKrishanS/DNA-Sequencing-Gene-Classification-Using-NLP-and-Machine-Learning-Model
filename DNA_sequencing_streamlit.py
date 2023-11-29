import  pickle
import streamlit as st
import pybase64
from streamlit_option_menu import option_menu

model = pickle.load(open("DNA_sequencing_model.pkl", "rb"))
cv = pickle.load(open("DNA_sequencing_cv.pkl","rb"))

st.markdown("<h2 style='color: orange;'> DNA Sequencing: Gene Classification Using NLP and Machine Learning Model </h2>", unsafe_allow_html = True)

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return pybase64.b64encode(data).decode()
img = get_img_as_base64("Background_image.jpg")


page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/png;base64,{img}");
background-size: 100%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

def getKmers(sequence, size=6):
    kmers = []
    for i in range(len(sequence) - size + 1):
        kmer = sequence[i:i+size].lower()
        kmers.append(kmer)
    return kmers


def prediction(input_data):
    kmers = getKmers(input_data)
    kmers = ' '.join(kmers)
    input = cv.transform([kmers])
    predicted_class = model.predict(input)
    return predicted_class


with st.sidebar:
    selected = option_menu(
        menu_title="Gene family prediction",  
        options=["Home","---","Start predicting"],
        icons=["house","", ""], 
        menu_icon="",
        default_index=0,
    )
    

if selected == "Home":
    st.markdown("<h3 style='color: #FF4B4B;'> Summary: </h3>", unsafe_allow_html = True)
    st.markdown("<h5 style='color: white;'> The gene classification project involved a dataset with two columns, 'sequence' and  'class'. The project initiated with a data cleaning process to ensure data quality. Subsequently, the DNA sequences were processed using k-mers counting with a size of 6. K-mers are subsequences of length k, and in this case, a size of 6 was chosen for counting.</h5>", unsafe_allow_html = True)
    st.markdown("<h5 style='color: white;'>Following the k-mers counting methodology, the gene sequences underwent Natural Language Processing (NLP) techniques, specifically using CountVectorizer. This technique transformed the gene sequences into a bag of words representation, facilitating further analysis. </h5>", unsafe_allow_html = True)
    st.markdown("<h5 style='color: white;'> For the classification task, a machine learning model was trained using the Random Forest Classifier algorithm and got an accuracy of 89%. The choice of Random Forest was based on its demonstrated good performance in the context of gene classification.</h5>", unsafe_allow_html = True)
    st.markdown("<h5 style='color: white;'> The successful model was then integrated into a user-friendly web application using Streamlit.</h5>", unsafe_allow_html = True)

if selected == "Start predicting":
    st.markdown("<h3 style='color: black'> Enter the message for predicting: </h3>", unsafe_allow_html = True)
    input = st.text_area("Paste the sequence")

    if st.button("Predict"):
        gene_predict = prediction(input)
        if (gene_predict[0] == 0):
            st.success("This sequence belongs to 'G protein coupled receptor'. ")
        if (gene_predict[0] == 1):
            st.success("This sequence belongs to 'Tyrosine kinase'. ")
        if (gene_predict[0] == 2):
            st.success("This sequence belongs to 'Tyrosine Phosphatase '. ")
        if (gene_predict[0] == 3):
            st.success("This sequence belongs to 'Synthetase'. ")
        if (gene_predict[0] == 4):
            st.success("This sequence belongs to 'Synthase'. ")
        if (gene_predict[0] == 5):
            st.success("This sequence belongs to 'Ion channel'. ")
        if (gene_predict[0] == 6):
            st.success("This sequence belongs to 'Transcription factor'. ")
