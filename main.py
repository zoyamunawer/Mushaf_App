import streamlit as st
import requests

# ========== PAGE CONFIG ==========
st.set_page_config(page_title="Mushaf App", page_icon="📖", layout="wide")

# ========== CUSTOM STYLING ==========
st.markdown(
    """
    <style>
        /* Background gradient */
        .stApp {
            background: linear-gradient(135deg, #d7e9f7, #b5d9f5, #a8e0f0);
            color: #003366;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        /* Titles */
        h1, h2, h3 {
            color: #004d80;
            text-align: center;
            font-weight: bold;
            text-shadow: 1px 1px 2px #ffffff;
        }

        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background: linear-gradient(135deg, #a8e0f0, #d7f5f7);
            color: #003366;
        }
        section[data-testid="stSidebar"] * {
            color: #003366 !important;
            font-weight: 500;
        }

        /* Card-like box for ayahs */
        .ayah-box {
            background: rgba(255, 255, 255, 0.8);
            border-radius: 12px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.2);
        }

        /* Translation box */
        .tr-box {
            background: #f0faff;
            border-left: 4px solid #004d80;
            padding: 10px;
            border-radius: 8px;
            margin-top: 5px;
        }

        /* Footer */
        .footer {
            text-align: center;
            margin-top: 50px;
            font-size: 14px;
            color: #004466;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ========== HEADER ==========
st.image("logo.png", width=120)  # 👈 تم بعد میں اپنی تصویر replace کر دینا
st.title("📖 Mushaf - Quran Explorer")
st.markdown("---")

# ========== SIDEBAR ==========
st.sidebar.title("🔍 Controls")
st.sidebar.write("Select a Surah and Options:")

# Fetch Surah List
surah_list = requests.get("http://api.alquran.cloud/v1/surah").json()["data"]
surah_names = [f"{s['number']}. {s['englishName']} ({s['name']})" for s in surah_list]

selected_surah = st.sidebar.selectbox("Choose a Surah:", surah_names)
selected_surah_num = int(selected_surah.split(".")[0])

# Options
search_keyword = st.sidebar.text_input("Search Ayah in Arabic")
show_tr = st.sidebar.checkbox("Show Translation", value=True)
show_audio = st.sidebar.checkbox("Play Recitation")
tr_choice = st.sidebar.selectbox(
    "Choose Translation:",
    ["ur.maududi", "ur.junagarhi", "ur.jalandhry"]
)

# ========== FETCH AYAH (Arabic & Audio) ==========
recitation_url = f"http://api.alquran.cloud/v1/surah/{selected_surah_num}/ar.alafasy"
rec_response = requests.get(recitation_url).json()
ayah_arabic = rec_response["data"]["ayahs"]

# Fetch Translation if enabled
if show_tr:
    tr_url = f"http://api.alquran.cloud/v1/surah/{selected_surah_num}/{tr_choice}"
    tr_response = requests.get(tr_url).json()
    ayah_tr = tr_response["data"]["ayahs"]
else:
    ayah_tr = [None] * len(ayah_arabic)

# Apply Search Filter
if search_keyword.strip():
    filter_ar = []
    filter_tr = []
    for i, ayah in enumerate(ayah_arabic):
        if search_keyword in ayah["text"]:
            filter_ar.append(ayah)
            filter_tr.append(ayah_tr[i] if show_tr else None)
    ayah_arabic = filter_ar
    ayah_tr = filter_tr

# ========== MAIN CONTENT ==========
st.subheader(selected_surah)

for i, ayah in enumerate(ayah_arabic):
    st.markdown(
        f"""
        <div class="ayah-box">
            <b>{ayah['numberInSurah']}</b> - {ayah['text']}
        </div>
        """, unsafe_allow_html=True
    )

    if show_audio and 'audio' in ayah and ayah["audio"]:
        st.audio(ayah["audio"])

    if show_tr and ayah_tr[i]:
        st.markdown(f"<div class='tr-box'>{ayah_tr[i]['text']}</div>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'>✨ Developed by ZMA✨</div>", unsafe_allow_html=True)
