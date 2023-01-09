import streamlit as st
from utils.markdown import show_markdown


def main():
    show_markdown("README.md")
    st.markdown("___")
    st.subheader("LICENSE")
    show_markdown("LICENSE")


if __name__ == '__main__':
    main()
