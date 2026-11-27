"""
User Routes API Documentation
=============================
All endpoints are registered in users/userRoutes.py.
Authentication is handled by AuthMiddleware (JWT), EXCEPT for the paths listed
in EXCLUDED_PATHS in middleware/AuthMiddleware.py.
"""

# ─── AUTH FLOWS ──────────────────────────────────────────────────────────────

createUserDocumentation = """
**Purpose:**
1. Create a user with `name` and `email` (or reuse the existing one with that email).
2. Return a JWT `token` for that user.

**Code Explanation:**
1. Receive `name` and `email` in the request body.
2. Find the user in `users` by email.
   - If found → use its `_id`.
   - If not → insert a new document with `name`, `email`, `createdAt`, `updatedAt`.
3. Create a token with `{"id": userId}` and return it.

**Excluded from auth middleware:** Yes (no token required).
"""

# ─── PROFILE ─────────────────────────────────────────────────────────────────

getUserDetailsDocumentation = """
**Purpose:**
1. Return the logged-in user's details.

**Code Explanation:**
1. AuthMiddleware decodes the `token` header and sets `request.state.userId`.
2. Find the user in `users` by `_id`.
   - If not found → return 404: "User not found".
3. Return `userDetails`.

**Excluded from auth middleware:** No (token required).
"""
