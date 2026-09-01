from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..models import (
    ContactMessage,
    Enrollment,
    EnterpriseRequest,
    News,
    Program,
    Session as CourseSession,
    SiteSetting,
    Testimonial,
)
from ..schemas import ContactIn, EnrollmentIn, EnterpriseIn

router = APIRouter()


def serialize_program(p: Program) -> dict:
    return {
        "id": str(p.id),
        "slug": p.slug,
        "code": p.code,
        "title_fr": p.title_fr,
        "title_en": p.title_en,
        "tagline_fr": p.tagline_fr,
        "tagline_en": p.tagline_en,
        "description_fr": p.description_fr,
        "description_en": p.description_en,
        "objectives": p.objectives or [],
        "audience_fr": p.audience_fr,
        "audience_en": p.audience_en,
        "modules": p.modules or [],
        "prerequisites_fr": p.prerequisites_fr,
        "prerequisites_en": p.prerequisites_en,
        "image_url": p.image_url,
        "category": p.category,
        "is_featured": p.is_featured,
        "sort_order": p.sort_order,
    }


def serialize_session(s: CourseSession, include_program: bool = True) -> dict:
    data = {
        "id": str(s.id),
        "program_id": str(s.program_id),
        "slug": s.slug,
        "title_fr": s.title_fr,
        "title_en": s.title_en,
        "summary_fr": s.summary_fr,
        "summary_en": s.summary_en,
        "start_date": s.start_date.isoformat() if s.start_date else None,
        "end_date": s.end_date.isoformat() if s.end_date else None,
        "duration_fr": s.duration_fr,
        "duration_en": s.duration_en,
        "status": s.status,
        "tuition_usd": s.tuition_usd,
        "enrollment_fee_usd": s.enrollment_fee_usd,
        "format": s.format,
        "cta_fr": s.cta_fr,
        "cta_en": s.cta_en,
        "is_highlighted": s.is_highlighted,
        "max_seats": s.max_seats,
    }
    if include_program and s.program:
        data["program"] = serialize_program(s.program)
    return data


@router.get("/programs")
def list_programs(db: Session = Depends(get_db)):
    rows = (
        db.query(Program)
        .filter(Program.is_published.is_(True))
        .order_by(Program.sort_order, Program.title_fr)
        .all()
    )
    return [serialize_program(p) for p in rows]


@router.get("/programs/{slug}")
def get_program(slug: str, db: Session = Depends(get_db)):
    p = (
        db.query(Program)
        .options(joinedload(Program.sessions))
        .filter(Program.slug == slug, Program.is_published.is_(True))
        .first()
    )
    if not p:
        raise HTTPException(404, "Formation introuvable")
    data = serialize_program(p)
    data["sessions"] = [serialize_session(s, include_program=False) for s in p.sessions]
    return data


@router.get("/sessions")
def list_sessions(highlighted: bool = False, db: Session = Depends(get_db)):
    q = db.query(CourseSession).options(joinedload(CourseSession.program))
    if highlighted:
        q = q.filter(CourseSession.is_highlighted.is_(True))
    rows = q.order_by(CourseSession.start_date.asc().nullslast()).all()
    return [serialize_session(s) for s in rows]


@router.get("/news")
def list_news(db: Session = Depends(get_db)):
    rows = (
        db.query(News)
        .filter(News.is_published.is_(True))
        .order_by(News.published_at.desc())
        .all()
    )
    return [
        {
            "id": str(n.id),
            "slug": n.slug,
            "title_fr": n.title_fr,
            "title_en": n.title_en,
            "excerpt_fr": n.excerpt_fr,
            "excerpt_en": n.excerpt_en,
            "content_fr": n.content_fr,
            "content_en": n.content_en,
            "image_url": n.image_url,
            "category": n.category,
            "published_at": n.published_at.isoformat() if n.published_at else None,
        }
        for n in rows
    ]


@router.get("/news/{slug}")
def get_news(slug: str, db: Session = Depends(get_db)):
    n = db.query(News).filter(News.slug == slug, News.is_published.is_(True)).first()
    if not n:
        raise HTTPException(404, "Article introuvable")
    return {
        "id": str(n.id),
        "slug": n.slug,
        "title_fr": n.title_fr,
        "title_en": n.title_en,
        "excerpt_fr": n.excerpt_fr,
        "excerpt_en": n.excerpt_en,
        "content_fr": n.content_fr,
        "content_en": n.content_en,
        "image_url": n.image_url,
        "category": n.category,
        "published_at": n.published_at.isoformat() if n.published_at else None,
    }


@router.get("/testimonials")
def list_testimonials(db: Session = Depends(get_db)):
    rows = (
        db.query(Testimonial)
        .filter(Testimonial.is_published.is_(True))
        .order_by(Testimonial.sort_order)
        .all()
    )
    return [
        {
            "id": str(t.id),
            "name": t.name,
            "role_fr": t.role_fr,
            "role_en": t.role_en,
            "quote_fr": t.quote_fr,
            "quote_en": t.quote_en,
            "photo_url": t.photo_url,
        }
        for t in rows
    ]


@router.get("/settings/contact")
def get_contact(db: Session = Depends(get_db)):
    row = db.query(SiteSetting).filter(SiteSetting.key == "contact").first()
    return row.value if row else {}


@router.post("/enrollments")
def create_enrollment(payload: EnrollmentIn, db: Session = Depends(get_db)):
    if not payload.privacy_accepted:
        raise HTTPException(400, "Veuillez accepter la politique de confidentialité.")
    row = Enrollment(
        full_name=payload.full_name.strip(),
        whatsapp=payload.whatsapp.strip(),
        email=payload.email,
        program_id=payload.program_id,
        session_id=payload.session_id,
        prior_level=payload.prior_level,
        format_preference=payload.format_preference,
        objective=payload.objective,
        privacy_accepted=True,
        status="pending",
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": str(row.id), "status": "ok"}


@router.post("/enterprise")
def create_enterprise(payload: EnterpriseIn, db: Session = Depends(get_db)):
    row = EnterpriseRequest(**payload.model_dump())
    db.add(row)
    db.commit()
    return {"status": "ok"}


@router.post("/contact")
def create_contact(payload: ContactIn, db: Session = Depends(get_db)):
    row = ContactMessage(**payload.model_dump())
    db.add(row)
    db.commit()
    return {"status": "ok"}
