# Windows Print Management Dashboard & REST API

This program contains two main components:
1. Dashboard `dashboard.py`:

This is a web-based dashboard by `Streamlit` to monitor the printers and their jobs.
Each printer job can be restarted, paused, canceled, deleted and resumed.

2. REST API `api.py`:

This is a RESTful API developed by `FastAPI` to give control over the printers and their jobs.

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

Streamlit
```bash
streamlit run dashboard.py
```

FastAPI
```bash
python -m api.py --port=5000
```

___
## GitHub Repo
This project is open-source, and it is available on GitHub at [https://github.com/kavehbc/win-print-management](https://github.com/kavehbc/win-print-management).

## Developer(s)
Kaveh Bakhtiyari - [Website](http://bakhtiyari.com) | [Medium](https://medium.com/@bakhtiyari)
  | [LinkedIn](https://www.linkedin.com/in/bakhtiyari) | [Github](https://github.com/kavehbc)

## Contribution
Feel free to join the open-source community and contribute to this repository.
