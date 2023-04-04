import pdfkit, jinja2, io
from fastapi import FastAPI, Body , Request
from fastapi.responses import StreamingResponse

app = FastAPI()

# This would help us to get the content of our html
templateLoader = jinja2.FileSystemLoader(searchpath="html")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "home.html"
template = templateEnv.get_template(TEMPLATE_FILE)


@app.get("/home/{name}")
def write_home(request: Request, name:str):
    # Here we have given context using jinja2
    outputText = template.render({'name': name})
    # The above content of html is now being passed as outputText to get our pdf form
    output  = pdfkit.from_string(outputText, output_path=False)
    # Here we could also have used File response instead of Streaming response as both are method to get file response for a given http request
    # But streaming response one important feature that it gives the large file responses in chunks not like file response do which first completely generate response and then give it to client
    # Streaming response streams the file response in chunks speeding up the visibilty of process
    return StreamingResponse(
        io.BytesIO(output),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment;filename=generated.pdf"}
    )

