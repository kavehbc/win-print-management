import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import win32print
import datetime
import asyncio
from utils.date_time import get_date_time_delta
from utils.printer_job import get_printers_jobs, set_job_command, last_job


async def watch(st_status):
    while True:
        df_printers, _ = get_printers_jobs()
        if "printers" not in st.session_state:
            local_printers = df_printers.copy()
        else:
            local_printers = st.session_state["printers"]

        if not df_printers.equals(local_printers):
            # st.write("There is an update")
            st_status.info("Update: Updating...")
            st.experimental_rerun()
        else:
            st_status.info("Update: Live")

        _ = await asyncio.sleep(1)


def main():
    st.title("Print Server Monitor")

    chk_live = st.sidebar.checkbox("Live Update")

    df_printers, df_jobs = get_printers_jobs()
    st.session_state["printers"] = df_printers

    st.subheader(f"Printers")
    total_printers = df_printers.shape[0]
    live_printers = df_printers.loc[(df_printers["live"])].count()[0]
    offline_printers = df_printers.loc[(~df_printers["live"])].count()[0]

    col1, col2, col3, col4 = st.columns(4)
    st_status = col1.empty()
    col2.warning(f"TOTAL: **{total_printers}**")
    col3.success(f"LIVE: **:green[{live_printers}]**")
    col4.error(f"OFFLINE: **:red[{offline_printers}]**")

    js_code = JsCode("""
                function(params) {
                    if (params.data.live === false) {
                        return {
                            'color': 'white',
                            'backgroundColor': 'red'
                        }
                    }
                };
                """)

    gb = GridOptionsBuilder.from_dataframe(df_printers)
    gb.configure_selection("single")
    gb.configure_grid_options(domLayout='normal')
    gb.configure_column("name", header_name="Printer Name")
    gb.configure_column("desc", header_name="Description")
    gb.configure_column("jobs", header_name="# of Jobs", width=50)
    gb.configure_column("live", header_name="Live", width=50)
    grid_options = gb.build()
    grid_options['getRowStyle'] = js_code

    grid_response = AgGrid(
        df_printers,
        gridOptions=grid_options,
        height=300,
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
        last_job_id, last_job_date_time = last_job(printer_name)
        if last_job_date_time is None:
            minutes_diff = None
        else:
            last_job_date_time = last_job_date_time.replace(microsecond=0)
            minutes_diff = get_date_time_delta(last_job_date_time)

        st.subheader(f"Jobs ({printer_name})")

        col1, col2 = st.columns(2)
        col1.info(f"Total Jobs: **{df_jobs_filtered.shape[0]}**")
        col2.success(f"Last Job: {last_job_id} / {last_job_date_time} - {'' if minutes_diff is None else str(minutes_diff) + ' min. ago'}")

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

    if chk_live:
        asyncio.run(watch(st_status))
    else:
        st_status.info(f"Update: {datetime.datetime.now().time().replace(microsecond=0)}")


if __name__ == '__main__':
    main()
