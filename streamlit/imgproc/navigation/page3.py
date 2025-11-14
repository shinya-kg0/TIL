from PIL import Image, ImageFilter
import streamlit as st
from save import st_render

st.header(":rainbow[ポスタリゼーション]")

colors = st.number_input("色数", min_value=2, max_value=256,
                         value=256, step=1, key="image_colors")


if "image_upload" in st.session_state:
    img = st.session_state.image_upload
    mode_filter = ImageFilter.ModeFilter(size=7)
    filtered = img.filter(mode_filter)
    poster = filtered.quantize(colors=colors)
    poster.filename = st.session_state.image_upload.filename
    st.image(poster)
    
    st_render(poster)