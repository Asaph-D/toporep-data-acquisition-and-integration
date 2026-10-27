# Fiche de données — Acquisition et intégration de données multi-omiques

## Finalité

Ce jeu prépare l'étude de mécanismes de repositionnement de médicaments à partir des
relations structure–cible, puis leur confrontation à des preuves multi-omiques publiques.
Il est conçu pour évaluer la généralisation à des composés, squelettes et protéines non
familiers, et non pour maximiser une séparation aléatoire de couples déjà connus.

## Contenu

| Composant | Contenu | Cardinalité principale |
|---|---|---:|
| Bioactivité | mesures ChEMBL 37 et BindingDB harmonisées | 7 173 067 mesures |
| Labels | vues pActivity 5, 6 et 7 | 2 201 705 couples par vue |
| Composés | structures RDKit standardisées et groupes chimiques | 1 203 548 |
| Cibles | UniProt, séquences et groupes MMseqs2 | 5 186 |
| LINCS | signatures Level 5 MODZ indexées sans agrégation globale | 69 059 reliées |
| Voies | relations cible–Reactome | 70 851 arêtes |
| Masques | disponibilité à sept bits pour chaque couple et chaque seuil | 6 605 115 lignes |
| Index natifs | positions exactes dans LINCS, TCGA, GTEx et DepMap | 20 746 cible–source |

Les matrices omiques volumineuses restent dans leurs formats qualifiés HDF5/GCTX. Les
tables d'intégration donnent chemin, dataset, unité et position; elles ne dupliquent pas
les valeurs.

## Origine et transformations

Les sources principales sont ChEMBL 37, BindingDB, LINCS/CMap, TCGA, GTEx, DepMap,
Reactome et les collections transcriptomiques GEO/ArrayExpress/Expression Atlas
qualifiées. Les transformations comprennent : conservation des mesures originales,
conversion documentée vers pActivity, standardisation RDKit, résolution UniProt,
projection vers les axes de gènes, matérialisation float32, matrices creuses lorsque
nécessaire et contrôles de valeurs non finies.

Les transformations qui modifieraient une signification biologique sans contraste
identifiable sont interdites. Aucune correction de lot aveugle et aucune imputation
multi-omique apprise ne sont appliquées.

## Labels et négatifs

Les trois vues utilisent les seuils pActivity 5, 6 et 7. Un négatif correspond à une
inactivité expérimentalement mesurée. L'absence d'une interaction, d'une signature ou
d'une caractéristique ne produit jamais un négatif. Les relations censurées et conflits
sont traités selon les règles versionnées de `config/dti_labels_v1.yml`.

## Disponibilité des preuves

Le masque contient sept indicateurs : signature LINCS du composé, gène de la cible,
Reactome, TCGA, GTEx, DepMap et gène LINCS. `false` signifie seulement « non disponible ».
Le faible recouvrement composé–LINCS — 2 654 sur 1 203 548 — est une propriété du plan
d'expérience public, pas une mesure de plausibilité pharmacologique.

## Partitions recommandées

Les groupes livrés permettent au minimum :

- cold-drug avec groupes chimiques disjoints;
- cold-target avec groupes MMseqs2 disjoints;
- séparation simultanée scaffold+séquence;
- coupure temporelle fondée sur la date documentaire;
- analyses stratifiées selon la disponibilité des preuves;
- ablations structure–cible seule, source par source et leave-one-source-out.

Une séparation aléatoire au niveau des lignes n'est pas une évaluation principale
acceptable, car elle laisse passer analogues chimiques, homologues protéiques et mesures
du même document entre apprentissage et test.

## Usages appropriés

- formulation et classement d'hypothèses mécanistiques;
- préentraînement ou apprentissage DTI avec négatifs mesurés;
- comparaison de stratégies de fusion tolérant les modalités manquantes;
- études d'ablation et de généralisation hors familiarité.

## Usages inappropriés

- décision clinique ou recommandation thérapeutique directe;
- interprétation de LINCS comme vérité universelle;
- mise à zéro des modalités absentes;
- apprentissage d'une imputation avant la séparation des groupes;
- comparaison directe de nombres provenant d'unités omiques incompatibles;
- déclaration d'un composé inactif parce qu'il n'existe pas dans une base publique.

## Biais et limites

Les bases publiques surreprésentent les entités populaires, les lignées faciles à cultiver
et certains espaces pathologiques. Les contextes LINCS sont limités par cellule, dose et
durée; TCGA décrit des tumeurs, GTEx des tissus non tumoraux et DepMap des lignées
cancéreuses. Les 534 cibles sans résolution complète vers le registre de gènes restent
visibles. Les licences et conditions de redistribution doivent être revérifiées source
par source avant publication DOI.

## Reproductibilité et version

P4-06 a reconstruit deux fois dix artefacts scientifiques depuis les checkpoints
OMIQUE-1, DTI-1 et GROUPS-1. Les dix SHA-256 sont identiques entre les passes. Le jeu
reste candidat jusqu'au gel P4-08 sous le nom
`acquisition-et-integration-de-donnees-multi-omiques`; le manifeste de release
constituera la source canonique des empreintes et versions.
