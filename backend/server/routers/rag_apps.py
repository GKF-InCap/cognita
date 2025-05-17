from fastapi import APIRouter, Path, Depends
from fastapi.responses import JSONResponse

from backend.logger import logger
from backend.modules.metadata_store.base import BaseMetadataStore
from backend.modules.metadata_store.client import get_client
from backend.types import CreateRagApplication
from backend.server.auth import hasura_jwt_auth

router = APIRouter(prefix="/v1/apps", tags=["apps"])


@router.post("")
async def register_rag_app(
    rag_app: CreateRagApplication,
    user_claims=Depends(hasura_jwt_auth),
):
    """Create a rag app"""
    logger.info(f"Creating rag app: {rag_app}")
    metadata_store_client: BaseMetadataStore = await get_client()
    created_rag_app = await metadata_store_client.acreate_rag_app(rag_app)
    return JSONResponse(
        content={"rag_app": created_rag_app.model_dump()}, status_code=201
    )


@router.get("/list")
async def list_rag_apps(user_claims=Depends(hasura_jwt_auth)):
    """Get rag apps"""
    metadata_store_client: BaseMetadataStore = await get_client()
    rag_apps = await metadata_store_client.alist_rag_apps()
    return JSONResponse(content={"rag_apps": rag_apps})


@router.get("/{app_name}")
async def get_rag_app_by_name(
    app_name: str = Path(title="App name"),
    user_claims=Depends(hasura_jwt_auth),
):
    """Get the rag app config given its name"""
    metadata_store_client: BaseMetadataStore = await get_client()
    rag_app = await metadata_store_client.aget_rag_app(app_name)
    if rag_app is None:
        return JSONResponse(content={"rag_app": []})
    return JSONResponse(content={"rag_app": rag_app.model_dump()})


@router.delete("/{app_name}")
async def delete_rag_app(
    app_name: str = Path(title="App name"),
    user_claims=Depends(hasura_jwt_auth),
):
    """Delete the rag app config given its name"""
    metadata_store_client: BaseMetadataStore = await get_client()
    await metadata_store_client.adelete_rag_app(app_name)
    return JSONResponse(content={"deleted": True})
