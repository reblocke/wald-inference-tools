#!/usr/bin/env node

import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { writeFileSync } from "node:fs";

const RELEASES = [
  {
    name: "reblocke/wald-inference-core",
    tag: "v0.4.1",
    liveUrl: null,
  },
  {
    name: "reblocke/scientific-applet-template",
    tag: "v0.1.1",
    liveUrl:
      "https://reblocke.github.io/scientific-applet-template/assets/py/manifest.json",
  },
  {
    name: "reblocke/compatibility-curve",
    tag: "v0.1.3",
    liveUrl: "https://reblocke.github.io/compatibility-curve/assets/py/manifest.json",
  },
  {
    name: "reblocke/wald-likelihood-support",
    tag: "v0.1.2",
    liveUrl:
      "https://reblocke.github.io/wald-likelihood-support/assets/py/manifest.json",
  },
  {
    name: "reblocke/critical-effect-size",
    tag: "v0.1.3",
    liveUrl: "https://reblocke.github.io/critical-effect-size/assets/py/manifest.json",
  },
  {
    name: "reblocke/type-s-m-calibrator",
    tag: "v0.1.3",
    liveUrl: "https://reblocke.github.io/type-s-m-calibrator/assets/py/manifest.json",
  },
  {
    name: "reblocke/precision-guardrail-planner",
    tag: "v0.1.2",
    liveUrl:
      "https://reblocke.github.io/precision-guardrail-planner/assets/py/manifest.json",
  },
  {
    name: "reblocke/wald-inference-tools",
    tag: "v0.1.1",
    liveUrl: "https://reblocke.github.io/wald-inference-tools/data/tools.json",
  },
  {
    name: "reblocke/conf_curve_likelihood",
    tag: "v0.2.5",
    liveUrl:
      "https://reblocke.github.io/conf_curve_likelihood/assets/py/manifest.json",
  },
];

function parseArgs(argv) {
  const values = {};
  for (let index = 0; index < argv.length; index += 2) {
    const key = argv[index];
    const value = argv[index + 1];
    if (!key?.startsWith("--") || value === undefined) {
      throw new Error(
        "usage: collect_release_inventory.mjs --validated-at <RFC3339> --output <path>",
      );
    }
    values[key.slice(2)] = value;
  }
  if (!values["validated-at"] || !values.output) {
    throw new Error("--validated-at and --output are required");
  }
  return values;
}

function ghJson(args) {
  const output = execFileSync("gh", args, {
    encoding: "utf8",
    maxBuffer: 32 * 1024 * 1024,
  });
  return JSON.parse(output);
}

function selectRun(runs, predicate) {
  const matches = runs.filter(predicate);
  if (matches.length !== 1) {
    throw new Error(`expected exactly one workflow run, observed ${matches.length}`);
  }
  return matches[0];
}

const fetchedArtifacts = new Map();

async function fetchBytes(url) {
  const response = await fetch(url, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`${url} returned HTTP ${response.status}`);
  }
  return Buffer.from(await response.arrayBuffer());
}

