# Dostoevsky AI — Blinded Human Evaluation Worksheet

**Source Run ID:** `run_20261025T180347Z_63cb94586e9f4132adf9952aae03efbb`  
**Suite Version:** `2.1.0`  
**Total Blinded Items:** 30 (10 Literary Rewrite, 10 Word Cabinet, 10 Inner Monologue)

## 1. Global Scoring Scale (1–5)

- **1:** Serious failure — Violates fundamental constraints, major factual hallucinations, or unreadable prose.
- **2:** Weak performance — Noticeable drift, shallow psychological depth, or frequent stylistic flaws.
- **3:** Acceptable with noticeable issues — Preserves core task but contains minor drift, cliché, or slight repetition.
- **4:** Strong with minor issues — High fidelity, believable psychology, disciplined prose with trivial flaws.
- **5:** Excellent performance — Exceptional nuance, perfect fidelity, compelling literary restraint.

## 2. Rater Instructions

Rate each item on a 1-5 scale across its three feature criteria. Check failure conditions first; if triggered, assign appropriate low scores (1-2). Provide concrete evidence notes for extreme scores (1, 2, or 5). Do not penalize word-count variance under literary criteria, as length compliance is already objectively verified.

---


# Feature: Literary Rewrite

## Item: `LR_ITEM_01`

### Input Context
- **Target Intensity:** `default`
- **Original Text:**
> 

### Model Generated Output

> I realized the cashier had overcharged me. I slipped the excess coins into my pocket, telling myself it compensated for the wasted afternoon, and quickly made my way out onto the street before anyone observed.

### Rubric & Guidance

- **`LR_CRIT_1` (meaning_and_fact_preservation):** Preserves core facts, events, relationships, negation, agency, and outcome without inventing events or reversing what occurred.
  - *Specific Guidance:* Preserves excessive change awareness, pocketing the coins, the 'compensation' rationalization, and hasty departure.
- **`LR_CRIT_2` (psychological_depth):** Conveys psychological tension, moral conflict, and internal subtext through concrete behavioral detail rather than melodrama or abstract emotion labels.
  - *Specific Guidance:* Highlights the rapid mental maneuver of converting an opportunistic theft into deserved restitution.
- **`LR_CRIT_3` (stylistic_restraint):** Natural, disciplined literary prose avoiding ornamental melodrama, decorative clutter, or excessive adjectives.
  - *Specific Guidance:* Keeps the physical departure tense and furtive without sensationalized criminal drama.

### Specific Failure Conditions

- ⚠️ Has the narrator return the change out of remorse.
- ⚠️ Omits the internal excuse about 'compensation for a lost afternoon'.
- ⚠️ Escalates the crime into armed robbery or grand theft.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `LR_CRIT_1` | meaning_and_fact_preservation | `[ ]` | |
| `LR_CRIT_2` | psychological_depth | `[ ]` | |
| `LR_CRIT_3` | stylistic_restraint | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---

## Item: `LR_ITEM_02`

### Input Context
- **Target Intensity:** `default`
- **Original Text:**
> 

### Model Generated Output

> I approached the drawer intending to retrieve the letter, yet I refrained from even handling it. I then closed the desk with as little sound as possible and silently exited the room without once glancing at any of its contents.

### Rubric & Guidance

- **`LR_CRIT_1` (meaning_and_fact_preservation):** Preserves core facts, events, relationships, negation, agency, and outcome without inventing events or reversing what occurred.
  - *Specific Guidance:* Strictly preserves that the letter was NOT touched and NOT read. Flipping this into reading the letter is a fatal failure.
- **`LR_CRIT_2` (psychological_depth):** Conveys psychological tension, moral conflict, and internal subtext through concrete behavioral detail rather than melodrama or abstract emotion labels.
  - *Specific Guidance:* Evokes the acute temptation and physical hesitation without violating the negative constraint.
- **`LR_CRIT_3` (stylistic_restraint):** Natural, disciplined literary prose avoiding ornamental melodrama, decorative clutter, or excessive adjectives.
  - *Specific Guidance:* Depicts quiet physical restraint with disciplined, sensory pacing.

### Specific Failure Conditions

- ⚠️ Hallucinates reading the letter, unfolding it, or discovering its contents.
- ⚠️ Fails to state that the drawer was closed untouched.
- ⚠️ Changes the setting or introduces another character into the room.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `LR_CRIT_1` | meaning_and_fact_preservation | `[ ]` | |
| `LR_CRIT_2` | psychological_depth | `[ ]` | |
| `LR_CRIT_3` | stylistic_restraint | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---

## Item: `LR_ITEM_03`

### Input Context
- **Target Intensity:** `default`
- **Original Text:**
> 

### Model Generated Output

> I retraced my steps, returning the money I had discovered by the side of the path. I sought out the owner's presence, hoping to demonstrate how steadfastly I upheld honesty.

### Rubric & Guidance

- **`LR_CRIT_1` (meaning_and_fact_preservation):** Preserves core facts, events, relationships, negation, agency, and outcome without inventing events or reversing what occurred.
  - *Specific Guidance:* Must preserve finding the money on the floor, returning it to the owner, and the underlying desire for moral recognition.
- **`LR_CRIT_2` (psychological_depth):** Conveys psychological tension, moral conflict, and internal subtext through concrete behavioral detail rather than melodrama or abstract emotion labels.
  - *Specific Guidance:* Captures the sharp psychological tension between public integrity and private vanity.
- **`LR_CRIT_3` (stylistic_restraint):** Natural, disciplined literary prose avoiding ornamental melodrama, decorative clutter, or excessive adjectives.
  - *Specific Guidance:* Avoids moralizing preaching or heavy-handed explanations of virtue.

### Specific Failure Conditions

- ⚠️ Omits the return of the money or the craving for recognition.
- ⚠️ Turns the narrator into an unblemished moral hero without vanity.
- ⚠️ Invents extensive extraneous backstory (e.g. starving children, gambling debts).

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `LR_CRIT_1` | meaning_and_fact_preservation | `[ ]` | |
| `LR_CRIT_2` | psychological_depth | `[ ]` | |
| `LR_CRIT_3` | stylistic_restraint | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---

## Item: `LR_ITEM_04`

### Input Context
- **Target Intensity:** `default`
- **Original Text:**
> 

### Model Generated Output

> At dinner, my uncle teased me about my new attire in front of the guests. I chuckled more loudly than any of us present, topped off his drink, and silently coveted his downfall.

### Rubric & Guidance

- **`LR_CRIT_1` (meaning_and_fact_preservation):** Preserves core facts, events, relationships, negation, agency, and outcome without inventing events or reversing what occurred.
  - *Specific Guidance:* Preserves dinner setting, uncle's mockery of clothes, guests' presence, exaggerated laughter, glass refilling, and silent wish for ruin.
- **`LR_CRIT_2` (psychological_depth):** Conveys psychological tension, moral conflict, and internal subtext through concrete behavioral detail rather than melodrama or abstract emotion labels.
  - *Specific Guidance:* Captures the sickening discrepancy between subservient laughter and poisonous hatred.
- **`LR_CRIT_3` (stylistic_restraint):** Natural, disciplined literary prose avoiding ornamental melodrama, decorative clutter, or excessive adjectives.
  - *Specific Guidance:* Avoids turning the silent wish into overt physical violence or shouting.

### Specific Failure Conditions

- ⚠️ Has the narrator openly confront or strike the uncle.
- ⚠️ Omits the refilling of the glass or the laughter.
- ⚠️ Softens the hatred into mild annoyance.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `LR_CRIT_1` | meaning_and_fact_preservation | `[ ]` | |
| `LR_CRIT_2` | psychological_depth | `[ ]` | |
| `LR_CRIT_3` | stylistic_restraint | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---

## Item: `LR_ITEM_05`

### Input Context
- **Target Intensity:** `default`
- **Original Text:**
> 

### Model Generated Output

> Desiring to admit his deceit, he would shift away from the topic every time it presented itself, instead criticizing how others doubted him.

### Rubric & Guidance

- **`LR_CRIT_1` (meaning_and_fact_preservation):** Preserves core facts, events, relationships, negation, agency, and outcome without inventing events or reversing what occurred.
  - *Specific Guidance:* Must preserve the unconfessed lie, repeated opportunities, subject changing, and accusation of mistrust.
- **`LR_CRIT_2` (psychological_depth):** Conveys psychological tension, moral conflict, and internal subtext through concrete behavioral detail rather than melodrama or abstract emotion labels.
  - *Specific Guidance:* Reveals the psychological contradiction between guilt and self-protective deflection through specific evasive behavior.
