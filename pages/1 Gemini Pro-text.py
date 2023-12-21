import google.generativeai as genai
import streamlit as st
import json
import markdown
from io import BytesIO

# Function to initialize session state
def initialize_session_state():
    return st.session_state.setdefault('api_key', None)

# Main Streamlit app
def text_page():
    st.title("Gemini BitDoze")

    # Initialize session state
    initialize_session_state()

    # Configure API key
    api_key = st.sidebar.text_input("Enter your API key:", value=st.session_state.api_key)

    # Check if the API key is provided
    if not api_key:
        st.sidebar.error("Please enter your API key.")
        st.stop()
    else:
        # Store the API key in session state
        st.session_state.api_key = api_key

    genai.configure(api_key=api_key)

    # Set up the prompt input field
    prompt = st.text_area("Enter your Query:", height=200)

    # Submit button to generate text
    if st.button("Generate Text"):
        # Check if prompt is provided
        if not prompt:
            st.error("Please enter your query.")
            st.stop()


        # Configure the model
        generation_config = {
            "temperature": 0.9,
            "top_p": 1.0,
            "top_k": 1,
            "max_output_tokens": 1024,
        }

        safety_settings = "{}"
        safety_settings = json.loads(safety_settings)
        
        # Generate text using Gemini Pro
        gemini = genai.GenerativeModel(model_name="gemini-pro",
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)

        # Pass the prompt as the contents argument
        response = gemini.generate_content(contents=[prompt])

        # Display generated text
        st.subheader("Gemini:")

        if response.text:
            st.write(response.text)

            # Markdown Download
            markdown_str = f"## Gemini Output:\n\n{response.text}"
            markdown_file = BytesIO()
            markdown_file.write(markdown_str.encode('utf-8'))

            # Use streamlit.markdown() to render the Markdown code directly in a text area
            st.markdown(markdown_str)

            # Download button for Markdown
            st.markdown(
                "### Download Markdown",
                unsafe_allow_html=True,
                key="markdown-download",
                on_click=lambda: download_file(markdown_file, "Gemini_Output.md"),
            )

            # HTML Download
            html_str = f"<h2>Gemini Output:</h2>\n\n{response.text}"
            html_file = BytesIO()
            html_file.write(html_str.encode('utf-8'))

            # Download button for HTML
            st.markdown(
                "### Download HTML",
                unsafe_allow_html=True,
                key="html-download",
                on_click=lambda: download_file(html_file, "Gemini_Output.html"),
            )

        else:
            st.write("No output from Gemini.")

# Function to download file
def download_file(file, filename):
    file.seek(0)
    st.download_button(
        label="Click here to download",
        key=filename,
        data=file.read(),
        file_name=filename,
        mime="text/markdown",
    )

# Run the Streamlit app
if __name__ == "__main__":
    text_page()
