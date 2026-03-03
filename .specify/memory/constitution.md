<!--
  Sync Impact Report
  ==================
  Version change: [template] → 1.0.0
  Modified principles: N/A (initial ratification)
  Added sections:
    - Core Principles (3 principles: TDD, Proven Solutions, No Premature Optimization)
    - Development Standards (accessibility, layered architecture, contract-first)
    - Quality Gates (merge criteria, test coverage, lint requirements)
    - Governance (amendment procedure, compliance expectations)
  Removed sections: All template placeholders replaced
  Templates requiring updates:
    - .specify/templates/plan-template.md ✅ No change needed (Constitution Check
      is a dynamic placeholder filled at plan time)
    - .specify/templates/spec-template.md ✅ No change needed (already enforces
      testable requirements and acceptance scenarios)
    - .specify/templates/tasks-template.md ✅ No change needed (already mandates
      tests-first ordering and Red-Green-Refactor notes)
  Follow-up TODOs: None
-->

# Donation Genie Constitution

## Core Principles

### I. Test-Driven Development (NON-NEGOTIABLE)

Every feature MUST follow the Red-Green-Refactor cycle:

1. **Red**: Write failing tests that define the expected behavior
2. **Green**: Write the minimum code to make the tests pass
3. **Refactor**: Clean up while keeping tests green

Rules:

- Tests MUST be written and approved before implementation begins
- Tests MUST fail before any production code is written for that behavior
- No production code MUST be merged without corresponding test coverage
- Backend tests use pytest; frontend unit tests use Vitest;
  E2E and accessibility tests use Playwright with @axe-core/playwright
- Acceptance scenarios from the spec MUST map to executable tests
- Test names MUST describe the behavior being verified, not the
  implementation

### II. Proven Solutions Over Clever Ones

Use battle-tested, well-documented libraries and patterns. Reject
novelty for novelty's sake.

Rules:

- When a well-maintained library solves the problem, use it instead
  of writing custom code
- Prefer standard patterns documented in official framework guides
  (Django docs, React docs, TanStack Router docs)
- New dependencies MUST have active maintenance (commits within
  6 months), clear documentation, and a meaningful user base
- Custom abstractions are permitted only when no suitable library
  exists or when the library adds disproportionate complexity
- Code MUST be readable by a developer unfamiliar with the project;
  clever one-liners that sacrifice clarity are prohibited
- When multiple approaches exist, choose the one with the most
  community precedent and documentation

### III. No Premature Optimization

Build the simplest thing that works. Optimize only when measurements
prove a bottleneck exists.

Rules:

- YAGNI: Do not add code, abstractions, caching layers, or
  configuration for hypothetical future requirements
- Every abstraction MUST solve a current, demonstrated problem —
  not a speculated one
- Performance optimization MUST be preceded by profiling or
  measurement that identifies the specific bottleneck
- Prefer straightforward, linear code over indirection; three
  similar lines are better than a premature abstraction
- Do not introduce design patterns (Factory, Strategy, Observer,
  etc.) unless the code already has the problem the pattern solves
- Feature flags, plugin architectures, and extensibility points
  MUST NOT be added until a concrete second use case exists

## Development Standards

- **Accessibility**: All user-facing features MUST meet WCAG 2.1 AA.
  Automated accessibility tests (@axe-core/playwright) MUST pass
  before merge. Static accessibility linting (eslint-plugin-jsx-a11y)
  MUST report zero errors.
- **Layered architecture (backend)**: Views are thin HTTP adapters
  with no business logic. Services contain pure business logic
  functions. Models handle data access only.
- **Contract-first (API)**: Backend exposes an OpenAPI schema via
  drf-spectacular. Frontend TypeScript types are generated from
  that schema. Schema changes MUST be committed alongside the
  code that produces them.
- **Responsive design**: All pages MUST render correctly on mobile
  (375px), tablet (768px), and desktop (1280px+) viewports.

## Quality Gates

Before any feature branch merges to main:

1. **All tests pass**: pytest (backend), Vitest (frontend unit),
   Playwright (E2E, accessibility, responsive)
2. **Linting clean**: ruff (backend), ESLint with jsx-a11y strict
   (frontend) — zero errors
3. **TDD evidence**: Tests demonstrably existed before or alongside
   implementation (commit history SHOULD show test commits preceding
   implementation commits)
4. **No [NEEDS CLARIFICATION] markers**: All spec ambiguities
   resolved before implementation begins
5. **Accessibility audit**: @axe-core/playwright WCAG 2.1 AA scan
   passes on all new or modified pages

## Governance

This constitution supersedes all other development conventions
in the Donation Genie project. When a practice conflicts with
a principle above, the principle wins.

Amendment procedure:

- Any principle change MUST be documented with rationale
- MAJOR version bump for principle removal or redefinition
- MINOR version bump for new principle or section addition
- PATCH version bump for clarifications and wording fixes
- All amendments MUST update the "Last Amended" date below

Compliance:

- All code reviews MUST verify adherence to these principles
- Complexity beyond what these principles allow MUST be justified
  in the plan's Complexity Tracking section
- Violations without justification MUST be resolved before merge

**Version**: 1.0.0 | **Ratified**: 2026-02-26 | **Last Amended**: 2026-02-26
