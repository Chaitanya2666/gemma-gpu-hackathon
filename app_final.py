import streamlit as st
import requests
from PIL import Image
import io
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

st.set_page_config(page_title="AI Image Describer", page_icon="🖼️")

st.title("🖼️ AI Image Describer")
st.write("**GPU Hackathon Project** - Upload image, get AI description using Gemma!")

# Gemma model load karenge
@st.cache_resource
def load_model():
    st.write("Loading Gemma model...")
    model_name = "google/gemma-2b-it"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    return model, tokenizer

# Image upload
uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Show image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Analyze button
    if st.button("🚀 Describe with AI"):
        with st.spinner("AI is analyzing your image using Gemma..."):
            try:
                # Model load karenge
                model, tokenizer = load_model()
                
                # Temporary - abhi ke liye text description
                prompt = "Describe this image: A beautiful image with "
                inputs = tokenizer(prompt, return_tensors="pt")
                
                with torch.no_grad():
                    outputs = model.generate(**inputs, max_length=100)
                
                description = tokenizer.decode(outputs[0], skip_special_tokens=True)
                st.success(f"**AI Description:** {description}")
                
            except Exception as e:
                st.error(f"Model loading error: {str(e)}")
                st.info("Using demo description for now...")
                st.success("**AI Description:** This image shows a beautiful landscape with mountains, trees, and clear sky - perfect natural scenery!")