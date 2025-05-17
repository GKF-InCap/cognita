from fastapi import APIRouter, Depends

from backend.modules.dataloaders.loader import list_dataloaders
from backend.modules.parsers.parser import list_parsers
from backend.modules.query_controllers.query_controller import list_query_controllers
from backend.server.auth import hasura_jwt_auth

router = APIRouter(prefix="/v1/components", tags=["components"])


@router.get("/parsers")
def get_parsers(
    user_claims=Depends(hasura_jwt_auth),
):
    """Get available parsers from the registered parsers"""
    return list_parsers()


@router.get("/dataloaders")
def get_dataloaders(
    user_claims=Depends(hasura_jwt_auth),
):
    """Get available data loaders from registered data loaders"""
    return list_dataloaders()


@router.get("/query_controllers")
def get_query_controllers(
    user_claims=Depends(hasura_jwt_auth),
):
    """Get available query controllers from registered query controllers"""
    return list_query_controllers()
