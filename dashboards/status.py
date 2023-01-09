import streamlit as st
import win32print


def main():
    st.warning(":warning: This is still under development.")

    st.title("Printers Status")

    printer_name = "Microsoft Print to PDF"

    handle = win32print.OpenPrinter(printer_name)
    # http://timgolden.me.uk/pywin32-docs/win32print__GetPrinter_meth.html
    attributes = win32print.GetPrinter(handle)[13]
    # https://learn.microsoft.com/en-us/windows/win32/printdocs/printer-info-2
    # https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-rprn/1625e9d9-29e4-48f4-b83d-3bd0fdaea787
    # 0x00000400 is the hex code of PRINTER_ATTRIBUTE_WORK_OFFLINE
    st.write(f'{printer_name} is offline? :{(attributes & 0x00000400) >> 10}')


if __name__ == '__main__':
    main()
