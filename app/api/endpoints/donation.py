from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.donation import donation_crud
from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB
from app.services.investment import investment_process_donation

EXCLUDE_FIELDS = (
    'user_id',
    'invested_amount',
    'fully_invested',
    'close_date'
)

router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationDB],
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True
)
async def get_all_donations_superuser(
    session: AsyncSession = Depends(get_async_session),
):
    """Get all the donations.
        This endpoint is available only for superuser.
    """
    donations = await donation_crud.get_multiple(session)
    return donations


@router.get(
    '/my',
    response_model=List[DonationDB],
    response_model_exclude={*EXCLUDE_FIELDS}
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Get all the donations for the current user."""
    donations = await donation_crud.get_donations_by_user(
        session=session, user=user
    )
    return donations


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude={*EXCLUDE_FIELDS}
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """"""
    # Think about validation
    await investment_process_donation(donation, session)
    new_donation = await donation_crud.create(
        donation, session, user
    )
    return new_donation
