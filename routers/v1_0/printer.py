from fastapi import APIRouter, Query
import win32print
from utils.options import printers_list, command_list
from utils.printer_job import get_printers_jobs, set_job_command, last_job

router = APIRouter(
    prefix="",
    tags=[""],
    #    dependencies=[Depends(get_token_header)],
    #    responses={404: {"description": "Not found"}},
)


# current_user: User = Depends(get_current_user)
@router.get("/")
def version():
    return "v1.0"


@router.get("/printers")
def get_all_printers():
    """
    Get the list of all printers \n
    :return: Pandas dataframe in the JSON format
    """
    df_printers, _ = get_printers_jobs()
    return df_printers.to_json(orient='index')


@router.get("/jobs")
def get_all_jobs():
    """
    Get the list of all jobs for all printers \n
    :return: Pandas dataframe in the JSON format
    """
    _, df_jobs = get_printers_jobs()
    return df_jobs.to_json(orient='index')


@router.post("/printer/jobs")
def get_jobs_by_printer_name(printer_name: str = Query(None, description="Printer Name")):
    """
    Get the list of all jobs by a printer name \n
    :param printer_name: Printer Name \n
    :return: Pandas dataframe in the JSON format
    """

    df_printers, df_jobs = get_printers_jobs()
    df_jobs_filtered = df_jobs.loc[df_jobs["pPrinterName"] == printer_name]
    return df_jobs_filtered.to_json(orient='index')


@router.post("/printer/command")
def execute_by_job_id(printer_name: str = Query(..., enum=printers_list(), description="Printer Name"),
                      job_id: int = Query(None, description="Printer JobID"),
                      command: str = Query(..., enum=command_list(), description="Printer Command")):
    """
    Execute a printer command based on a printer name and job id \n
    :param printer_name: Printer Name \n
    :param job_id: Job ID (int) \n
    :param command: Printer command (e.g. RESTART, CANCEL, DELETE, PAUSE, RESUME) \n
    :return: "OK"
    """

    if command == "RESTART":
        cmd_printer = win32print.JOB_CONTROL_RESTART
    if command == "CANCEL":
        cmd_printer = win32print.JOB_CONTROL_CANCEL
    if command == "DELETE":
        cmd_printer = win32print.JOB_CONTROL_DELETE
    if command == "PAUSE":
        cmd_printer = win32print.JOB_CONTROL_PAUSE
    if command == "RESUME":
        cmd_printer = win32print.JOB_CONTROL_RESUME

    try:
        set_job_command(printer_name, job_id, cmd_printer)
        status = "OK"
    except:
        status = "Failed"

    return {"status": status}


@router.post("/printer/last_job")
def last_job_by_printer_name(printer_name: str = Query(..., enum=printers_list(), description="Printer Name")):
    """
    This returns the last JobID and Submitted date/time by printer name \n
    :param printer_name: Printer Name \n
    :return: job_id, submitted date/time
    """

    job_id, submitted_date_time = last_job(printer_name)

    return {"job_id": job_id, "submitted": submitted_date_time}
