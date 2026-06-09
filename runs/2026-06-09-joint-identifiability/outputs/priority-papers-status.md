# Priority papers — dedup, metadata, and verified claims (2026-06-09)

Status of the 6 priority papers from the scout synthesis
(`planning/scout-2026-06-09-identifiability-remediation-SYNTHESIS.md`), checked for
the joint-model pivot discussion. **Dedup was the step the scouts could not confirm**
(missing `httpx`); it is now confirmed directly against `~/Zotero/zotero.sqlite`
(read-only). Metadata fetched via the shared `lit-search.py` (`uv run --with httpx`).

## Dedup + metadata

| paper | DOI | in Zotero? | PDF? | key claim (verified source) |
|---|---|---|---|---|
| **Huang & Bandeen-Roche 2004** | 10.1007/bf02295837 | **NEW** | — | "Building an **Identifiable** Latent Class Model with **Covariate Effects**…**Theory for model identification is developed**" (CrossRef abstract) — the identification theorem licensing the joint model |
| **Gustafson 2010** | 10.2202/1557-4679.1206 | **NEW** | — | "the **identification region**…is strictly contained in the a-priori-plausible set but strictly contains the true value… the large-sample posterior will have the **identification region as its support**" — why a *prior* can't fix partial-ID; you must add data to *shrink the region* |
| **Feller et al. 2016** | 10.48550/arxiv.1602.06595 | **NEW** | — | "in finite samples the MLE behaves like a **threshold estimator**…can give strong evidence that the means are equal when the truth is otherwise" — the "confidently wrong" mechanism (= POC Exp 1) |
| Bronk Ramsey 2009 (OxCal outliers) | 10.1017/s0033822200034093 | in library | none | two-component reliable/unreliable outlier mixture — the structural archetype |
| Bayliss 2015 | 10.1080/00438243.2015.1067640 | in library | none | quality classification as a prerequisite for chronological inference |
| Verhagen et al. 2016 | 10.1016/j.jasrep.2016.10.006 | in library | none | Roman-period dating-quality classification + per-class aoristic |

Feller's preferred citation DOI may be the *Ann. Appl. Stat.* 2019 journal version (the
SYNTHESIS flag); the arXiv DataCite DOI is what is verified here. Authors confirmed:
Feller, Greif, Ho, Miratrix, Pillai.

## What the trio establishes for the pivot (grounded in authoritative abstracts)

The three statistical papers, read together, give the pivot a clean theoretical spine:

1. **Feller** — when convention and genuine both live in AD 100–300 (weak separation),
   the temporal-mixture likelihood is not merely flat in α but *confidently wrong*. With
   the **shared** basis, α>0 additionally forces a shape misfit, deepening the wrong
   confidence — POC Exp 1's α≈0.
2. **Gustafson** — α is *partially identified*: the posterior's support is the
   identification region, so no prior over that region (the refuted informed-α prior)
   moves it. The fix must **shrink the identification region** by adding an independent
   observable.
3. **Huang & Bandeen-Roche** — adding a **covariate effect on latent-class membership**
   (our grid-alignment classification → α) **restores identifiability**. The per-unit
   basis first removes the shape-misfit (so the problem is genuinely partial-ID, not
   confidently-wrong), and the classification likelihood then shrinks the region to ~a
   point — POC Exp 2/3's recovery.

## Outstanding (tracked follow-ups)

- **Full-text reading.** Abstracts verified the load-bearing claims; full text would
  add: Feller's specific weak-separation **diagnostics** (could sharpen our
  identifiability flag) and Huang & Bandeen-Roche's **identification lemmas** (for the
  amendment justification). Gustafson + H&BR are paywalled (try Scholar Gateway /
  Unpaywall); Feller is open (arXiv). Bronk Ramsey / Verhagen open-ish.
- **Zotero staging.** The 3 NEW papers should be imported into the staging collection
  via the canonical path (a minimal `/lit-scout-iterate` workspace → `lit-scout-zotero-
  import.py --live`), NOT a bespoke script (project CLAUDE.md). PDF-attach needs the
  shared importer extended on a branch (known gap). Deferred to a clean follow-up.
- **Tooling blocker.** `lit-search.py` / the importer fail under system `python3`
  (`ModuleNotFoundError: httpx`) — the documented "personal-assistant venv" is not the
  interpreter being used. Workaround that works: `uv run --with httpx python …`. Durable
  fix: install `httpx` into the pa venv or invoke the tool with that venv's python.
