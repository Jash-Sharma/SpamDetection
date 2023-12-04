import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer

nltk.download('punkt')
nltk.download('stopwords')

ps = PorterStemmer()


def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

st.title("Email/SMS Spam Classifier")

input_sms = st.text_area("Enter the message")

if st.button('Predict'):

    # 1. preprocess
    transformed_sms = transform_text(input_sms)
    # 2. vectorize
    vector_input = tfidf.transform([transformed_sms])
    # 3. predict
    result = model.predict(vector_input)[0]
    # 4. Display
    st.title("Result :")
    if result == 1:
        st.header("It is a spam")
    else:
        st.header("It is not a spam")

footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;

}

a:hover,  a:active {
color: red;
background-color: transparent;

}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: #0e1117;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with ❤ by <a style='text-align: center;' href="https://jash-sharma.github.io/Portfolio/" target="_blank">Jash Sharma</a></p>
<p>Might Make Mistakes</p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)