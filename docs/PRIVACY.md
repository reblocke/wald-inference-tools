# Privacy

The catalog is a static navigation site. It has no form fields, statistical calculation, Pyodide,
telemetry, analytics, cookies, local storage, session storage, saved state, or service worker.

On initial load, the browser requests only checked-in catalog assets from the same origin:
`index.html`, `styles.css`, `app.js`, and `data/tools.json`. It does not contact app repositories,
GitHub APIs, or other third parties. Public release checks run only when a maintainer explicitly
invokes `make live-check`; they are development/CI checks, not browser behavior.

App and repository links are plain input-free URLs. Following one is an ordinary user-initiated
navigation. No entered values exist to encode in a URL or send to another tool.

The linked apps have their own privacy documentation and should be reviewed independently. This
catalog is educational software and is not clinical decision support.
