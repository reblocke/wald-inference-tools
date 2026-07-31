#!/usr/bin/env node

import { createHash } from "node:crypto";
import { readdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { basename, join, relative, resolve, sep } from "node:path";

function parseArgs(argv) {
  const values = {};
  for (let index = 0; index < argv.length; index += 2) {
    const key = argv[index];
    const value = argv[index + 1];
    if (!key?.startsWith("--") || value === undefined) {
      throw new Error(
        "usage: build_evidence_index.mjs --root <dir> --catalog-version <X.Y.Z> --validated-at <RFC3339>",
      );
    }
    values[key.slice(2)] = value;
  }
  for (const key of ["root", "catalog-version", "validated-at"]) {
    if (!values[key]) {
      throw new Error(`--${key} is required`);
    }
  }
  return values;
}

function walk(root, directory = root) {
  const paths = [];
  for (const name of readdirSync(directory).sort()) {
    const path = join(directory, name);
    if (statSync(path).isDirectory()) {
      paths.push(...walk(root, path));
    } else if (resolve(path) !== resolve(join(root, "index.json"))) {
      paths.push(path);
    }
  }
  return paths;
}

const EVIDENCE_KINDS = new Map([
  ["browser/browser-summary.json", "browser-result"],
  [
    "browser/corrected-live-browser-results.json",
    "lane-e-browser-privacy-accessibility",
  ],
  [
    "browser/corrected-mobile-containment.json",
    "lane-e-browser-privacy-accessibility",
  ],
  [
    "browser/corrected-required-error-recovery.json",
    "lane-e-browser-privacy-accessibility",
  ],
  ["commands/README_COMMANDS.md", "command-ledger"],
  ["drivers/audit_focused_diffs.py", "audit-driver"],
  ["drivers/audit_integrated_diff.py", "audit-driver"],
  ["drivers/audit_precision_app_repairs.py", "audit-driver"],
  ["drivers/build_evidence_index.mjs", "audit-driver"],
  ["drivers/collect_release_inventory.mjs", "audit-driver"],
  ["drivers/focused_error_links_audit.py", "audit-driver"],
  ["drivers/live_browser_audit.py", "audit-driver"],
  ["drivers/mobile_containment_audit.py", "audit-driver"],
  ["drivers/required_error_recovery_audit.py", "audit-driver"],
  ["inventory/release-inventory.json", "release-inventory"],
  ["lanes/all-ticket-acceptance-final.md", "lane-f-docs-rights"],
  ["lanes/catalog-template-v0.1.1-cdef.md", "lane-c-cold-start"],
  ["lanes/compatibility-v0.1.2-cdef.md", "lane-c-cold-start"],
  ["lanes/core-likelihood-final-ab.md", "lane-b-parity"],
  ["lanes/corrected-release-set-lane-ab.md", "lane-b-parity"],
  ["lanes/corrected-release-set-lane-cd.md", "lane-d-provenance"],
  ["lanes/critical-v0.1.2-cdef.md", "lane-c-cold-start"],
  [
    "lanes/focused-docs-only-final-release-supplement.md",
    "lane-f-docs-rights",
  ],
  ["lanes/final-release-set-v0.4.2-lane-ab.md", "lane-b-parity"],
  ["lanes/final-release-set-v0.4.2-lane-cd.md", "lane-d-provenance"],
  [
    "lanes/final-release-set-v0.4.2-lane-ef.md",
    "lane-e-browser-privacy-accessibility",
  ],
  ["lanes/integrated-v0.2.2-blocker-audit.md", "lane-f-docs-rights"],
  ["lanes/integrated-v0.2.5-cdef.md", "lane-c-cold-start"],
  ["lanes/likelihood-v0.1.2-cdef.md", "lane-c-cold-start"],
  ["lanes/original-release-set-lane-ab.md", "lane-a-numerical"],
  ["lanes/original-release-set-lane-cd.md", "lane-d-provenance"],
  [
    "lanes/original-release-set-lane-ef.md",
    "lane-e-browser-privacy-accessibility",
  ],
  ["lanes/type-s-m-v0.1.2-cdef.md", "lane-c-cold-start"],
  ["results/core-likelihood-final-ab.json", "lane-b-parity"],
  ["results/core-precision-boundary-audit.txt", "lane-a-numerical"],
  ["results/core-v0.4.1-baseline-parity.json", "lane-a-numerical"],
  ["results/core-v0.4.2-baseline-parity.json", "lane-a-numerical"],
  [
    "results/core-v0.4.2-independent-recomputation.json",
    "lane-a-numerical",
  ],
  [
    "results/final-release-set-v0.4.2-cold-start.json",
    "lane-c-cold-start",
  ],
  [
    "results/focused-docs-only-final-release-supplement.json",
    "lane-f-docs-rights",
  ],
]);

function evidenceKind(path) {
  const kind = EVIDENCE_KINDS.get(path);
  if (kind === undefined) {
    throw new Error(`no explicit evidence kind mapping for ${path}`);
  }
  return kind;
}

function description(path) {
  const label = basename(path)
    .replace(/\.[^.]+$/, "")
    .replaceAll("-", " ")
    .replaceAll("_", " ");
  return `Preserved CC-MIG-11 evidence: ${label}.`;
}

const args = parseArgs(process.argv.slice(2));
const root = resolve(args.root);
const files = walk(root).map((path) => {
  const relativePath = relative(root, path).split(sep).join("/");
  const bytes = readFileSync(path);
  if (bytes.length === 0) {
    throw new Error(`empty evidence file: ${relativePath}`);
  }
  return {
    path: relativePath,
    sha256: createHash("sha256").update(bytes).digest("hex"),
    kind: evidenceKind(relativePath),
    description: description(relativePath),
  };
});
files.sort((left, right) => left.path.localeCompare(right.path));
const index = {
  schema_version: 1,
  catalog_version: args["catalog-version"],
  validated_at: args["validated-at"],
  files,
};
writeFileSync(join(root, "index.json"), `${JSON.stringify(index, null, 2)}\n`, {
  encoding: "utf8",
});
