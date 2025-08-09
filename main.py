from fastapi import FastAPI
import redis
import os

app = FastAPI(title="Jenkins Learning API", version="1.0.0")

# Redis connection
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

@app.get("/")
async def root():
    """Root endpoint returning hello world"""
    return {"message": "Hello World"}

@app.get("/counter")
async def get_counter():
    """Get current counter value and increment by 1"""
    try:
        # Get current counter value (default to 0 if not exists)
        current_count = redis_client.get("counter")
        if current_count is None:
            current_count = 0
        else:
            current_count = int(current_count)
        
        # Increment counter by 1
        new_count = redis_client.incr("counter")
        
        return {
            "message": f"Counter updated! Previous: {current_count}, Current: {new_count}",
            "previous_count": current_count,
            "current_count": new_count
        }
    except redis.RedisError as e:
        return {"error": f"Redis connection failed: {str(e)}"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        redis_client.ping()
        return {"status": "healthy", "redis": "connected"}
    except redis.RedisError:
        return {"status": "unhealthy", "redis": "disconnected"}
