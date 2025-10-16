"""Vercel ASGI handler"""

from app.main import app

# Export for Vercel
handler = app

