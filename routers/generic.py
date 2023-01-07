from fastapi import APIRouter
from fastapi.responses import HTMLResponse


router = APIRouter()


@router.get("/", include_in_schema=False, response_class=HTMLResponse)
def homepage():
    """
    This is the default page
    :return: a hello world message
    """
    html_file_path = "responses/homepage.html"
    with open(html_file_path, 'r', encoding="utf-8") as outfile:
        html_content = outfile.read()

    return HTMLResponse(html_content, status_code=200)
