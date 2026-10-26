# Qualification de la phase 1 — acquisition, normalisation et intégration

**Projet :** `toporep-data-acquisition-and-integration`  
**Date de qualification :** 2026-10-23  
**Décision globale :** **OMIQUE-1 QUALIFIÉE — phase globale encore ouverte sur DTI-1 et GROUPS-1**

## 1. Périmètre et référentiel

La qualification porte sur les artefacts locaux de collecte, de contrôle qualité, de
normalisation et d'intégration. Elle ne qualifie ni les analyses différentielles, ni les
modèles prédictifs, ni la validation expérimentale.

Références utilisées :

1. `OmicData/1253251-fr-FR.pdf`, section 3.1, qui demande collecte, contrôle qualité,
   prétraitement, normalisation, correction des effets de lot et harmonisation des
   caractéristiques avant l'intégration ;
2. `OmicData/TOPOREP_Master2_Research_Proposal_and_Literature_Review fr-FR.pdf`,
   section 4.1 (WP1), qui demande provenance typée, normalisation et déduplication des
   entités, négatifs mesurés, seuils pChEMBL 5/6/7, réduction de redondance et manifeste
   reproductible ;
3. les contrats internes décrits dans `PLAN.md`, `INVENTAIRE.md` et
   `CONCEPTION_NORMALISATION_HARMONISATION.md`.

## 2. Résultat synthétique

| Domaine | Décision | Éléments probants | Réserve bloquante |
|---|---|---|---|
| Acquisition | **QUALIFIÉE** pour le catalogue local déclaré | 22 bases actives ; audit de présence sans écart ; fichiers `VERSION.txt` et `qc_summary.md` présents ; DrugBank et OMIM explicitement hors catalogue | La qualification ne prouve pas que chaque archive distante est exhaustive ou toujours accessible |
| Traçabilité et QC documentaire | **QUALIFIÉS** au niveau du contrat interne | `integration/VALIDATION_TRACE_QC.md` : 22/22 PASS ; date, URL, mention SHA-256 et critère QC présents | Le validateur contrôle surtout la présence des champs, pas la concordance de toutes les empreintes avec tous les fichiers locaux |
| Normalisation des matrices omiques | **QUALIFIÉE — GO OMIQUE-1** | Matrices versionnées, contrats d'unité, axes, exclusions, rapports avant/après et scan exhaustif de 36 matrices | Le périmètre exclut explicitement les séries sans unité/mapping et les artefacts corrompus |
| Harmonisation des entités | **QUALIFIÉE AVEC RÉSERVES** | 155 266 composés uniques ; 30 448 lignes gène/protéine uniques ; registre natif séparé | 23 544 composés restent natifs ; élimination des sels et canonisation des tautomères non démontrées ; cible de référence pas uniformément ramenée à UniProt |
| Intégrité des graphes intégrés | **QUALIFIÉE** pour les trois graphes produits | 330 143 arêtes médicament–cible, 145 321 médicament–effet, 27 977 gène–maladie ; aucun doublon de ligne complète ni sommet manquant dans les registres | PrimeKG n'est pas fusionné et le graphe médicament–cible ne porte pas le niveau de preuve requis par WP1 |
| Jeu d'apprentissage WP1 | **NON QUALIFIÉ** | Sources DTI disponibles localement | Pas de vrais négatifs mesurés, pas de matrices pChEMBL 5/6/7, pas de conflits d'activité signalés, pas de groupes Bemis–Murcko/ECFP4 ou MMseqs2, pas de manifeste machine-readable complet |

## 3. Contrôles exécutés

### 3.1 Contrôles réussis

- `python scripts/_audit_tour.py` : aucun problème signalé sur les 24 dossiers du
  catalogue (22 actifs et 2 hors catalogue).
- `python -m compileall -q scripts` : compilation syntaxique réussie.
- Unicité de `integration/entities_compounds.csv` : 155 266 identifiants sur
  155 266 lignes.
- Unicité des couples `(gene_symbol, uniprot_id)` dans
  `integration/entities_genes.csv` : 30 448 sur 30 448 lignes.
- Intégrité référentielle : zéro extrémité absente et zéro ligne entièrement dupliquée
  dans les trois graphes intégrés.

### 3.2 Limite des contrôles existants

Le résultat `PASS` de `scripts/validate_trace_qc.py` signifie que les métadonnées exigées
sont présentes. Il ne suffit pas à démontrer que :

