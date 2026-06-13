# Track derived_fields_validation_manifests_20260609 Context

Add validation tests/manifests for derived fields.

This is the shared QA gate for member identity, party attribution, and speech-turn derived artifacts. It prevents derived fields from being published without schema, provenance, confidence, and regression validation.

The track now includes the shared validation schema, policy doc, helper script, per-artifact manifests, and regression tests. Member identity remains blocked pending implementation, party attribution remains blocked pending validated member identity, and speech-turn remains blocked pending validated member identity plus explicit release-decision handling.
