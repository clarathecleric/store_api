from fastapi import APIRouter, HTTPException, status
from typing import List
from uuid import UUID

from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.usecases.product import product_usecase
from store.core.exceptions import NotFoundException, InsertException

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductIn):
    try:
        return await product_usecase.create(product)
    except InsertException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: UUID):
    try:
        return await product_usecase.get(product_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=List[ProductOut])
async def list_products():
    return await product_usecase.query()


@router.patch("/{product_id}", response_model=ProductUpdateOut)
async def update_product(product_id: UUID, product: ProductUpdate):
    try:
        return await product_usecase.update(product_id, product)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: UUID):
    try:
        deleted = await product_usecase.delete(product_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Product not found")
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


# Rota de filtro de preço
@router.get("/filter/price", response_model=List[ProductOut])
async def filter_price(min_price: float, max_price: float):
    return await product_usecase.filter_by_price(min_price, max_price)
