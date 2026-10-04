# Deployment

## Current state

Pure static. Serve `client/` from any HTTP server.

Status of the handoff steps below, as of 2026-09-03:

| Step | State |
|---|---|
| `render.yaml` blueprint at repo root | in place |
| Render Static Site actually created | **no**, see below |
| AIMS Vercel route `/evaluarium/*` | **pending** |
| Site content committed | yes, as of 2026-09-03 |

**Pushing does not deploy anything today.** The blueprint says Render
auto-deploys on push, but that only applies once someone creates the service
from it, and nobody has. Verified 2026-09-03: `evaluarium.onrender.com` returns
`x-render-routing: no-server`, which is Render's edge saying no service exists
at that hostname. For contrast, `benchmark-caliper.onrender.com` returns
`suspend-by-user`, a service that exists and is paused. Both
`evaluarium.onrender.com` and `aimslab.stanford.edu/evaluarium/` 404.

**But the repo is public.** `aims-foundations/evarium` has
`"visibility": "public"`, so everything pushed is world-readable on GitHub
immediately, whether or not it is ever deployed. Deploying is a separate,
deliberate act; publishing the source is not.

**What was missing until 2026-09-03.** Only seven files under `client/` were
tracked; `explorer.html`, `simulation.html`, `js/ecosystem_data_v2.js`,
`js/sim_data.js` and `js/vendor/d3.v7.min.js` had never been committed. A
deploy in that state would have served an `index.html` whose data file 404s,
so the map would not have rendered at all, plus two 404 pages and two chart
pages with no d3. All five are committed now, so a clone is self-sufficient:
anyone with access can serve `website/client/` and get the whole site. Still
worth running `git status --porcelain website/client` before relying on an
auto-deploy, since Render publishes the default branch, not your working tree.

## Target: `aimslab.stanford.edu/evaluarium/`

Mirrors `aims-foundations/benchmark-caliper`, with one difference:
caliper uses a Render **Web Service** (Docker, paid) because it has
a FastAPI backend. Evaluarium uses a Render **Static Site** (free)
because it has no backend yet.

The handoff to AIMS infrastructure is:

1. Someone with Render access creates a Static Site from the repo-root
   [`render.yaml`](../render.yaml), which publishes `website/client/`.
   This step has not happened yet and is what the table above records.
   Once the service exists, Render auto-deploys on push to the default
   branch, at `https://evaluarium.onrender.com`.
2. AIMS adds a Vercel proxy route
   `/evaluarium/*  ->  https://evaluarium.onrender.com`,
   matching the existing `/benchmark-caliper/*` route.

That's the whole deployment. No Docker, no persistent disk, no env
vars, no monthly cost. Both steps need someone with the respective
access; neither happens as a side effect of a push.

Nothing in the client is built, so a collaborator does not need this
repo's Python environment, the simulation, or any toolchain. Cloning
and serving `website/client/` over plain HTTP is sufficient, and the
site works under any mount point (see Subpath safety below).

## Subpath safety

All URLs in the HTML are relative; the site works under any mount
point. The only thing that needs to change if the data origin moves
(e.g., to a CDN or HF) is `Evaluarium.config` in `client/js/loader.js`.

## Naming

The git remote is `aims-foundations/evarium`; the deploy path, Render service
and `render.yaml` all say `evaluarium`; the JS namespace is `Evaluarium`. This
mismatch is known and deliberate for now. The repo rename is owned elsewhere,
and the established deploy paths are being left alone, so do not "fix" the
spelling in `render.yaml`, `loader.js` or the Vercel route. Nothing a visitor
sees carries any of these names.

## Caching

`index.html` versions its data file as `js/ecosystem_data_v2.js?v=N`. Bump
that `N` whenever the data file changes, or returning visitors keep the old
figure from cache. The HTML files themselves are unversioned, so changes to
markup, CSS or inline script depend on the host's cache headers and may need
a hard reload to appear. Worth confirming Render's defaults for `.html`
before announcing a URL.

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
