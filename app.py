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

phishing = ["verify","account","suspend","login","secure","update","identity",'reset',"password",'confirm','security',"alert","authorize","verification","details"]
promo = ['sale','offer','special','exclusive','limited','discount','price','code','buy','free','promotional','clearance','access','only','last','bonus','one','savings','alert','event']
scams = ['action','bonus','building','cash','claim','confirmed','congratulations','draw','earnings','easy','exclusive','fast','final','financial','free','freedom','get','gift','guaranteed','instant','instructions','investment','jackpot','lottery','lucky','millionaire','money','needed','notice','notification','now','offer','opportunity','paid','payout','prize','profit','quick','required','response','reward','rich','risk-free','secret','secure','selected','strategy','transfer','unclaimed','urgent','waiting','wealth','win','windfall','winner','winning','winnings','won',"you've",'your']   
malware = ['access','action','activity','advisory','against','alert','antivirus','assistance','at','attack','attempt','breach','compromised','critical','cyber','cybersecurity','dangerous','data','detected','device','encryption','file','files','firewall','hacking','harmful','identity','immediate','infected','infection','link','malicious','malware','notice','online','patch','phishing','protect','protection','ransomware','removal','required','risk','scam','scan','secure','security','software','spyware','system','theft','threat','unauthorized','update','urgent','virus','vulnerability','warning','your']
adult = ['adult','cam','chat','club','content','dating','entertainment','erotic','explicit','film','fun','games','girls','hookup','hot','live','mature','meet','naughty','nude','only','personals','pics','play','private','scene','scenes','service','sex','sexy','show','singles','stars','uncensored','video','videos','website','xxx','zone']

catergory = {'promo' : 0,
             'adult' : 0,
             'scams' : 0,
             'phishing': 0,
             'malware' : 0}

st.title("SMS Spam Classifier")

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
        for i in input_sms.lower().split(" "):  
            if i in adult:
                catergory['adult'] += 1
            elif i in malware:
                catergory['malware'] += 1
            elif i in promo:
                catergory['promo'] += 1
            elif i in phishing:
                catergory['phishing'] += 1  
            elif i in scams:
                catergory['scams'] += 1
        maxi = 0
        for i in catergory:
            if catergory[i] > maxi:
                maxi = catergory[i]
                spam = i
        st.header(f'It is a/an {spam} spam')
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
<p>Developed with ❤ by Jash</p>
<p>Might Make Mistakes</p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)