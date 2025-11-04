import streamlit as st
from recommender import recommend_games
import base64

# --- Encode background image ---
image_path = "background.jpeg"
with open(image_path, "rb") as f:
    encoded_image = base64.b64encode(f.read()).decode()

# --- Page config ---
st.set_page_config(page_title="🎮 Game Recommender", layout="centered")

# --- CSS styling ---
st.markdown(f"""
<style>
.stApp {{
    background-image: url("data:image/jpeg;base64,{encoded_image}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* Gradient overlay for better readability */
[data-testid="stAppViewContainer"]::before {{
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.3));
    z-index: 0;
}}

.stApp > div:first-child {{
    position: relative;
    z-index: 1;
}}

h1, h2, h3, h4, label, p {{
    color: white !important;
    text-shadow: 1px 1px 4px rgba(0,0,0,0.8);
}}

[data-testid="stHeader"] {{
    display: none;
}}
</style>
""", unsafe_allow_html=True)


# --- Actual content inside container ---
with st.container():
    st.markdown('<div class="main-box">', unsafe_allow_html=True)

    st.title("🎮 Game Recommender System")
    st.markdown("Find the **best games** for you using AI")

    query = st.text_input("Describe the kind of game you want:",
                          "e.g. open-world fantasy RPG with dragons")

    top_n = st.slider("Number of recommendations:", 1, 20, 5)

    with st.expander("Advanced Settings (Weights)"):
        alpha = st.slider("Story Weight", 0.0, 1.0, 0.6)
        beta = st.slider("Genre Match Weight", 0.0, 1.0, 0.2)
        gamma = st.slider("Game Score Weight", 0.0, 1.0, 0.2)

    if st.button("🔍 Recommend Games"):
        if query.strip() == "":
            st.warning("Please enter a game description first.")
        else:
            with st.spinner("Finding your perfect games..."):
                results = recommend_games(query, top_n, alpha, beta, gamma)

            st.success("Here are your recommended games:")
            for _, row in results.iterrows():
                st.subheader(f"🎮 {row['Game']} (Score: {row['Score']:.2f})")
                st.caption(f"Genres: {row['Genres']} | Match Score: {row['Hybrid_Score']:.2f}")
                st.write(row['Summary'])
                st.write(row['Page'])
                st.divider()

    st.markdown('</div>', unsafe_allow_html=True)

# --- Signature / Footer ---
st.markdown("""
<style>
.footer {
    position: relative;
    bottom: 0;
    width: 100%;
    padding: 1.2rem 0;
    text-align: center;
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.8);
    background: rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(6px);
    border-top: 1px solid rgba(255,255,255,0.2);
    margin-top: 3rem;
}

.footer a {
    color: #00b4d8;
    text-decoration: none;
    margin: 0 0.5rem;
}

.footer a:hover {
    text-decoration: underline;
}
</style>

<div class="footer">
    <p>🎮 <b>Game Recommender System</b> — discover your next favorite game using AI-powered recommendations.</p>
    <p>
         <a href="https://github.com/uguratli" target="_blank">GitHub</a> |
         <a href="https://www.kaggle.com/uuratl" target="_blank">Kaggle</a> |
         <a href="mailto:uguratli.contact@gmail.com">Email</a>
    </p>
    <p>Made with ❤️ using <b>Streamlit</b> and <b>Python</b> by <b>Your Name</b>.</p>
</div>
""", unsafe_allow_html=True)