from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
import os
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="DevOps Automation App",
    description="Sample application for DevOps CI/CD automation",
    version="1.0.0"
)

# Models
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class ItemResponse(Item):
    id: int

# In-memory storage (replace with database in production)
items_db = {}
item_counter = 1

# Middleware
@app.middleware("http")
async def add_process_time_header(request, call_next):
    import time
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Health check endpoints
@app.get("/health", tags=["Health"])
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "environment": os.getenv("ENVIRONMENT", "unknown")
    }

@app.get("/ready", tags=["Health"])
async def readiness_check():
    """Kubernetes readiness probe endpoint"""
    return {
        "status": "ready",
        "version": "1.0.0"
    }

@app.get("/live", tags=["Health"])
async def liveness_check():
    """Kubernetes liveness probe endpoint"""
    return {
        "status": "alive"
    }

# API endpoints
@app.get("/", tags=["Root"])
async def read_root():
    """Root endpoint"""
    return {
        "message": "Welcome to DevOps Automation API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "health": "/health"
        }
    }

@app.get("/items", tags=["Items"])
async def list_items(skip: int = 0, limit: int = 10):
    """List all items"""
    items_list = list(items_db.values())
    return {
        "total": len(items_list),
        "items": items_list[skip:skip + limit]
    }

@app.get("/items/{item_id}", tags=["Items"])
async def get_item(item_id: int):
    """Get a specific item"""
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
    return items_db[item_id]

@app.post("/items", tags=["Items"], response_model=ItemResponse)
async def create_item(item: Item):
    """Create a new item"""
    global item_counter
    item_id = item_counter
    item_counter += 1
    
    item_response = ItemResponse(id=item_id, **item.dict())
    items_db[item_id] = item_response
    
    logger.info(f"Created item {item_id}")
    return item_response

@app.put("/items/{item_id}", tags=["Items"], response_model=ItemResponse)
async def update_item(item_id: int, item: Item):
    """Update an existing item"""
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
    
    item_response = ItemResponse(id=item_id, **item.dict())
    items_db[item_id] = item_response
    
    logger.info(f"Updated item {item_id}")
    return item_response

@app.delete("/items/{item_id}", tags=["Items"])
async def delete_item(item_id: int):
    """Delete an item"""
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
    
    deleted_item = items_db.pop(item_id)
    logger.info(f"Deleted item {item_id}")
    return {
        "message": "Item deleted successfully",
        "item": deleted_item
    }

@app.get("/metrics", tags=["Monitoring"])
async def metrics():
    """Prometheus metrics endpoint"""
    return {
        "total_items": len(items_db),
        "app_version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
