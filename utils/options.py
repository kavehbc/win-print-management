from utils.printer_job import get_printers_jobs


def printers_list():
    df_printers, _ = get_printers_jobs()
    return df_printers["name"].tolist()


def command_list():
    commands = ["RESTART", "CANCEL", "DELETE", "PAUSE", "RESUME"]
    return commands
