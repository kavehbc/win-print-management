import streamlit as st
from utils.markdown import show_readme


def main():
    show_readme("README.md")
    st.markdown("___")
    st.subheader("LICENSE")
    show_readme("LICENSE")


if __name__ == '__main__':
    main()
