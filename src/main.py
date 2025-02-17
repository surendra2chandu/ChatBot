# Importing necessary classes
from fastapi import FastAPI
from src.routers.ChatBotRouter import router as chatbot_router
from src.routers.PDFDataInjectorRouter import router as pdf_data_injector_router
from src.routers.BatchPDFInjectoRouter import router as batch_pdf_injector_router
from src.routers.RetrivalRouter import router as retrival_router
from src.routers.TextSummarizerRouter import router as text_summarizer_router
from src.routers.RawPdfDataInjectorRouter import router as raw_pdf_data_injector_router
from src.routers.BatchPdfRawDataInjectorRouter import router as batch_pdf_raw_data_injector_router

# Initialize the FastAPI app
app = FastAPI()

# Include the PDF data injector router
app.include_router(pdf_data_injector_router)

# Include the batch PDF injector router
app.include_router(batch_pdf_injector_router)

# Include the retrival router
app.include_router(retrival_router)

# Include the chatbot router
app.include_router(chatbot_router)

# Include the text summarizer router
app.include_router(text_summarizer_router)

# Include the raw PDF data injector router
app.include_router(raw_pdf_data_injector_router)

# Include the batch raw PDF data injector router
app.include_router(batch_pdf_raw_data_injector_router)
