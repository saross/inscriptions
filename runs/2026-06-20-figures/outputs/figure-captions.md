# Figure captions — for the non-statistician reader

Plain-language captions for the key-findings figure set
(`runs/2026-06-20-figures/`), aimed at an archaeologist or ancient historian who
is **not** a statistician. Each caption answers three questions: **What is this?**
(what you are looking at), **What does it mean?** (how to read it), and **Why does
it matter?** (why it belongs in the paper). UK/Australian English; BC/AD.

A few terms used throughout:

- **SPD (summed-probability distribution / "SPA", summed-probability analysis).**
  A curve showing how a body of dated material is spread through time. Because
  most inscriptions are not dated to a single year but to a *range* (e.g. "AD
  100–150"), each inscription's single "vote" is spread evenly across its range;
  adding up all those spread-out votes gives the curve. The taller the curve at a
  date, the more inscription activity that date carries.
- **Editorial-convention contamination.** Modern editors often record an
  inscription's date as a round-number bracket ("AD 1–100", "AD 100–200") even
  when nothing about the stone itself demands such a wide, tidy range. These
  conventional brackets pile artificial "slabs" of probability onto round dates,
  distorting the SPD.
- **Deconvolution.** Our statistical correction that estimates and removes those
  conventional slabs, recovering the *genuine* underlying distribution of dates.
- **Credible band (95 %).** The shaded ribbon around a curve: the range within
  which the true value almost certainly lies. A wide band means "we are unsure
  here"; a narrow band means "we are confident here". Honest uncertainty, shown.
- **The two frames.** *Empire* (blue) = all provinces, our broad context. *Latin*
  (vermillion) = the Latin-speaking provinces with the city of Rome removed; this
  is our cleaner "diagnostic" sample, because Rome is a vast outlier that can
  dominate any total.

---

## F1 — Deconvolution before/after (the method in one picture)

**What is this?** The empire-wide inscription curve through time, shown twice: the
*raw* version (grey dashed) that you get straight from the dates as editors
recorded them, and the *genuine* version (solid blue, with its 95 % band) after
our correction removes the editorial-convention slabs (the orange shaded block).

**What does it mean?** The orange block is the portion of the raw curve that is an
artefact of round-number dating conventions, not real ancient behaviour. Once it
is removed, the genuine curve is *sharper*, not smoother: real peaks of activity
(around AD 90 and again around AD 210) stand out that the conventional "smearing"
had flattened and spread out.

**Why does it matter?** This is the paper's central methodological claim made
visible. Conventional dating does not just add noise — it systematically hides the
real shape of epigraphic activity. If you study Roman inscriptions through time
without this correction, you are partly studying the habits of modern editors. The
correction lets us see the ancient signal underneath.

---

## F2 — Empire and Latin, corrected vs uncorrected

**What is this?** The same before/after as F1, shown side by side for both frames:
the whole empire (left) and the Latin-minus-Rome diagnostic sample (right). Grey
dashed = raw; coloured solid + band = genuine.

**What does it mean?** The correction does the same kind of work in both frames —
it sharpens real peaks and strips conventional slabs — so the result is not a
quirk of one particular sample. The Latin frame shows even stronger peaks because
removing Rome removes a smothering bulk of material.

**Why does it matter?** It shows the method is robust across the samples the paper
relies on, and it establishes the two frames (empire context, Latin diagnostic)
that the rest of the figures use.

---

## F3 — Province-level deconvolution (six provinces)

**What is this?** Six provinces spanning the empire — the Italian core (Latium et
Campania), Iberia, Africa, the Balkans, the Rhine frontier, and Britain — each
with its raw (grey dashed) and genuine (vermillion + band) curve. The number in
each title is how many inscriptions that province contributes; Britain is starred
because its sample is small and uncertain.

**What does it mean?** Each province has a genuinely different chronological
profile: the Italian core peaks early, frontier provinces peak later as they were
drawn into the epigraphic habit. The correction works province by province, and
where a province has few inscriptions (Britain) the credible band is honestly much
wider — we do not pretend to certainty we do not have.

**Why does it matter?** It demonstrates that the empire-wide result is built from
real regional variation, not an averaging artefact, and that the method degrades
gracefully (wider bands) rather than misleadingly when data are thin.

---

## F4 — Anchor-city deconvolution (the validation)

**What is this?** Five cities whose history is independently known, used to check
the method. Most important is **Pompeii**, buried by Vesuvius in **AD 79** (dotted
line): no genuine inscription activity should appear after that date.

**What does it mean?** Pompeii's genuine curve rises sharply and then collapses to
essentially zero right at AD 79 — exactly as it must, since the city ceased to
exist. Ostia peaks in the 2nd century, matching its known commercial apogee;
Mogontiacum shows the sharp early peak of a military foundation.

**Why does it matter?** This is the method passing an external reality check. When
we apply it to cities whose true history we already know, it recovers that history.
That earns confidence in what it tells us about cities whose history we *don't*
already know.

---

## F5 — Content (letter-count) tracks the inscription count

**What is this?** Two ways of measuring epigraphic output over time for the whole
empire: counting *inscriptions* (grey) versus counting *letters* (vermillion) — a
proxy for how much was actually written, not just how many stones survive.

**What does it mean?** The two curves move together: periods rich in inscriptions
are also periods rich in text. The small gaps between them are periods when
inscriptions were, on average, wordier or terser than usual.

**Why does it matter?** It shows our findings do not depend on the (somewhat
arbitrary) decision to count stones rather than words. The temporal story is the
same whichever unit of "epigraphic production" you prefer — a robustness check that
a sceptical reader will want to see.

---

## F6 — Provincial capitals over-produce inscriptions

**What is this?** A comparison of how many inscriptions provincial capitals
produced versus ordinary towns of the *same population*. Panel (a) is the overall
result for both frames, with its 95 % credible interval; panel (b) breaks it down
into eight 50-year periods.

**What does it mean?** Capitals consistently carry more inscriptions than their
population alone would predict — about two-and-a-half times more on the model's
scale (the contrast is roughly +1.0). Panel (b) shows this held in *every* period
of the empire: the effect is structural, not a one-off of a single golden age.

**Why does it matter?** It quantifies the "capital effect": administrative and
status centrality, not just headcount, drove the epigraphic habit. This separates
*being a capital* from *being big* — two things that usually travel together and
are easily confused.

---

## F7 — Population and epigraphy: a within-province relationship

**What is this?** The relationship between a city's population and its inscription
output, split two ways. Panel (a) — *within* a province: do bigger cities than
their provincial neighbours produce more? Panel (b) — *between* provinces: do
provinces with bigger cities on average produce more? Each point is a city (a) or
a province (b); the line is the fitted trend.

**What does it mean?** Within a province the relationship is strong and steep
(bigger city → more inscriptions; the exponent is about 0.73). Between provinces it
is flat and uncertain (the line is essentially horizontal and its uncertainty
crosses zero). Capitals (triangles in panel a) sit above the cloud, over-producing
as in F6.

**Why does it matter?** The population–epigraphy link is a *local* phenomenon: it
operates among neighbouring cities that share a regional culture of inscribing, not
as a universal law comparing one province to another. That is a substantive claim
about *why* people inscribed — local competition and emulation, not raw demography
empire-wide.

---

## F8 — Relative city trajectories over time (illustrative)

**What is this?** For the cities with enough data to support it, an inferred
trajectory of population *relative to the empire-wide trend* (the dotted line at
1.0 = "tracking the empire average"). The bold line is the typical (median) city;
the shaded band is the spread between cities (the middle half of them).

**What does it mean?** The typical city rises towards the empire trend at the
**Antonine peak (AD 188)**, falls to a **trough around AD 262** (the troubled mid-
3rd century), and partly recovers afterwards. But cities are very varied — the band
is wide — so this is a story about a general tendency, not a uniform collapse.

**Why does it matter?** It connects the epigraphic record to the wider demographic
and political history of the empire (the Antonine plague, the 3rd-century crisis).
**The caption stresses that this is an illustrative relative shape, NOT a
population estimate**: the method recovers *change relative to the empire*, not
absolute numbers of people, and the independently-dated anchor cities are
deliberately excluded so they cannot flatter the result.

---

## F9 — The size of each ingredient

**What is this?** A city's inscription rate through time is built from four
ingredients: a shared empire-wide rhythm, a province-specific wobble, a city-
specific wobble, and a steady level (how prolific the city is overall, regardless
of timing). The bars show how *big* each ingredient is, on a common scale.

**What does it mean?** The shared empire-wide rhythm is the largest single
ingredient — on its own it accounts for roughly **54 %** of the ups and downs in a
typical city's timeline. Province and city wobbles are smaller but real; the
overall "how prolific" level is the smallest.

**Why does it matter?** It tells us that most of *when* inscriptions appear is
driven by something common to the whole empire (a shared habit, demography, and
economy moving together), with regional and local character layered on top. It
locates where the action is before we start interpreting it.

> Note for the statistically minded: the three time-varying ingredients are
> *negatively correlated* (when one is high, the others tend low), so their shares
> do not add tidily to 100 %. The exact partition is recorded separately
> (`temporal-three-way-split.json`); the bars deliberately show magnitudes, which
> are unambiguous.

---

## F10 — How the population effect changed over time

**What is this?** The strength of the within-province population effect (the steep
slope from F7), refitted separately in each 50-year period, for both frames. The
dotted line at 1.0 marks a hypothetical "linear" world where doubling population
doubles inscriptions.

**What does it mean?** In every period the slope is well below 1.0 — bigger cities
inscribe more, but *less than proportionally* (doubling a city's size less than
doubles its inscriptions). The slope dips to a plateau around 0.58 in the high
empire and steepens slightly at the margins, tracing a shallow U.

**Why does it matter?** "Sublinear scaling" is a recognised signature of how
settlement systems work; finding it in epigraphy, stable across four centuries,
puts Roman inscribing alongside other studied urban phenomena and shows the effect
is a durable structural feature, not a passing fashion.

---

## F11 — Two kinds of "over-production" are independent

**What is this?** Two different ways a city can exceed expectations: producing more
*inscriptions* than its population predicts (horizontal axis, "prolific for size")
and producing more *letters per inscription* than its count predicts (vertical
axis, "verbose per act"). Each dot is a city.

**What does it mean?** The cloud is round and the trend line is flat — knowing that
a city over-produced inscriptions tells you nothing about whether its inscriptions
were unusually wordy. The two tendencies are statistically unrelated (correlation
essentially zero).

**Why does it matter?** It shows "epigraphic intensity" is not a single dial.
*How much* a community inscribed and *how much it said* per inscription are
separate cultural choices, and should be studied as such rather than lumped into
one notion of "epigraphic habit".

---

## F12 — When the method can be trusted (its operating envelope)

**What is this?** A reliability map for the deconvolution itself. The grid tests
how well the method recovers a known answer as the sample size (left to right) and
the amount of convention contamination (bottom to top) vary. Brighter = better
recovery; a filled dot marks "reliable", an open dot "marginal".

**What does it mean?** Recovery improves with more inscriptions and worsens as
convention contamination rises. The method is dependable for easy cases from about
500 inscriptions, needs up to ~2,000 for hard cases, and should not be pushed past
roughly 70 % contamination.

**Why does it matter?** Honesty about limits. It tells the reader (and us) exactly
which provinces and cities are inside the method's trustworthy zone and which
results should be read cautiously — the "spec sheet" for the instrument.

---

## F13 — A chronological atlas of the provinces

**What is this?** The genuine inscription curve for each of 25 provinces (those
with enough data), drawn small so they can be compared at a glance. Each comes from
the hierarchical model that pools information across a province's smaller cities;
the number in parentheses is how many cities contribute.

**What does it mean?** The provinces do not march in step. The Italian regions peak
early; frontier provinces such as Dacia, Britain, and Macedonia peak later and more
sharply, as the habit of inscribing spread outwards and was taken up at different
times in different places.

**Why does it matter?** It turns the single empire-wide story into a *geography* of
the epigraphic habit — showing where and when the practice took hold, province by
province. This regional texture is what a historian can connect to conquest dates,
urbanisation, military presence, and provincial administration.

> Note: F13 uses the §5 hierarchical trajectory model (which smooths and pools
> across small cities), a *different* correction from the F1–F4 deconvolution. The
> two are complementary views of the same provinces; the anchor cities are held
> out of this model.
