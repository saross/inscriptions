**BLOCKING**

### 1. Internal contradiction: H3c is cross-sectional and cannot be mixture-corrected

*   **Pointer:** §2 Description ("Scope of the mixture correction"); §3 "Bayesian NBR for H3a" (Response variable); Plain-English Walkthrough Step 6; §9 Known limitations.
*   **Problem:** The text repeatedly asserts that the Bayesian mixture model corrects "the H3c residual analysis where it uses the H3a posterior". However, Decision 22 correctly established that H3a runs on *raw, uncorrected* date-window-filtered counts because a cross-sectional per-city mixture fit is unidentified at low N. Because H3c calculates spatial Pearson residuals directly from the H3a posterior (`y_c - mu_c,s`), H3c is completely cross-sectional and mathematically inherits the *uncorrected* nature of H3a.
*   **Why it matters:** (Rubric 2: Logical gap opened by Decision 22). This is a direct internal contradiction. You cannot have an uncorrected base regression (H3a) yield a mathematically corrected spatial residual (H3c) just by declaring it so. Reviewers will immediately catch this ghost left over from the rewrite. 
*   **Suggested fix:** Sever H3c from all lists of "mixture-corrected" analyses. In §2, §3, Step 6, and §9, explicitly group H3c with H3a as an uncorrected, cross-sectional spatial analysis protected *only* by the date-window filter. For example, in §2: "The Bayesian deconvolution-mixture model corrects the temporal analyses (H2.1 validation; H3b deviation-detection). It is *not* applied to the cross-sectional H3a regression or its derivative H3c residual analysis."

---

**SHOULD-FIX**

### 2. "Year-0" terminology at the BC → AD transition

*   **Pointer:** §2 Description; §9 Known limitations ("BC → AD year-0 step").
*   **Problem:** The text repeatedly refers to a "+1,159 step at the year-0 boundary". There is no "Year 0" in the Julian or Gregorian calendars (1 BC is followed directly by AD 1), unless the project is explicitly using astronomical year numbering (where Year 0 = 1 BC), which is not stated.
*   **Why it matters:** (Rubric 3: Stale-anchoring drift / Explanatory text). While mathematically it represents the zero-crossing in your code/arrays, historians and epigraphers will reflexively flag the phrase "year 0" as a basic chronological error, which undermines the paper's credibility right as it attempts to diagnose chronological artefacts.
*   **Suggested fix:** Replace references to the "year-0 boundary" with "the 1 BC / AD 1 boundary" or "the BC → AD transition". Keep the specific step magnitude (+1,159) exactly as is.

---

### Overall assessment

**Real work remaining (but very minor).** The document has saturated remarkably well. The three rounds of adversarial review and the resulting methodology pivots (forward-fitting, the Bayesian mixture respecification, the slab-dictionary artefact reframing) have produced an exceptionally tight preregistration. The only thing preventing immediate lodgement is the BLOCKING logical contradiction regarding H3c, which is just a cleanup oversight from Decision 22 (the author realized H3a couldn't be mixture-corrected, but forgot to pull its derivative, H3c, out of the "corrected" bucket in the explanatory text). 

Fix that single contradiction, adjust the "year 0" phrasing for the historian audience, and **this document will be fully saturated and ready to lodge**, subject to Martin's statistician consultation. No further adversarial revision cycles are necessary.