# Importing necessary classes
from fastapi import FastAPI
from src.routers.ChatBotRouter import router as chatbot_router
from src.routers.PDFDataInjectorRouter import router as pdf_data_injector_router
from src.routers.BatchPDFInjectoRouter import router as batch_pdf_injector_router
from src.routers.RetrivalRouter import router as retrival_router

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