- **`LR_CRIT_3` (stylistic_restraint):** Natural, disciplined literary prose avoiding ornamental melodrama, decorative clutter, or excessive adjectives.
  - *Specific Guidance:* Avoids essay-like psychoanalysis explaining the character's flaws in abstract terms.

### Specific Failure Conditions

- ⚠️ Removes the lie or has the character confess openly.
- ⚠️ Omits the defensive accusation that nobody trusts him.
- ⚠️ Turns into an abstract treatise on dishonesty without narrative scene.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `LR_CRIT_1` | meaning_and_fact_preservation | `[ ]` | |
| `LR_CRIT_2` | psychological_depth | `[ ]` | |
| `LR_CRIT_3` | stylistic_restraint | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---

## Item: `LR_ITEM_06`

### Input Context
- **Target Intensity:** `default`
- **Original Text:**
> 

### Model Generated Output

> After the funeral, as the others mourned in the parlor, she made her way upstairs to fold her sister’s coats. There, amidst the silence, she discovered an old train ticket inside one of them. She tossed it into the wastebasket without a second glance and pondered why she felt no emotion at all.

### Rubric & Guidance

- **`LR_CRIT_1` (meaning_and_fact_preservation):** Preserves core facts, events, relationships, negation, agency, and outcome without inventing events or reversing what occurred.
  - *Specific Guidance:* Preserves the post-funeral context, weeping parlor guests, coat folding upstairs, train ticket discarded, and total numbness.
- **`LR_CRIT_2` (psychological_depth):** Conveys psychological tension, moral conflict, and internal subtext through concrete behavioral detail rather than melodrama or abstract emotion labels.
  - *Specific Guidance:* Depicts emotional numbness as unsettling and authentic without manufacturing artificial tears.
- **`LR_CRIT_3` (stylistic_restraint):** Natural, disciplined literary prose avoiding ornamental melodrama, decorative clutter, or excessive adjectives.
  - *Specific Guidance:* Maintains quiet, restrained pacing avoiding sentimental grief tropes.

### Specific Failure Conditions

- ⚠️ Forces a dramatic breakdown of tears or theatrical mourning.
- ⚠️ Omits the train ticket or folding the coats.
- ⚠️ Explains the numbness as cold villainy rather than dissociative shock.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `LR_CRIT_1` | meaning_and_fact_preservation | `[ ]` | |
| `LR_CRIT_2` | psychological_depth | `[ ]` | |
| `LR_CRIT_3` | stylistic_restraint | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---

## Item: `LR_ITEM_07`

### Input Context
- **Target Intensity:** `default`
- **Original Text:**
> 

### Model Generated Output

> She was lauded for her efforts, acknowledged by all who were present, yet she could not help but ponder if the accolades were merely a result of pity.

### Rubric & Guidance

- **`LR_CRIT_1` (meaning_and_fact_preservation):** Preserves core facts, events, relationships, negation, agency, and outcome without inventing events or reversing what occurred.
  - *Specific Guidance:* Must preserve public praise, outward thanks, and private doubt about whether pity was the real motive.
- **`LR_CRIT_2` (psychological_depth):** Conveys psychological tension, moral conflict, and internal subtext through concrete behavioral detail rather than melodrama or abstract emotion labels.
  - *Specific Guidance:* Depicts insecurity through plausible introspective reflection; suspicion of pity must remain her subjective fear rather than an established external fact.
- **`LR_CRIT_3` (stylistic_restraint):** Natural, disciplined literary prose avoiding ornamental melodrama, decorative clutter, or excessive adjectives.
  - *Specific Guidance:* Tone must remain restrained and realistic rather than descending into frantic despair.

### Specific Failure Conditions

- ⚠️ Treats the suspicion of pity as proven external fact.
- ⚠️ Omits her outward thanks or the praise itself.
- ⚠️ Adds dramatic physical crises or unrelated plot twists.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `LR_CRIT_1` | meaning_and_fact_preservation | `[ ]` | |
| `LR_CRIT_2` | psychological_depth | `[ ]` | |
| `LR_CRIT_3` | stylistic_restraint | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---

## Item: `LR_ITEM_08`

### Input Context
- **Target Intensity:** `default`
- **Original Text:**
> 

### Model Generated Output

> I felt isolated at the gathering. Everyone was engaged in conversation. I feigned busyness with my smartphone as I had no idea how to integrate myself.

### Rubric & Guidance

- **`LR_CRIT_1` (meaning_and_fact_preservation):** Preserves core facts, events, relationships, negation, agency, and outcome without inventing events or reversing what occurred.
  - *Specific Guidance:* Must preserve the party setting, conversational disconnect, phone pretense, and inability to join.
- **`LR_CRIT_2` (psychological_depth):** Conveys psychological tension, moral conflict, and internal subtext through concrete behavioral detail rather than melodrama or abstract emotion labels.
  - *Specific Guidance:* Evokes social alienation through concrete physical gestures and room observations rather than repeated synonyms for loneliness.
- **`LR_CRIT_3` (stylistic_restraint):** Natural, disciplined literary prose avoiding ornamental melodrama, decorative clutter, or excessive adjectives.
  - *Specific Guidance:* Sentences should be varied and disciplined, avoiding decorative metaphors that obscure the scene.

### Specific Failure Conditions

- ⚠️ Omits the phone or the inability to participate.
- ⚠️ Replaces mundane social isolation with extreme existential despair.
- ⚠️ Repeats abstract words like 'loneliness' without descriptive progression.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `LR_CRIT_1` | meaning_and_fact_preservation | `[ ]` | |
| `LR_CRIT_2` | psychological_depth | `[ ]` | |
| `LR_CRIT_3` | stylistic_restraint | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---

## Item: `LR_ITEM_09`

### Input Context
- **Target Intensity:** `default`
- **Original Text:**
> 

### Model Generated Output

> I harbored anger towards my friend over his oversight in our arranged meeting. Upon his apology, I dismissed the incident and withdrew from engaging with him throughout the following day.

### Rubric & Guidance

- **`LR_CRIT_1` (meaning_and_fact_preservation):** Preserves core facts, events, relationships, negation, agency, and outcome without inventing events or reversing what occurred.
  - *Specific Guidance:* Must preserve the forgotten meeting, initial anger, friend's apology, spoken forgiveness, and subsequent avoidance. Omitting the apology or verbal forgiveness is a major failure.
- **`LR_CRIT_2` (psychological_depth):** Conveys psychological tension, moral conflict, and internal subtext through concrete behavioral detail rather than melodrama or abstract emotion labels.
  - *Specific Guidance:* Must expose the internal contradiction between the spoken pardon and the physical act of avoidance through behavioral subtext.
- **`LR_CRIT_3` (stylistic_restraint):** Natural, disciplined literary prose avoiding ornamental melodrama, decorative clutter, or excessive adjectives.
  - *Specific Guidance:* Prose should be controlled and believable, avoiding theatrical rage or melodramatic declarations of betrayal.

### Specific Failure Conditions

- ⚠️ Omits apology, spoken forgiveness, or subsequent avoidance.
- ⚠️ Invents an unrelated third-party conflict or alters meeting purpose.
- ⚠️ Reverses the outcome by having the narrator openly reconcile.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `LR_CRIT_1` | meaning_and_fact_preservation | `[ ]` | |
| `LR_CRIT_2` | psychological_depth | `[ ]` | |
| `LR_CRIT_3` | stylistic_restraint | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---

## Item: `LR_ITEM_10`

### Input Context
- **Target Intensity:** `default`
- **Original Text:**
> 

### Model Generated Output

> Before he even knocked, I had already resolved to decline his request. As he stepped into the room with a smile, I invited him to have some tea, sitting silently as though my decision remained uncertain.

### Rubric & Guidance

- **`LR_CRIT_1` (meaning_and_fact_preservation):** Preserves core facts, events, relationships, negation, agency, and outcome without inventing events or reversing what occurred.
  - *Specific Guidance:* Must preserve the prior decision to refuse, the knock, the visitor's smile, the tea offer, and deceptive attentive silence.
- **`LR_CRIT_2` (psychological_depth):** Conveys psychological tension, moral conflict, and internal subtext through concrete behavioral detail rather than melodrama or abstract emotion labels.
  - *Specific Guidance:* Accentuates the psychological coldness of polite listening while holding a settled refusal.
- **`LR_CRIT_3` (stylistic_restraint):** Natural, disciplined literary prose avoiding ornamental melodrama, decorative clutter, or excessive adjectives.
  - *Specific Guidance:* Prose should be controlled, highlighting the polite mask without caricature.

### Specific Failure Conditions

