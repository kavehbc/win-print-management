from fastapi import FastAPI
import click
import uvicorn

# --- Custom Libraries ---
import routers

available_versions = [
                        {"version": "v1.0", "url": "/v1.0", "description": "Version 1.0"}
                     ]

app = FastAPI(title="Print Server API",
              version="1.0",
              description="Check the compatibility version in each corresponding API.",
              root_path="")

app.include_router(routers.generic.router)


@app.on_event("startup")
def startup():
    print("API Starting...")


@app.on_event("shutdown")
def shutdown():
    print("API Shutting down...")


@app.get("/versions")
def get_all_versions():
    return available_versions


v1_0 = FastAPI(title="Print Server API",
               version="1.0",
               description="Print Server API v. 1.0")
v1_0.include_router(routers.v1_0.printer.router)
v1_0.include_router(routers.v1_0.authenticate.router)
app.mount("/v1.0", v1_0)


@click.command()
@click.option('--port', default=5000, help='Server port')
def run(port):
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=True, access_log=False)


if __name__ == "__main__":
    run()
