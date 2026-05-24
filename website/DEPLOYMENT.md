# Deployment

## Current state

Pure static. Serve `client/` from any HTTP server.

## Target: `aimslab.stanford.edu/evaluarium/`

Mirrors `aims-foundations/benchmark-caliper`, with one difference:
caliper uses a Render **Web Service** (Docker, paid) because it has
a FastAPI backend. Evaluarium uses a Render **Static Site** (free)
because it has no backend yet.

The handoff to AIMS infrastructure is:

1. The repo-root [`render.yaml`](../render.yaml) declares a Render
   Static Site that publishes `website/client/`. Render auto-deploys
   on push to the default branch; the resulting URL is
   `https://evaluarium.onrender.com`.
2. AIMS adds a Vercel proxy route
   `/evaluarium/*  ->  https://evaluarium.onrender.com`,
   matching the existing `/benchmark-caliper/*` route.

That's the whole deployment. No Docker, no persistent disk, no env
vars, no monthly cost.

## Subpath safety

All URLs in the HTML are relative; the site works under any mount
point. The only thing that needs to change if the data origin moves
(e.g., to a CDN or HF) is `Evaluarium.config` in `client/js/loader.js`.

## When the backend arrives (T3)

For BYOK LLM mode the architecture grows to:

- A backend under `website/server/` (likely FastAPI, matching the
  `benchmark-caliper` template)
- The repo-root `render.yaml` flips from `runtime: static` to a
  Docker Web Service, gaining build/start commands and any env vars
  the backend needs
- The AIMS Vercel proxy route is unchanged &mdash; the origin URL
  stays the same, just now points at a server instead of a static
  bucket

Migration at that point is a `render.yaml` edit plus backend code,
not a rewrite of the existing client or a change to how AIMS routes.