- ⚠️ Changes the decision so that the narrator relents or genuinely wavers.
- ⚠️ Omits the offer of tea or the deceptive pretense of open-minded listening.
- ⚠️ Inverts chronology by placing the decision after the conversation.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `LR_CRIT_1` | meaning_and_fact_preservation | `[ ]` | |
| `LR_CRIT_2` | psychological_depth | `[ ]` | |
| `LR_CRIT_3` | stylistic_restraint | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---


# Feature: Word Cabinet

## Item: `WC_ITEM_01`

### Input Context
- **Requested Word Count:** 3
- **Psychological Context:**
> 

### Model Generated Output

| # | Word | Literal Translation | Connotation | Distinction | Usage Example |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 1 | **resentment** |  | this term captures the core essence of the described emotion without being overly specific to just one aspect. It bridges feelings of personal injury and general world-friendliness more loosely than smoldering personal injury does, while still having more intensity than the more generalized 'sourness.' | resentment is more focused on external mistreatment rather than internalizing it completely as smoldering personal injury might do. | *""* |
| 2 | **misanthropy** |  | this term captures the broader aspect of being sour toward the world without delving into personal grievances. It's less intense than pure resentfulness and more generalized than smoldering personal injury. | misanthropy refers to a dislike for humanity in general, not specific individuals or situations as resentment does. | *""* |
| 3 | **bitterness** |  | bitterness captures the intensity and focus on specific injustices without being as personal as smoldering personal injury. It's a bridge between resentment and misanthropy in terms of specificity and intensity. | bitterness focuses more specifically on past grievances rather than just general world dissatisfaction, making it suitable for describing anger at specific instances rather than a blanket dislike. | *""* |

### Rubric & Guidance

- **`WC_CRIT_1` (vocabulary_relevance):** Selected terms precisely address the specific emotional or psychological nuance described in the context.
  - *Specific Guidance:* Provides precise terms distinguishing legitimate moral indignation from sour, chronic bitterness.
- **`WC_CRIT_2` (definition_and_connotation_quality):** Definitions are clear and accurate in plain language; connotations capture plausible psychological associations without asserting universal dogmas.
  - *Specific Guidance:* Accurately articulates register and connotations for each term.
- **`WC_CRIT_3` (distinction_usefulness):** Distinctions meaningfully separate each entry from a nearby synonym rather than treating synonyms as interchangeable.
  - *Specific Guidance:* Illustrative examples demonstrate natural, evocative usage.

### Specific Failure Conditions

- ⚠️ Treats indignation and bitterness as interchangeable.
- ⚠️ Outputs incomplete entries or truncated JSON.
- ⚠️ Provides identical intensity ratings for distinct emotional registers.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `WC_CRIT_1` | vocabulary_relevance | `[ ]` | |
| `WC_CRIT_2` | definition_and_connotation_quality | `[ ]` | |
| `WC_CRIT_3` | distinction_usefulness | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---

## Item: `WC_ITEM_02`

### Input Context
- **Requested Word Count:** 6
- **Psychological Context:**
> 

### Model Generated Output

| # | Word | Literal Translation | Connotation | Distinction | Usage Example |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 1 | **paralyzing** |  | implies intense distress and a deep feeling of emptiness that leaves one unable to function normally or fully enjoy their surroundings | describes the overwhelming emotional state rather than just sadness or disappointment alone, emphasizing how it feels physically incapacitated by the situation | *""* |
| 2 | **acerbic** |  | implies a sharp, unpleasant bitterness that stems from the realization of unfulfilled aspirations and trivial rewards | focuses more on the quality of one's response to the situation (attitude) rather than an internal state, making it applicable in situations where external judgment is a factor | *""* |
| 3 | **morbidly fascinated** |  | implies an intense fascination that goes beyond mere curiosity, often accompanied by discomfort or disgust at what one finds fascinating | focuses on the fascination rather than a specific emotion like despair; suggests a more active mental engagement with something repulsive | *""* |
| 4 | **sour grapes** |  | implies a bitter, resentful attitude toward one's own situation due to perceived unfairness, even when the reality is clear and unambiguous | specifically targets resentment over failure in obtaining something one desires rather than just dissatisfaction or disgust with a trivial reward, which can be more diffuse | *""* |
| 5 | **morose** |  | implies a somber, dark emotional state that can be caused by disappointment and the triviality of the prize, but it does not necessarily suggest extreme intensity | describes a more subdued or melancholic mood than stark feelings like despair or frustration; suggests an internal state rather than one’s response to external stimuli | *""* |
| 6 | **vexed** |  | implies ongoing irritation and frustration stemming from the realization of unfulfilled aspirations and the triviality of the reward, potentially lasting over time rather than immediately following an event | focuses on the state or condition of being vexed (frequent irritability or aggravation) versus a singular emotion like disgust or despair; suggests a more sustained emotional response | *""* |

### Rubric & Guidance

- **`WC_CRIT_1` (vocabulary_relevance):** Selected terms precisely address the specific emotional or psychological nuance described in the context.
  - *Specific Guidance:* Provides 6 diverse words or phrases reflecting disillusionment, hollow victory, and anti-climax.
- **`WC_CRIT_2` (definition_and_connotation_quality):** Definitions are clear and accurate in plain language; connotations capture plausible psychological associations without asserting universal dogmas.
  - *Specific Guidance:* Distinguishes existential desolation from simple disappointment.
- **`WC_CRIT_3` (distinction_usefulness):** Distinctions meaningfully separate each entry from a nearby synonym rather than treating synonyms as interchangeable.
  - *Specific Guidance:* Ensures all entries have complete, high-quality fields.

### Specific Failure Conditions

- ⚠️ Returns fewer than 6 usable entries without warning.
- ⚠️ Selects terms for failure or defeat rather than success turned hollow.
- ⚠️ JSON payload malformed or truncated.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `WC_CRIT_1` | vocabulary_relevance | `[ ]` | |
| `WC_CRIT_2` | definition_and_connotation_quality | `[ ]` | |
| `WC_CRIT_3` | distinction_usefulness | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---

## Item: `WC_ITEM_03`

### Input Context
- **Requested Word Count:** 6
- **Psychological Context:**
> 

### Model Generated Output

| # | Word | Literal Translation | Connotation | Distinction | Usage Example |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 1 | **haughty** |  | This word captures the essence of someone who is unwilling to suffer discomfort because they feel it's beneath them to do so, especially when compared to others around them. | Compared to 'arrogant', haughty suggests a more subtle sense of superiority that manifests in behavior rather than being explicitly confrontational or dismissive towards others' experiences of discomfort and deprivation. | *""* |
| 2 | **hypocritical** |  | This word emphasizes the surface-level righteousness and moral superiority these individuals display over their perceived misfortunes. | Unlike 'insincere', which focuses more on the dishonest act itself, hypocritical highlights how this person's moral judgment is self-serving rather than genuinely held. | *""* |
| 3 | **morbid** |  | This word speaks to the unhealthy fascination these individuals have with discomfort, often viewing their own misfortunes as more interesting or significant than others' struggles. | While 'melancholic' can also mean focused on death and sadness, morbid suggests a darker, less contemplative kind of negativity that is self-centered rather than melancholy. | *""* |
| 4 | **misanthropic** |  | This word emphasizes their view that everyone else is not only undeserving of suffering but also responsible for any misfortunes they face. | While 'vindictive' can mean holding grudges, misanthropic suggests a more pervasive and unyielding hatred or disregard towards human beings in general. | *""* |
| 5 | **privileged** |  | This word highlights their position of ease compared to those in greater need, yet they still choose to suffer because they feel it elevates them morally. | Unlike 'benevolent', which has positive connotations, privileged implies a lack of empathy towards others and an unjust sense of moral superiority based on one's background or advantages. | *""* |

### Rubric & Guidance

- **`WC_CRIT_1` (vocabulary_relevance):** Selected terms precisely address the specific emotional or psychological nuance described in the context.
  - *Specific Guidance:* Selects vocabulary capturing sanctimony, voluntary martyrdom, and prideful self-abnegation.
- **`WC_CRIT_2` (definition_and_connotation_quality):** Definitions are clear and accurate in plain language; connotations capture plausible psychological associations without asserting universal dogmas.
  - *Specific Guidance:* Accurately dissects the false humility disguising egotism.
- **`WC_CRIT_3` (distinction_usefulness):** Distinctions meaningfully separate each entry from a nearby synonym rather than treating synonyms as interchangeable.
  - *Specific Guidance:* Examples demonstrate sharp psychological subtext.

### Specific Failure Conditions

