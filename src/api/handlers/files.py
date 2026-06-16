# from typing import Annotated
# from fastapi import APIRouter, UploadFile as UF, File
# from pydantic import WithJsonSchema
#
# router = APIRouter(prefix="/api/v1/files", tags=["files"])
#
# UploadFile = Annotated[
#     UF, WithJsonSchema({"type": "string", "format": "binary"})
# ]
#
#
# @router.post("/upload")
# async def upload_file(uploaded_file: UploadFile):
#     file = uploaded_file.file
#     filename = uploaded_file.filename
#     with open(f"1_{filename}", "wb") as f:
#         f.write(file.read())
#
#
# @router.post("/multiply_files")
# async def upload_files(uploaded_files: list[UploadFile] = File(...)):
#     for uploaded_file in uploaded_files:
#         file = uploaded_file.file
#         filename = uploaded_file.filename
#         with open(f"1_{filename}", "wb") as f:
#             f.write(file.read())
