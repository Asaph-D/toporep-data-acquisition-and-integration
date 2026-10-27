# Qualification — acquisition et intégration de données multi-omiques

**Projet :** `toporep-data-acquisition-and-integration`

**Date :** 27 octobre 2026

**Décision :** **GO pour OMIQUE-1, DTI-1, GROUPS-1 et MULTIOMICS-1**

**État de diffusion :** version 1.0.0 gelée et paquet DOI préparé sous le nom
`acquisition-et-integration-de-donnees-multi-omiques`; dépôt DOI non encore publié

## Portée de la décision

La décision qualifie l'acquisition, la normalisation, l'harmonisation des bioactivités,
les labels expérimentaux, les groupes anti-redondance et les index multi-omiques. Elle
ne qualifie aucun modèle prédictif, aucune partition définitive d'apprentissage et
aucune validation clinique ou expérimentale.

| Lot | Décision | Preuve principale |
|---|---:|---|
| OMIQUE-1 | GO | axes et unités versionnés; 36 matrices scannées sans valeur non finie |
| DTI-1 | GO | 7 173 067 mesures harmonisées; structures et cibles résolues; vues pActivity 5/6/7 |
| GROUPS-1 | GO | groupes chimiques Murcko/ECFP4 et protéines MMseqs2 90/70/50 |
| MULTIOMICS-1 | GO | mappings, masques, index natifs et validation P4-01–P4-05 |
| Reproductibilité P4-06 | PASS | deux reconstructions, dix Parquet, zéro différence SHA-256 |

## Invariants scientifiques qualifiés

1. Les unités incompatibles restent séparées; aucune concaténation numérique implicite
   n'est autorisée.
2. Les négatifs DTI sont des mesures expérimentales, jamais des arêtes absentes.
3. Les valeurs censurées et contradictions restent traçables jusqu'à l'essai source.
4. Les groupes de composés et de protéines sont transmis aux futures partitions pour
   empêcher la fuite de voisins proches.
5. L'interaction structure–cible formule l'hypothèse mécanistique primaire.
6. Une couche omique peut renforcer ou affaiblir cette hypothèse dans son contexte;
   elle ne constitue ni une vérité universelle ni une condition d'éligibilité.
7. Une modalité absente est masquée et neutre; elle n'est ni mise à zéro ni imputée.
8. Les 69 059 signatures LINCS conservent cellule, dose et durée; aucune moyenne globale
   ne fabrique une pseudo-signature de composé.

## Résultats mesurés

- ChEMBL 37 extrait : 24 527 044 activités.
- Mesures harmonisées ChEMBL/BindingDB : 7 173 067.
- Vues pActivity 5, 6 et 7 : 2 201 705 couples chacune.
- Univers DTI : 1 203 548 composés et 5 186 cibles.
- LINCS relié : 2 654 composés, 2 669 `pert_id`, 69 059 signatures.
- Cibles reliées : TCGA 4 560; GTEx 4 560; DepMap 4 642; LINCS-gènes 3 874;
  Reactome 4 291.
- Double reconstruction : 495,2 s puis 599,4 s; dix artefacts identiques bit à bit.

## Contrôles et incidents significatifs

Les validateurs couvrent cardinalités, schémas, unicité, intégrité référentielle,
bornes d'index, cohérence des masques, vrais négatifs, stabilité des groupes et SHA-256.
Le journal `rapports/preuves/P2_INCIDENTS_ET_CORRECTIONS.md` conserve aussi les échecs :
formats de dates BindingDB, alias DuckDB réservé, axes LINCS dans un ordre différent du
Parquet, clés HGNC/Ensembl/symboles et exclusions TCGA. Ces incidents ont arrêté les
calculs avant qualification et ont conduit à des contrôles permanents.

## Limites et biais à transmettre

- Seulement 2 654 des 1 203 548 composés DTI ont une signature LINCS reliée. Ce biais
  reflète principalement la sélection expérimentale LINCS; il interdit de traiter
  l'absence de signature comme un signal négatif.
- Les mesures publiques sont plus denses pour les cibles et composés historiquement
  étudiés. Une performance moyenne peut donc masquer une dépendance à la familiarité.
- TCGA, GTEx, DepMap et LINCS décrivent des contextes différents. Leur disponibilité ne
  les rend pas interchangeables.
- Les groupes et dates permettent les futures évaluations cold-drug, cold-target,
  scaffold+séquence et temporelles, mais les partitions finales appartiennent au lot
  de modélisation suivant.
- Les 512 cibles sans symbole UniProt local et 22 symboles absents du registre ne sont
  pas forcés vers un gène.

## Critères de clôture P4-07

- présent document consolidé : satisfait;
- fiche `FICHE_DONNEES_ACQUISITION_INTEGRATION_MULTI_OMIQUES.md` : satisfaite;
- rapport calculatoire illustré actualisé : satisfait;
- preuves de reconstruction et validations : satisfaites.

P4-08 a enregistré les manifestes, licences, versions, empreintes, taille du paquet et
instructions de citation sans recopier les grandes matrices natives. La qualification
de l'acquisition et de l'intégration est close. La publication effective du DOI demeure
une action externe distincte et exige la revue finale des licences source par source.
