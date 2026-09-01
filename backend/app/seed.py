from datetime import date, datetime

from sqlalchemy.orm import Session

from .auth import hash_password
from .config import settings
from .models import AdminUser, News, Program, Session as CourseSession, SiteSetting, Testimonial


PROGRAMS = [
    {
        "slug": "anglais",
        "code": "ENG",
        "title_fr": "Anglais",
        "title_en": "English",
        "tagline_fr": "Communiquez avec confiance dans votre environnement.",
        "tagline_en": "Communicate with confidence in any setting.",
        "description_fr": "Formation centrée sur l’expression orale, la compréhension, le vocabulaire et la confiance dans différents contextes : études, vie quotidienne, travail, échanges avec des partenaires et voyages.",
        "description_en": "A course focused on speaking, listening, useful vocabulary and confidence across studies, daily life, work, partner conversations and travel.",
        "objectives": [
            {"fr": "Converser plus aisément selon son niveau.", "en": "Hold conversations more easily at your level."},
            {"fr": "Utiliser un vocabulaire utile et approprié.", "en": "Use useful, appropriate vocabulary."},
            {"fr": "Comprendre et participer à des échanges en anglais.", "en": "Understand and take part in English exchanges."},
            {"fr": "Gagner en confiance dans des situations réelles.", "en": "Build confidence in real situations."},
        ],
        "audience_fr": "Débutants souhaitant poser des bases solides, apprenants intermédiaires qui veulent gagner en aisance, et professionnels ayant besoin d’anglais au quotidien.",
        "audience_en": "Beginners building solid foundations, intermediate learners seeking fluency, and professionals who need English at work.",
        "modules": [
            {"fr": "Compréhension orale et vocabulaire actif", "en": "Listening and active vocabulary"},
            {"fr": "Expression orale guidée et conversation", "en": "Guided speaking and conversation"},
            {"fr": "Situations réelles : travail, études, voyages", "en": "Real situations: work, study, travel"},
            {"fr": "Prononciation et confiance à l’oral", "en": "Pronunciation and speaking confidence"},
        ],
        "prerequisites_fr": "Aucun prérequis pour le Level 1. Le Level 2 s’adresse aux apprenants qui possèdent déjà des bases.",
        "prerequisites_en": "No prerequisite for Level 1. Level 2 is for learners who already have foundations.",
        "image_url": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1400&q=80",
        "category": "langues",
        "sort_order": 1,
    },
    {
        "slug": "communication-professionnelle",
        "code": "COP",
        "title_fr": "Communication professionnelle",
        "title_en": "Professional communication",
        "tagline_fr": "Exprimez vos idées avec impact.",
        "tagline_en": "Express your ideas with impact.",
        "description_fr": "Formation destinée à renforcer la communication orale et écrite, la prise de parole, la gestion du stress et la capacité à convaincre.",
        "description_en": "A course to strengthen spoken and written communication, public speaking, stress management and the ability to persuade.",
        "objectives": [
            {"fr": "Structurer un message clair et convaincant.", "en": "Structure a clear, convincing message."},
            {"fr": "Prendre la parole avec aisance.", "en": "Speak in public with ease."},
            {"fr": "Maîtriser la communication non verbale.", "en": "Master non-verbal communication."},
            {"fr": "Rédiger avec précision et impact.", "en": "Write with precision and impact."},
        ],
        "audience_fr": "Cadres, entrepreneurs, porte-parole, étudiants et toute personne amenée à présenter, négocier ou représenter une organisation.",
        "audience_en": "Managers, entrepreneurs, spokespersons, students and anyone who presents, negotiates or represents an organisation.",
        "modules": [
            {"fr": "Art oratoire et rhétorique", "en": "Public speaking and rhetoric"},
            {"fr": "Communication non verbale", "en": "Non-verbal communication"},
            {"fr": "Prise de parole en public et gestion de l’auditoire", "en": "Public speaking and audience management"},
            {"fr": "Communication institutionnelle, commerciale et écrite", "en": "Institutional, commercial and written communication"},
        ],
        "prerequisites_fr": "Aucun prérequis technique.",
        "prerequisites_en": "No technical prerequisite.",
        "image_url": "https://images.unsplash.com/photo-1557804506-669a67965ba0?auto=format&fit=crop&w=1400&q=80",
        "category": "communication",
        "sort_order": 2,
    },
    {
        "slug": "intelligence-artificielle-fondamentale",
        "code": "IAF",
        "title_fr": "Intelligence artificielle fondamentale",
        "title_en": "Foundational artificial intelligence",
        "tagline_fr": "Utilisez l’IA pour travailler plus efficacement.",
        "tagline_en": "Use AI to work more effectively.",
        "description_fr": "Initiation pratique aux usages de l’intelligence artificielle dans les études, la bureautique, la communication, l’organisation du travail et la création de contenus.",
        "description_en": "A practical introduction to AI for studies, office work, communication, work organisation and content creation.",
        "objectives": [
            {"fr": "Comprendre ce que l’IA peut réellement faire pour vous.", "en": "Understand what AI can actually do for you."},
            {"fr": "Utiliser les outils d’IA au quotidien, avec méthode.", "en": "Use AI tools daily, with method."},
            {"fr": "Protéger vos données personnelles.", "en": "Protect your personal data."},
            {"fr": "Gagner du temps sur la rédaction et la productivité.", "en": "Save time on writing and productivity."},
        ],
        "audience_fr": "Professionnels, étudiants et entrepreneurs qui veulent intégrer l’IA dans leur pratique sans bagage technique préalable.",
        "audience_en": "Professionals, students and entrepreneurs who want to bring AI into their practice without a technical background.",
        "modules": [
            {"fr": "Culture numérique et outils d’IA", "en": "Digital culture and AI tools"},
            {"fr": "Données personnelles et usage responsable", "en": "Personal data and responsible use"},
            {"fr": "Rédaction, bureautique et production visuelle", "en": "Writing, office work and visual production"},
            {"fr": "Productivité et organisation du travail", "en": "Productivity and work organisation"},
        ],
        "prerequisites_fr": "Savoir utiliser un ordinateur et un navigateur web.",
        "prerequisites_en": "Comfortable using a computer and a web browser.",
        "image_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1400&q=80",
        "category": "numerique",
        "sort_order": 3,
    },
    {
        "slug": "intelligence-artificielle-avancee",
        "code": "IAA",
        "title_fr": "Intelligence artificielle avancée",
        "title_en": "Advanced artificial intelligence",
        "tagline_fr": "Passez de l’utilisation à la maîtrise.",
        "tagline_en": "Move from using AI to mastering it.",
        "description_fr": "Formation destinée aux personnes qui utilisent déjà régulièrement l’IA et souhaitent approfondir leur pratique.",
        "description_en": "For people who already use AI regularly and want to go further.",
        "objectives": [
            {"fr": "Concevoir des prompts avancés et reproductibles.", "en": "Design advanced, repeatable prompts."},
            {"fr": "Créer des contenus multimédias assistés par l’IA.", "en": "Create AI-assisted multimedia content."},
            {"fr": "Analyser des données avec l’aide de l’IA.", "en": "Analyse data with AI support."},
            {"fr": "Intégrer l’IA dans les processus d’une organisation.", "en": "Integrate AI into organisational processes."},
        ],
        "audience_fr": "Professionnels déjà familiers des outils d’IA, responsables innovation, créateurs de contenus et équipes projet.",
        "audience_en": "Professionals already familiar with AI tools, innovation leads, content creators and project teams.",
        "modules": [
            {"fr": "Prompt engineering avancé", "en": "Advanced prompt engineering"},
            {"fr": "Création multimédia assistée", "en": "AI-assisted multimedia creation"},
            {"fr": "Analyse de données et programmation assistée", "en": "Data analysis and assisted programming"},
            {"fr": "Intégration de l’IA en entreprise", "en": "AI integration in organisations"},
        ],
        "prerequisites_fr": "Pratique régulière d’au moins un outil d’IA générative.",
        "prerequisites_en": "Regular use of at least one generative AI tool.",
        "image_url": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&w=1400&q=80",
        "category": "numerique",
        "sort_order": 4,
    },
    {
        "slug": "entrepreneuriat",
        "code": "ENT",
        "title_fr": "Entrepreneuriat",
        "title_en": "Entrepreneurship",
        "tagline_fr": "Structurez votre projet et passez à l’action.",
        "tagline_en": "Structure your project and take action.",
        "description_fr": "Formation destinée aux porteurs de projets et entrepreneurs qui souhaitent structurer, formaliser ou développer leur activité.",
        "description_en": "For founders and entrepreneurs who want to structure, formalise or grow their venture.",
        "objectives": [
            {"fr": "Clarifier et formaliser une idée de projet.", "en": "Clarify and formalise a project idea."},
            {"fr": "Comprendre les obligations essentielles.", "en": "Understand essential obligations."},
            {"fr": "Préparer un pitch convaincant.", "en": "Prepare a convincing pitch."},
            {"fr": "Se préparer aux opportunités de financement.", "en": "Get ready for funding opportunities."},
        ],
        "audience_fr": "Porteurs de projets, entrepreneurs en phase de lancement ou de croissance, et professionnels qui envisagent de créer une activité.",
        "audience_en": "Project holders, early-stage and growing entrepreneurs, and professionals considering starting a venture.",
        "modules": [
            {"fr": "Idée de projet et formalisation", "en": "Project idea and formalisation"},
            {"fr": "Obligations essentielles et organisation", "en": "Essential obligations and organisation"},
            {"fr": "Présentation de projet et pitch", "en": "Project presentation and pitch"},
            {"fr": "Préparation aux opportunités de financement", "en": "Preparing for funding opportunities"},
        ],
        "prerequisites_fr": "Avoir une idée de projet ou une activité existante à structurer.",
        "prerequisites_en": "Have a project idea or an existing activity to structure.",
        "image_url": "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=1400&q=80",
        "category": "business",
        "sort_order": 5,
    },
    {
        "slug": "bureautique-moderne",
        "code": "BUM",
        "title_fr": "Bureautique moderne",
        "title_en": "Modern office tools",
        "tagline_fr": "Maîtrisez les outils indispensables au travail.",
        "tagline_en": "Master the tools work actually requires.",
        "description_fr": "Formation pratique portant sur les outils de productivité administrative et professionnelle.",
        "description_en": "Hands-on training on the administrative and professional productivity tools used every day.",
        "objectives": [
            {"fr": "Produire des documents Word professionnels.", "en": "Produce professional Word documents."},
            {"fr": "Exploiter Excel et Google Sheets avec méthode.", "en": "Use Excel and Google Sheets with method."},
            {"fr": "Concevoir des présentations claires.", "en": "Design clear presentations."},
            {"fr": "Collaborer efficacement en ligne.", "en": "Collaborate effectively online."},
        ],
        "audience_fr": "Assistants, étudiants, agents administratifs et professionnels qui veulent gagner en efficacité sur les outils du quotidien.",
        "audience_en": "Assistants, students, administrative staff and professionals who want to work faster with everyday tools.",
        "modules": [
            {"fr": "Word professionnel", "en": "Professional Word"},
            {"fr": "Excel et Google Sheets", "en": "Excel and Google Sheets"},
            {"fr": "PowerPoint et présentations", "en": "PowerPoint and presentations"},
            {"fr": "Google Workspace, organisation numérique et collaboration", "en": "Google Workspace, digital organisation and collaboration"},
        ],
        "prerequisites_fr": "Savoir allumer un ordinateur et utiliser un clavier. Le reste s’apprend ici.",
        "prerequisites_en": "Be able to use a computer and a keyboard. The rest is taught here.",
        "image_url": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1400&q=80",
        "category": "numerique",
        "sort_order": 6,
    },
]


