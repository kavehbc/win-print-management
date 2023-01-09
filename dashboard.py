import streamlit as st
from utils.menu_options import get_dic_keys, get_dic_code, get_dic_index_by_key
import dashboards


def main():
    options = {"printer": "Printer Management",
               "report": "Reporting & Visualization",
               "about": "About"}

    selected_menu = st.sidebar.selectbox("Main Menu", options=get_dic_keys(options),
                                         format_func=lambda x: get_dic_code(options, x),
                                         index=get_dic_index_by_key(options, "printer"))

    if selected_menu == "printer":
        dashboards.printer.main()
    elif selected_menu == "report":
        dashboards.report.main()
    elif selected_menu == "about":
        dashboards.help.main()


if __name__ == '__main__':
    st.set_page_config(
        page_title="Print Server Monitoring",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/kavehbc/win-print-management',
            'Report a bug': "https://github.com/kavehbc/win-print-management",
            'About': """
            # Print Server Monitoring
            
            Version 1.0 - By [Kaveh Bakhtiyari](http://kaveh.me)
            """
        }
    )
    main()
