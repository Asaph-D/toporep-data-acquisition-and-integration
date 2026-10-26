# Conception — normalisation, correction de batch, harmonisation

**Statut :** document de conception. Aucun script de cette étape n'est lancé ici.  
**S'appuie sur :** la validation du 2026-10-13 (`integration/VALIDATION_TRACE_QC.md`), 22 bases actives au contrat traçabilité + contrôle qualité.  
**Hors de ce document :** archive PDB complète, registre ClinicalTrials exhaustif, et les deux bases sorties du catalogue (leur rôle est déjà couvert, voir `INVENTAIRE.md`).

---

## 1. Ce que les fichiers permettent déjà

Les matrices ne sont pas dans la même unité, et le registre n'est pas une jointure.

| Couche | Unité actuelle | Jointure possible aujourd'hui |
|--------|----------------|-------------------------------|
| TCGA Toil | RSEM TPM | Sur l'échantillon et le gène du fichier, pas avec GTEx ni GEO |
| GTEx v8 | TPM | Sur le tissu GTEx |
| DepMap 24Q4 | log2(TPM + 1), gènes codants | Sur `ModelID` |
| LINCS Level 5 (GSE92742) | score MODZ, déjà un z robuste | Sur `sig_id` / `pert_id`, pas sur un gène HGNC du registre |
| GEO | 180 séries, plus de 70 plateformes | À l'intérieur d'une série seulement |
| Expression Atlas | TPM, FPKM ou analytics, 30 expériences | Fichiers `_dl_*` complets ; les `matrix_head_*` sont des aperçus |
| BindingDB | 500 000 premières lignes, sans seuil d'affinité | SMILES × UniProt |
| Graphe drug–cible | 492 814 arêtes | Identifiants de natures différentes sur la même colonne |

Deux erreurs de sens sont déjà dans `scripts/acquire/build_registry.py` et devront être défaites avant toute jointure, pas « corrigées » par une normalisation :

- le nom de perturbation LINCS (`pert_iname`) est écrit dans `gene_symbol` ;
- le label de catalogue GEO est écrit dans `gene_symbol`.

---

## 2. Normalisation — décision par couche

On ne réécrit pas une unité qui est déjà l'unité de publication. On refuse de coller deux unités sous un même nom.

| Couche | Décision | Motif |
|--------|----------|--------|
| TCGA, GTEx | Garder le TPM. Pas de second log tant qu'un modèle ne l'exige pas. | Les deux fichiers sont déjà des TPM, issus de pipelines différents. |
| DepMap | Garder le log2(TPM + 1). Le documenter dans le nom de colonne le jour où on le juxtapose à un TPM. | Revenir au TPM seulement pour une comparaison explicite avec TCGA ou GTEx. |
| LINCS Level 5 | Ne pas z-scorer une seconde fois. | Le MODZ est déjà le consensus des réplicats. |
| GEO | Rester série par série. Pas de fusion des GPL dans la première implémentation. | Intensités d'array et comptes RNA-seq ne partagent pas une échelle. |
| Expression Atlas | Garder l'unité du fichier (TPM, FPKM ou analytics) et ne pas la mélanger à GEO. | Le type est dans le nom du fichier. |
| BindingDB | Au moment de l'implémentation seulement : restreindre aux lignes avec au moins une constante (Ki, IC50 ou Kd) numérique, puis exprimer cette constante en p-activité (−log10 de la molaire) si l'unité source est le nM. | Le cap des 500 000 lignes n'est pas un filtre biologique. |
| ChEMBL | Extraire les essais du dump PostgreSQL déjà empreinté, avec le même principe de p-activité, séparément du chemreps. | Le chemreps est un catalogue de structures, pas une activité. |
| GDSC | Garder LN_IC50 et AUC tels que publiés. | Le contrôle qualité a déjà retiré les couples lignée–médicament vides. |

Le passage BindingDB au-delà des 500 000 lignes fait partie de cette étape, parce que le zip complet est déjà local (TSV décompressé 8,6 Go). Ce n'est pas un nouveau téléchargement.

---

## 3. Correction de batch — où elle a un sens

La correction de batch n'est pas une étape globale. Elle ne s'applique qu'à un empilement d'échantillons que l'on veut traiter comme une seule matrice de gènes.

| Empilement envisagé | Facteur de batch | Décision |
|---------------------|------------------|----------|
| Séries GEO d'une même indication, même plateforme | La série (GSE) | Autorisé plus tard, et seulement après un identifiant de gène commun dans la série. Méthode de la famille ComBat / modèle linéaire à effet série. |
| Séries GEO de plateformes différentes | La plateforme (GPL) | Interdit dans la première implémentation. Le facteur se confond avec la technologie. |
| TCGA et GTEx | Le projet (Toil contre GTEx) | Interdit comme concaténation silencieuse. Une comparaison tumeur contre tissu normal devra porter un facteur projet, ou rester en deux contrastes séparés. |
| LINCS | Déjà agrégé en Level 5 | Pas de seconde correction. La lignée, la dose et le temps restent des métadonnées de signature, pas un batch à effacer. |
| DepMap | Une release, un pipeline | Pas de correction interne. |
| Graphes drug–cible, pathways, essais, effets | Pas des matrices d'expression | Aucune correction de batch. |

