# Data acquisition and integration — Plan

**Projet :** `toporep-data-acquisition-and-integration`  
**Référence :** Irham L.M., Adikusuma W. *Harnessing Multi-OMICS Data to Accelerate Drug Repurposing*. IntechOpen. https://www.intechopen.com/online-first/1253251

**Stockage :** uniquement des jeux **processed** (artefacts prêts à l’intégration), sur le modèle Bai et al. (tables / matrices curées + métadonnées de version). Pas de sous-dossiers `raw/`.

---

## 1. Objectif

Produire une **représentation cohérente** multi-couches via :

| Opération | Contenu |
|-----------|---------|
| Quality control | Filtres échantillons, features, métadonnées |
| Normalisation | Protocoles par plateforme (RNA-seq, microarray, L1000, …) |
| Batch-effect correction | Correction inter-études / inter-plateformes |
| Feature harmonization | Entrez · Ensembl · UniProt · InChIKey · LINCS pert_id |

**Livrable :** `integration/` (registre d’IDs, graphes, matrices, rapport de mapping).

---

## 2. Couches de données

| Couche | Bases |
|--------|-------|
| Transcriptomique / génomique maladie | TCGA, GEO, ArrayExpress, Expression Atlas |
| Référence tissus normaux | GTEx |
| Perturbation médicament | LINCS / CMap |
| Pharmacogénomique cellulaire | CCLE, GDSC, DepMap |
| Drug–gène / cibles | DGIdb, TTD, ChEMBL, BindingDB, STITCH |
| Bioactivité / structures | ChEMBL, BindingDB, UniProt, PDB / AlphaFold |
| Réseaux & sécurité | STITCH, SIDER |
| Pathways | KEGG, Reactome |
| Clinique / gène–maladie | PharmGKB, ClinicalTrials.gov, Hetionet, PrimeKG, TTD |

---

## 3. Filtrages / amputations (oui)

Des exclusions systématiques sont prévues ; chaque script les documente en tête de module (motif + critère + effet sur N).

| Domaine | Exclusion typique |
|---------|-------------------|
| Bioactivité (style Bai) | IC50 hors seuils (+/−) ; drogues mono-étiquette ; paires / SMILES invalides |
| Omique expression | Échantillons QC insuffisant ; gènes / features à couverture trop faible ; séries GEO hors labels catalogue |
| LINCS | Perturbations / doses hors QC ; lignées sans métadonnée utilisable |
| Pharmacogénomique | Lignées ou scores manquants ; mapping d’ID impossible |
| Drug–gène | Doublons ; cibles / composés sans ID harmonisable |
| Intégration | Nœuds orphelins après mapping InChIKey / UniProt / Entrez |

Traçabilité : `VERSION.txt` (URL, date, checksum) + compteurs avant/après dans le rapport d’intégration.

---

## 4. Exécution

### 4.1 Cadre

| # | Livrable | Statut |
|---|----------|--------|
| A1 | Inventaire des bases | Fait |
| A2 | Arborescence `data/<base>/` (processed only) | Fait |
| A3 | Registre d’URLs d’accès | Fait |

### 4.2 Acquisition → processed

**Stratégie TOPOREP :** explorer **l’ensemble** des catalogues déjà structurés (tous les types TCGA, tous les tissus GTEx standardisés, panel LINCS / DepMap étiquetés indication–tissu). Le volume se gère par **artefacts processed** et filtrages QC, pas par un sous-choix a priori d’une seule indication. **GEO / ArrayExpress** : seules les séries alignées sur les labels indication/tissu déjà présents dans TCGA–GTEx–DepMap–LINCS au moment de l’acquisition.

| Ordre | Bases | Artefact stocké |
|------:|-------|-----------------|
| 1 | DGIdb, TTD | Tables interactions + IDs natifs |
| 2 | SIDER, STITCH | Edge lists filtrées |
| 3 | DepMap, CCLE, GDSC | Matrices expression / sensibilité (+ métadonnées lignée) |
| 4 | LINCS / CMap | Signatures Level 5 (panel lignées standard) |
| 5 | GEO, ArrayExpress | Séries ciblées via labels indication/tissu du catalogue |
| 6 | GTEx | Matrices par tissus standardisés |
| 7 | TCGA | Matrices + clinical (tous types tumoraux du catalogue) |
| 8 | Expression Atlas | Exports curés |
| 9 | KEGG, Reactome | GMT / graphe |
| 10 | PharmGKB, ClinicalTrials.gov | Tables filtrées |
| — | ChEMBL, BindingDB, UniProt, AlphaFold | Réutilisation des acquisitions existantes |

Par base, sous `data/<base>/` :

```
VERSION.txt
features.parquet|csv
sample_metadata.csv   # si applicable
id_map.csv
qc_summary.md         # N avant/après, critères d’exclusion
```

### 4.3 Intégration

| Artefact | Contenu |
|----------|---------|
| `integration/registry_ids.csv` | Clés natives (plus de nom LINCS ni de label GEO dans `gene_symbol`) |
| `integration/entities_compounds.csv` | Une ligne par composé ; InChIKey, sinon PubChem, sinon natif |
| `integration/entities_genes.csv` | Une ligne par gène ; HGNC et accession UniProt |
| `integration/graph_drug_target.edgelist` | Arêtes à identifiants stables (330 143 acceptées) |
| `integration/graph_drug_se.edgelist` | SIDER relié au même composé via STITCH / PubChem |
| `integration/graph_gene_disease.edgelist` | Hetionet DaG / DuG / DdG |
| `integration/INTEGRATION_REPORT.md` | Mapping, pertes d’IDs, versions |

**État :** registre et graphes d'amorce existent. `graph_gene_disease.edgelist` et `matrices/` sont spécifiés dans la conception, pas encore produits. Versions et URLs des bases actives sont traçables.

---

## 5. Prochaines actions

1. ~~Figer indication / tissu~~ **stratégie explore-all** (catalogues structurés ; GEO filtré a posteriori).  
2. ~~Acquisition DGIdb, TTD, SIDER, STITCH~~ **fait**.  
3. ~~Amorcer `integration/registry_ids.csv`~~ **fait**.  
4. ~~DepMap / CCLE / GDSC, LINCS, GTEx, TCGA, pathways, clinique~~ **fait**.  
5. ~~GEO (180 séries), LINCS Level 5, ArrayExpress (40 JSON), Expression Atlas (30 expériences)~~ **fait**.  
6. ~~Traçabilité et contrôle qualité~~ **validés** (`integration/VALIDATION_TRACE_QC.md`).  
7. ~~Harmonisation des identifiants (registre, entités, graphes)~~ **fait** (`harmonize_entities.py`, `INTEGRATION_REPORT.md`). Normalisation d'expression et batch : conception seulement, pas d'implémentation.  
8. Téléchargements encore ouverts, hors de cette validation : matrices ArrayExpress `E-*` et LINCS phase II (`scripts/additionnal_downloads/`). L'archive PDB complète n'est pas un objectif.
