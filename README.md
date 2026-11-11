# protac degradation prediction

## project goal

investigate whether pretrained protein representations improve protac degradation prediction for **unseen protein targets**.

**main question:** do esm-2 target embeddings improve held-out-target performance compared with molecule-only models?

planned models:
- xgboost + morgan fingerprints
- pytorch mlp + morgan fingerprints
- pytorch multimodal model + morgan fingerprints + esm-2 + e3 context

primary metric: **mcc on held-out targets**

---

## reference paper: se(3)-protacs

se(3)-protacs combines 3d protac representations with esm-2 protein embeddings to predict degradation.

they define a good degrader as:

```text
dc50 <= 100 nm AND dmax >= 80%
```

key results:

| split | auroc | mcc |
|---|---:|---:|
| random | 0.871 | 0.607 |
| cold target | 0.650 | 0.326 |
| temporal | 0.701 | 0.318 |

main takeaway: performance drops substantially on unseen targets, suggesting random splits overestimate real-world generalization.

**our approach:** focus specifically on this generalization gap and test whether esm-2 target representations improve held-out-target performance without reproducing the full se(3) architecture.

---

## data summary

protac-db export:

```text
rows: 15,502
columns: 89
unique raw smiles: 10,728
unique canonical smiles: 10,728
```

### e3 distribution

```text
crbn       10,862
vhl         3,947
ciap1         152
mdm2           87
dcaf11         86
```

dataset is strongly dominated by crbn and vhl.

### top targets

```text
eralpha    713
brd4       533
btk        501
ar         417
tau        362
ar-v7      294
```

---

## degradation measurement cleaning

dc50 and dmax contain exact values, bounds, ranges, repeated measurements, and missing values.

examples:

```text
5
<5
<=100
>1000
10~100
>5 and <50
87/66
n.d.
```

created `parsing.py` to classify measurements as:

```text
exact
lower_bound
upper_bound
range
multiple
missing
unparsed
```

### parser summary

| type | dc50 | dmax |
|---|---:|---:|
| missing | 12,001 | 13,177 |
| exact | 2,277 | 1,586 |
| lower bound | 402 | 327 |
| upper bound | 399 | 41 |
| multiple | 360 | 216 |
| range | 60 | 153 |
| unparsed | 3 | 2 |

only **5 values remain unparsed**.

important decisions:
- preserve censored measurements rather than coercing them to numbers
- do not average repeated measurements such as `87/66`
- preserve raw values
- leave ambiguous/corrupted values as `unparsed`

---

## molecular structure cleaning

used rdkit to parse and canonicalize all smiles.

```text
missing raw smiles: 0
failed rdkit parses: 0
unique raw smiles: 10,728
unique canonical smiles: 10,728
```

canonicalization did not reveal additional duplicate structures.

### compound id issue

```text
10,722 compound ids -> 1 structure
3 compound ids      -> 2 structures
```

affected ids:

```text
4151
5363
5369
```

the structures are genuinely different, not alternative smiles representations.

**decision:** use canonical smiles as molecular identity for modeling; retain compound id only as source metadata.

---

## other data decisions

- compound id identifies a protac database entry, not a unique experiment
- repeated rows may represent different targets, variants, assays, or cell contexts
- do not automatically aggregate repeated observations
- preserve both `target` and `uniprot`
- multiple target variants can share one canonical uniprot id
- some missing uniprot ids correspond to fusion proteins or other complex targets and may require special handling before esm-2

---

## pending: degradation labels

final labels have **not been chosen yet**.

reference definition:

```text
good degrader:
dc50 <= 100 nm AND dmax >= 80%
```

options to evaluate:

1. standard binary threshold
2. high-confidence positive/negative labels with ambiguous observations excluded

before choosing, compare:
- labeled sample count
- positive/negative balance
- unique targets retained
- target frequency
- feasibility of held-out-target evaluation

---

## current status

- [x] initial protac-db exploration
- [x] dc50/dmax format audit
- [x] degradation measurement parser
- [x] parser validation
- [x] rdkit smiles validation
- [x] smiles canonicalization
- [x] compound id / molecular identity audit
- [ ] degradation label definition
- [ ] model-ready dataset
- [ ] held-out-target split
- [ ] morgan fingerprints
- [ ] xgboost baseline
- [ ] esm-2 embeddings
- [ ] pytorch models
- [ ] unseen-target evaluation
