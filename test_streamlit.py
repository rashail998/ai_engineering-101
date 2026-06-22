import streamlit as st

# This is the title - renders as big header text
st.title("My First Streamlit App :)")

# This renders a test input box, returns whatever the user typed
user_input = st.text_input("Type something: ")

# This only runs if there's something in the input
if user_input:
    st.write(f"You typed: {user_input}")

# A button - returns True only when clicked
if st.button("Click me!"):
    st.button("Button was clicked!")