from litestar import Litestar, get
from litestar.stores.registry import StoreRegistry
from rate_limit import RateLimitConfig
import cache
import uvicorn


@get("/")
def hello_world() -> dict[str, str]:
    """Keeping the tradition alive with hello world."""
    return {"hello": "world"}


app = Litestar(
    route_handlers=[hello_world],
    middleware=[RateLimitConfig(rate_limit=("second", 1)).middleware],
    stores=StoreRegistry(default_factory=cache.redis_store_factory),
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
