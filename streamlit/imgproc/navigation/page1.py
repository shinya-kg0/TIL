from PIL import Image
import streamlit as st
from save import st_render

st.header(":rainbow[元画像]")

def onchage():
    img = Image.open(st.session_state._image_upload)
    img.filename = st.session_state._image_upload.name
    st.session_state.image_upload = img
    
st.file_uploader("画像ファイルをアップロードしてください",
                key="_image_upload", on_change=onchage)

if "img_upload" not in st.session_state:
    st.session_state.img_upload = None

if "image_upload" in st.session_state:
    img = st.session_state.image_upload
    st.image(img)
    st_render(img)