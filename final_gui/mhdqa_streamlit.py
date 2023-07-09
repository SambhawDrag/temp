import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
import datetime
import base64
from pathlib import Path
from utilities import load_bootstrap
from ui_elements import message_func

# Compulsorily the first part of the script and can be set only once
# Set the page configuration that has the following fields:
st.set_page_config(page_title="MHDQA-GUI",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="",
    menu_items={
        'About': '''### Multi-Hop Document Based Open-Domain Question Answering
    > To use the application, upload all your necessary documents and ask a question.
    > For the background documentation refer: [Confluence Page]()'''
    }
)

## Helper Functions:
load_bootstrap()
def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded
def img_to_html(img_path):
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
      img_to_bytes(img_path)
    )
    return img_html

# Initial message
INITIAL_MESSAGE = [
    {
        "role": "user", 
        "content": "Hello."
    },
    {
        "role": "assistant",
        "content": "Hey. I'm a document grounded, question answering system. You can upload your documents, and ask questions, related to them.",
    },
]

st.markdown(
    """
    <style>
        .reportview-container .main .block-container {
            max-width: 1200px;
        }
        .stButton>button {
            border-radius: 10px;
        }
        .stTextInput>div>div>input {
            border-radius: 25px;
        }
        .stSidebar .sidebar .sidebar-content {
            background-color: black;
        }
        .sidebar .block-container {
            border-radius: 10px;
        }
        .file-info-box {
            background-color: black;
            border-radius: 15px;
            padding: 10px;
            margin: 10px 0;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# The Sidebar - Document Uploading and Listing, with details

with st.sidebar:
    # Set the sidebar title
    st.markdown(
        "<h1 style='font-family:sans-serif; color:#000;'>MHDQA: <br> Multi-Hop Document Question Answering</b></h1>",
        unsafe_allow_html=True
    )

    # Placeholder for uploading documents
    st.markdown('''
    ## :page_facing_up: **Documents**
    **Upload your documents here &darr;**
    _(Use PDFs preferably)_''')

    uploaded_files = st.file_uploader(
                                    "**+ New Document**",
                                    type=["pdf", "doc", "docx"],
                                    accept_multiple_files=True,
                                    )   
    # Placeholder for listing uploaded documents
    st.markdown("""<hr style="border:2px solid gray">""", unsafe_allow_html=True)
    add_vertical_space(3)
    document_list = st.sidebar.empty()

    # Store uploaded files details
    uploaded_documents = []
    # Process uploaded files
    for uploaded_file in uploaded_files:
        # Placeholder for processing uploaded files
        file_size = (uploaded_file.size/(1024*1024))
        uploaded_documents.append({
            'file_name': uploaded_file.name,
            'file_size': file_size,
            'upload_date': datetime.datetime.now(),
            # Placeholder for number of pages
            'number_of_pages': 'N/A'
        })
    
    # Display uploaded files in the sidebar:
    uploaded_documents = sorted(uploaded_documents, key=lambda x: x['upload_date'], reverse=True)
    document_list.markdown(f"""<div style='background-color: #000; color: #FFF; border-radius: 5px; padding: 10px;'>
                           <b> Uploaded Documents : </b>
                           </div>""", 
                           unsafe_allow_html=True)
    st.markdown("""<hr style="border:2px solid gray">""", unsafe_allow_html=True)
    add_vertical_space(1)
    for document in uploaded_documents:
        if st.sidebar.button(document['file_name']):
            # Placeholder for opening document in a new tab
            pass
        st.sidebar.markdown(
            f"""
            <div style='background-color: #6B96C3; color: #FFF; border-radius: 10px; padding: 10px;'>
            <p>File Name: {document['file_name']}</p>
            <p>File Size: {"%.2f" % (document['file_size'])} MB</p>
            <p>Upload Date: {document['upload_date']}</p>
            <p>Total Pages: {document['number_of_pages']}</p>
            </div>""",
            unsafe_allow_html=True
        )
        st.sidebar.markdown("---")

    # Placeholder for Restart Button
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    if st.sidebar.button("Restart Chat"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.session_state["messages"] = INITIAL_MESSAGE
        st.session_state["history"] = []


# Chat Header Ribbon
col1, col2, col3 = st.columns([1, 3, 4])
with col1:
    # Placeholder for logo
    st.markdown(img_to_html('Goldman_Sachs.png'), unsafe_allow_html=True)

with col2:
    st.markdown(
        "<h1 style='font-family:Helvetica; color:#6B96C3;'><b>Ask Me Anything: <br> Credit Risk Assistant</b></h1>",
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        "<h2 style='text-align: right; background-color: rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 40px;'><i>Document Based Question Answering</i></h2>",
        unsafe_allow_html=True
    )

# Session State for Chat
if "messages" not in st.session_state.keys():
    st.session_state["messages"] = INITIAL_MESSAGE

if "history" not in st.session_state:
    st.session_state["history"] = []

with open("styles.md", "r") as styles_file:
    styles_content = styles_file.read()
st.write(styles_content, unsafe_allow_html=True)


# Chat Functions
# ------------------------------
def get_question():
    question = st.chat_input(placeholder="Your question here...", 
                             key="input",
                             )
    return question

def generate_response(prompt):
    response = "Will be modified: " + prompt
    return response

def append_chat_history(question, answer):
    st.session_state["history"].append((question, answer))

def append_message(content, role="assistant", display=False):
    message = {"role": role, "content": content}
    message_func(content, False, display)
    st.session_state.messages.append(message)
    if role != "data":
        append_chat_history(st.session_state.messages[-2]["content"], content)


## Message Flow
# ------------------------------
question = get_question()
if question:
    st.session_state.messages.append({"role": "user", "content": question})

for message in st.session_state.messages:
    message_func(
        message["content"],
        True if message["role"] == "user" else False,
        True if message["role"] == "data" else False,
    )

if st.session_state.messages[-1]["role"] != "assistant":
    content = st.session_state.messages[-1]["content"]
    if isinstance(content, str):
        result = generate_response(content)
        append_message(result)