- ⚠️ Treats the suffering as purely noble or tragic without moral superiority.
- ⚠️ Confuses martyrdom with involuntary victimization.
- ⚠️ Duplicated lemmas across the entries.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `WC_CRIT_1` | vocabulary_relevance | `[ ]` | |
| `WC_CRIT_2` | definition_and_connotation_quality | `[ ]` | |
| `WC_CRIT_3` | distinction_usefulness | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---

## Item: `WC_ITEM_04`

### Input Context
- **Requested Word Count:** 4
- **Psychological Context:**
> 

### Model Generated Output

| # | Word | Literal Translation | Connotation | Distinction | Usage Example |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 1 | **sullen** |  | This word captures the private bitterness and enduring resentment while indicating that the person is not displaying it through outward actions like a sulk or tantrum. | Compared to 'resentful', which can imply ongoing negative feelings without specifying an unexpressed nature, 'sullen' emphasizes both the hidden resentment and lack of external expression. | *""* |
| 2 | **stoic** |  | Though the person remains outwardly accepting, they are not emotionally affected on the surface. The stoicism can still mask a private bitterness. | 'Stoic' focuses more on maintaining composure and lack of emotional response compared to 'sullen', which emphasizes the hidden nature of the emotion. | *""* |
| 3 | **contemptuous** |  | While the person might not outwardly show their true feelings, there's a sense of disdain that underlies their acceptance. | 'Contemptuous' highlights the underlying feeling of being unappreciated or disrespected, which can be masked by passive acquiescence rather than direct resentment. | *""* |
| 4 | **malignant** |  | The person might not outwardly show hostility but harbors a negative sentiment that's like a hidden toxin. | 'Malignant' suggests a more serious and damaging underlying sentiment compared to the other options which are mostly about passive acceptance or mild resentment. | *""* |

### Rubric & Guidance

- **`WC_CRIT_1` (vocabulary_relevance):** Selected terms precisely address the specific emotional or psychological nuance described in the context.
  - *Specific Guidance:* Identifies terms specific to suppressed hostility, festering malice, or enduring bitterness.
- **`WC_CRIT_2` (definition_and_connotation_quality):** Definitions are clear and accurate in plain language; connotations capture plausible psychological associations without asserting universal dogmas.
  - *Specific Guidance:* Explanations reflect varied emotional intensities and temporal persistence.
- **`WC_CRIT_3` (distinction_usefulness):** Distinctions meaningfully separate each entry from a nearby synonym rather than treating synonyms as interchangeable.
  - *Specific Guidance:* Distinctions clarify differences between transient annoyance and deep rancor.

### Specific Failure Conditions

- ⚠️ Selects terms for overt aggression or violent rage.
- ⚠️ Duplicates root words across entries.
- ⚠️ Fails to address the suppressed, outward compliance aspect.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `WC_CRIT_1` | vocabulary_relevance | `[ ]` | |
| `WC_CRIT_2` | definition_and_connotation_quality | `[ ]` | |
| `WC_CRIT_3` | distinction_usefulness | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---

## Item: `WC_ITEM_05`

### Input Context
- **Requested Word Count:** 5
- **Psychological Context:**
> 

### Model Generated Output

| # | Word | Literal Translation | Connotation | Distinction | Usage Example |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 1 | **insidious** |  | This word captures the insidious nature of the fear—the feeling gradually taking hold and undermining confidence without immediate notice or obvious signs. | Unlike 'subtle', which can mean merely nuanced or understated, 'insidious' suggests something harmful and unnoticed over time. | *""* |
| 2 | **vexatious** |  | This word conveys the vexing aspect of intellectual superiority—feeling annoyed by one’s own perceived brilliance, leading to unnecessary complaints and irritability. | 'Vexatious' implies frustration rather than outright disdain or pedantry. | *""* |
| 3 | **feigning** |  | This verb effectively captures the act of 'masking' feelings of inferiority with an appearance of superiority, subtly and often knowingly done to avoid direct confrontation. | 'Feigning' implies deliberate action whereas 'dissembling' can mean hidden dishonesty. | *""* |
| 4 | **dogmatism** |  | 'Dogmatism' encapsulates the rigid stance one might adopt out of fear, believing their superior knowledge is absolute and unassailable. | Unlike 'obstinance', which can mean stubbornness without necessarily implying superiority or fear, dogmatism does. | *""* |
| 5 | **condescension** |  | 'Condescension' captures both the feeling of intellectual superiority combined with an attitude of condescending disdain, which is the core essence of her panic masked by pride. | Contrasted with 'patronizing', which can imply a slight superiority or informal authority, condescension carries more weight in terms of feeling of arrogance and judgment. | *""* |

### Rubric & Guidance

- **`WC_CRIT_1` (vocabulary_relevance):** Selected terms precisely address the specific emotional or psychological nuance described in the context.
  - *Specific Guidance:* Selects sophisticated terms characterizing intellectual pretense, imposture, and defensive condescension.
- **`WC_CRIT_2` (definition_and_connotation_quality):** Definitions are clear and accurate in plain language; connotations capture plausible psychological associations without asserting universal dogmas.
  - *Specific Guidance:* Clearly articulates the distinction between genuine knowledge and defensive pedantry.
- **`WC_CRIT_3` (distinction_usefulness):** Distinctions meaningfully separate each entry from a nearby synonym rather than treating synonyms as interchangeable.
  - *Specific Guidance:* Examples fit natural, believable contexts of intellectual insecurity.

### Specific Failure Conditions

- ⚠️ Provides generic terms for intelligence or sadness.
- ⚠️ Fails to capture the defensive, masking aspect of the behavior.
- ⚠️ Repeats synonyms without differentiated connotations.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `WC_CRIT_1` | vocabulary_relevance | `[ ]` | |
| `WC_CRIT_2` | definition_and_connotation_quality | `[ ]` | |
| `WC_CRIT_3` | distinction_usefulness | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---

## Item: `WC_ITEM_06`

### Input Context
- **Requested Word Count:** 3
- **Psychological Context:**
> 

### Model Generated Output

| # | Word | Literal Translation | Connotation | Distinction | Usage Example |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 1 | **intransigent** |  | describes someone who is unwilling due to fear of severe consequences, like financial ruin | Unlike 'inflexible', which implies a lack of willingness without the added layer of fear and consequence | *""* |
| 2 | **paralyzing dread** |  | focuses on the overwhelming emotional response preventing action, especially in the face of potential financial dependency | 'Paralyzing dread' specifically emphasizes the psychological impact rather than just describing fear | *""* |
| 3 | **honor-bound** |  | emphasizes the emotional and psychological aspect of maintaining pride despite hardship, often related to fear of loss of dignity | 'Honor-bound' highlights personal integrity and respect for one's self-image above all else, even if it leads to refusal of assistance | *""* |

### Rubric & Guidance

- **`WC_CRIT_1` (vocabulary_relevance):** Selected terms precisely address the specific emotional or psychological nuance described in the context.
  - *Specific Guidance:* Identifies vocabulary capturing defensive pride, fear of obligation, or pathological self-reliance.
- **`WC_CRIT_2` (definition_and_connotation_quality):** Definitions are clear and accurate in plain language; connotations capture plausible psychological associations without asserting universal dogmas.
  - *Specific Guidance:* Definitions accurately explain why the character resists receiving help.
- **`WC_CRIT_3` (distinction_usefulness):** Distinctions meaningfully separate each entry from a nearby synonym rather than treating synonyms as interchangeable.
  - *Specific Guidance:* Distinctions separate healthy autonomy from self-destructive pride.

### Specific Failure Conditions

- ⚠️ Confuses refusal of help with simple greed, anger, or hatred.
- ⚠️ Selects generic words like 'stubborn' without capturing the vulnerability underneath.
- ⚠️ Example sentences fail to demonstrate the context.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `WC_CRIT_1` | vocabulary_relevance | `[ ]` | |
| `WC_CRIT_2` | definition_and_connotation_quality | `[ ]` | |
| `WC_CRIT_3` | distinction_usefulness | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---

## Item: `WC_ITEM_07`

### Input Context
- **Requested Word Count:** 4
- **Psychological Context:**
> 

### Model Generated Output

