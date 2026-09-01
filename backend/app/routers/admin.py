from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from ..auth import get_current_admin
from ..database import get_db
from ..models import (
    AdminUser,
    ContactMessage,
    Enrollment,
    EnterpriseRequest,
    News,
    Program,
    Session as CourseSession,
    SiteSetting,
    Testimonial,
)
from ..schemas import (
    EnrollmentStatusIn,
    NewsIn,
    ProgramIn,
    SessionIn,
    SettingsIn,
    TestimonialIn,
)
from ..utils import serialize

router = APIRouter(dependencies=[Depends(get_current_admin)])


def apply(model, data: dict, db: Session):
    for k, v in data.items():
        setattr(model, k, v)
    db.commit()
    db.refresh(model)
    return serialize(model)


@router.get("/stats")
def stats(db: Session = Depends(get_db), _admin: AdminUser = Depends(get_current_admin)):
    return {
        "programs": db.query(Program).count(),
        "sessions": db.query(CourseSession).count(),
        "enrollments": db.query(Enrollment).count(),
        "pending": db.query(Enrollment).filter(Enrollment.status == "pending").count(),
        "news": db.query(News).count(),
        "enterprise": db.query(EnterpriseRequest).count(),
        "messages": db.query(ContactMessage).count(),
    }


@router.get("/programs")
def programs(db: Session = Depends(get_db)):
    return [serialize(p) for p in db.query(Program).order_by(Program.sort_order).all()]


@router.post("/programs")
def create_program(payload: ProgramIn, db: Session = Depends(get_db)):
    if db.query(Program).filter(Program.slug == payload.slug).first():
        raise HTTPException(400, "Ce slug existe déjà.")
    row = Program(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return serialize(row)


@router.put("/programs/{item_id}")
def update_program(item_id: UUID, payload: ProgramIn, db: Session = Depends(get_db)):
    row = db.query(Program).filter(Program.id == item_id).first()
    if not row:
        raise HTTPException(404)
    return apply(row, payload.model_dump(), db)


@router.delete("/programs/{item_id}")
def delete_program(item_id: UUID, db: Session = Depends(get_db)):
    row = db.query(Program).filter(Program.id == item_id).first()
    if not row:
        raise HTTPException(404)
    db.delete(row)
    db.commit()
    return {"ok": True}


@router.get("/sessions")
def sessions(db: Session = Depends(get_db)):
    rows = (
        db.query(CourseSession)
        .options(joinedload(CourseSession.program))
        .order_by(CourseSession.start_date.asc().nullslast())
        .all()
    )
    return [serialize(s, extra={"program": serialize(s.program) if s.program else None}) for s in rows]


@router.post("/sessions")
def create_session(payload: SessionIn, db: Session = Depends(get_db)):
    row = CourseSession(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return serialize(row)


@router.put("/sessions/{item_id}")
def update_session(item_id: UUID, payload: SessionIn, db: Session = Depends(get_db)):
    row = db.query(CourseSession).filter(CourseSession.id == item_id).first()
    if not row:
        raise HTTPException(404)
    return apply(row, payload.model_dump(), db)


@router.delete("/sessions/{item_id}")
def delete_session(item_id: UUID, db: Session = Depends(get_db)):
    row = db.query(CourseSession).filter(CourseSession.id == item_id).first()
    if not row:
        raise HTTPException(404)
    db.delete(row)
    db.commit()
    return {"ok": True}


@router.get("/enrollments")
def enrollments(db: Session = Depends(get_db)):
    rows = (
        db.query(Enrollment)
        .options(joinedload(Enrollment.program), joinedload(Enrollment.session))
        .order_by(Enrollment.created_at.desc())
        .all()
    )
    return [
        serialize(
            e,
            extra={
                "program": serialize(e.program) if e.program else None,
                "session": serialize(e.session) if e.session else None,
            },
        )
        for e in rows
    ]


@router.patch("/enrollments/{item_id}")
def update_enrollment(item_id: UUID, payload: EnrollmentStatusIn, db: Session = Depends(get_db)):
    row = db.query(Enrollment).filter(Enrollment.id == item_id).first()
    if not row:
        raise HTTPException(404)
    row.status = payload.status
    row.notes = payload.notes
    db.commit()
    return {"ok": True}


@router.get("/news")
def news_list(db: Session = Depends(get_db)):
    return [serialize(n) for n in db.query(News).order_by(News.published_at.desc()).all()]


@router.post("/news")
def create_news(payload: NewsIn, db: Session = Depends(get_db)):
    data = payload.model_dump()
    if not data.get("published_at"):
        data["published_at"] = datetime.utcnow()
    row = News(**data)
    db.add(row)
    db.commit()
    db.refresh(row)
    return serialize(row)


@router.put("/news/{item_id}")
def update_news(item_id: UUID, payload: NewsIn, db: Session = Depends(get_db)):
    row = db.query(News).filter(News.id == item_id).first()
    if not row:
        raise HTTPException(404)
    return apply(row, payload.model_dump(), db)


@router.delete("/news/{item_id}")
def delete_news(item_id: UUID, db: Session = Depends(get_db)):
    row = db.query(News).filter(News.id == item_id).first()
    if not row:
        raise HTTPException(404)
    db.delete(row)
    db.commit()
    return {"ok": True}


@router.get("/testimonials")
def testimonials(db: Session = Depends(get_db)):
    return [serialize(t) for t in db.query(Testimonial).order_by(Testimonial.sort_order).all()]


@router.post("/testimonials")
def create_testimonial(payload: TestimonialIn, db: Session = Depends(get_db)):
    row = Testimonial(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return serialize(row)


@router.put("/testimonials/{item_id}")
def update_testimonial(item_id: UUID, payload: TestimonialIn, db: Session = Depends(get_db)):
    row = db.query(Testimonial).filter(Testimonial.id == item_id).first()
    if not row:
        raise HTTPException(404)
    return apply(row, payload.model_dump(), db)


@router.delete("/testimonials/{item_id}")
def delete_testimonial(item_id: UUID, db: Session = Depends(get_db)):
    row = db.query(Testimonial).filter(Testimonial.id == item_id).first()
    if not row:
        raise HTTPException(404)
    db.delete(row)
    db.commit()
    return {"ok": True}


@router.get("/enterprise")
def enterprise(db: Session = Depends(get_db)):
    return [serialize(r) for r in db.query(EnterpriseRequest).order_by(EnterpriseRequest.created_at.desc()).all()]


@router.patch("/enterprise/{item_id}")
def update_enterprise(item_id: UUID, payload: EnrollmentStatusIn, db: Session = Depends(get_db)):
    row = db.query(EnterpriseRequest).filter(EnterpriseRequest.id == item_id).first()
    if not row:
        raise HTTPException(404)
    row.status = payload.status
    db.commit()
    return {"ok": True}


@router.get("/messages")
def messages(db: Session = Depends(get_db)):
    return [serialize(m) for m in db.query(ContactMessage).order_by(ContactMessage.created_at.desc()).all()]


@router.get("/settings/contact")
def get_settings(db: Session = Depends(get_db)):
    row = db.query(SiteSetting).filter(SiteSetting.key == "contact").first()
    return row.value if row else {}


@router.put("/settings/contact")
def update_settings(payload: SettingsIn, db: Session = Depends(get_db)):
    row = db.query(SiteSetting).filter(SiteSetting.key == "contact").first()
    if not row:
        row = SiteSetting(key="contact", value=payload.value)
        db.add(row)
    else:
        row.value = payload.value
    db.commit()
    return row.value
