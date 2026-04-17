import streamlit as st

# Webpage title
st.title('Streamlit Markdown Example')

# Markdown text stored in a variable
markdown_text = '''
## Building a ML Model Drift Detection System with Streamlit and Python

### 👨‍💻 Developer
**Md Ali Shekh** — Backend Developer
[GitHub](https://github.com/mdalishekh) 
[LinkedIn](https://linkedin.com/in/mdalishekh)
'''

# Render the markdown content
st.markdown(markdown_text)
