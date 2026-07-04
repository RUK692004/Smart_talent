from fastapi import Request
from fastapi.responses import JSONResponse
import traceback


async def global_exception_handler(request: Request, exc: Exception):
    traceback.print_exc()
    print(f"GLOBAL ERROR: {str(exc)}")
    return JSONResponse(status_code=500, content={"detail": str(exc)})