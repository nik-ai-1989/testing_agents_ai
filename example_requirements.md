# Project Requirements: User Authentication & Profile Management

## Project Overview
Add a secure user authentication system and profile management feature to our web application. Users must be able to register, log in, reset their password, and manage their personal profile.

## Business Context
Currently users share a single admin account. We need individual accounts to support audit trails, personalised settings, and future role-based access control.

## Stakeholders
- **End Users**: Need a simple, secure way to create and manage their own accounts
- **Admins**: Need to view, deactivate, and manage user accounts
- **Security Team**: Requires MFA, session management, and audit logging

## Functional Requirements

### Registration
1. Users can register with an email address and password
2. Email must be verified before the account is activated
3. Password must be at least 12 characters and contain uppercase, lowercase, number, and special character
4. Duplicate email addresses must be rejected with a clear error message

### Login
5. Users can log in with email and password
6. Failed login attempts are counted; after 5 consecutive failures the account is locked for 15 minutes
7. Users can optionally enable two-factor authentication (TOTP, e.g. Google Authenticator)
8. A "Remember me" option keeps the session alive for 30 days; without it sessions expire after 8 hours

### Password Reset
9. Users can request a password reset via their registered email
10. The reset link is valid for 1 hour and is single-use
11. After a reset, all other active sessions are invalidated

### Profile Management
12. Users can view and update their display name, avatar, and timezone
13. Users can change their email address (new address must be verified before it takes effect)
14. Users can change their password (must confirm current password first)
15. Users can view and terminate their active sessions from a "Security" settings tab
16. Users can delete their account; deletion is soft (data retained 30 days for recovery)

### Admin
17. Admins can list all users with filters (active/inactive, registration date range)
18. Admins can deactivate or reactivate a user account
19. Admins can impersonate a user for support purposes (action is logged)
20. An audit log records all authentication events (login, logout, password change, MFA changes)

## Non-Functional Requirements
- **Performance**: Login endpoint must respond within 500ms at the 95th percentile
- **Security**: Passwords stored as bcrypt hashes (cost factor ≥ 12); HTTPS only
- **Usability**: All forms must be accessible (WCAG 2.1 AA) and work on mobile
- **Availability**: Auth service must achieve 99.9% uptime

## Constraints
- Must integrate with the existing PostgreSQL database
- Cannot use third-party identity providers (e.g. Auth0) — must be self-hosted
- The admin panel is separate from the user-facing app (different subdomain)

## Out of Scope
- Social login (Google, GitHub, etc.) — planned for Phase 2
- Role-based access control beyond admin/user distinction — planned for Phase 3
- SSO / SAML — future enterprise feature
