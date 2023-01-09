import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import numpy as np

from utils.printer_job import get_printers_jobs


def main():
    st.title("Reporting & Visualization")
    df_printers, df_jobs = get_printers_jobs()

    all_printers = df_printers["name"].unique().tolist()
    selected_printers = st.sidebar.multiselect("Select Printers", options=all_printers)
    st.sidebar.caption("No printer selected = all printers selected")
    if len(selected_printers) == 0:
        selected_printers = all_printers

    min_date_time = df_jobs["Submitted"].min()
    last_24hours = datetime.today() - timedelta(hours=24)

    col1, col2 = st.sidebar.columns(2)
    from_date = col1.date_input("From Date",
                                value=last_24hours.date(),
                                min_value=min_date_time.date(),
                                max_value=datetime.today().date())
    from_time = col2.time_input("From Time")
    from_date_time = datetime.combine(from_date, from_time)

    col1, col2 = st.sidebar.columns(2)
    to_date = col1.date_input("To Date",
                              value=datetime.today().date(),
                              min_value=min_date_time.date(),
                              max_value=datetime.today().date())
    to_time = col2.time_input("To Time")
    to_date_time = datetime.combine(to_date, to_time)

    # Applying Filters
    df_filtered_jobs = df_jobs.loc[(df_jobs["pPrinterName"].isin(selected_printers))
                                   & (df_jobs["Submitted"] >= from_date_time)
                                   & (df_jobs["Submitted"] <= to_date_time)]
    df_filtered_printers = df_printers.loc[(df_printers["name"].isin(selected_printers))]

    # Reporting Starts Here
    st.success(f"Total Jobs: {df_filtered_jobs.shape[0]}")

    # Printers Jobs
    st.subheader("Printers Jobs")
    df_printers_jobs = df_filtered_printers.merge(df_filtered_jobs, left_on='name', right_on='pPrinterName', how="left")
    df_printers_jobs["count"] = np.where(df_printers_jobs["pPrinterName"].isnull(), 0, 1)
    df_printers_jobs = df_printers_jobs.groupby(['name'])['count'].sum()
    st.bar_chart(df_printers_jobs)

    # Hourly Distribution
    st.subheader("Hourly Distribution")

    lst_hours = list(range(24))
    df_hours = pd.DataFrame(lst_hours, columns=["hours"])

    df_filtered_jobs["hours"] = df_filtered_jobs["Submitted"].dt.hour
    df_hours = df_hours.merge(df_filtered_jobs, left_on='hours', right_on='hours', how="left")
    df_hours["count"] = np.where(df_hours["pPrinterName"].isnull(), 0, 1)
    df_hours = df_hours.groupby(['hours'])['count'].sum()
    st.line_chart(df_hours)


if __name__ == '__main__':
    main()
