import streamlit as st

# st.title("Hello World.")
# st.header("大見出し")
# st.subheader("中見出し")
# st.text(":blue[test]")

print('reloaded', flush=True)
st.title('title string `<h1>`')
st.header('大見出し `<h2>`')
st.subheader(
    body='中見出し`<h3>`',
    anchor='title',
    help='`<h3>`あるいは`###`に相当するStreamlitのコマンド',
    divider=True
)
st.caption('キャプション `<caption>`')

st.text('''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris vel velit leo.
    Suspendisse fermentum augue metus, ac lacinia ipsum varius sit amet.
    Nullam sagittis, tellus id finibus tincidunt, elit mi pellentesque sem, sed suscipit mi lectus non quam.
    ''')

st.code('''
        import streamlit as st
        st.show()''',
        language='python',
        line_numbers=True)