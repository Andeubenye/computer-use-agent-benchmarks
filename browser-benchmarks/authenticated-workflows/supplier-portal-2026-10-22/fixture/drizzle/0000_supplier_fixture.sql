CREATE TABLE sessions (token_hash TEXT PRIMARY KEY, username TEXT NOT NULL, created_at TEXT NOT NULL, expires_at TEXT NOT NULL, revoked INTEGER NOT NULL DEFAULT 0);
--> statement-breakpoint
CREATE TABLE suppliers (id TEXT PRIMARY KEY, batch_id TEXT NOT NULL, pair_index INTEGER NOT NULL, cohort TEXT NOT NULL, name TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'Pending', notes TEXT NOT NULL DEFAULT '', version INTEGER NOT NULL DEFAULT 0, confirmation_id TEXT, updated_at TEXT, updated_session_hash TEXT);
--> statement-breakpoint
CREATE TABLE audit_events (event_id TEXT PRIMARY KEY, at TEXT NOT NULL, kind TEXT NOT NULL, record_id TEXT, session_hash TEXT, details TEXT NOT NULL);
--> statement-breakpoint
CREATE INDEX supplier_batch_idx ON suppliers(batch_id, pair_index);
--> statement-breakpoint
CREATE INDEX audit_record_idx ON audit_events(record_id, at);
