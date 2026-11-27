# How to add a new module (e.g. `products`)

Same shape as `users/`:

```
products/
  __init__.py
  productRoutes.py        # APIRouter + add_api_route lines
  views/
    __init__.py
    createProduct.py      # one file = one api
documentation/
  productRoutesAPIDocumentation.py
```

1. **Collection** – `core/database.py`
   ```python
   products_collection = db.products
   ```

2. **View** – `products/views/createProduct.py`
   ```python
   from fastapi import Request, Depends, Body
   from fastapi.responses import JSONResponse
   from helper_function.apis_requests import get_current_user
   from core.database import products_collection

   async def createProduct(request: Request, token: str = Depends(get_current_user), body: dict = Body(
       example={"name": "Pen", "price": 10}
   )):
       try:
           body = await request.json()
           userId = request.state.userId
           result = await products_collection.insert_one({**body, "createdBy": userId})
           return JSONResponse({"id": str(result.inserted_id)}, status_code=200)
       except Exception as err:
           return JSONResponse({"msg": str(err)}, status_code=500)
   ```
   Guest api (token optional): use `token: Optional[str] = Header(None)` instead of
   `Depends(get_current_user)` and add the path to `OPTIONAL_TOKEN_PATHS`.

3. **Docs** – `documentation/productRoutesAPIDocumentation.py`
   ```python
   createProductDocumentation = """**Purpose:** create a product."""
   ```

4. **Router** – `products/productRoutes.py`
   ```python
   from fastapi import APIRouter
   from products.views.createProduct import createProduct
   from documentation.productRoutesAPIDocumentation import *

   product_router = APIRouter(prefix="/product")
   product_router.add_api_route("/create", createProduct, methods=["POST"], description=createProductDocumentation, tags=["Products"])
   ```

5. **Register** – `core/routes.py`
   ```python
   from products.productRoutes import product_router
   api_router.include_router(product_router)
   ```

6. **No token needed?** add the path to `EXCLUDED_PATHS` in `middleware/AuthMiddleware.py`.
