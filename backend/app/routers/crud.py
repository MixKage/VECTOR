from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.models import Region, City, Specialization, University, Company
from app.schemas.crud import (
    RegionIn, RegionOut, CityIn, CityOut, SpecializationIn, SpecializationOut,
    UniversityIn, UniversityOut, CompanyIn, CompanyOut
)
from app.dependencies import get_db

router = APIRouter(prefix="/api", tags=["crud"])

# --- Регионы ---
@router.post("/regions", response_model=RegionOut, status_code=201)
async def create_region(payload: RegionIn, db: AsyncSession = Depends(get_db)):
    """Создать регион.
    
    Args:
        payload (RegionIn): Данные региона для создания.
        db (AsyncSession): Сессия базы данных.

    Returns:
        RegionOut: Созданный регион.
    """
    region = Region(title=payload.title)
    db.add(region)
    await db.commit()
    await db.refresh(region)
    return region


@router.get("/regions", response_model=List[RegionOut])
async def list_regions(db: AsyncSession = Depends(get_db)):
    """Список регионов.

    Args:
        db (AsyncSession): Сессия базы данных.

    Returns:
        List[RegionOut]: Список регионов.
    """
    rows = (await db.scalars(select(Region))).all()
    return rows


@router.get("/regions/{region_id}", response_model=RegionOut)
async def get_region(region_id: int, db: AsyncSession = Depends(get_db)):
    """Получить регион по id.
    
    Args:
        region_id (int): Идентификатор региона.
        db (AsyncSession): Сессия базы данных.

    Returns:
        RegionOut: Информация о регионе.

    Raises:
        HTTPException: Если регион не найден (404).
    """
    obj = await db.get(Region, region_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Регион не найден")
    return obj


@router.put("/regions/{region_id}", response_model=RegionOut)
async def update_region(region_id: int, payload: RegionIn, db: AsyncSession = Depends(get_db)):
    """Обновить регион по id.
    
    Args:
        region_id (int): Идентификатор региона.
        payload (RegionIn): Данные региона для обновления.
        db (AsyncSession): Сессия базы данных.

    Returns:
        RegionOut: Обновленный регион.

    Raises:
        HTTPException: Если регион не найден (404).
    """
    obj = await db.get(Region, region_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Регион не найден")
    obj.title = payload.title
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/regions/{region_id}", status_code=204)
async def delete_region(region_id: int, db: AsyncSession = Depends(get_db)):
    """Удалить регион по id.
    
    Args:
        region_id (int): Идентификатор региона.
        db (AsyncSession): Сессия базы данных.

    Raises:
        HTTPException: Если регион не найден (404).
    """
    obj = await db.get(Region, region_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Регион не найден")
    await db.delete(obj)
    await db.commit()

# --- Города ---
@router.post("/cities", response_model=CityOut, status_code=201)
async def create_city(payload: CityIn, db: AsyncSession = Depends(get_db)):
    """Создать город.
    
    Args:
        payload (CityIn): Данные города для создания.
        db (AsyncSession): Сессия базы данных.

    Returns:
        CityOut: Созданный город.
    """
    obj = City(region_id=payload.region_id, title=payload.title)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/cities", response_model=List[CityOut])
async def list_cities(db: AsyncSession = Depends(get_db)):
    """Список городов.

    Args:
        db (AsyncSession): Сессия базы данных.

    Returns:
        List[CityOut]: Список городов.
    """
    rows = (await db.scalars(select(City))).all()
    return rows


@router.put("/cities/{city_id}", response_model=CityOut)
async def update_city(city_id: int, payload: CityIn, db: AsyncSession = Depends(get_db)):
    """Обновить город по id.
    
    Args:
        city_id (int): Идентификатор города.
        payload (CityIn): Данные города для обновления.
        db (AsyncSession): Сессия базы данных.

    Returns:
        CityOut: Обновленный город.

    Raises:
        HTTPException: Если город не найден (404).
    """
    obj = await db.get(City, city_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Город не найден")
    obj.region_id = payload.region_id
    obj.title = payload.title
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/cities/{city_id}", status_code=204)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    """Удалить город по id.
    
    Args:
        city_id (int): Идентификатор города.
        db (AsyncSession): Сессия базы данных.

    Raises:
        HTTPException: Если город не найден (404).
    """
    obj = await db.get(City, city_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Город не найден")
    await db.delete(obj)
    await db.commit()

# --- Специализации ---
@router.post("/specializations", response_model=SpecializationOut, status_code=201)
async def create_specialization(payload: SpecializationIn, db: AsyncSession = Depends(get_db)):
    """Создать специализацию.
    
    Args:
        payload (SpecializationIn): Данные специализации для создания.
        db (AsyncSession): Сессия базы данных.

    Returns:
        SpecializationOut: Созданная специализация.
    """
    obj = Specialization(title=payload.title, specialization_code=payload.specialization_code)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/specializations", response_model=List[SpecializationOut])
async def list_specializations(db: AsyncSession = Depends(get_db)):
    """Список специализаций.

    Args:
        db (AsyncSession): Сессия базы данных.

    Returns:
        List[SpecializationOut]: Список специализаций.
    """
    rows = (await db.scalars(select(Specialization))).all()
    return rows


@router.put("/specializations/{spec_id}", response_model=SpecializationOut)
async def update_specialization(spec_id: int, payload: SpecializationIn, db: AsyncSession = Depends(get_db)):
    """Обновить специализацию по id.
    
    Args:
        spec_id (int): Идентификатор специализации.
        payload (SpecializationIn): Данные специализации для обновления.
        db (AsyncSession): Сессия базы данных.

    Returns:
        SpecializationOut: Обновленная специализация.

    Raises:
        HTTPException: Если специализация не найдена (404).
    """
    obj = await db.get(Specialization, spec_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Специализация не найдена")
    obj.title = payload.title
    obj.specialization_code = payload.specialization_code
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/specializations/{spec_id}", status_code=204)
async def delete_specialization(spec_id: int, db: AsyncSession = Depends(get_db)):
    """Удалить специализацию по id.
    
    Args:
        spec_id (int): Идентификатор специализации.
        db (AsyncSession): Сессия базы данных.

    Raises:
        HTTPException: Если специализация не найдена (404).
    """
    obj = await db.get(Specialization, spec_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Специализация не найдена")
    await db.delete(obj)
    await db.commit()

# --- Университеты ---
@router.post("/universities", response_model=UniversityOut, status_code=201)
async def create_university(payload: UniversityIn, db: AsyncSession = Depends(get_db)):
    """Создать университет.
    
    Args:
        payload (UniversityIn): Данные университета для создания.
        db (AsyncSession): Сессия базы данных.

    Returns:
        UniversityOut: Созданный университет.
    """
    obj = University(account_id=payload.account_id, title=payload.title, city_id=payload.city_id)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/universities", response_model=List[UniversityOut])
async def list_universities(db: AsyncSession = Depends(get_db)):
    """Список университетов.

    Args:
        db (AsyncSession): Сессия базы данных.

    Returns:
        List[UniversityOut]: Список университетов.
    """
    rows = (await db.scalars(select(University))).all()
    return rows


@router.put("/universities/{uni_id}", response_model=UniversityOut)
async def update_university(uni_id: int, payload: UniversityIn, db: AsyncSession = Depends(get_db)):
    """Обновить университет по id.
    
    Args:
        uni_id (int): Идентификатор университета.
        payload (UniversityIn): Данные университета для обновления.
        db (AsyncSession): Сессия базы данных.

    Returns:
        UniversityOut: Обновленный университет.

    Raises:
        HTTPException: Если университет не найден (404).
    """
    obj = await db.get(University, uni_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Университет не найден")
    obj.account_id = payload.account_id
    obj.title = payload.title
    obj.city_id = payload.city_id
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/universities/{uni_id}", status_code=204)
async def delete_university(uni_id: int, db: AsyncSession = Depends(get_db)):
    """Удалить университет по id.
    
    Args:
        uni_id (int): Идентификатор университета.
        db (AsyncSession): Сессия базы данных.

    Raises:
        HTTPException: Если университет не найден (404).
    """
    obj = await db.get(University, uni_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Университет не найден")
    await db.delete(obj)
    await db.commit()

# --- Компании ---
@router.post("/companies", response_model=CompanyOut, status_code=201)
async def create_company(payload: CompanyIn, db: AsyncSession = Depends(get_db)):
    """Создать компанию.
    
    Args:
        payload (CompanyIn): Данные компании для создания.
        db (AsyncSession): Сессия базы данных.

    Returns:
        CompanyOut: Созданная компания.
    """
    obj = Company(account_id=payload.account_id, title=payload.title, city_id=payload.city_id)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/companies", response_model=List[CompanyOut])
async def list_companies(db: AsyncSession = Depends(get_db)):
    """Список компаний.

    Args:
        db (AsyncSession): Сессия базы данных.

    Returns:
        List[CompanyOut]: Список компаний.
    """
    rows = (await db.scalars(select(Company))).all()
    return rows


@router.put("/companies/{company_id}", response_model=CompanyOut)
async def update_company(company_id: int, payload: CompanyIn, db: AsyncSession = Depends(get_db)):
    """Обновить компанию по id.
    
    Args:
        company_id (int): Идентификатор компании.
        payload (CompanyIn): Данные компании для обновления.
        db (AsyncSession): Сессия базы данных.

    Returns:
        CompanyOut: Обновленная компания.

    Raises:
        HTTPException: Если компания не найдена (404).
    """
    obj = await db.get(Company, company_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Компания не найдена")
    obj.account_id = payload.account_id
    obj.title = payload.title
    obj.city_id = payload.city_id
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/companies/{company_id}", status_code=204)
async def delete_company(company_id: int, db: AsyncSession = Depends(get_db)):
    """Удалить компанию по id.
    
    Args:
        company_id (int): Идентификатор компании.
        db (AsyncSession): Сессия базы данных.

    Raises:
        HTTPException: Если компания не найдена (404).
    """
    obj = await db.get(Company, company_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Компания не найдена")
    await db.delete(obj)
    await db.commit()


