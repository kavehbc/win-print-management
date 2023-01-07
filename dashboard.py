import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import win32print
from utils.printer_job import get_printers_jobs, set_job_command


def main():
    st.title("FC Print Server Monitor")

    df_printers, df_jobs = get_printers_jobs()

    st.subheader(f"Printers: #{df_printers.shape[0]}")

    gb = GridOptionsBuilder.from_dataframe(df_printers)
    gb.configure_selection("single")
    gb.configure_grid_options(domLayout='normal')
    grid_options = gb.build()

    grid_response = AgGrid(
        df_printers,
        gridOptions=grid_options,
        height=300,
        width='100%',
        data_return_mode=DataReturnMode.FILTERED,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
        enable_enterprise_modules=False
        )

    selected_printer = grid_response['selected_rows']
    if len(selected_printer) > 0 and df_jobs.shape[0] > 0:
        printer_name = selected_printer[0]["name"]

        df_jobs_filtered = df_jobs.loc[df_jobs["pPrinterName"] == printer_name]
        st.subheader(f"Jobs: #{df_jobs_filtered.shape[0]}")

        gb = GridOptionsBuilder.from_dataframe(df_jobs_filtered)
        gb.configure_selection("multiple",
                               use_checkbox=True, groupSelectsChildren=True, groupSelectsFiltered=True,
                               header_checkbox=True, header_checkbox_filtered_only=True)

        # gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_grid_options(domLayout='normal')
        grid_options = gb.build()

        grid_response = AgGrid(
            df_jobs_filtered,
            gridOptions=grid_options,
            height=300,
            width='100%',
            data_return_mode=DataReturnMode.FILTERED,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            fit_columns_on_grid_load=False,
            allow_unsafe_jscode=True,
            enable_enterprise_modules=False
            )

        selected_jobs = grid_response['selected_rows']
        # st.write(selected_jobs)

        if len(selected_jobs) > 0:
            st.subheader("Actions")

            col1, col2, col3, col4, col5 = st.columns(5)
            btn_restart = col1.button("Restart")
            btn_cancel = col2.button("Cancel")
            btn_delete = col3.button("Delete")
            btn_pause = col4.button("Pause")
            btn_resume = col5.button("Resume")

            btn_clicked = False
            if btn_restart:
                command = win32print.JOB_CONTROL_RESTART
                btn_clicked = True
            if btn_cancel:
                command = win32print.JOB_CONTROL_CANCEL
                btn_clicked = True
            if btn_delete:
                command = win32print.JOB_CONTROL_DELETE
                btn_clicked = True
            if btn_pause:
                command = win32print.JOB_CONTROL_PAUSE
                btn_clicked = True
            if btn_resume:
                command = win32print.JOB_CONTROL_RESUME
                btn_clicked = True

            if btn_clicked:
                for job in selected_jobs:
                    set_job_command(job["pPrinterName"], job["JobId"], command)
                st.experimental_rerun()


if __name__ == '__main__':
    st.set_page_config(
        page_title="FC Print Server Monitor",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "https://www.extremelycoolapp.com/bug",
            'About': "# FC Print Server Monitor"
        }
    )
    main()
