import warnings

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers.pdf_api import pdf_router

warnings.filterwarnings("ignore")

app = FastAPI()

# Configure CORS
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(pdf_router, prefix="", tags=["pdf"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010, reload=False)
