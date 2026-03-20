import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(page_title="AI-Cook", page_icon="👨‍🍳")

# --- API CONFIG ---
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# --- UI ---
st.title("👨‍🍳 AI-Cook")
st.write("Upload a photo of your ingredients to get a custom recipe!")

uploaded_file = st.file_uploader(
    "Upload ingredient image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Ingredients", use_container_width=True)

    if st.button("Generate Recipe"):

        with st.spinner("Chef Gemini is thinking..."):

            prompt = """
You are a professional chef.

1. Identify the ingredients in the image.
2. Suggest one healthy recipe using them.
3. Provide:
   - Recipe name
   - Ingredient list
   - Step-by-step instructions
   - Optional extra ingredients if needed.
"""

            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[prompt, image]
                )

                st.markdown(response.text)

            except Exception as e:
                st.error(f"AI request failed: {e}")
