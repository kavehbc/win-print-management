# Windows Print Management Web-based Dashboard

This program contains two main components:
1. Dashboard `dashboard.py`:

This is a web-based dashboard by `Streamlit` to monitor and control the printers and their jobs.
Each printer job can be restarted, paused, canceled, deleted and resumed.
There is a reporting and visualization section which plots the jobs on printers based on a given
timeframe.

2. REST API `api.py`:

This is a RESTful API developed by `FastAPI` to provide remote control over the printers and their jobs.

> In order to monitor and control the printer's job, make sure to enable `Keep printed documents` under the `Advanced` tab of the printer's settings.

## Execution
We firstly need to create a `conda` environment

```bash
conda env create -f environment.yml
```

Once the environment is created, we should activate it.

```bash
conda activate print-server
```

Now, we can run the Streamlit dashboard and/or FastAPI.

**Batch File**
```bash
run.bat
```

By running the above batch file, you will be given the option to select the application you wish to run.

**Streamlit**
```bash
streamlit run dashboard.py
```

**FastAPI**
```bash
python api.py --port=5000
```

## Streamlit
Once the dashboard is running, Streamlit would report the port number on which it is running.
By default, if there is no other Streamlit app running, the port number is `8501`. The dashboard can be accessed via:

http://localhost:8501

`localhost` can be replaced with any other domain/host name or IP address of the machine.

## FastAPI
FastAPI supports OpenAPI, and it comes with two UIs of Swagger and ReDoc to fetch API functions and test them.
The default port number set for the API is `5000`, unless changed in the runtime or the source code.

- **OpenAPI**<br/>
http://localhost:5000/v1.0/openapi.json

- **Swagger**<br/>
http://localhost:5000/v1.0/docs

- **ReDoc**<br/>
http://localhost:5000/v1.0/redoc

___
## GitHub Repo
This project is open-source, and it is available on GitHub at [https://github.com/kavehbc/win-print-management](https://github.com/kavehbc/win-print-management).

## Developer(s)
Kaveh Bakhtiyari - [Website](http://bakhtiyari.com) | [Medium](https://medium.com/@bakhtiyari)
  | [LinkedIn](https://www.linkedin.com/in/bakhtiyari) | [GitHub](https://github.com/kavehbc)

## Contribution
Feel free to join the open-source community and contribute to this repository.

## References
- [Streamlit](https://streamlit.io/)<br/>
  This package is used to develop the dashboards

- [FastAPI](https://fastapi.tiangolo.com/)<br/>
  The module is used to develop REST APIs with Swagger UI

- [Win32Print](http://timgolden.me.uk/pywin32-docs/win32print.html)<br/>
  This library meditates between the Python app and Windows Print APIs

- [Uvicorn](https://www.uvicorn.org/)<br/>
  This is an ASGI web server for Python used for FastAPI