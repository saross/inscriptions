---
title: "Adela's feedback on the RAC-TRAC deck — and Shawn's response"
date: 2026-05-22
audience: "Shawn + Claude (next-session) — primary source for the deck revision pass"
purpose: "Capture Adela's per-slide feedback verbatim, plus Shawn's reply outlining the revised narrative. Anchor for the per-slide revision plan."
provenance: "Email thread, 2026-05-22; pasted by Shawn into the CC session."
---

# Adela's feedback (verbatim)

> Hi Shawn,
>
> Thank you for the slides and notes, this is very technical with tons abbreviations so I will try to do my best to unpack these so people don't fall asleep.
>
> Here are my questions for each slide
>
> What is the contribution here, what [historical, historiographical, archaeological] problem are we solving with all these graphs and numbers, what implications it has on epigraphic studies beyond 'better understanding of our data'
>
> 2 — editorial distortion — you lost me here — what do you mean by editorial distortion (fuzzy chrono categories, selection of samples, ??) Context needed.
>
> 3 — so the meaning of the slide is that for analysis of a subset one needs to have at least 1549 inscriptions? And for empire-wide analysis (ie. Both space and temporal extent of 400 years) at least 50,000? I don't quite understand the y axis 'bracket' labels, are these 25 and 50-year bins? What are the 20-50pc? What are 96 reachable analysis cells?
>
> 4 — ok, so this is a shape of the epigraphic production per city vs province when mapped with SPA. What does it tell us except that each place is a tad different, peaks meaning good signal/economy vs troughs meaning ...?
>
> 5 — I am lost! perhaps the most unclear slide: mysterious templates intervals again; what is alpha and the posterior on alpha. This slides needs a narrative.
>
> 6 — the trend is rising, nonetheless, indicating that the number of inscription tracks even if at a slower rate. On what grounds should be expect a function of 1 or more here given preservation biases, pressure for space (are graffiti included, e.g.). , etc. What can we relate this ratio to? — greater inequality gap between large and small cities? Why is Hanson's number higher — is he including Rome? What does it actually mean on the ground for the Roman Empire, if anything?
>
> 6b you actually need to do this over a multi-scale comparison os u-c spatial cluster to do this properly to control for the cardinal sin of ecological fallacy or MAUP. Where does the 30:70% ratio come from? I do not see it in the graphs at all
>
> What is the benefit of Bayesian Mundlak? This study is literally a 'throw all methods at the inscriptions', in need of strong rationale especially at the ECR event such as TRAC. I am not sure I can do a good presentation without stronger disciplinary/research grounding for each slide.
>
> How do your results inform my study that has ca 200 samples for each 50-year bin and a total of 800 wife and 500 daughter 'filtered / LIRE' records with date-time (that's the ceiling).
>
> B10 I need to look again at the Hanson 2021 paper. Moran's I of less that 0.3 or -0.3 is considered "random spatial structure", even if p is <0.05. Did you run a MC over the Moran? Sometimes it helps, as Moran is not super-robust, but I would not bother for this paper.
>
> Best,
> Adela

# Shawn's response (verbatim, sent back to Adela)

> Thanks, I'll work on explaining all these things today. I planned on spending more time on making implications clearer.
>
> The main narrative is:
>
> - In radiocarbon, SPAs are used to study demographics — there is some controversy around that, which I respect, but let's set that aside for the moment an see if we can borrow the technique
> - When I've made this argument to Classicists before, they've essentially said 'inscriptions and inscription counts only reflect epigraphic habit, not 'real' phenomena re: demographics, etc.) — I got that message very strongly at ANU, for example, essentially that I was wasting my time
> - When I spoke with Petra about it, she was more sympathetic but indicated it would be a significant contribution even if I could find a weak relationship between inscription count / SPA and population — that if underlying population drove even 10% of count, that would be important.
> - The goal of this paper is to determine, one way or the other, whether there is any relationship between population and inscriptions — is the radiocarbon parallel valid *at all* justifying any further exploration of this technique.
> - To even begin doing that, we've first got to 'fix' the date ranges on the inscriptions because '2th century' doesn't *really* mean that the inscription has equal chance of being in any year from 100–199 (and just changing the distribution to e.g., trapezoidal doesn't fix this), instead epigraphers call something 'Nth century' or 'mid-Flavian' or 'second quarter of the 3rd century' out of *convention* as a way of expressing rough dates. This is a demonstrable feature of the dataset, where there are big 'slabs' corresponding to century (and to a lesser extent, half-century and quarter-century) and 'spikes' at the midpoints of dynasties. Crema deals with analogous problems in ceramics, etc., with Bayesian treatment of interval-dated archaeological data, and we've borrowed that. In my 2024 work I just discarded long date-ranges, but the median date range is >100 years so you lose a lot of data that way, making it even harder to work on provinces / urban areas that have relatively few inscriptions to start with. The idea here is to not merely discard that data but have it contribute to a bayesian model of inscription counts / SPA. I'm curious if the more statistically minded attendees buy this.
> - Once we have a corrected SPA, we can compare it to Hanson's population estimates
> - We do that, but first we look at the patterns within and between provinces, since comparisons of two towns in Italia vs. one town in Italia and one in Britannia contain different signals (within-province has fewer confounds of any population-inscription relationship, e.g., administrative history, cultural habits, social organisation, etc.). This within-between decomposition is borrowed from Mundlak, a foundational text on time-series and cross-sectional data from the 1970s. This attempts to have us comparing apples with apples when we compare population-versus-SPA.
> - After we do that, when we compare population-versus-SPA, we find about a 0.3 correlation (uncorrected). If we tier cities by size (possibly another confound) that can go as high as 0.5. If this result holds up to scrutany, we're refuted the argument that inscription counts only reflect cultural habits, and can say that population explains 30–50% of variation.
> - I eventually hope to extend this approach to isolating other factors, e.g., population, economics (wealth), social (competition), cultural (epigraphic habit), etc. as per traditional social complexity studies, with the goal of being able to use inscription counts as a proxy for social complexity in an informed way.
> - SPA over snapshot counts adds a temporal dimension that lets you study change over time.
>
> That's the basic story.
>
> As for minimum counts, the high counts you mention (1.5k for an urban area) are required if you want to detect a *signal of a particular size*, in this case, a 50% change in the 'real' number of inscriptions produced over a 50-year period (given the characteristics of the LIRE dataset, e.g., that the average inscription has a date range spanning >100 years). This provides an indication of sensitivity of the SPA to fluctuations in the inscription count over time. It's conservative; shorter, sharper changes are easier to detect, longer, shallower changes are harder, and 50%-over-50y is fairly long and moderately shallow. This shows that we can detect changes on the scale likely caused by something like the crisis of the third century. Calculating this via simulation conveys more information than just doing bootstrap CIs on SPA: the latter tell you the sampling uncertainty in the count in any given year, but we're actually using synthetic data to see (a) if the SPA is different from what we'd expect in a 'smooth null' (like rcarbon's modelTest), AND if we can detect signals of a certain magnitude and duration (50%-50y).
>
> This doesn't mean that lower numbers of inscriptions are useless. You can do lots of studies that either meet this threshold (e.g., province-level studies; the top eight provinces have >4500 inscriptions, which gets you more sensitivity), or if you have fewer inscriptions, you can still use them for descriptive shape comparison, e.g., 'Citra peaks in the 2nd century' or for cross-sectional analyses like 'do bigger cities produce proportionally more inscriptions'.
>
> I do object to the characterisation of 'throw all the methods at the inscriptions' — it's actually much narrower than what I tried in 2024, and I've preregistered a *specific* set of statistical tests. I don't know what you expect / want here.
>
> I'll go revise the slides — my inclination after reading your comments is 'essentially no discussion of statistical method in the main slides other than saying what was done, focus *entirely* on reason why we're doing this, what the implications of the results are, and what the contribution is.
>
> I may do a couple of version — this is a bigger rewrite than I was expecting so I will have less time for 'make slides beautiful' and 'polish the prose in the script', but your questions have forced me to take 1.5 hours to go back and make sure that I understand what we are doing and why — it's exactly what I felt like when the editors at JCH made a similar critique of Martin's statistical approach... (I have a meeting with him on Monday to review these results).
>
> Ok, more soon, I'll try to build in this response to the slides / script.
>
> Cheers,
> Shawn

# Director's notes for the revision (Claude's working summary — not part of the email thread)

**Direction Shawn has committed to in the reply (the operative instruction):**

> *"essentially no discussion of statistical method in the main slides other than saying what was done, focus entirely on reason why we're doing this, what the implications of the results are, and what the contribution is."*

This means the main 9 slides become **narrative-only**: problem → hazard → what-we-did (one-liner each) → what we found → what it means. All "alpha", "posterior", "Mundlak", "NBR", "f_within" terminology moves to G-series (methods glossary) and B-series (anticipated-question reserve). Substantive findings (30 % within-province, ~1,600 minimum, editorial-template signature numbers) stay — only the *presentation* changes.

**Specific themes from Adela that the rewrite must hit:**

1. **Contribution / "what problem are we solving"** — the missing framing on slide 1. Shawn's reply has it: refute the strong "habit-only" position; open inscriptions as a (partial) population proxy à la radiocarbon SPA. Even a 10–30 % signal is a contribution.
2. **"Editorial distortion" is opaque** — rename to something like *convention-based dating* or *epigraphic dating convention*. Show the slab/spike signature as a demonstrable feature.
3. **Reachability slide y-axis is opaque** — "bracket" labels, "20-50pc", "96 reachable cells" all unexplained. Reframe the headline as *sensitivity*: "what scale of change can we detect with the data we have?" — concrete: 50%-over-50y, comparable to a third-century-crisis-scale shift.
4. **"So what?" on the per-city SPA shapes (slide 4)** — interpret peaks/troughs historically; tie at least one to a recognisable event.
5. **Slide 5 needs a narrative** — drop alpha-posterior framing entirely; show only that the convention is real (54.5 % / 53 % editorial signature) → we model it out → cleaner SPA.
6. **Slide 6a (frequentist NBR)** — historical interpretation of β < 1. What does sublinear scaling mean for the empire? Compare to Hanson explicitly (does he include Rome — confirm — clarify).
7. **Slide 6b (Bayesian Mundlak)** — show the 30 % visually (currently it's a posterior summary readers can't see in the graphs); justify Mundlak as "comparing apples with apples", not "another method".
8. **Adela's MAUP/ecological-fallacy point** — within-province decomposition partially addresses it; flag honestly as a remaining limitation, don't bury.
9. **"Throw all methods" perception** — name the *narrow*, preregistered set explicitly. Shawn pushed back hard on this characterisation in his reply; the deck needs to make the narrowness visible.
10. **What this means for Adela's own work (and similar small-N projects)** — 200 inscriptions per 50y bin sits above the descriptive-shape threshold but below the change-detection threshold. Include this as a worked example in implications.

**What stays as backup (B / G series):** all the statistical mechanics — within-between decomposition formalism, Mundlak history, alpha-posterior visuals, R-hat / ESS gates, Moran's I diagnostics, the measurement-error sensitivity, the three-weighting divergence.

**Preregistered findings that must survive the rewrite (do not lose):**

- ~ 30 % within-province population-attributable variance (the headline)
- Editorial-template signature: 54.5 % `not_before` = `01`; 53 % `not_after` = `00`
- ~ 1,600 minimum inscriptions (range 1,400 – 1,950 across nulls) for 50%-over-50y crisis-scale detection
- Top eight provinces have > 4,500 inscriptions (the descriptive-shape comfort zone)
- Phase A sensitivities: measurement-error ROBUST under σ_pop ∈ {0.1, 0.2, 0.3}; three-weighting shows material divergence (binding per §5)
