from pathlib import Path
from typing import List

from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile, status


router = APIRouter(prefix="/models", tags=["Model Registry"])


@router.post("/upload-models")
async def upload_models(files: List[UploadFile] = File(...)):
    """Upload exactly 2 .pkl files and optionally 1 .json file."""
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No files uploaded. Upload exactly 2 .pkl files and optionally 1 .json file."
        )

    valid_suffixes = {".pkl", ".json"}

    def file_suffix(upload_file: UploadFile) -> str:
        filename = upload_file.filename or ""
        return Path(filename).suffix.lower()

    pkl_files = [file for file in files if file_suffix(file) == ".pkl"]
    json_files = [file for file in files if file_suffix(file) == ".json"]
    invalid_files = [file.filename or "<unnamed>" for file in files if file_suffix(file) not in valid_suffixes]

    if invalid_files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file types: {invalid_files}. Only .pkl and optional .json are allowed."
        )

    if len(pkl_files) != 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Exactly 2 .pkl files are required."
        )

    if len(json_files) > 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only 1 .json file is allowed."
        )

    if len(files) > 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Too many files uploaded. Upload exactly 2 .pkl files and optionally 1 .json file."
        )

    target_dir = Path(__file__).resolve().parents[4] / "models"
    target_dir.mkdir(parents=True, exist_ok=True)

    saved_files = []
    for upload_file in files:
        filename = upload_file.filename
        if not filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is missing a filename."
            )
        destination = target_dir / filename
        contents = await upload_file.read()
        destination.write_bytes(contents)
        saved_files.append(destination.name)
        
        
        print(Path(__file__).resolve())

    for i in range(6):
        print(i, Path(__file__).resolve().parents[i])

    return {
        "status": "success",
        "message": "Files uploaded successfully.",
        "saved_files": saved_files,
        "upload_path": str(target_dir)
    }