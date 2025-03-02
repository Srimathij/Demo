import streamlit as st
import pandas as pd
import requests
from PIL import Image
 
 
 
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
 
   # Load and resize image
    image = Image.open("kgisl-logo.png")
    resized_image = image.resize((200, 75))  # (width, height)
 
    # Display resized image
    st.image(resized_image, use_container_width=False)
 
    st.markdown("<h2 class='center-text'>Tender Document</h2>", unsafe_allow_html=True)
    # Navigation Bar
    # Layout: Sidebar (Navigation) + Main Content + Right Panel
    col1, col2 = st.columns([3, 2])  # Left Sidebar (3) | Right Panel (2)
 
    st.sidebar.title("Menu")
    # Left Sidebar (Navigation Menu)
    with col1:
        st.sidebar.title("Menu")
 
        # Apply custom CSS styling for uniform button width
        st.markdown(
            """
            <style>
                .stButton > button {
                    width: 100%;
                    height: 40px;
                    border-radius: 8px;
                    font-size: 16px;
                }
            </style>
            """,
            unsafe_allow_html=True
        )
 
        # Function to create buttons
        def create_button(text, on_click=None):
            st.sidebar.button(text, key=text, on_click=on_click)
 
        # Define button configurations
        buttons = [
            {"text": "Dashboard", "on_click": lambda: navigate_to("dashboard")},
            {"text": "Logout", "on_click": logout},
            {"text": "Settings", "on_click": None},
            {"text": "Help", "on_click": None},
            {"text": "About", "on_click": None},
        ]
 
        # Render buttons
        for button in buttons:
            create_button(button["text"], button["on_click"])
 
        # Display PDF Files in Table Format
        pdf_files = [
            {"File Name": "Report 1", "Download Link": "https://democppp.nic.in/cppp8/sites/default/files/standard_biddingdocs/Procurement_Consultancy_Services.pdf"},
            {"File Name": "Report 2", "Download Link": "https://democppp.nic.in/cppp8/sites/default/files/standard_biddingdocs/MTD%20Goods%20NIC.pdf"},
        ]
        df = pd.DataFrame(pdf_files)
 
        for index, row in df.iterrows():
            st.write(f"**{row['File Name']}**")
            pdf_content = fetch_pdf(row["Download Link"])
            if pdf_content:
                st.download_button(label="Download", data=pdf_content, file_name=row["File Name"] + ".pdf", mime="application/pdf")
 
            # **Corrigendum Table**
        st.markdown("### 📑 Corrigendum Details")
 
        corrigendum_data = [
            ["CORRIGENDUM IV AND REPLY TO PRE BID QUERIES", "NHAI/Kerala/ 13Nos.Blackspot (24-25)/ EPC", "11-Mar-2025 11:00 AM", "12-Mar-2025 11:30 AM"],
            ["Bid Auto Extn Corrigendum", "AAI/BLY/SnackBar/2025", "08-Mar-2025 06:00 PM", "10-Mar-2025 11:00 AM"],
            ["Bid Auto Extn Corrigendum", "JPL-CnM- 1100012440", "06-Mar-2025 06:00 PM", "08-Mar-2025 11:00 AM"],
            ["Corrigendum for extension of Bid Submission and Opening Date", "NPCIL/KK34/MECH/PT/2025/09", "12-Mar-2025 05:00 PM", "14-Mar-2025 10:00 AM"],
            ["Bid Auto Extn Corrigendum", "AAi/Leh/Comml/SIMCard", "08-Mar-2025 04:00 PM", "10-Mar-2025 04:00 PM"],
            ["Corrigendum02", "HITES/IDS/LATUR/MPCS/24/28", "12-Mar-2025 03:00 PM", "13-Mar-2025 03:00 PM"],
            ["Bid Auto Extn Corrigendum", "P/C/95/SSM/SO/STE/24-25", "08-Mar-2025 03:00 PM", "10-Mar-2025 03:00 PM"],
            ["Bid Auto Extn Corrigendum", "AAI/MDU/COMML/ET/202425/07", "08-Mar-2025 03:00 PM", "10-Mar-2025 03:30 PM"],
            ["Bid Auto Extn Corrigendum", "RFQ No. 11132 for Lifting and lowering of submersible pump and rewinding of motor", "04-Mar-2025 02:30 PM", "06-Mar-2025 09:00 AM"],
            ["Bid Auto Extn Corrigendum", "HLL/CHO/PROJ/INT/IFC/AMEN/2025", "08-Mar-2025 03:00 PM", "10-Mar-2025 03:00 PM"],
        ]
 
        corrigendum_df = pd.DataFrame(
            corrigendum_data,
            columns=["Corrigendum Title", "Reference No", "Closing Date", "Bid Opening Date"]
        )
 
        st.dataframe(corrigendum_df, height=400)
 
 
    # Right Panel (Additional Elements)
    with col2:
        st.markdown("### 🔍 Quick Search")
        search_query = st.text_input("Search for tenders...")
 
        st.markdown("---")
 
        st.markdown("### 📊 Recent Activity")
        st.write("✅ Uploaded Report 1 on Feb 28, 2025")
        st.write("✅ Downloaded Report 2 on Feb 27, 2025")
        st.write("📂 New tender available for review")
 
        st.markdown("---")
 
        st.markdown("### 📌 Notifications")
        st.info("🚀 New tenders will be uploaded tomorrow!")
 
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