- les valeurs SHA-256 correspondent encore aux artefacts courants ;
- les transformations biologiques sont correctes ;
- les matrices sont comparables entre plateformes ;
- la suppression des sels, la canonisation des tautomères et la déduplication
  inter-sources ont été appliquées conformément au WP1 ;
- les étiquettes positives et négatives sont exemptes de fuite de provenance.

## 4. Non-conformités et réserves

### NC-01 — Normalisation omique — levée le 2026-10-23

Le critère est satisfait sur le périmètre décrit dans
`normalized/omics/QUALIFICATION_OMIQUE_1.md`. Les unités restent volontairement séparées,
LINCS est matérialisé, les sources hétérogènes sont traitées série par série et le scan
exhaustif de 36 matrices ne trouve aucun NaN ni infini. Aucune correction de lot n'est
appliquée sans contraste déclaré.

### NC-02 — Contrat WP1 de bioactivité incomplet — majeure

Le graphe intégré contient la source mais pas le type de preuve, la puissance, l'unité,
l'étiquette actif/inactif ni le seuil appliqué. Il ne peut donc pas constituer la vérité de
référence demandée par la proposition de Master 2.

**Critère de levée :** créer une table DTI canonique au niveau essai avec au minimum
`compound_id`, `uniprot_id`, `source`, `evidence_type`, `assay_id`, `activity_type`,
`activity_value`, `activity_unit`, `pactivity`, `threshold`, `label`, `publication_date` et
un indicateur de conflit. Générer ensuite les vues pChEMBL 5, 6 et 7.

### NC-03 — Négatifs expérimentaux absents — majeure

Les associations absentes du graphe ne sont pas des négatifs. Aucun artefact dédié aux
composés testés et mesurés inactifs n'a été trouvé.

**Critère de levée :** conserver les essais inactifs mesurés dans une classe séparée,
traçable jusqu'à l'essai source ; ne jamais convertir une absence d'arête en négatif vrai.

### NC-04 — Standardisation chimique insuffisamment démontrée — majeure

L'InChIKey est utilisé quand disponible, mais les artefacts et scripts ne démontrent pas
l'élimination des sels, la normalisation des charges et la canonisation des tautomères.

**Critère de levée :** versionner la recette de standardisation, conserver identifiant et
structure avant/après, journaliser les rejets et dédupliquer au niveau
`(standard_inchikey, uniprot_id)`.

### R-01 — Couverture partielle des entités — réserve

23 544 composés sur 155 266 (15,16 %) restent sous identifiant natif. Cette situation est
acceptable pour un registre d'acquisition, mais ces composés ne doivent pas entrer dans un
jeu DTI canonique sans strate de confiance explicite.

### R-02 — Réduction de redondance absente — réserve

Les groupes de composés par squelette Bemis–Murcko/similarité ECFP4 et les groupes de
cibles à 90 %, 70 % et 50 % d'identité ne sont pas produits. Ils sont nécessaires avant la
définition des partitions d'évaluation honnêtes du WP2.

### R-03 — Reproductibilité incomplète — réserve

Les scripts sont présents, mais aucun environnement verrouillé, workflow
Snakemake/Nextflow, manifeste global machine-readable ou dépôt DOI n'est fourni dans ce
dossier. Les scripts compilent, ce qui ne constitue pas un test fonctionnel de bout en bout.

## 5. Décision et règle de clôture

La branche omique est désormais qualifiée (`GO OMIQUE-1`). La phase complète ne doit pas
encore être figée comme jeu d'apprentissage WP1 : la table DTI canonique, les vrais
négatifs mesurés, les vues de seuil et les groupes de redondance restent à produire.

La clôture pourra être prononcée lorsque NC-02 à NC-04 seront levées et qu'un paquet de
qualification contiendra :

1. un manifeste global versionné et lisible par machine ;
2. les matrices omiques normalisées avec diagnostics avant/après ;
3. la table DTI canonique avec provenance et hiérarchie de preuves ;
4. les négatifs expérimentaux et les vues pChEMBL 5/6/7 ;
5. les groupes de redondance chimique et protéique ;
6. des tests automatiques d'intégrité, de reproductibilité et d'absence de fuite ;
7. une version figée avec empreintes vérifiées et, au stade de diffusion, un DOI.