def seed_if_empty(db: Session) -> None:
    if db.query(AdminUser).count() == 0:
        db.add(
            AdminUser(
                email=settings.admin_email,
                name="Acad'Emy Admin",
                hashed_password=hash_password(settings.admin_password),
            )
        )

    if db.query(Program).count() == 0:
        programs_by_code: dict[str, Program] = {}
        for data in PROGRAMS:
            p = Program(**data, is_featured=True, is_published=True)
            db.add(p)
            db.flush()
            programs_by_code[p.code] = p

        english = programs_by_code["ENG"]
        db.add_all(
            [
                CourseSession(
                    program_id=english.id,
                    slug="english-level-1",
                    title_fr="English Level 1",
                    title_en="English Level 1",
                    summary_fr="Une formation pour construire ou consolider les bases de l’anglais. Les participants développent progressivement leur compréhension, leur vocabulaire et leur capacité à s’exprimer dans des situations simples.",
                    summary_en="A course to build or consolidate English foundations. Participants gradually develop comprehension, vocabulary and the ability to express themselves in simple situations.",
                    start_date=date(2026, 9, 22),
                    end_date=date(2026, 11, 7),
                    duration_fr="Du 22 septembre au 7 novembre 2026",
                    duration_en="22 September to 7 November 2026",
                    status="open",
                    tuition_usd=80,
                    enrollment_fee_usd=10,
                    format="in_person",
                    cta_fr="S’inscrire au Level 1",
                    cta_en="Enroll in Level 1",
                    is_highlighted=True,
                ),
                CourseSession(
                    program_id=english.id,
                    slug="english-level-2",
                    title_fr="English Level 2",
                    title_en="English Level 2",
                    summary_fr="Une formation pour les apprenants qui possèdent déjà des bases et veulent communiquer avec plus d’aisance. Elle permet de renforcer la compréhension, l’expression orale et le vocabulaire utile.",
                    summary_en="For learners who already have foundations and want to communicate with more ease. It strengthens comprehension, speaking and useful vocabulary.",
                    start_date=date(2026, 9, 22),
                    end_date=date(2026, 11, 7),
                    duration_fr="Du 22 septembre au 7 novembre 2026",
                    duration_en="22 September to 7 November 2026",
                    status="open",
                    tuition_usd=80,
                    enrollment_fee_usd=10,
                    format="in_person",
                    cta_fr="S’inscrire au Level 2",
                    cta_en="Enroll in Level 2",
                    is_highlighted=True,
                ),
                CourseSession(
                    program_id=english.id,
                    slug="speaking-lab",
                    title_fr="Acad’Emy Speaking Lab",
                    title_en="Acad’Emy Speaking Lab",
                    summary_fr="Un atelier pratique de conversation anglaise. Les participants pratiquent l’expression orale à travers des discussions, jeux de rôle, mises en situation et exercices de vocabulaire.",
                    summary_en="A practical English conversation workshop. Participants practise speaking through discussions, role-plays, real-life situations and vocabulary drills.",
                    start_date=date(2026, 9, 19),
                    end_date=None,
                    duration_fr="4 samedis à partir du 19 septembre 2026",
                    duration_en="4 Saturdays from 19 September 2026",
                    status="open",
                    tuition_usd=15,
                    enrollment_fee_usd=0,
                    format="in_person",
                    cta_fr="Réserver ma place au Speaking Lab",
                    cta_en="Reserve my Speaking Lab seat",
                    is_highlighted=True,
                ),
            ]
        )

    if db.query(News).count() == 0:
        db.add_all(
            [
                News(
                    slug="inscriptions-anglais-2026",
                    title_fr="Inscriptions ouvertes — Sessions d’anglais 2026",
                    title_en="Enrollment open — English sessions 2026",
                    excerpt_fr="Développez votre aisance en anglais grâce à des formations pratiques, structurées et orientées vers la communication réelle.",
                    excerpt_en="Build your English fluency with practical, structured training focused on real communication.",
                    content_fr=(
                        "Les inscriptions aux sessions d’anglais 2026 sont ouvertes.\n\n"
                        "English Level 1 et English Level 2 se tiennent du 22 septembre au 7 novembre 2026 "
                        "(80 USD + 10 USD de frais d’inscription).\n\n"
                        "L’Acad’Emy Speaking Lab commence le 19 septembre 2026, pendant 4 samedis (15 USD).\n\n"
                        "Choisissez votre niveau ou rejoignez le Speaking Lab pour pratiquer l’anglais chaque samedi "
                        "dans une ambiance dynamique."
                    ),
                    content_en=(
                        "Enrollment for the 2026 English sessions is now open.\n\n"
                        "English Level 1 and English Level 2 run from 22 September to 7 November 2026 "
                        "(USD 80 + USD 10 enrollment fee).\n\n"
                        "Acad’Emy Speaking Lab starts on 19 September 2026, for 4 Saturdays (USD 15).\n\n"
                        "Choose your level or join the Speaking Lab to practise English every Saturday "
                        "in a lively setting."
                    ),
                    image_url="https://images.unsplash.com/photo-1524178232363-1fb2b075b655?auto=format&fit=crop&w=1400&q=80",
                    category="inscriptions",
                    published_at=datetime(2026, 8, 20),
                ),
                News(
                    slug="speaking-lab-samedis",
                    title_fr="Speaking Lab : quatre samedis pour oser parler",
                    title_en="Speaking Lab: four Saturdays to start speaking",
                    excerpt_fr="Discussions, jeux de rôle et mises en situation. Un atelier court, concret, pour débloquer l’oral.",
                    excerpt_en="Discussions, role-plays and real-life situations. A short, concrete workshop to unlock speaking.",
                    content_fr=(
                        "Le Speaking Lab n’est pas un cours théorique. Pendant quatre samedis, vous parlez, "
                        "vous vous corrigez, vous recommencez.\n\n"
                        "Début : 19 septembre 2026. Frais de participation : 15 USD. Places limitées."
                    ),
                    content_en=(
                        "Speaking Lab is not a theory class. Over four Saturdays you speak, get corrected, and try again.\n\n"
                        "Start: 19 September 2026. Fee: USD 15. Limited seats."
                    ),
                    image_url="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=1400&q=80",
                    category="evenements",
                    published_at=datetime(2026, 8, 25),
                ),
                News(
                    slug="cinq-minutes-anglais-chaque-jour",
                    title_fr="Conseil : cinq minutes d’anglais chaque jour",
                    title_en="Tip: five minutes of English every day",
                    excerpt_fr="La régularité bat l’intensité. Voici une routine simple pour progresser avant la rentrée de septembre.",
                    excerpt_en="Consistency beats intensity. A simple routine to progress before the September intake.",
                    content_fr=(
                        "Écoutez un court extrait audio, répétez à voix haute, notez trois mots utiles. "
                        "Cinq minutes suffisent si vous les tenez chaque jour.\n\n"
                        "En septembre, vous arriverez déjà en mouvement."
                    ),
                    content_en=(
                        "Listen to a short clip, repeat it out loud, write down three useful words. "
                        "Five minutes is enough if you keep it every day.\n\n"
                        "In September you will already be in motion."
                    ),
                    image_url="https://images.unsplash.com/photo-1456513080800-7d93dbe9f26b?auto=format&fit=crop&w=1400&q=80",
                    category="conseils",
                    published_at=datetime(2026, 8, 28),
                ),
            ]
        )

    if db.query(Testimonial).count() == 0:
        db.add_all(
            [
                Testimonial(
                    name="Grace M.",
                    role_fr="Responsable administrative",
                    role_en="Administrative officer",
                    quote_fr="J’avais besoin d’anglais pour les réunions avec des partenaires. En quelques semaines, je prends la parole sans traduire chaque phrase dans ma tête.",
                    quote_en="I needed English for meetings with partners. Within weeks I was speaking without translating every sentence in my head.",
                    photo_url="",
                    sort_order=1,
                ),
                Testimonial(
                    name="Patrick K.",
                    role_fr="Entrepreneur",
                    role_en="Entrepreneur",
                    quote_fr="La méthode est concrète : on pratique, on corrige, on réapplique. Ce n’est pas un cours pour remplir un cahier.",
                    quote_en="The method is concrete: you practise, get corrected, then apply it again. It is not a course for filling a notebook.",
                    photo_url="",
                    sort_order=2,
                ),
                Testimonial(
                    name="Sarah L.",
                    role_fr="Étudiante",
                    role_en="Student",
                    quote_fr="Le Speaking Lab m’a débloquée. L’ambiance est exigeante et bienveillante à la fois. Je recommande.",
                    quote_en="Speaking Lab unlocked me. The atmosphere is both demanding and kind. I recommend it.",
                    photo_url="",
                    sort_order=3,
                ),
            ]
        )

    if db.query(SiteSetting).filter(SiteSetting.key == "contact").count() == 0:
        db.add(
            SiteSetting(
                key="contact",
                value={
                    "phone": "+243 81 000 0243",
                    "whatsapp": "243810000243",
                    "email": "contact@acad-emy.com",
                    "address_fr": "Kinshasa, République Démocratique du Congo",
                    "address_en": "Kinshasa, Democratic Republic of the Congo",
                    "hours_fr": "Lundi – Vendredi : 8h – 17h\nSamedi : 9h – 13h\nDimanche : fermé",
                    "hours_en": "Monday – Friday: 8:00 – 17:00\nSaturday: 9:00 – 13:00\nSunday: closed",
                    "maps_embed": "https://www.google.com/maps?q=Kinshasa&output=embed",
                    "maps_url": "https://maps.google.com/?q=Kinshasa",
                    "facebook": "https://facebook.com",
                    "instagram": "https://instagram.com",
                    "linkedin": "https://linkedin.com",
                    "parent": "LawApp Group50",
                },
            )
        )

    db.commit()
