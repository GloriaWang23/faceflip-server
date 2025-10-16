"""Vercel ASGI handler using Mangum adapter"""

from mangum import Mangum
from app.main import app

# Mangum adapter converts ASGI app to AWS Lambda compatible handler
# This is required for Vercel's serverless Python runtime
handler = Mangum(app, lifespan="off")