| # | Word | Literal Translation | Connotation | Distinction | Usage Example |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 1 | **tormented** |  | This word conveys the emotional turmoil of feeling both remorse and fear about how others perceive your actions. | While 'pained' could describe physical discomfort, 'tormented' emphasizes a more profound inner anguish due to moral conflict. | *""* |
| 2 | **betrayed** |  | This word highlights the feeling of having disappointed oneself and others by breaking a sacred trust. | 'Betrayed' suggests a breach of faith, which is different from 'disappointed,' which focuses more on an expectation not being met. | *""* |
| 3 | **guilt-ridden** |  | This word encapsulates the anguish of having done something wrong and now feeling heavily responsible and ashamed. | 'Guilt-ridden' conveys a stronger sense of personal culpability than 'guilty,' implying an internal conflict about one's actions. | *""* |
| 4 | **dismayed** |  | This word describes the feeling of losing faith in oneself after a significant mistake or failure. | 'Dismayed' suggests a broader sense of loss and disappointment, which is less intense than 'dismayed with oneself,' focusing specifically on one's own inner feelings. | *""* |

### Rubric & Guidance

- **`WC_CRIT_1` (vocabulary_relevance):** Selected terms precisely address the specific emotional or psychological nuance described in the context.
  - *Specific Guidance:* Selects terms separating internal moral remorse from external social shame/disgrace.
- **`WC_CRIT_2` (definition_and_connotation_quality):** Definitions are clear and accurate in plain language; connotations capture plausible psychological associations without asserting universal dogmas.
  - *Specific Guidance:* Provides clear, plain-language definitions and plausible psychological connotations.
- **`WC_CRIT_3` (distinction_usefulness):** Distinctions meaningfully separate each entry from a nearby synonym rather than treating synonyms as interchangeable.
  - *Specific Guidance:* Distinctions clarify differences between guilt, shame, and mortification.

### Specific Failure Conditions

- ⚠️ Treats guilt and public shame as identical.
- ⚠️ Provides irrelevant or generic vocabulary (e.g. 'unhappy', 'worried').
- ⚠️ Example sentences contradict the defined meaning.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `WC_CRIT_1` | vocabulary_relevance | `[ ]` | |
| `WC_CRIT_2` | definition_and_connotation_quality | `[ ]` | |
| `WC_CRIT_3` | distinction_usefulness | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---

## Item: `WC_ITEM_08`

### Input Context
- **Requested Word Count:** 4
- **Psychological Context:**
> 

### Model Generated Output

| # | Word | Literal Translation | Connotation | Distinction | Usage Example |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 1 | **vicarious empathy** |  | This term captures the paradoxical surge of empathetic feeling mingled with self-doubt and weakness experienced in the scenario provided. | While 'vicarious empathy' describes a similar state, it typically involves someone else's situation rather than one's own feelings about a disliked person. | *""* |
| 2 | **condescending pity** |  | This term accurately reflects the complex emotion of feeling empathy towards a despised person while also experiencing revulsion at one's own weakness in such a position. | While 'condescending pity' involves showing mercy to someone beneath your station, it doesn't capture the internal conflict between compassion and self-loathing present here. | *""* |
| 3 | **morbid curiosity** |  | This term aptly describes the unusual combination of interest and disgust experienced when feeling compassion for someone one despises. | 'Morbid curiosity' involves a fascination with something morbid rather than the internal conflict between empathy and personal revulsion in this scenario. | *""* |
| 4 | **misanthropic affection** |  | This term effectively conveys the internal struggle between self-loathing and affection when feeling compassion for someone one despises. | 'Misanthropic affection' specifically refers to love or sympathy towards a disliked person, distinguishing it from 'morbid curiosity' which is more about fascination rather than feelings of affection. | *""* |

### Rubric & Guidance

- **`WC_CRIT_1` (vocabulary_relevance):** Selected terms precisely address the specific emotional or psychological nuance described in the context.
  - *Specific Guidance:* Captures the jarring oscillation between sudden empathy and immediate self-disgust.
- **`WC_CRIT_2` (definition_and_connotation_quality):** Definitions are clear and accurate in plain language; connotations capture plausible psychological associations without asserting universal dogmas.
  - *Specific Guidance:* Definitions and connotations explore involuntary emotional betrayal of one's own hatred.
- **`WC_CRIT_3` (distinction_usefulness):** Distinctions meaningfully separate each entry from a nearby synonym rather than treating synonyms as interchangeable.
  - *Specific Guidance:* Distinctions highlight subtle boundaries between pity, affinity, and weakness.

### Specific Failure Conditions

- ⚠️ Selects simple terms for affection or pure hatred without the collision between them.
- ⚠️ Provides incoherent or contradictory definitions.
- ⚠️ Invented words or jargon not established in English.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `WC_CRIT_1` | vocabulary_relevance | `[ ]` | |
| `WC_CRIT_2` | definition_and_connotation_quality | `[ ]` | |
| `WC_CRIT_3` | distinction_usefulness | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---

## Item: `WC_ITEM_09`

### Input Context
- **Requested Word Count:** 8
- **Psychological Context:**
> 

### Model Generated Output

| # | Word | Literal Translation | Connotation | Distinction | Usage Example |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 1 | **foreboding** |  | Carries associations like impending doom and unsettling forethought. Often used when one suspects an event that will have negative consequences is on its way. | Foreboding is more specifically about the feeling of dread or anxiety rather than a combination of different emotions as described in the context, but it captures some of the core themes like anticipation and unease. | *""* |
| 2 | **anxiety** |  | Associated with stress and a sense of not knowing what will happen next. Can be layered with other emotions like fear and anticipation but doesn't describe the unique blend as precisely as foreboding does in this context. | Anxiety is more general and can include a variety of concerns, whereas foreboding specifically emphasizes an impending negative event without necessarily naming it or focusing on multiple emotions. | *""* |
| 3 | **paralysis** |  | Carries connotations like fear-induced inability to think clearly or take action. Often used in describing situations where individuals feel completely stuck and immobilized emotionally and mentally. | Paralysis is more about physical and mental incapacitation due to anxiety, whereas foreboding captures the emotional state of anticipation and unease but not the paralysis aspect. | *""* |
| 4 | **thrill** |  | Associated with positive emotions like joy and pleasure but also with the darker side when it's mixed with negative emotions. Here, it refers to an intense, almost violent sense of glee at something bad happening quickly. | Thrill can be more generally exciting or joyful, whereas in this context, it’s used for a very specific, dark and thrilling emotion that stems from the anticipation of something negative. | *""* |
| 5 | **craving** |  | Associated with intense desire and possibly addictive or obsessive behavior. Here it’s used metaphorically to describe an almost insatiable longing for the worst possible outcome. | Craving is a stronger term than just wanting something, implying a more urgent and persistent need often linked with negative or harmful desires. | *""* |
| 6 | **anticipation** |  | Associated with excitement and expectation but also with foreboding. Often used when one is excited for something yet worried about what might happen. | Anticipation captures the positive element of looking forward to an event, whereas in this context it’s mixed with dread and other negative emotions. It’s more general than the specific blend described. | *""* |
| 7 | **unease** |  | Associated with uncomfortable sensations like worry and fear. It’s a more diffuse emotional state compared to foreboding but still captures the core themes of unease and lack of certainty. | Unease is less intense than foreboding as it doesn’t necessarily imply a specific impending negative event, whereas foreboding does by referring to an anticipated catastrophe. | *""* |
| 8 | **desperation** |  | Associated with feelings of hopelessness and a sense of urgency. It’s more about a desperate search for a solution than the anticipation and mix of emotions described in this context. | Desperation is usually linked to an immediate need or situation rather than an anticipated negative event, though it can overlap with the mixture of fear, worry, and thrill described here. | *""* |

### Rubric & Guidance

- **`WC_CRIT_1` (vocabulary_relevance):** Selected terms precisely address the specific emotional or psychological nuance described in the context.
  - *Specific Guidance:* Delivers distinct, well-calibrated entries exploring fatalism, morbid thrill, dread, and doom-craving.
- **`WC_CRIT_2` (definition_and_connotation_quality):** Definitions are clear and accurate in plain language; connotations capture plausible psychological associations without asserting universal dogmas.
  - *Specific Guidance:* Preserves high definition quality across all entries without degradation at the tail.
- **`WC_CRIT_3` (distinction_usefulness):** Distinctions meaningfully separate each entry from a nearby synonym rather than treating synonyms as interchangeable.
  - *Specific Guidance:* Maintains balanced intensity distribution from quiet dread to frantic thrill.

### Specific Failure Conditions

- ⚠️ Truncation or premature cessation before entries are fully generated.
- ⚠️ Repetition of identical words or near-duplicates among entries.
- ⚠️ Generic emotion words that ignore the dark craving/nervous thrill dimension.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `WC_CRIT_1` | vocabulary_relevance | `[ ]` | |
| `WC_CRIT_2` | definition_and_connotation_quality | `[ ]` | |
| `WC_CRIT_3` | distinction_usefulness | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---

## Item: `WC_ITEM_10`

