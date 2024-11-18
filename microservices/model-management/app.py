from fastapi import FastAPI, Query, File, UploadFile
from MLFlowRouter import MLFlowRouter

app = FastAPI()
app.include_router(MLFlowRouter, prefix="/mlflow")

@app.post("/uploadfile", tags=["File operations"])
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    # Process the file contents here
    return {"filename": file.filename, "content_type": file.content_type}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8889, reload=True)