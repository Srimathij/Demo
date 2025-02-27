import streamlit as st
import pandas as pd
import requests

# Function to set background image using CSS
def set_background_image(image_url: str):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url({image_url});
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .center-text {{
            text-align: center;
            font-size: 24px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Initialize session state
def initialize_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "name" not in st.session_state:
        st.session_state.name = ""
    if "number" not in st.session_state:
        st.session_state.number = ""
    if "page" not in st.session_state:
        st.session_state.page = "login"

initialize_session_state()

# Function to handle login
def login():
    if st.session_state.name and st.session_state.number:
        st.session_state.logged_in = True
        st.session_state.page = "dashboard"
    else:
        st.error("Please enter both your name and number!")

# Function to handle logout
def logout():
    st.session_state.logged_in = False
    st.session_state.name = ""
    st.session_state.number = ""
    st.session_state.page = "login"

# Navigation function
def navigate_to(page):
    st.session_state.page = page

# List of Tender PDFs with URLs
pdf_files = [
    {"File Name": "Report 1", "Download Link": "https://democppp.nic.in/cppp8/sites/default/files/standard_biddingdocs/Procurement_Consultancy_Services.pdf"},
    {"File Name": "Report 2", "Download Link": "https://democppp.nic.in/cppp8/sites/default/files/standard_biddingdocs/MTD%20Goods%20NIC.pdf"},
]

# Function to fetch PDF file content
def fetch_pdf(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        st.error(f"Failed to fetch file: {url}")
        return None

# Dashboard Page
def dashboard():
    st.markdown("<h2 class='center-text'>Tender Document</h2>", unsafe_allow_html=True)
    
    # Navigation Bar
    st.sidebar.title("Menu")
    if st.sidebar.button("Dashboard"):
        navigate_to("dashboard")
    st.sidebar.button("Logout", on_click=logout)
    
    # Display PDF Files in Table Format
    df = pd.DataFrame(pdf_files)
    
    for index, row in df.iterrows():
        st.write(f"**{row['File Name']}**")
        pdf_content = fetch_pdf(row["Download Link"])
        
        if pdf_content:
            st.download_button(label="Download", data=pdf_content, file_name=row["File Name"] + ".pdf", mime="application/pdf")

# Login Page
def login_page():
    set_background_image("https://t3.ftcdn.net/jpg/09/66/43/60/360_F_966436072_AsibYvj7JnhEoHQrD0kcxvGdOBFEMpCf.jpg")
    st.markdown("<h1 style='text-align: center;'>EuroMec Dashboard!</h1>", unsafe_allow_html=True)
    st.session_state.name = st.text_input("Enter your Name", placeholder="Enter your name")
    st.session_state.number = st.text_input("Enter your Number", placeholder="Enter your mobile number")
    st.button("Login", on_click=login)

# Page Routing
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "dashboard":
    dashboard()