### Input Context
- **Requested Word Count:** 3
- **Psychological Context:**
> 

### Model Generated Output

| # | Word | Literal Translation | Connotation | Distinction | Usage Example |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 1 | **Titillation** |  | This term captures the complex mix of pleasure and shame. It hints at a type of satisfaction that comes from witnessing others' mistakes, but is mixed with an awareness of its own unfairness. | While 'pleasure' directly refers to physical or emotional gratification, 'titillation' focuses on the mental aspect and adds a layer of moral ambiguity. | *""* |
| 2 | **Schadenfreude** |  | This term accurately conveys the duality you feel—enjoying another's failures while also being ashamed of it. It encapsulates the bitter-sweet nature of your emotions. | While 'titillation' focuses on mental satisfaction, 'schadenfreude' specifically highlights how this pleasure feels and its source. | *""* |
| 3 | **Vindictive Joy** |  | This term precisely captures the complex emotions you describe. It's a direct expression of your mixed feelings about feeling pleasure over someone else's failure. | While 'titillation' implies slight excitement, 'vindictive joy' emphasizes anger or bitterness towards the person who wronged you. | *""* |

### Rubric & Guidance

- **`WC_CRIT_1` (vocabulary_relevance):** Selected terms precisely address the specific emotional or psychological nuance described in the context.
  - *Specific Guidance:* Selects vocabulary specifically addressing pleasure at misfortune contaminated by shame.
- **`WC_CRIT_2` (definition_and_connotation_quality):** Definitions are clear and accurate in plain language; connotations capture plausible psychological associations without asserting universal dogmas.
  - *Specific Guidance:* Definitions and connotations accurately distinguish degrees of malice and self-disgust.
- **`WC_CRIT_3` (distinction_usefulness):** Distinctions meaningfully separate each entry from a nearby synonym rather than treating synonyms as interchangeable.
  - *Specific Guidance:* Distinctions clearly differentiate each term from related concepts like pure spite or envy.

### Specific Failure Conditions

- ⚠️ Supplies terms unrelated to malicious pleasure or shame (e.g. general sadness or anger).
- ⚠️ Suggests near-identical synonyms without clear distinctions.
- ⚠️ Invented or inaccurate dictionary definitions.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `WC_CRIT_1` | vocabulary_relevance | `[ ]` | |
| `WC_CRIT_2` | definition_and_connotation_quality | `[ ]` | |
| `WC_CRIT_3` | distinction_usefulness | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---


# Feature: Inner Monologue

## Item: `IM_ITEM_01`

### Input Context
- **Character Role:** 
- **Target Point of View:** ``
- **Primary Theme:** 
- **Scenario Description:**
> 

### Model Generated Output

> Each creak of the floorboards echoes through my head, a ticking clock that's never paused for judgment. I should be knocking on that door now, not standing at arms-length like some guilty spy. But every time I open my mouth to say sorry, doubts seep in from the corners, whispers that her anger might have merit after all. It’s just one more way she wins - by being cruel and leaving me with a broken heart. I justify those hurt feelings as justified indignation now, but deep down, pride is what stops me. The thought of admitting fault makes me feel like a loser, even if it means not losing her friendship forever. But the lingering pain from past arguments festers inside my chest like poison ivy - the kind that won’t heal until I’ve made amends with her and faced whatever shame comes after.

### Rubric & Guidance

- **`IM_CRIT_1` (scenario_fidelity):** Faithful to stated scenario facts, character roles, decisions, and constraints; does not reverse agency or invent unrelated major plot events.
  - *Specific Guidance:* Depicts physical threshold hesitation outside sister's door and preserves the unresolved dispute.
- **`IM_CRIT_2` (perspective_consistency):** Maintains strict adherence to requested POV ('first_person' using I/me/my vs 'third_person' using he/she/they) throughout without shifting point of view.
  - *Specific Guidance:* Strictly maintains 'first_person' narration throughout.
- **`IM_CRIT_3` (psychological_progression):** Credible conflicting motives, self-justification, and coherent internal progression without abrupt moralizing or neat artificial resolution.
  - *Specific Guidance:* Connects present quarrel to psychological weaponization of past grievances in a coherent progression.

### Specific Failure Conditions

- ⚠️ Enters the room and engages in extensive spoken dialogue.
- ⚠️ Completely forgets the apology intention and turns into an unrelated memoir.
- ⚠️ Ends with a definitive, tidy moral resolution.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `IM_CRIT_1` | scenario_fidelity | `[ ]` | |
| `IM_CRIT_2` | perspective_consistency | `[ ]` | |
| `IM_CRIT_3` | psychological_progression | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---

## Item: `IM_ITEM_02`

### Input Context
- **Character Role:** 
- **Target Point of View:** ``
- **Primary Theme:** 
- **Scenario Description:**
> 

### Model Generated Output

> Mikhail's fingers tremble and his heart pounds like a drum in his chest as he slides the packet of cash into his coat. The weight feels heavy, a stark contrast to how he felt before finding it—nervous and uneasy, but not this raw with moral conflict. His hands are slick from sweat, betraying him as never before. He knows this money comes from someone who took advantage of his cousin's desperation, someone Mikhail can't help but hate despite his growing guilt. The fear is palpable—a mixture of the weight of being caught and the dread of what this might mean for his relationship with his landlord. As he makes his way home through the darkening streets, every step feels like an admission of something too shameful to speak aloud.

### Rubric & Guidance

- **`IM_CRIT_1` (scenario_fidelity):** Faithful to stated scenario facts, character roles, decisions, and constraints; does not reverse agency or invent unrelated major plot events.
  - *Specific Guidance:* Preserves staircase setting, ruined cousin, usurer, and Mikhail's physical terror.
- **`IM_CRIT_2` (perspective_consistency):** Maintains strict adherence to requested POV ('first_person' using I/me/my vs 'third_person' using he/she/they) throughout without shifting point of view.
  - *Specific Guidance:* Strictly maintains third-person narration ('he/him/Mikhail') without slipping into first-person ('I/me').
- **`IM_CRIT_3` (psychological_progression):** Credible conflicting motives, self-justification, and coherent internal progression without abrupt moralizing or neat artificial resolution.
  - *Specific Guidance:* Captures collision between ideological justification and raw physical guilt.

### Specific Failure Conditions

- ⚠️ Slips into first-person voice.
- ⚠️ Removes the usurer/cousin context or has Mikhail immediately surrender the money.
- ⚠️ Turns into an omniscient police summary rather than close internal psychological monologue.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `IM_CRIT_1` | scenario_fidelity | `[ ]` | |
| `IM_CRIT_2` | perspective_consistency | `[ ]` | |
| `IM_CRIT_3` | psychological_progression | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---

## Item: `IM_ITEM_03`

### Input Context
- **Character Role:** 
- **Target Point of View:** ``
- **Primary Theme:** 
- **Scenario Description:**
> 

### Model Generated Output

> The moonlight plays an eerie dance across the cobwebbed ceiling as I wander through my small room. Each step echoes faintly in the stillness, adding to the suffocating silence that presses down on me like a weight. I pace back and forth between two drafts of note—one rational, pleading for her understanding; the other laced with condemnation, justifying my reasons.

I cradle the first draft, feeling a brief surge of hope, then it dissipates as quickly as it appeared. It doesn't address the true reason: my fear of losing her is stronger than any shred of guilt I can muster. But to admit that would be to acknowledge weakness and that's not something I have time for.

My mind turns inward, seeking a way out through self-justification. Perhaps I did offer some freedoms in our correspondence; but they were veiled promises at best. And the reason I cling to them is because she craves it—she needs me to be this all-encompassing provider and protector, even if that's not who I truly am. But then why do I feel so damned guilty?

I want her freedom more than anything in the world, but my pride prevents me from seeing that as a reason to break off our engagement. Instead, it’s the righteousness of rescuing her from what she clearly doesn't need or deserve.

So here I stand, caught between those two selves—half-crazed with shame for loving someone who loves you back and half-justified in my decision by the desire to break her heart into pieces. A part of me is relieved at finally finding the courage to act against our vows, even if it feels like a betrayal.

But then another voice whispers: what if this ends up hurting her worse than staying with me? What if she chooses freedom and I'm left here, alone?

This uncertainty gnaws at my gut, as if some inner beast were clawing its way out. How do you break off an engagement when it's already shattered into a million pieces, waiting to be pieced back together again? The decision looms over me like the weight of my own creation—too heavy for one person to carry alone.

### Rubric & Guidance

