# Database & API
Tables:
users, roles, consent_records, mood_checkins, journal_entries, selfcare_items, selfcare_uses,
knowledge_items, knowledge_versions, conversation_sessions, conversation_messages,
policy_events, safety_events, professionals, availability_slots, appointments,
notification_preferences, help_contacts, feature_flags, model_versions, model_runs, audit_events.

Use Alembic migrations.

P0 APIs:
/auth/login /auth/refresh /me
/consents
/mood-checkins
/journal
/selfcare
/chat/messages
/help-contacts
/professionals
/appointments
/privacy/export
/privacy/delete-request
/admin/knowledge
/admin/policies
/admin/audit
/admin/dashboard
/research/model-card

Every owner-scoped endpoint must enforce ownership server-side.