function sha256(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

function stagedRecordDigest(records) {
  const digest = createHash("sha256");
  for (const record of [...records].sort((left, right) =>
    left.path.localeCompare(right.path),
  )) {
    digest.update(`${record.path}\0${record.sha256}\0${record.bytes}\n`);
  }
  return digest.digest("hex");
}

async function verifyStagedManifest(manifest, manifestUrl) {
  if (
    !Array.isArray(manifest.packages) ||
    manifest.packages.length === 0 ||
    typeof manifest.bundle_sha256 !== "string"
  ) {
    throw new Error(`${manifestUrl} is not a staged-package manifest`);
  }
  const allRecords = [];
  for (const packageRecord of manifest.packages) {
    if (!Array.isArray(packageRecord.files) || packageRecord.files.length === 0) {
      throw new Error(`${manifestUrl} contains an empty staged package`);
    }
    const observedPaths = packageRecord.files.map((record) => record.path);
    const expectedPaths = [...observedPaths].sort();
    if (
      new Set(observedPaths).size !== observedPaths.length ||
      JSON.stringify(observedPaths) !== JSON.stringify(expectedPaths)
    ) {
      throw new Error(`${manifestUrl} package files are not unique and ordered`);
    }
    for (const fileRecord of packageRecord.files) {
      const fileUrl = new URL(fileRecord.path, manifestUrl).href;
      const bytes = await fetchBytes(fileUrl);
      if (bytes.length !== fileRecord.bytes || sha256(bytes) !== fileRecord.sha256) {
        throw new Error(`${fileUrl} differs from its staged manifest record`);
      }
      allRecords.push(fileRecord);
    }
    if (
      "package_sha256" in packageRecord &&
      packageRecord.package_sha256 !== stagedRecordDigest(packageRecord.files)
    ) {
      throw new Error(
        `${manifestUrl} package ${packageRecord.distribution} digest is inconsistent`,
      );
    }
    if (packageRecord.artifact_url !== null && packageRecord.artifact_url !== undefined) {
      const artifactUrl = packageRecord.artifact_url;
      let artifactBytes = fetchedArtifacts.get(artifactUrl);
      if (artifactBytes === undefined) {
        artifactBytes = await fetchBytes(artifactUrl);
        fetchedArtifacts.set(artifactUrl, artifactBytes);
      }
      if (sha256(artifactBytes) !== packageRecord.artifact_sha256) {
        throw new Error(`${artifactUrl} differs from the manifest artifact digest`);
      }
    }
  }
  if (stagedRecordDigest(allRecords) !== manifest.bundle_sha256) {
    throw new Error(`${manifestUrl} bundle digest is inconsistent`);
  }
}

async function collect(entry) {
  const repository = ghJson([
    "repo",
    "view",
    entry.name,
    "--json",
    "nameWithOwner,url,visibility,isTemplate,licenseInfo,defaultBranchRef",
  ]);
  const ref = ghJson(["api", `repos/${entry.name}/git/ref/tags/${entry.tag}`]);
  if (ref.object.type !== "tag") {
    throw new Error(`${entry.name}@${entry.tag} is not an annotated tag`);
  }
  const tagObject = ghJson([
    "api",
    `repos/${entry.name}/git/tags/${ref.object.sha}`,
  ]);
  if (
    tagObject.tag !== entry.tag ||
    tagObject.object.type !== "commit" ||
    typeof tagObject.object.sha !== "string"
  ) {
    throw new Error(`${entry.name}@${entry.tag} tag object does not target a commit`);
  }
  const commit = tagObject.object.sha;
  const release = ghJson([
    "release",
    "view",
    entry.tag,
    "--repo",
    entry.name,
    "--json",
    "tagName,isPrerelease,isDraft,publishedAt,url,assets,name,targetCommitish",
  ]);
  const runs = ghJson([
    "run",
    "list",
    "--repo",
    entry.name,
    "--limit",
    "100",
    "--json",
    "databaseId,workflowName,status,conclusion,headSha,headBranch,event,url,createdAt,updatedAt",
  ]);
  const releaseRun = selectRun(
    runs,
    (run) =>
      run.workflowName === "Release" &&
      run.headBranch === entry.tag &&
      run.headSha === commit,
  );
  if (releaseRun.status !== "completed" || releaseRun.conclusion !== "success") {
    throw new Error(`${entry.name}@${entry.tag} release workflow is not successful`);
  }

  const ciRuns = runs.filter(
    (run) =>
      run.workflowName === "CI" &&
      run.headSha === commit &&
      run.status === "completed" &&
      run.conclusion === "success",
  );
  let pages = null;
  let live = null;
  if (entry.liveUrl !== null) {
    const deployments = ghJson([
      "api",
      `repos/${entry.name}/deployments?environment=github-pages&per_page=100`,
    ]);
    const deployment = deployments.find((candidate) => candidate.sha === commit);
    if (!deployment) {
      throw new Error(`${entry.name}@${entry.tag} has no matching Pages deployment`);
    }
    const statuses = ghJson([
      "api",
      `repos/${entry.name}/deployments/${deployment.id}/statuses`,
    ]);
    const deploymentStatus = statuses[0];
    if (deploymentStatus?.state !== "success") {
      throw new Error(`${entry.name}@${entry.tag} Pages deployment is not successful`);
    }
    const pagesRuns = runs.filter(
      (run) =>
        run.workflowName === "Deploy Pages" &&
        run.headSha === commit &&
        run.status === "completed" &&
        run.conclusion === "success",
    );
    pages = {
      deployment_id: deployment.id,
      sha: deployment.sha,
      created_at: deployment.created_at,
      status: deploymentStatus.state,
      environment_url: deploymentStatus.environment_url,
      workflow_runs: pagesRuns,
    };

    const bytes = await fetchBytes(entry.liveUrl);
    const parsed = JSON.parse(bytes.toString("utf8"));
    if ("source_commit" in parsed && parsed.source_commit !== commit) {
      throw new Error(`${entry.liveUrl} does not name the released commit`);
    }
    const hasPackages = Array.isArray(parsed.packages);
    if (hasPackages) {
      await verifyStagedManifest(parsed, entry.liveUrl);
    }
    live = {
      url: entry.liveUrl,
      sha256: sha256(bytes),
      source_commit: parsed.source_commit ?? null,
      catalog_version: parsed.catalog_version ?? null,
      bundle_sha256: parsed.bundle_sha256 ?? null,
      packages: parsed.packages ?? null,
      staged_files_verified: hasPackages ? true : null,
    };
  }

  return {
    name: entry.name,
    repository_url: repository.url,
    visibility: repository.visibility,
    default_branch: repository.defaultBranchRef.name,
    is_template: repository.isTemplate,
    license: repository.licenseInfo?.key ?? null,
    release: entry.tag,
    tag_object: ref.object.sha,
    peeled_commit: commit,
    tag_ref: {
      name: entry.tag,
      type: ref.object.type,
      sha: ref.object.sha,
    },
    tag_target: {
      type: tagObject.object.type,
      sha: tagObject.object.sha,
    },
    tagger: tagObject.tagger,
    release_record: {
      tag_name: release.tagName,
      url: release.url,
      name: release.name,
      published_at: release.publishedAt,
      is_draft: release.isDraft,
      is_prerelease: release.isPrerelease,
      assets: release.assets.map((asset) => ({
        name: asset.name,
        size: asset.size,
        digest: asset.digest,
        url: asset.url,
      })),
    },
    release_workflow: releaseRun,
    successful_ci_runs: ciRuns,
    pages,
    live,
  };
}

const args = parseArgs(process.argv.slice(2));
const repositories = [];
for (const entry of RELEASES) {
  repositories.push(await collect(entry));
}
const inventory = {
  schema_version: 1,
  audited_at: args["validated-at"],
  catalog_evidence_carrier: {
    release: "v0.2.0",
    note:
      "The audited catalog predecessor is v0.1.1; v0.2.0 carries this inventory and is verified after publication without circularly establishing the verdict.",
  },
  repositories,
};
writeFileSync(args.output, `${JSON.stringify(inventory, null, 2)}\n`, {
  encoding: "utf8",
});