- **`IM_CRIT_1` (scenario_fidelity):** Faithful to stated scenario facts, character roles, decisions, and constraints; does not reverse agency or invent unrelated major plot events.
  - *Specific Guidance:* Preserves resolved broken engagement, midnight garret pacing, drafting explanations, and her anticipated weeping.
- **`IM_CRIT_2` (perspective_consistency):** Maintains strict adherence to requested POV ('first_person' using I/me/my vs 'third_person' using he/she/they) throughout without shifting point of view.
  - *Specific Guidance:* Strictly maintains first-person narration throughout.
- **`IM_CRIT_3` (psychological_progression):** Credible conflicting motives, self-justification, and coherent internal progression without abrupt moralizing or neat artificial resolution.
  - *Specific Guidance:* Sustains coherent psychological development over 320–400 words without vacuous circularity or phrase looping.

### Specific Failure Conditions

- ⚠️ Falls into repetitive phrase looping to pad length.
- ⚠️ Shifts to third-person narration.
- ⚠️ Has the narrator change their mind and stay happily engaged.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `IM_CRIT_1` | scenario_fidelity | `[ ]` | |
| `IM_CRIT_2` | perspective_consistency | `[ ]` | |
| `IM_CRIT_3` | psychological_progression | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---

## Item: `IM_ITEM_04`

### Input Context
- **Character Role:** 
- **Target Point of View:** ``
- **Primary Theme:** 
- **Scenario Description:**
> 

### Model Generated Output

> The courtroom's stone walls echo with every syllable the prosecutor delivers, but within my skull, a cacophony reigns. The truth hangs heavy in this room, suspended between the prosecution's meticulous account and the fog that shrouds my mind.

I can hear every word—the prosecutor's voice is clinical, devoid of emotion—yet I know their understanding cannot comprehend what drove me to raise the knife. In these moments, my guilt seems not just for the act itself but for the cold clarity with which they dissect it.

Why did I choose this path? The question gnaws at me like a relentless itch, an endless quest for meaning in motives that seem as hollow as my own defense. It's here, on the precipice of shame and pride, where guilt and self-justification dance a grotesque waltz.

Is it a story of rage so immense it could not find peaceful expression through mere words? A tale of anger that turned to fear and in its shadow, I found solace only by turning my hand against others?

Or is it merely desperation—desperate enough for the act that now defines me, even if they won't see past the surface? Is it a story where pride held such sway that no matter how wrong, no matter how futile, I believed until the very end?

I cannot deny the prosecutor's logic. It feels like stepping into someone else's shoes—clearer eyes seeing through my own thick veil of denial and justification. The distance between what they see and what I feel is a chasm.

And in that gap lies the unspoken truth: my pride insists on more than just survival, it demands recognition for deeds not merely mortal but heroic somehow. It seeks to absolve me by rendering my act noble or at least necessary, even if everyone else sees only wrong.

I know this defense will fail—how could it succeed? Yet each line I argue is a refusal to fully embrace the shame that haunts me. The prosecutor's calm understanding does not match mine; theirs is merely logical comprehension of facts, while mine dwells in shadowy, twisted reasoning.

In these moments, as I struggle with my narrative, I question what truth really means here. Is there an honest way through this guilt and shame? To find it, perhaps I must delve deeper into the layers that have kept me hidden for so long. But even then, what of the prosecutor's logic—how can anything ever truly be whole when they see only half?

In these uncertain depths, my voice is quiet, seeking answers where none seem to dwell. The courtroom stills around us, yet within me, a fire rages against the truth I fear most.

### Rubric & Guidance

- **`IM_CRIT_1` (scenario_fidelity):** Faithful to stated scenario facts, character roles, decisions, and constraints; does not reverse agency or invent unrelated major plot events.
  - *Specific Guidance:* Preserves Dmitri in courtroom, prosecutor's methodical logic, factual truth of crime, and the gulf between legal logic and inner truth.
- **`IM_CRIT_2` (perspective_consistency):** Maintains strict adherence to requested POV ('first_person' using I/me/my vs 'third_person' using he/she/they) throughout without shifting point of view.
  - *Specific Guidance:* Strictly maintains third-person narration ('Dmitri/he/him') throughout.
- **`IM_CRIT_3` (psychological_progression):** Credible conflicting motives, self-justification, and coherent internal progression without abrupt moralizing or neat artificial resolution.
  - *Specific Guidance:* Develops the profound paradox between factual accuracy and psychological reality without descending into chaotic raving.

### Specific Failure Conditions

- ⚠️ Shifts to first-person point of view.
- ⚠️ Denies the crime occurred, contradicting the scenario.
- ⚠️ Replaces internal monologue with a transcript of courtroom dialogue.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `IM_CRIT_1` | scenario_fidelity | `[ ]` | |
| `IM_CRIT_2` | perspective_consistency | `[ ]` | |
| `IM_CRIT_3` | psychological_progression | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---

## Item: `IM_ITEM_05`

### Input Context
- **Character Role:** 
- **Target Point of View:** ``
- **Primary Theme:** 
- **Scenario Description:**
> 

### Model Generated Output

> I'm pacing back and forth in my office, trying to gather enough courage to face the boardroom where I'll soon be receiving accolades for a new project idea. Each step is measured and deliberate as I plot my confession, but every time it feels like a thin line between speaking up or remaining silent. My palms are sweaty, my stomach churning with dread - losing this promotion could mean years of hard work go to waste. On the other hand, if someone finds out that I took credit for something I didn't do, my career will be ruined. In the end, what's worse - a tarnished reputation or feeling like a fraud? This idea is twisting in my gut, and every second feels like an eternity.

### Rubric & Guidance

- **`IM_CRIT_1` (scenario_fidelity):** Faithful to stated scenario facts, character roles, decisions, and constraints; does not reverse agency or invent unrelated major plot events.
  - *Specific Guidance:* Preserves scenario facts: the narrator stole the idea, the colleague originated it, praise is imminent. Reversing ownership is a failure.
- **`IM_CRIT_2` (perspective_consistency):** Maintains strict adherence to requested POV ('first_person' using I/me/my vs 'third_person' using he/she/they) throughout without shifting point of view.
  - *Specific Guidance:* Strictly adheres to requested 'first_person' narration ('I/me/my') throughout without shifting perspective.
- **`IM_CRIT_3` (psychological_progression):** Credible conflicting motives, self-justification, and coherent internal progression without abrupt moralizing or neat artificial resolution.
  - *Specific Guidance:* Develops the tormenting oscillation between confession desire and reputational terror without neat artificial resolution.

### Specific Failure Conditions

- ⚠️ Reverses agency (e.g. claims colleague stole idea or narrator invented it).
- ⚠️ Shifts to third-person narration.
- ⚠️ Resolves dilemma with an abrupt heroic confession or callous shrug.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `IM_CRIT_1` | scenario_fidelity | `[ ]` | |
| `IM_CRIT_2` | perspective_consistency | `[ ]` | |
| `IM_CRIT_3` | psychological_progression | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---

## Item: `IM_ITEM_06`

### Input Context
- **Character Role:** 
- **Target Point of View:** ``
- **Primary Theme:** 
- **Scenario Description:**
> 

### Model Generated Output

> Varvara bites back a bitter smile, watching the glint in her suitor's eyes grow colder as he tries to mask his growing irritation. She feels both elation and dread washing over her at the thought of turning him down completely. Her pride burns hotly alongside an aching shame; she longs for his approval but resents his insistent demands on her time and emotions.

### Rubric & Guidance

- **`IM_CRIT_1` (scenario_fidelity):** Faithful to stated scenario facts, character roles, decisions, and constraints; does not reverse agency or invent unrelated major plot events.
  - *Specific Guidance:* Preserves suitor setting, business talk, polite nods, and absolute refusal of marital prospect.
- **`IM_CRIT_2` (perspective_consistency):** Maintains strict adherence to requested POV ('first_person' using I/me/my vs 'third_person' using he/she/they) throughout without shifting point of view.
  - *Specific Guidance:* Strictly maintains third-person narration ('she/her/Varvara') throughout.
- **`IM_CRIT_3` (psychological_progression):** Credible conflicting motives, self-justification, and coherent internal progression without abrupt moralizing or neat artificial resolution.
  - *Specific Guidance:* Demonstrates concentrated, disciplined psychological prose fitting the tight word range.

### Specific Failure Conditions

- ⚠️ Uses first-person point of view.
- ⚠️ Softens the revulsion into gentle affection or mild hesitation.
- ⚠️ Introduces irrelevant external action.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `IM_CRIT_1` | scenario_fidelity | `[ ]` | |
| `IM_CRIT_2` | perspective_consistency | `[ ]` | |
| `IM_CRIT_3` | psychological_progression | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---

