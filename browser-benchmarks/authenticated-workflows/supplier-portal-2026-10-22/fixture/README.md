# Synthetic supplier portal fixture

This is the actual deployed Worker source and schema from the authenticated-workflow experiment, not browser-local simulated authentication. It uses a Sites-provisioned D1 binding named DB. The hosting.example.json is a template, not the executed manifest; use a new Site ID instead of overwriting the existing experiment.

Runtime secret names: FIXTURE_PASSWORD_SHA256 and FIXTURE_ADMIN_KEY. Generate a dedicated high-entropy synthetic password; configure its SHA-256 digest and a separate owner/admin key through the platform secret tool. No secret values, cookies or browser profiles are supplied here. The synthetic username is benchmark-buyer. Login sets a Secure, HttpOnly, same-site session cookie; server state records its one-way digest. Owner-only administration seeds/resets/verifies records and revokes sessions. Public reads/updates require the synthetic authenticated session, and saves require a session-bound CSRF value and current record version.

Apply the bounded schema migration using the hosting platform before testing. The build includes migrations in the artifact. The initial source-only deployment lacked its tables; that shared setup failure and repair are preserved. The ordinary hosting archive was attached before deploying corrected version 2. Functional fixture QA used SUP-C999 and removed it from the dashboard before scored runs. It is not an evaluated-agent success.

The benchmark fixture is intentionally small, uses synthetic data only and is not offered as a production supplier-management system. Earlier browser/desktop fixtures and installed applications were not modified.
