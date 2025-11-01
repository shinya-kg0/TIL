import streamlit as st

from aozora import get_aozora, parse_text_into_sentences
from wc import get_tokens, get_pos_ids, get_wordcloud
from sentiment import get_model, get_sentiment, SENTIMENTS

@st.cache_data
def retrieve_aozora(url):
    print(f"Retrieving Aozora: {url}.")
    return get_aozora(url)

@st.cache_data
def prepare_pos_ids():
    print(f'Retriving POS_IDs.')
    return get_pos_ids()

@st.cache_data
def process_tokens(text):
    print(f'Generating tokens from the text.')
    return get_tokens(text)

@st.cache_resource
def prepare_sentiment_model():
    print(f'Preparing the model.')
    return get_model()


st.title("Book")

tab_text, tab_wc, tab_sentiment = st.tabs(["テキスト", "ワードクラウド", "感情分析"])

with tab_text:
    aozora_url = st.text_input("**青空文庫 Zip ファイルURL**", value=None)
    

with tab_wc:
    pos_ids = prepare_pos_ids()
    pos_list = st.multiselect("品詞", pos_ids, default="名詞")
    

with tab_sentiment:
    trace_on = st.checkbox("文単位の感情", value=False)
    graph = st.empty()
    with graph:
        bar = st.progress(value=0.0, text="計算中")
        

if aozora_url is not None:
    try:
        text = retrieve_aozora(aozora_url)
    except Exception as e:
        st.error(
            f"`{aozora_url}`が取得できない、あるいはそのZipが正しく解凍できませんでした。",
            icon=":material/network_locked:")
        st.exception(e)
        st.stop()
        
    with tab_text:
        st.markdown(text.replace("\n", "\n\n"))
        
    with tab_wc:
        tokens = process_tokens(text)
        img = get_wordcloud(tokens, pos_list)
        st.image(img, width=800)
        
    with tab_sentiment:
        pipe = prepare_sentiment_model()
        sentences = parse_text_into_sentences(text)
        sentiments = {key: 0 for key in SENTIMENTS}
        
        for idx, sentence in enumerate(sentences):
            emotion = get_sentiment(pipe, sentence)
            bar.progress(value=idx/len(sentences), text="計算中")
            sentiments[emotion] = sentiments[emotion] + 1
            
            if trace_on is True:
                st.markdown(f"{sentence} ==> {emotion}")
                
        graph.bar_chart(sentiments)