Règle d'arrêt : si le facteur que l'on veut retirer est aussi le facteur biologique (tissu, indication, lignée), on ne le retire pas.

---

## 4. Harmonisation — schéma cible

Le fichier `integration/registry_ids.csv` (3 514 120 lignes) reste l'inventaire des clés natives. Il n'est pas le produit fini. Le produit fini est deux tables d'entités, une ligne par entité, et des arêtes dont les deux bouts existent dans ces tables.

### 4.1 Composé

Clé préférée : InChIKey.  
Clés acceptées en attente de résolution : ChEMBL, PubChem CID, identifiant STITCH, `pert_id` LINCS, identifiant TTD, clé DGIdb.

Ordre de résolution, du plus stable au plus fragile :

1. InChIKey déjà porté par TTD ou par le chemreps ChEMBL.
2. PubChem CID porté par STITCH, SIDER ou BindingDB, puis InChIKey via ce CID.
3. Nom LINCS (`pert_iname`) vers ChEMBL ou PubChem. Le nom n'est jamais un symbole de gène.
4. Clé DGIdb laissée non résolue si aucun des trois liens précédents n'existe. Elle reste une clé native, pas une arête perdue en silence.

### 4.2 Gène ou protéine

Clé préférée : symbole HGNC, avec UniProt et Entrez en colonnes.  
Sources : UniProt humain reviewed (20 425), TTD, DGIdb, STITCH (alias HGNC / Entrez), Reactome (UniProt humain), PharmGKB.

Une arête dont la cible ne résout ni en symbole ni en UniProt sort du graphe intégré et reste dans le fichier source, avec un compteur dans le rapport.

### 4.3 Maladie ou tissu

Pas une troisième table mondiale dans la première implémentation.  
Les labels déjà utilisés pour GEO, ArrayExpress et Expression Atlas (indication TCGA, tissu GTEx, maladie DepMap) restent le vocabulaire. Hetionet et PrimeKG apportent les arêtes gène–maladie. ClinicalTrials garde l'identifiant NCT et le libellé d'indication tel que l'API l'a donné.

---

## 5. Graphe — ce qui change par rapport à l'amorce

| Artefact actuel | Décision |
|-----------------|----------|
| `graph_drug_target.edgelist` | À reconstruire après résolution. Une arête n'entre que si le composé a un InChIKey ou, à défaut documenté, un PubChem CID, et si la cible a un HGNC ou un UniProt. Les trois namespaces d'aujourd'hui (InChIKey ou identifiant TTD, clé DGIdb, identifiant STITCH) ne restent pas dans la même colonne. |
| `graph_drug_se.edgelist` | Le composé SIDER est déjà un identifiant STITCH. Le relier au même composé que le graphe drug–cible via PubChem CID. |
| Graphe gène–maladie | À créer depuis Hetionet et PrimeKG, pas depuis une base absente du catalogue. Sommets gène résolus comme en 4.2. |
| `integration/matrices/` | Première matrice utile : lignée DepMap × médicament GDSC, après alignement des noms de lignées. Les signatures LINCS restent en GCTX, indexées par `sig_id`, pas recopiées en CSV dense. |

Compte obligatoire du rapport d'implémentation : lignes sources, lignes résolues, lignes laissées en clé native, arêtes refusées faute de sommet.

---

## 6. Ordre quand on passera au code

1. ~~Corriger le registre~~ **fait** (`build_registry.py` : 605 270 clés natives ; LINCS et GEO hors `gene_symbol`).
2. ~~Tables d'entités composé et gène~~ **fait** (155 266 composés, 131 722 résolus ; 30 448 gènes).
3. ~~Reconstruire le graphe drug–cible et relier les effets~~ **fait** (330 143 arêtes drug–cible ; 145 321 effets, 0 refus composé).
4. ~~Graphe gène–maladie Hetionet~~ **fait** (27 977 arêtes DaG / DuG / DdG). PrimeKG n'est pas fusionné : pas de typage d'arête comparable.
5. Seuils d'affinité BindingDB sur le TSV déjà local, puis essais ChEMBL depuis le dump déjà empreinté.
6. Seulement ensuite, et seulement pour un contraste explicitement demandé : z intra-série GEO sur une plateforme unique, ou facteur projet si TCGA et GTEx doivent être lus ensemble.

---

## 7. Ce qui ne fait pas partie de cette conception

- Télécharger l'archive PDB (~200 Go). Les 1 808 mmCIF ciblés et l'index AlphaFold (20 550) restent la couche structure.
- Rendre ClinicalTrials exhaustif. Les 17 489 études déjà filtrées restent l'échantillon.
- Fusionner les plateformes GEO en une matrice unique.
- Re-normaliser LINCS Level 5.
