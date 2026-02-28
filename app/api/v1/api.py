from fastapi import APIRouter

from app.api.v1.endpoints import cases, jurisdictions, dockets, documents, secondary_sources, taxonomies

api_router = APIRouter()
api_router.include_router(cases.router, prefix="/cases", tags=["cases"])
api_router.include_router(jurisdictions.router, prefix="/jurisdictions", tags=["jurisdictions"])
api_router.include_router(dockets.router, prefix="/dockets", tags=["dockets"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(secondary_sources.router, prefix="/secondary-sources", tags=["secondary-sources"])
api_router.include_router(taxonomies.router, prefix="/taxonomies", tags=["taxonomies"])
