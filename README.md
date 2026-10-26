# TOPOREP — Data acquisition and integration

Collecte et intégration multi-OMICS : quality control, normalisation, correction de batch, harmonisation des features.

Stockage : **processed only** (comme les artefacts Bai — tables / matrices curées + métadonnées de version).

**Référence :** Irham L.M., Adikusuma W. *Harnessing Multi-OMICS Data to Accelerate Drug Repurposing*. IntechOpen. https://www.intechopen.com/online-first/1253251

| Document | |
|----------|--|
| Plan | [`PLAN.md`](PLAN.md) |
| Inventaire | [`INVENTAIRE.md`](INVENTAIRE.md) |
| Qualification phase 1 | [`QUALIFICATION_PHASE_1.md`](QUALIFICATION_PHASE_1.md) |
| URLs | [`urls.env`](urls.env) |

```
toporep-data-acquisition-and-integration/
├── PLAN.md
├── INVENTAIRE.md
├── urls.env
├── integration/
├── _meta/
└── data/<base>/          # artefacts processed + VERSION.txt / qc_summary.md
```

| Étape | Statut |
|-------|--------|
| Inventaire & arborescence | Fait |
| Acquisition des bases actives | Fait |
| Traçabilité et contrôle qualité | Validés le 2026-10-13 (`integration/VALIDATION_TRACE_QC.md`) |
| Harmonisation des identifiants | Fait (`entities_compounds.csv`, graphes reconstruits) |
| Normalisation d'expression et batch | Conception écrite, pas implémentée (`CONCEPTION_NORMALISATION_HARMONISATION.md`) |
