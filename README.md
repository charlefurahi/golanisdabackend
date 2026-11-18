# GolaniSDA Backend

Django 6 + DRF backend, rebuilt against the frontend/backend gap analysis so the
API now matches what the Vue frontend actually calls.

## What changed (per the gap analysis)

- **New `apps/accounts` app** — custom email-based `User` model (`phone`, `role`),
  full JWT flow via `djangorestframework-simplejwt`: register, login, logout
  (blacklists refresh token), token refresh, `me` (get/patch), change-password,
  password-reset request + confirm, and admin user list/detail.
- **API versioned at `/api/v1/...`** to match `VITE_API_BASE_URL`.
- **Global permissions locked down.** Default is `IsAuthenticatedOrReadOnly`;
  every admin-content viewset additionally uses `IsAdminOrReadOnly` (public read,
  admin write) or `IsAdminOnly` (admin read+write) from `apps/common/permissions.py`.
- **Field names aligned to the frontend** across announcements, events, sermons,
  leadership, contact, and donations — see the table in the original gap
  analysis for the full before/after per app.
- **New models added:** `EventRSVP`, `Campaign`, `NewsletterSubscriber`,
  `LeadershipInquiry`, and a `GalleryCategory` / `Album` / `Photo` structure
  replacing the old flat `GalleryItem`.
- **New endpoints implemented:** `events/{upcoming,past,all_events,featured,
  categories}`, `events/{id}/rsvp/` + `events/{id}/rsvps/`, `sermons/{featured,
  categories,speakers}`, `donations/{stats,verify,campaigns}`,
  `contact/admin/`, `contact/newsletter/{subscribe,unsubscribe}`,
  `leadership/inquiries/`, `gallery/photos/bulk/`.
- **`django-filter`** wired in everywhere (`?search=`, `?ordering=`, and
  per-app `filterset_fields`), plus `PageNumberPagination` (`page_size` param
  supported, default page size 20).
- **Fixed the hardcoded `127.0.0.1:8000`** in the ministries serializer — it
  now uses `request.build_absolute_uri()`.
- **Fixed the leadership router path** (`/leadership/leaders/...` instead of
  serving leaders at the app root), and added `/leadership/inquiries/`.

Every model/serializer/view file was rewritten from scratch, migrations were
regenerated from zero, and the whole stack was smoke-tested end-to-end
(register → login → refresh → change-password → logout, permission checks for
anon/member/admin, and full create/read flows for every app including the
RSVP-capacity check and the gallery bulk-upload endpoint) against a live dev
server before packaging.

## Design assumptions worth knowing about

The gap analysis inferred field names from the frontend's service files, not
the actual form markup, so a few judgment calls were made:

- **`_url` suffixed fields** (`banner_url`, `thumbnail_url`, `photo_url`,
  `pdf_file_url`, etc.) are implemented as **read-only computed fields**
  returning an absolute URL, while the underlying file itself is still
  uploaded via the un-suffixed field name (`banner`, `thumbnail`, `photo`,
  `pdf_file`) as multipart form data. If the frontend actually posts a raw
  URL string to these `_url` fields (e.g. for externally-hosted media)
  instead of uploading a file, that'll need a quick adjustment.
- **Events `category`** and **Sermons `category`** are plain free-text
  `CharField`s (not a FK to a fixed list), since the frontend calls
  `/categories/` for a distinct list rather than a fixed enum.
- **Sermon `speaker`** was kept as a FK to `Leadership` (not a free-text
  field) per the analysis's own recommendation — the admin form will need to
  use a leader-picker rather than a text input.
- **Donations `create`** and **`verify`** stay public (`AllowAny`); list/
  retrieve/stats are admin-only, since donor PII shouldn't be publicly
  listable even though the original analysis flagged this as "defer."
- **`giving_type`**, **`priority`**, **`role`** etc. are `choices`-constrained
  `CharField`s with the values named in the gap analysis — extend the
  `_CHOICES` list in the model if you need more.

## Running it locally

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser  # prompts for email/password
python manage.py runserver
```

The API is served at `http://127.0.0.1:8000/api/v1/`, admin at `/admin/`.

### Environment variables (all optional, sensible dev defaults)

| Variable | Default | Purpose |
|---|---|---|
| `SECRET_KEY` | insecure dev key | set a real one in production |
| `DEBUG` | `True` | set `False` in production |
| `FRONTEND_URL` | `http://localhost:5173` | used to build password-reset links |
| `EMAIL_BACKEND` | console backend | swap for SMTP in production |
| `DEFAULT_FROM_EMAIL` | `no-reply@golanisda.org` | |

Password-reset emails print to the console in dev (no SMTP configured) — this
is expected, not a bug.

## Deploying to Render with the Vercel frontend

The repository includes a `render.yaml` Blueprint for the Django web service,
PostgreSQL database, and persistent media disk. In Render, create a Blueprint
from this repository and apply the generated configuration. The service runs
database migrations when it starts. Its health check uses `/`.

After Render creates the service, copy its public URL and set this environment
variable in the Vercel project for `sdachurch-golani.vercel.app`:

```text
VITE_API_BASE_URL=https://<your-render-service>.onrender.com/api/v1
```

Redeploy the Vercel frontend after saving the variable. The backend's
`CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS`, and `FRONTEND_URL` are set in
the Blueprint for `https://sdachurch-golani.vercel.app`. Add any other frontend
domains as comma-separated origins in the corresponding Render environment
variables.

Uploaded media is stored on the Blueprint's persistent disk and served under
`/media/`. Email remains on Django's console backend until SMTP settings are
configured. Donation verification is still a placeholder and does not confirm
payments with a provider.

## Full endpoint list

See `golanisdabackend/urls.py` and each app's `urls.py` for the definitive
routing; the shape matches the "Recommended endpoint contract" table from the
gap analysis (section 4) with one exception: `donations/campaigns/` is a full
CRUD viewset (list/create/retrieve/update/delete) rather than list-only, since
an admin needs to manage campaigns, not just view them.

## What's intentionally out of scope

- Real payment-gateway integration for donations — `verify/` currently just
  checks whether a `transaction_id` exists in the database.
- Production media storage (S3, etc.) — media is still served from
  `MEDIA_ROOT` when `DEBUG=True`, same as before.
- The frontend-side issues noted in the gap analysis (§6): a missing
  `markInquiryRead` method in `leadershipService.js`, empty stub service
  files, and a duplicate `Events - Copy.vue` — these live in the frontend
  repo and weren't touched here.
