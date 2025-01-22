from fastapi import APIRouter, UploadFile, File, HTTPException, Response

from app.schemas.stdf import STDFData
from app.services.decoder import STDFDecoder
from app.services.encoder import STDFEncoder

router = APIRouter()


@router.post("/decode", response_model=STDFData)
async def decode_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.bin'):
        raise HTTPException(400, "File must be .bin format")

    content = await file.read()
    try:
        return STDFDecoder.decode_file(content)
    except Exception as e:
        raise HTTPException(400, f"Error decoding file: {str(e)}")


@router.post("/encode")
async def encode_data(data: STDFData, filename: str = None):
    try:
        if not filename or ".bin" not in filename:
            filename = "encoded.bin"

        encoded_data = STDFEncoder.encode_data(data)
        return Response(
            content=encoded_data,
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except Exception as e:
        raise HTTPException(400, f"Error encoding data: {str(e)}")
