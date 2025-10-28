import streamlit as st
import numpy as np
from acceptlang import parse_accept_lang_header

# html = '<p style="color: dodgerblue;">HTMLテキスト</p>'
# st.markdown(html)
# st.markdown(html, unsafe_allow_html=True)
# st.html(html) <- 今は使えない、、、

_MESSAGES = {
    'ja': 'Streamlit にようこそ',
    'en': 'Welcome to Streamlit',
    'es': 'Bienvenido a Streamlit',
    'cn': '欢迎来到 Streamlit',
    'unknown': 'tlhInganpu'
}


def find_language(al):
    for lang in al:
        if lang.name in _MESSAGES:
            return lang.name
    return "unknown"

lang = getattr(st.query_params, "lang", None)

if lang not in _MESSAGES.keys():
    al_value = st.context.headers["accept-language"]
    al_parsed = parse_accept_lang_header(al_value)
    lang = find_language(al_parsed)
    
st.markdown(f"## {_MESSAGES[lang]} :green[{lang}]")

st.write(st.query_params)
st.write(st.context.headers)

icon = 'https://upload.wikimedia.org/wikipedia/commons/4/48/Markdown-mark.svg'

st.set_page_config(
    page_title="Markdown Cheatsheet",
    page_icon=icon,
    layout="wide"
)

st.logo(icon, link='https://github.github.com/gfm/')
st.markdown("### Markdown チートシート")

left, right = st.columns(2)

left.markdown('**:memo: テキスト書式**')
left.markdown('''
要素 | :green[HTML] | 用法
--- | --- | --- 
見出し | `<h1>～<h6>` | `## 見出し`
太字 | `<strong>` | `**太字**`
斜体 | `<em>` | `*斜体*`
取り消し | `<strike>` | `~~取り消し~~`
引用 | `<blockquote>` | `> 引用文`
コード | `<code>` | `` ` `` `` ` ``
区切り線 | `<hr>` | `---`
改行 | `<br/>` | `␣␣`（空白2つ）
ESC | -- | `\\`（特殊文字）
''')

with right:
    st.markdown('**:material/format_list_bulleted: リスト**')
    st.markdown('''
要素 | :green-background[HTML] | 用法
---|---|---
順序なし | `<ul><li>` | `- `
順番付き | `<ol><li>` | `1.`
''')
    with st.expander('**リンク**', icon='🔗'):
        st.markdown('''
要素 | HTML | 用法
---|---|---
リンク | `<a href=...>` | `[文字列](url)`
画像 | `<img src=...>` | `![代替テキスト](url)`
''')
        
    with st.expander('**表**', icon=':material/table:', expanded=False):
        st.markdown('''```
    ヘッダ1 | ヘッダ2 | ヘッダ3 
    ---|---|---
    行1セル1 | 行1セル2 | 行1セル3
    行2セル1 | 行2セル2 | 行2セル3
    行3セル1 | 行3セル2 | 行3セル3
    ```
    ''')


st.markdown("---")

