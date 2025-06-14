import logging
from api.infrastructure.cat_api import get_all_breeds, get_all_categories, get_images_by_category_id
from api.models.breed import CatBreed
from api.models.image import CatImage
from api.models.category_image import CategoryImage
from api.models.base import Base
from api.database.connection import engine, SessionLocal

logger = logging.getLogger(__name__)

def clear_database(session):
    logger.info("Clearing database tables...")
    session.query(CatImage).delete()
    session.query(CategoryImage).delete()
    session.query(CatBreed).delete()
    session.commit()
    logger.info("Database cleared.")

def populate_breeds(session, breeds_data):
    logger.info(f"Inserting {len(breeds_data)} breeds...")
    for b in breeds_data:
        breed = CatBreed(
            id=b.get("id"),
            name=b.get("name"),
            origin=b.get("origin"),
            temperament=b.get("temperament"),
            description=b.get("description"),
        )
        session.add(breed)
    session.commit()
    logger.info("Breeds inserted.")

def populate_images(session, breeds_data):
    logger.info("Inserting images for breeds...")
    for b in breeds_data:
        breed_id = b.get("id")
        images = b.get("image")
        if images and images.get("url"):
            img = CatImage(url=images["url"], breed_id=breed_id)
            session.add(img)
    session.commit()
    logger.info("Breed images inserted.")

async def populate_category_images(session, categories):
    logger.info(f"Inserting category images for {len(categories)} categories...")
    for c in categories:
        category_name = c.get("name")
        if not category_name:
            continue

        category_id = c.get("id")
        try:
            images_urls = await get_images_by_category_id(category_id, limit=3)
        except Exception as e:
            logger.error(f"Erro ao buscar imagens para categoria {category_name}: {e}")
            images_urls = []

        for url in images_urls or []:
            cat_img = CategoryImage(url=url, category=category_name)
            session.add(cat_img)
    session.commit()
    logger.info("Category images inserted.")

async def populate_database():
    logger.info("Starting populate_db script...")

    # Cria tabelas se não existirem
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    try:
        clear_database(session)

        # Agora usamos await (sem asyncio.run)
        breeds_data = await get_all_breeds()
        categories = await get_all_categories()

        if breeds_data:
            populate_breeds(session, breeds_data)
            populate_images(session, breeds_data)
        else:
            logger.warning("No breed data fetched from API")

        if categories:
            await populate_category_images(session, categories)
        else:
            logger.warning("No categories fetched from API")

        logger.info("Database population finished successfully.")

    except Exception as e:
        logger.error(f"Error populating database: {e}")
        session.rollback()
    finally:
        session.close()

# Executar standalone no terminal (fora do FastAPI)
if __name__ == "__main__":
    import asyncio
    asyncio.run(populate_database())
