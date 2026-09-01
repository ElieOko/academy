from datetime import date, datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    name: str
    email: str


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class ProgramIn(BaseModel):
    slug: str
    code: str
    title_fr: str
    title_en: str
    tagline_fr: str = ""
    tagline_en: str = ""
    description_fr: str = ""
    description_en: str = ""
    objectives: list[Any] = Field(default_factory=list)
    audience_fr: str = ""
    audience_en: str = ""
    modules: list[Any] = Field(default_factory=list)
    prerequisites_fr: str = ""
    prerequisites_en: str = ""
    image_url: str = ""
    category: str = ""
    is_featured: bool = True
    is_published: bool = True
    sort_order: int = 0


class ProgramOut(ProgramIn):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class SessionIn(BaseModel):
    program_id: UUID
    slug: str
    title_fr: str
    title_en: str
    summary_fr: str = ""
    summary_en: str = ""
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    duration_fr: str = ""
    duration_en: str = ""
    status: str = "open"
    tuition_usd: float = 0
    enrollment_fee_usd: float = 0
    format: str = "in_person"
    cta_fr: str = "S'inscrire"
    cta_en: str = "Enroll"
    is_highlighted: bool = False
    max_seats: Optional[int] = None


class SessionOut(SessionIn):
    id: UUID
    created_at: datetime
    program: Optional[ProgramOut] = None

    class Config:
        from_attributes = True


class EnrollmentIn(BaseModel):
    full_name: str
    whatsapp: str
    email: EmailStr
    program_id: Optional[UUID] = None
    session_id: Optional[UUID] = None
    prior_level: str = ""
    format_preference: str = "in_person"
    objective: str = ""
    privacy_accepted: bool


class EnrollmentOut(BaseModel):
    id: UUID
    full_name: str
    whatsapp: str
    email: str
    program_id: Optional[UUID]
    session_id: Optional[UUID]
    prior_level: str
    format_preference: str
    objective: str
    status: str
    notes: str
    created_at: datetime
    program: Optional[ProgramOut] = None
    session: Optional[SessionOut] = None

    class Config:
        from_attributes = True


class EnrollmentStatusIn(BaseModel):
    status: str
    notes: str = ""


class NewsIn(BaseModel):
    slug: str
    title_fr: str
    title_en: str
    excerpt_fr: str = ""
    excerpt_en: str = ""
    content_fr: str = ""
    content_en: str = ""
    image_url: str = ""
    category: str = "news"
    is_published: bool = True
    published_at: Optional[datetime] = None


class NewsOut(NewsIn):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class TestimonialIn(BaseModel):
    name: str
    role_fr: str = ""
    role_en: str = ""
    quote_fr: str = ""
    quote_en: str = ""
    photo_url: str = ""
    is_published: bool = True
    sort_order: int = 0


class TestimonialOut(TestimonialIn):
    id: UUID

    class Config:
        from_attributes = True


class EnterpriseIn(BaseModel):
    company: str
    contact_name: str
    email: EmailStr
    phone: str = ""
    audience: str = ""
    topics: str = ""
    message: str = ""


class EnterpriseOut(EnterpriseIn):
    id: UUID
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ContactIn(BaseModel):
    name: str
    email: EmailStr
    phone: str = ""
    message: str


class ContactOut(ContactIn):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class SettingsIn(BaseModel):
    value: dict
