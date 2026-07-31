# Security Policy

## Supported versions

Security fixes are applied to the latest release and the current `main` branch. Older tags,
validation records, and release assets remain reproducibility records and are not silently
rewritten.

## Report a vulnerability privately

Use GitHub's **Report a vulnerability** control in this repository's Security tab:

<https://github.com/reblocke/wald-inference-tools/security/advisories/new>

Do not disclose vulnerability details in a public issue, pull request, discussion, commit, or
workflow log. If the private-reporting control is unavailable, use the repository's **Private
security coordination request** issue form. That public form records only that the control is
unavailable; do not identify the vulnerability class, affected component, reproduction, or impact
in that issue.

Include privately:

- the exact tag or full commit SHA;
- the affected manifest, validator, evidence gate, static site, workflow, Pages, or release path;
- a minimal reproduction using public metadata or synthetic examples;
- expected and observed behavior;
- environment and browser versions when relevant; and
- any suspected exposure of credentials or release-integrity material.

Never send protected health information, patient-level data, credentials, unpublished restricted
data, or other sensitive material. Redact local paths and logs. The catalog accepts no user input;
a reproducer should use the smallest safe public or synthetic artifact needed to demonstrate the
issue.

## Scope distinctions

- A vulnerability or privacy defect belongs in private vulnerability reporting.
- A catalog rendering, manifest-schema, live-metadata, evidence-gate, or release-integrity defect
  belongs in this repository.
- A numerical defect belongs in
  [`wald-inference-core`](https://github.com/reblocke/wald-inference-core).
- An app-specific orchestration or presentation defect belongs in that app's repository.
- A routine, nonsensitive repository bug may use the public engineering issue form.
- Requests for clinical interpretation are out of scope. Catalog publication and validation
  metadata do not establish clinical decision support or regulatory readiness.

Publishing a fixed release does not authorize moving an old tag, replacing an old asset, or
rewriting validation evidence. Preserve the affected record, publish a new version, and describe
the affected range.
