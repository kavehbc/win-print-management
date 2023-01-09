import win32print
import pandas as pd
from datetime import datetime
from dateutil import tz


def get_printer_details(printer_name):
    handle = win32print.OpenPrinter(printer_name)
    # http://timgolden.me.uk/pywin32-docs/win32print__GetPrinter_meth.html
    printer_details = win32print.GetPrinter(handle)

    printer_attributes = printer_details[13]
    printer_status = printer_details[18]
    printer_jobs = printer_details[19]

    # https://learn.microsoft.com/en-us/windows/win32/printdocs/printer-info-2
    # https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-rprn/1625e9d9-29e4-48f4-b83d-3bd0fdaea787
    # 0x00000400 is the hex code of PRINTER_ATTRIBUTE_WORK_OFFLINE
    printer_offline = (printer_attributes & 0x00000400) >> 10

    return_dict = {"raw": printer_details,
                   "attributes": printer_attributes,
                   "status": printer_status,
                   "jobs": printer_jobs,
                   "live": not printer_offline}
    return return_dict


def restart_last_job(printer_name):
    job_id, _ = last_job(printer_name)
    set_job_command(printer_name, job_id, command=win32print.JOB_CONTROL_RESTART)
    return job_id


def set_job_command(printer_name, job_id, command=win32print.JOB_CONTROL_RESTART):
    printer_handle = win32print.OpenPrinter(printer_name)
    # http://timgolden.me.uk/pywin32-docs/win32print__SetJob_meth.html
    win32print.SetJob(printer_handle, job_id, 0, None, command)
    win32print.ClosePrinter(printer_handle)
    return 1


def last_job(printer_name):
    df_printers, df_jobs = get_printers_jobs()

    if df_jobs.shape[0] > 0:
        df_jobs_filtered = df_jobs.loc[df_jobs["pPrinterName"] == printer_name]

        if df_jobs_filtered.shape[0] > 0:
            submitted_date_time = df_jobs_filtered["Submitted"].max()
            job_id = df_jobs_filtered.loc[df_jobs_filtered["Submitted"] == submitted_date_time]["JobId"].max()
        else:
            submitted_date_time = None
            job_id = None
    else:
        submitted_date_time = None
        job_id = None

    return job_id, submitted_date_time


def _get_jobs(printer_name):
    jobs = []
    printer_handle = win32print.OpenPrinter(printer_name)
    print_jobs = win32print.EnumJobs(printer_handle, 0, -1, 1)
    # if print_jobs:
    #     jobs.extend(list(print_jobs))
    for job in print_jobs:
        submitted = str(job["Submitted"])
        # sample format 2023-01-05 07:09:48.772000+00:00
        obj_dt = datetime.strptime(submitted.rstrip("+00:00"), '%Y-%m-%d %H:%M:%S.%f')

        utc_zone = tz.tzutc()
        local_zone = tz.tzlocal()

        # set obj_dt to UTC
        obj_dt = obj_dt.replace(tzinfo=utc_zone)
        # convert from UTC to local timezone
        local_date_time = obj_dt.astimezone(local_zone)

        # remove timezone from date/time
        local_date_time = local_date_time.replace(tzinfo=None)

        job["Submitted"] = local_date_time
        jobs.append(job)

    win32print.ClosePrinter(printer_handle)

    return jobs


def get_printers_jobs():
    """
    Prints out all jobs in the print queue
    https://www.blog.pythonlibrary.org/2013/12/19/pywin32-monitor-print-queue/
    """
    printers = []
    printers_columns = ["flags", "desc", "name", "comment", "live"]
    jobs = []
    for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL,
                                           None, 1):
        flags, desc, printer_name, comment = printer

        # converting tuple to list to make it modifiable
        printer = list(printer)

        # check if printer is live
        printer_details = get_printer_details(printer_name)
        # adding the printer's status to the list
        printer.append(printer_details["live"])

        # appending the printer info + status to the list of all printers
        printers.append(list(printer))
        jobs.extend(_get_jobs(printer_name))

    df_printers = pd.DataFrame(printers, columns=printers_columns)
    df_jobs = pd.DataFrame.from_dict(jobs)

    if df_jobs.shape[0] == 0:
        df_printers["jobs"] = 0
    else:
        df_jobs_count = df_jobs.groupby(['pPrinterName'])['JobId'].count()
        df_printers = df_printers.merge(df_jobs_count, how='left',
                                        left_on='name', right_on='pPrinterName', suffixes=(False, False))
        df_printers.rename(columns={'JobId': 'jobs'}, inplace=True)
        df_printers["jobs"].fillna(0, inplace=True)

    # remove time zone and convert to datetime object
    df_jobs["Submitted"] = pd.to_datetime(df_jobs["Submitted"])

    df_printers = df_printers[["name", "desc", "jobs", "live"]]
    df_printers = df_printers.astype(
        {'name': 'string',
         'desc': 'string',
         'jobs': 'int',
         'live': 'bool',
         }
    )

    df_jobs = df_jobs.astype(
        {'Submitted': 'datetime64[ns]'}
    )

    # sorting printer names ASC
    df_printers.sort_values(by='name', ascending=True, inplace=True)
    # sorting jobs DESC
    if df_jobs.shape[0] > 0:
        df_jobs.sort_values(by=['Submitted', 'JobId'], ascending=False, inplace=True)

    return df_printers, df_jobs
