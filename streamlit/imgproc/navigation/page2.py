from PIL import Image, ImageOps
import streamlit as st
from save import st_render

st.header(":rainbow[リサイズ]")

num = st.slider("倍率", min_value=0.1, max_value=2.0,
                value=1.0, step=0.1, key="image_scale")

if "img_upload" not in st.session_state:
    st.session_state.img_upload = None

if "image_upload" in st.session_state:
    img = st.session_state.image_upload
    resized = ImageOps.scale(img, num)
    resized.filename = img.filename
    st.image(resized, use_container_width="never")
    
    st_render(resized)