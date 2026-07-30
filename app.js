const MANIFEST_URL = "data/tools.json";

const labels = {
  "observed-data": "Observed data",
  design: "Design",
  mixed: "Integrated",
  no: "No",
  yes: "Yes",
  "for-design-views": "For design views",
};

function appendListItems(list, values) {
  values.forEach((value) => {
    const item = document.createElement("li");
    item.textContent = value;
    list.append(item);
  });
}

function renderCard(tool, template) {
  const card = template.content.firstElementChild.cloneNode(true);
  card.dataset.conditioning = tool.conditioning;
  card.querySelector("h3").textContent = tool.name;
  card.querySelector(".conditioning-badge").textContent = labels[tool.conditioning];
  card.querySelector(".validation-badge").textContent = tool.validation_status.replaceAll("-", " ");
  card.querySelector(".question").textContent = tool.question;
  card.querySelector(".x-axis").textContent = tool.x_axis;
  appendListItems(card.querySelector(".inputs"), tool.inputs);
  appendListItems(card.querySelector(".outputs"), tool.outputs);
  card.querySelector(".non-goal").textContent = tool.non_goals[0];
  card.querySelector(".limitation").textContent = tool.primary_limitation;
  card.querySelector(".versions").textContent =
    `App ${tool.app_version} · Core ${tool.core_version}`;

  const appLink = card.querySelector(".primary-action");
  appLink.href = tool.hosted_url;
  appLink.setAttribute("aria-label", `Open ${tool.name}`);
  const repositoryLink = card.querySelector(".secondary-action");
  repositoryLink.href = tool.repository_url;
  repositoryLink.setAttribute("aria-label", `View ${tool.name} repository`);
  return card;
}

function renderTableRow(tool) {
  const row = document.createElement("tr");
  const values = [
    tool.name,
    tool.question,
    labels[tool.conditioning],
    tool.x_axis,
    tool.outputs.join("; "),
    labels[tool.requires_assumed_truth],
    labels[tool.requires_selection_rule],
    tool.primary_limitation,
  ];
  values.forEach((value, index) => {
    const cell = document.createElement(index === 0 ? "th" : "td");
    if (index === 0) {
      cell.scope = "row";
    }
    cell.textContent = value;
    row.append(cell);
  });
  return row;
}

function applyFilter(value) {
  const cards = [...document.querySelectorAll(".tool-card")];
  let visible = 0;
  cards.forEach((card) => {
    const show =
      value === "all" ||
      card.dataset.conditioning === value ||
      card.dataset.conditioning === "mixed";
    card.hidden = !show;
    visible += Number(show);
  });
  document.querySelector("#catalog-status").textContent =
    `${visible} ${visible === 1 ? "tool" : "tools"} shown.`;
}

async function initializeCatalog() {
  const status = document.querySelector("#catalog-status");
  try {
    const response = await fetch(MANIFEST_URL, { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`manifest request returned ${response.status}`);
    }
    const manifest = await response.json();
    const cards = document.querySelector("#tool-cards");
    const table = document.querySelector("#comparison-body");
    const template = document.querySelector("#tool-card-template");
    manifest.tools.forEach((tool) => {
      cards.append(renderCard(tool, template));
      table.append(renderTableRow(tool));
    });
    document.querySelector("#catalog-version").textContent =
      `Catalog ${manifest.catalog_version} · ${manifest.portfolio_status.replaceAll("-", " ")}`;
    const coreRepositoryLink = document.querySelector("#core-repository-link");
    coreRepositoryLink.href = manifest.core.repository;
    coreRepositoryLink.removeAttribute("aria-disabled");
    applyFilter("all");
  } catch (error) {
    status.classList.add("error-panel");
    status.textContent =
      `The local tool manifest could not be rendered: ${error.message}. ` +
      "No calculation or user data were involved.";
  }
}

document.querySelectorAll('input[name="conditioning"]').forEach((input) => {
  input.addEventListener("change", (event) => applyFilter(event.target.value));
});

initializeCatalog();
