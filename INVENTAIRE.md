# Inventaire des bases — Data acquisition and integration

**Projet :** `toporep-data-acquisition-and-integration`  
**Référence :** Irham L.M., Adikusuma W. *Harnessing Multi-OMICS Data to Accelerate Drug Repurposing*. IntechOpen. https://www.intechopen.com/online-first/1253251

Stockage : **processed only** (artefacts curés + `VERSION.txt` / `qc_summary.md`).

Étiquetage : Base | Type | Usage TOPOREP | Couche | Dossier | Statut | Accès.

*Tour conformité : 2026-09-19 — audit `scripts/_audit_tour.py` + acquire ArrayExpress corrigé.*

---

## Tableau maître

| Base de données | Type de données | Usage principal dans TOPOREP | Couche pipeline | Dossier `data/` | Statut local | Accès |
| --- | --- | --- | --- | --- | --- | --- |
| **TCGA** | Génomique, transcriptomique (cancer) | Signatures multi‑omiques, profils tumoraux | Omique maladie (cancer) | `data/tcga/` | **OK** | UCSC Toil Xena RSEM TPM |
| **GEO** | Transcriptomique (microarrays, RNA‑seq) | Expression différentielle, signatures | Omique maladie / contrôle | `data/geo/` | **OK** (180 séries) | https://www.ncbi.nlm.nih.gov/geo/ |
| **GTEx** | Transcriptomique (tissus normaux) | Comparaison normal vs pathologique | Omique référence tissus | `data/gtex/` | **OK** | GTEx v8 gene TPM |
| **LINCS / CMap** | Transcriptomique perturbation | Signature matching (drug vs disease) | Omique réponse médicament | `data/lincs_cmap/` | **OK** (meta + Level5 GCTX) | GEO GSE92742 |
| **ArrayExpress** | Transcriptomique, génomique | Données omiques publiques | Omique maladie / contrôle | `data/arrayexpress/` | **OK** (40 études BioStudies) | https://www.ebi.ac.uk/biostudies/arrayexpress |
| **Expression Atlas** | Expression génique | Atlas multi‑contextes | Omique référence | `data/expression_atlas/` | **OK** (30 exp. + matrices TPM) | FTP EBI experiments |
| **CCLE** | Multi‑omique lignées cancéreuses | Profil cellulaire, dépendances | Pharmacogénomique cellule | `data/ccle/` | **OK** (via DepMap) | https://sites.broadinstitute.org/ccle/ |
| **GDSC** | Sensibilité aux médicaments | Corrélation omique ↔ réponse drug | Pharmacogénomique cellule | `data/gdsc/` | **OK** | https://cog.sanger.ac.uk/cancerrxgene/GDSC_release8.5/ |
| **DrugBank** | Pharmacologique (médicaments, cibles) | Rôle couvert par DGIdb, TTD, ChEMBL, BindingDB, STITCH, SIDER | Pharma / KG | `data/drugbank/` | **Hors catalogue** | — |
| **DGIdb** | Interactions drug–gene | Validation des cibles | Pharma / cibles | `data/dgidb/` | **OK** | https://www.dgidb.org/data/latest/interactions.tsv |
| **TTD** | Cibles thérapeutiques | Priorisation des targets | Pharma / cibles | `data/ttd/` | **OK** | https://ttd.idrblab.cn/files/download/P1-01-TTD_target_download.txt |
| **ChEMBL** | Bioactivité drug–target | Dataset DTI pour entraînement | DTI / assays | `data/chembl/` | **OK** (chemreps + dump PG) | https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/ |
| **BindingDB** | Affinités drug–target | Dataset DTI / arêtes ligand–cible | DTI / assays | `data/bindingdb/` | **OK** (TSV 202609 → edges) | https://www.bindingdb.org/rwd/bind/downloads/BindingDB_All_202609_tsv.zip |
| **UniProt** | Séquences protéiques | Annotation des cibles | Protéine | `data/uniprot/` | **OK** (Swiss-Prot human) | https://www.uniprot.org/ |
| **PDB / RCSB** | Structures 3D protéines | Docking, validation structurelle | Structure | `data/pdb/` | **OK** (1808 CIF BindingDB + AlphaFold 20 550) | https://www.rcsb.org/ |
| **PharmGKB** | Pharmacogénomique | Variants influençant réponse aux drugs | Clinique / variants | `data/pharmgkb/` | **OK** | https://s3.pgkb.org/data/ |
| **KEGG** | Pathways métaboliques | Enrichissement fonctionnel | Pathways | `data/kegg/` | **OK** (GMT MSigDB) | rest.kegg.jp + MSigDB |
| **Reactome** | Pathways biologiques | Validation des mécanismes | Pathways | `data/reactome/` | **OK** | https://reactome.org/download/ |
| **OMIM** | Gènes et maladies héréditaires | Rôle couvert par Hetionet, PrimeKG, PharmGKB, ClinicalTrials.gov, TTD | Clinique / phénotype | `data/omim/` | **Hors catalogue** | — |
| **ClinicalTrials.gov** | Essais cliniques | Validation translationnelle | Clinique | `data/clinicaltrials/` | **OK** (17 489 études API v2) | API v2 |
| **SIDER** | Effets secondaires | Polypharmacologie, sécurité | Sécurité / phénotype | `data/sider/` | **OK** | http://sideeffects.embl.de/ |
| **STITCH** | Interactions chimiques–protéines | Réseaux interactomiques | Réseau chimie–protéine | `data/stitch/` | **OK** | Zenodo 10200150 (humain 9606) |
| **DepMap** | Dépendances génétiques/pharmacologiques | Validation cancer multi‑omique | Pharmacogénomique cellule | `data/depmap/` | **OK** | Figshare DepMap 24Q4 |

### Compléments

| Base / jeu | Type | Usage TOPOREP | Statut |
| --- | --- | --- | --- |
| Davis / KIBA / BioSNAP / Human Liu | Benchmarks DTI | DeepDTA / DrugBAN | **OK** |
| AlphaFold human | Structures prédites | Docking / structure | **OK** (index 20 550) |
| Hetionet / PrimeKG | KG biomédical | Baseline réseaux | **OK** (Hetionet + PrimeKG ~982 Mo) |

---

## Couches

```
1. DTI / bioactivité     BindingDB, ChEMBL, Davis, KIBA, DGIdb, TTD, STITCH
2. Cible / structure     UniProt, PDB, AlphaFold
3. Omique maladie        TCGA, GEO, ArrayExpress, Expression Atlas
4. Omique référence      GTEx
5. Perturbation drug     LINCS / CMap
6. Pharmacogénomique     CCLE, GDSC, DepMap
7. Pathways              KEGG, Reactome
8. Clinique / sécurité   PharmGKB, ClinicalTrials.gov, SIDER, Hetionet, PrimeKG
```

---

## Statut résumé

| Statut | Bases |
|--------|--------|
| **OK** | TCGA, GEO, GTEx, LINCS+L5, ArrayExpress, Expression Atlas, CCLE, GDSC, DGIdb, TTD, ChEMBL, BindingDB, UniProt, **PDB/RCSB (1808)**, PharmGKB, KEGG, Reactome, ClinicalTrials, SIDER, STITCH, DepMap, Hetionet/PrimeKG, AlphaFold ; benchmarks DTI |
| **EN COURS** (0) | — |
| **Hors catalogue** (2) | DrugBank ; OMIM — rôles couverts par les bases actives |
| **MANQUANT** (0) | — |
