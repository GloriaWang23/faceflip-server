from pydantic import BaseModel


class FaceFlipOrder(BaseModel):
    order_id: str
    user_id: str
    product_id: str
    quantity: int
    total_price: float
    status: str