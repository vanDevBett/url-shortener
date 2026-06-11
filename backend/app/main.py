from fastapi import FastAPI

from app.api.links import router as links_router

app = FastAPI(title="URL Shortener")

app.include_router(links_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
