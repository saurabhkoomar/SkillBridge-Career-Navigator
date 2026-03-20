"""Data routes for sample resumes and other static data."""
from fastapi import APIRouter
from app.services.data_service import DataService

router = APIRouter(prefix="/data", tags=["data"])


def get_data_service() -> DataService:
    """Get DataService singleton."""
    return DataService()


@router.get("/resumes")
def get_sample_resumes():
    """Return all sample resumes for profile creation and demos."""
    data_service = get_data_service()
    return data_service.get_all_resumes()
