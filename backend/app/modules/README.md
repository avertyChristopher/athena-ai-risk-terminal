Backend module map for Athena AI Risk Terminal.

This directory prepares a product-oriented backend structure that mirrors the
frontend navigation. The existing app remains stable while modules are migrated
progressively.

Current status:
- equity_analysis exposes route, schema, service and domain wrappers here.
- other module folders are category anchors that document ownership and can be
  filled as each Athena feature matures.

Shared infrastructure such as database sessions, configuration, logging and
security remains centralized under app/core and app/database.
