# Online Kurs Platformasi

Django + DRF + Django Template asosidagi onlayn kurs platformasi. Admin panel ishlatilmaydi; barcha amallar autentifikatsiya orqali.

## Talablar

- Python 3.10+
- Django 4.2+, DRF, djangorestframework-simplejwt

## Oʻrnatish

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Brauzerda: **http://127.0.0.1:8000/**

## API (barcha endpointlar auth talab qiladi, login/register bundan mustasno)

- **Auth:** `POST /api/auth/register/`, `POST /api/auth/login/`, `POST /api/auth/logout/`, `GET /api/auth/me/`
- **Kurslar:** `GET|POST /api/courses/`, `GET|PUT|PATCH|DELETE /api/courses/<id>/`
- **Darslar:** `GET|POST /api/courses/<id>/lessons/`, `GET|PUT|PATCH|DELETE /api/lessons/<id>/`
- **Yozilish:** `GET|POST /api/enrollments/`, `POST /api/enrollments/<id>/leave/`

Token: Login javobida `access` va `refresh` beriladi. Soʻrovlarda header: `Authorization: Bearer <access>`.

## Rollar

- **Teacher:** kurs yaratish/tahrirlash/oʻchirish, dars qoʻshish/tahrirlash/oʻchirish.
- **Student:** kurslarni koʻrish, kursga yozilish, kursdan chiqish.

## Loyiha tuzilishi

- `config/` – sozlamalar (admin yoʻq)
- `accounts/` – Custom User (role, added_at), auth API
- `courses/` – Course, Lesson, Enrollment modellari, API va web sahifalar
- `templates/` – bitta layout, Bootstrap 5
