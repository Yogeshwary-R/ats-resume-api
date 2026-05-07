from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.services.pdf_parser import extract_text_from_pdf
from app.services.scorer import calculate_ats_score
from app.services.ai_suggester import get_ai_suggestions
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.scan_result import ScanResult

router = APIRouter()
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token. Please login again."
        )
    return payload

@router.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF files are accepted."
        )

    if len(job_description.strip()) < 20:
        raise HTTPException(
            status_code=400,
            detail="Job description too short. Please provide more details."
        )

    file_bytes = await file.read()

    if len(file_bytes) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File too large. Maximum allowed size is 5MB."
        )

    resume_text = extract_text_from_pdf(file_bytes)

    if not resume_text:
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from PDF. Make sure the PDF is not scanned image."
        )

    result = calculate_ats_score(resume_text, job_description)
    suggestions = await get_ai_suggestions(
        missing_skills=result["missing_skills"],
        job_description=job_description
    )

    scan = ScanResult(
        user_id=int(current_user["sub"]),
        filename=file.filename,
        ats_score=result["ats_score"],
        matched_skills=result["matched_skills"],
        missing_skills=result["missing_skills"],
        ai_suggestions=suggestions
    )
    db.add(scan)
    db.commit()

    return {
        "filename": file.filename,
        "status": "success",
        **result,
        "ai_suggestions": suggestions
    }

@router.get("/history")
def get_history(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    scans = db.query(ScanResult).filter(
        ScanResult.user_id == int(current_user["sub"])
    ).all()

    if not scans:
        return {"message": "No scan history found. Upload a resume to get started!"}

    return [
        {
            "id": scan.id,
            "filename": scan.filename,
            "ats_score": scan.ats_score,
            "matched_skills": scan.matched_skills,
            "missing_skills": scan.missing_skills,
            "ai_suggestions": scan.ai_suggestions,
            "created_at": scan.created_at
        }
        for scan in scans
    ]