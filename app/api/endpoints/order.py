from fastapi import APIRouter

from app.core.dependencies import CurrentUser, SupabaseClient
from app.core.response import success


router = APIRouter()

@router.get("/list")
async def get_order_list(current_user: CurrentUser, supabase_client: SupabaseClient):
    res = supabase_client.table("t_order").select("*").execute()
    print(res.data)
    """Get order list"""
    return success(
        data={
            "orders": [
                res.data
            ]
        }
    )
