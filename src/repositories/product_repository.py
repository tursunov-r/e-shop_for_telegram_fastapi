import asyncio
from decimal import Decimal

from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.models.product_model import ProductModel
from src.models.translate_product_model import TranslatedProductModel
from src.schemas.product_schemas import (
    CreateProductSchema,
    UpdateProductSchema,
    TranslateProductSchema,
)
from src.utils.exceptions.exceptions import (
    ProductAlreadyExists,
    NotFound,
)


class ProductRepository:
    @staticmethod
    async def _create_translate(
        product_id: ProductModel,
        product: TranslateProductSchema,
        session: AsyncSession,
    ):
        if len(product.title.strip()) == 0:
            raise ValueError("Title cannot be empty")
        new_translate_product = TranslatedProductModel(
            product_id=product_id.id,
            lang_code=product.lang_code,
            title=product.title.title().strip(),
            description=product.description.strip(),
        )
        session.add(new_translate_product)
        return new_translate_product

    @staticmethod
    async def create_products_query(
        product: CreateProductSchema, session: AsyncSession
    ):
        check_barcode = await session.execute(
            select(ProductModel.barcode).where(
                ProductModel.barcode == product.barcode
            )
        )
        result = check_barcode.scalar_one_or_none()
        if result:
            raise ProductAlreadyExists("Product already exists")
        new_product = ProductModel(
            barcode=product.barcode,
            price=product.price,
            purchase_price=product.purchase_price,
            quantity=product.stock,
            archived=product.archived,
        )

        session.add(new_product)
        await session.flush()
        translates = [
            ProductRepository._create_translate(
                product_id=new_product, product=p, session=session
            )
            for p in product.translate
        ]
        translated_product = await asyncio.gather(*translates)
        return {
            "product": new_product,
            "translated_product": translated_product,
        }

    @staticmethod
    async def get_all_products_from_db_query(session: AsyncSession):
        result = await session.execute(
            select(ProductModel)
            .options(joinedload(ProductModel.translate))
            .where(ProductModel.archived != True)
        )
        product = result.unique().scalars().all()
        if result:
            return product
        raise NotFound("Product not found")

    @staticmethod
    async def get_product_by_id_from_db_query(
        product_id: int, session: AsyncSession
    ):
        result = await session.execute(
            select(ProductModel)
            .options(joinedload(ProductModel.translate))
            .where(
                and_(
                    ProductModel.id == product_id,
                    ProductModel.archived != True,
                )
            )
        )
        product = result.unique().scalar_one_or_none()
        if product:
            return product
        raise NotFound("Product not found")

    @staticmethod
    async def search_product(
        search: str | None,
        min_price: Decimal | None,
        max_price: Decimal | None,
        session: AsyncSession,
    ):
        # Минимальная цена
        if min_price is None:
            price_min = await session.execute(
                select(ProductModel.price)
                .order_by(ProductModel.price.asc())
                .limit(1)
            )
            min_price = price_min.scalar_one_or_none() or Decimal("0")

        # Максимальная цена
        if max_price is None:
            price_max = await session.execute(
                select(ProductModel.price)
                .order_by(ProductModel.price.desc())
                .limit(1)
            )
            max_price = price_max.scalar_one_or_none() or Decimal("999999999")

        filters = [
            ProductModel.price.between(min_price, max_price),
            ProductModel.archived.is_(False),
        ]

        # Поиск по title ИЛИ barcode
        if search:
            filters.append(
                or_(
                    TranslatedProductModel.title.ilike(f"%{search}%"),
                    ProductModel.barcode.ilike(f"%{search}%"),
                )
            )

        stmt = await session.execute(
            select(ProductModel)
            .join(
                TranslatedProductModel,
                ProductModel.id == TranslatedProductModel.product_id,
            )
            .options(joinedload(ProductModel.translate))
            .where(and_(*filters))
        )

        products = stmt.unique().scalars().all()

        if not products:
            raise NotFound("Product not found")

        return products

    @staticmethod
    async def update_product_query(
        barcode: str,
        update: UpdateProductSchema,
        session: AsyncSession,
    ):
        result = await session.execute(
            select(ProductModel)
            .options(selectinload(ProductModel.translate))
            .where(ProductModel.barcode == barcode.strip())
        )
        product = result.scalar_one_or_none()
        if not product:
            raise NotFound("Product not found")

        if update.stock is not None:
            product.quantity = update.stock
        if update.price is not None:
            product.price = Decimal(str(update.price))
        if update.purchase_price is not None:
            product.purchase_price = Decimal(str(update.purchase_price))
        if update.archived is not None:
            product.archived = update.archived

        # Обновляем переводы
        if update.translate:
            existing = {t.lang_code: t for t in product.translate}
            for t_data in update.translate:
                lang = t_data.lang_code
                # если перевод есть — обновляем
                if lang in existing:
                    existing_translate = existing[lang]
                    existing_translate.title = t_data.title.title().strip()
                    existing_translate.description = t_data.description
                # если нет — создаём
                else:
                    new_translate = TranslatedProductModel(
                        product_id=product.id,
                        lang_code=lang,
                        title=t_data.title,
                        description=t_data.description,
                    )
                    session.add(new_translate)

        # await session.refresh(product)
        return product

    @staticmethod
    async def update_product_quantity(
        product_id: int, quantity: int, session: AsyncSession
    ):
        product = await session.execute(
            select(ProductModel).where(ProductModel.id == product_id)
        )
        product = product.scalar_one_or_none()
        if not product:
            raise NotFound("Product not found")
        if product.quantity < quantity:
            raise ValueError("Product quantity is too small")
        product.quantity -= quantity
        return product

    @staticmethod
    async def delete_product_query(barcode: str, session: AsyncSession):
        result = await session.execute(
            select(ProductModel).where(
                ProductModel.barcode == barcode.title().strip()
            )
        )
        product = result.scalar_one_or_none()
        if not product:
            raise NotFound("Product not found")
        await session.delete(product)
        return {"message": "Product deleted"}

    @staticmethod
    async def delete_product_by_id_from_db_query(
        product_id: int, session: AsyncSession
    ):
        product = await session.execute(
            select(ProductModel).where(ProductModel.id == product_id)
        )
        product = product.scalar_one_or_none()
        if not product:
            raise NotFound("Product not found")
        await session.delete(product)
        return {"message": "Product deleted"}


product_repository = ProductRepository()