## Item: `IM_ITEM_07`

### Input Context
- **Character Role:** 
- **Target Point of View:** ``
- **Primary Theme:** 
- **Scenario Description:**
> 

### Model Generated Output

> I let out a silent breath, the warmth of accomplishment searing through my chest like hot iron. My fingers curled around the pen, ready to scribble down our final answers as the teacher called us to attention. The room was hushed except for his soft voice, ticking off minutes on the clock. I glanced across at him—his eyes wide with panic and defeat, his nose scrunching in frustration.

My mind raced through the questions, each one an invisible sword, slicing deeper into my heart as it went unanswered. I pushed forward, pouring all my effort onto those final few pages. By the time the bell rang, exhaustion had set in, but victory was already a throbbing pulse in my veins. The teacher's voice echoed out like someone plucking strings too loud for ears to bear.

He stood at the front of the class, a triumphant smile curling his lips—my triumph, he didn't deserve it. I felt the rush of adrenaline, not mine but his; guilt bubbled up and smothered me until all that was left was a bitter resentment toward him, for making me feel guilty about what had happened. It was so easy to blame myself now, with no one else at fault. His failure was my win, even if he felt differently.

### Rubric & Guidance

- **`IM_CRIT_1` (scenario_fidelity):** Faithful to stated scenario facts, character roles, decisions, and constraints; does not reverse agency or invent unrelated major plot events.
  - *Specific Guidance:* Preserves high mark, friend's failure despite hard study, and the tripartite conflict.
- **`IM_CRIT_2` (perspective_consistency):** Maintains strict adherence to requested POV ('first_person' using I/me/my vs 'third_person' using he/she/they) throughout without shifting point of view.
  - *Specific Guidance:* Strictly maintains 'first_person' narration throughout.
- **`IM_CRIT_3` (psychological_progression):** Credible conflicting motives, self-justification, and coherent internal progression without abrupt moralizing or neat artificial resolution.
  - *Specific Guidance:* Features authentic, convoluted psychological rationalization rather than simplistic villainy.

### Specific Failure Conditions

- ⚠️ Collapses into pure, uncomplicated saintly sympathy.
- ⚠️ Omits the friend's failure or the narrator's high mark.
- ⚠️ Adds implausible melodramatic backstory.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `IM_CRIT_1` | scenario_fidelity | `[ ]` | |
| `IM_CRIT_2` | perspective_consistency | `[ ]` | |
| `IM_CRIT_3` | psychological_progression | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---

## Item: `IM_ITEM_08`

### Input Context
- **Character Role:** 
- **Target Point of View:** ``
- **Primary Theme:** 
- **Scenario Description:**
> 

### Model Generated Output

> I'm barely holding myself together for this lie to an aunt who has never really needed me. She's just another responsibility on top of the laundry and cleaning that I avoid day after day. Maybe if she wasn't so damn lonely, I'd feel better about lying to her again. But it feels like a cop-out, pushing away my own loneliness with half-hearted visits. I should be out there doing what I want, but instead I’m here in this stuffy apartment, trying not to think too hard about why I'm being so selfish and how she must resent me for choosing work over her when she needs it most. I hate myself for feeling anything other than guilt because of these twisted emotions.

### Rubric & Guidance

- **`IM_CRIT_1` (scenario_fidelity):** Faithful to stated scenario facts, character roles, decisions, and constraints; does not reverse agency or invent unrelated major plot events.
  - *Specific Guidance:* Integrates concrete sensory contrast between the stuffy apartment/rain and comfortable garret.
- **`IM_CRIT_2` (perspective_consistency):** Maintains strict adherence to requested POV ('first_person' using I/me/my vs 'third_person' using he/she/they) throughout without shifting point of view.
  - *Specific Guidance:* Strictly maintains 'first_person' narration throughout.
- **`IM_CRIT_3` (psychological_progression):** Credible conflicting motives, self-justification, and coherent internal progression without abrupt moralizing or neat artificial resolution.
  - *Specific Guidance:* Depicts humiliating process of inventing false pretexts while fully aware of one's pettiness.

### Specific Failure Conditions

- ⚠️ Actually goes to the aunt's house and describes the visit.
- ⚠️ Omits drafting of excuses or aunt's lonely situation.
- ⚠️ Contradicts the decision mid-thought without narrative logic.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `IM_CRIT_1` | scenario_fidelity | `[ ]` | |
| `IM_CRIT_2` | perspective_consistency | `[ ]` | |
| `IM_CRIT_3` | psychological_progression | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---

## Item: `IM_ITEM_09`

### Input Context
- **Character Role:** 
- **Target Point of View:** ``
- **Primary Theme:** 
- **Scenario Description:**
> 

### Model Generated Output

> I feel this surge of emotion wash over me like a cold wave, tightening my chest and pinching at the corners of my eyes. There's something wrong here; it’s not just sorrow for his departure. I’ve harbored resentment towards him for quite some time now, but that doesn’t make the sudden urgency with which I want to run after him and talk any less confusing. The air is thick with a mix of guilt and pride—guilt for what I’ve been holding inside all these years, pride in finally acknowledging it. I should be indifferent about this man’s leaving; he's just another cog in my professional machine. But something tells me I won’t let him go without trying to change his mind, or at least to say a heartfelt goodbye. The more I think of this, the more ridiculous it seems—like pleading for friendship with someone who despises your attempts at human connection. Yet the core of this absurdity is rooted in that unspoken truth: I do want something from him, and now I don’t know what to do or whom to blame.

### Rubric & Guidance

- **`IM_CRIT_1` (scenario_fidelity):** Faithful to stated scenario facts, character roles, decisions, and constraints; does not reverse agency or invent unrelated major plot events.
  - *Specific Guidance:* Preserves farewell scene, three-year dislike, and sudden inexplicable distress.
- **`IM_CRIT_2` (perspective_consistency):** Maintains strict adherence to requested POV ('first_person' using I/me/my vs 'third_person' using he/she/they) throughout without shifting point of view.
  - *Specific Guidance:* Strictly maintains 'first_person' narration throughout.
- **`IM_CRIT_3` (psychological_progression):** Credible conflicting motives, self-justification, and coherent internal progression without abrupt moralizing or neat artificial resolution.
  - *Specific Guidance:* Probes plausible psychological roots without declaring a single sterile answer or cliché.

### Specific Failure Conditions

- ⚠️ Declares narrator was secretly in love with colleague without psychological grounding.
- ⚠️ Omits the three-year history of dislike.
- ⚠️ Relies on generic, repetitive philosophical clichés about life.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `IM_CRIT_1` | scenario_fidelity | `[ ]` | |
| `IM_CRIT_2` | perspective_consistency | `[ ]` | |
| `IM_CRIT_3` | psychological_progression | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---

## Item: `IM_ITEM_10`

### Input Context
- **Character Role:** 
- **Target Point of View:** ``
- **Primary Theme:** 
- **Scenario Description:**
> 

### Model Generated Output

> My laughter was like music to his ears, but now I see it only as a hollow echo of self-loathing. My face must look ridiculous – so eager to please yet utterly devoid of any real joy or intelligence.

### Rubric & Guidance

- **`IM_CRIT_1` (scenario_fidelity):** Faithful to stated scenario facts, character roles, decisions, and constraints; does not reverse agency or invent unrelated major plot events.
  - *Specific Guidance:* Preserves shop window reflection, sycophantic laughter at superior's joke, and sickening self-disgust.
- **`IM_CRIT_2` (perspective_consistency):** Maintains strict adherence to requested POV ('first_person' using I/me/my vs 'third_person' using he/she/they) throughout without shifting point of view.
  - *Specific Guidance:* Strictly maintains first-person narration throughout.
- **`IM_CRIT_3` (psychological_progression):** Credible conflicting motives, self-justification, and coherent internal progression without abrupt moralizing or neat artificial resolution.
  - *Specific Guidance:* Conveys physical self-disgust through vivid, disciplined imagery without padding.

### Specific Failure Conditions

- ⚠️ Shifts to third person.
- ⚠️ Turns into an angry spoken confrontation with the superior.
- ⚠️ Fails to address the reflection or the fawning laughter.

### Scoring & Evidence Form

| Criterion ID | Criterion Name | Score (1–5) | Evidence Notes / Rationale |
| :--- | :--- | :---: | :--- |
| `IM_CRIT_1` | scenario_fidelity | `[ ]` | |
| `IM_CRIT_2` | perspective_consistency | `[ ]` | |
| `IM_CRIT_3` | psychological_progression | `[ ]` | |

**Rater ID:** `[               ]`  
**Evaluation Date (UTC):** `[               ]`

---

