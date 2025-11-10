import streamlit as st

if "image_upload" in st.session_state:
    st.sidebar.markdown(f"ファイル: {st.session_state.image_upload.filename}")

if "image_scale" in st.session_state:
    st.sidebar.markdown(f"リサイズ: {st.session_state.image_scale}")
    
if "image_colors" in st.session_state:
    st.sidebar.markdown(f"色数: {st.session_state.image_colors}")
    
pg = st.navigation({
    "画像処理サービス": [
        st.Page("page1.py", title="アップロード", icon="📤"),
        st.Page("page2.py", title="リサイズ", icon="📐"),
        st.Page("page3.py", title="ポスタリゼーション", icon="🎨")
    ]})

pg.run()

