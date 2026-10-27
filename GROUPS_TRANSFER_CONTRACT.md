# Contrat de transfert des groupes DTI

## Objet et périmètre

Ce contrat décrit les informations remises au futur dépôt d'évaluation. Le présent dépôt
ne fabrique aucune partition d'apprentissage, de validation ou de test. Il fournit des
identités et des groupes versionnés, puis vérifie leur couverture. Les paires ambiguës
restent disponibles pour l'audit, mais ne participent pas aux métriques principales.

## Régime cold-drug

L'unité indivisible est `standard_inchikey`. Toutes les activités, tous les types
Ki/Kd/IC50/EC50 et tous les seuils associés au même InChIKey doivent appartenir à une seule
partition. Après partitionnement, les intersections train–validation, train–test et
validation–test des InChIKey doivent être vides. Les empreintes ECFP4 peuvent servir à
des analyses de proximité, mais ne remplacent pas cette identité exacte.

## Régime cold-target

L'unité indivisible est `uniprot_id`. Toutes les mesures portant sur une même cible sont
assignées ensemble. Les trois intersections d'identifiants UniProt entre partitions
doivent être vides. Les complexes et familles non résolus ne sont pas réintroduits dans
ce régime : seuls les couples déjà qualifiés avec une protéine humaine simple sont admis.

## Régimes scaffold et séquence

Le régime scaffold utilise `murcko_group_id`. Une molécule dont le squelette n'a pas pu
être calculé est exclue de ce régime et comptée; elle n'est jamais placée dans un groupe
générique « inconnu », car ce groupe artificiel créerait une dépendance entre molécules
sans relation structurale démontrée.

Le régime de séquence utilise l'une des colonnes `cluster_90`, `cluster_70` ou
`cluster_50`. Le seuil doit être choisi avant l'optimisation du modèle et enregistré dans
le manifeste du split. Le seuil 50 est le défaut le plus strict pour l'évaluation de
généralisation distante. Aucun groupe du seuil choisi ne peut traverser une frontière de
partition.

## Régime combiné scaffold+séquence

Une simple clé composée `(murcko_group_id, cluster_50)` est insuffisante : elle permettrait
au même scaffold de se retrouver dans plusieurs partitions lorsqu'il est lié à plusieurs
clusters protéiques, ou inversement. Le dépôt d'évaluation doit construire un graphe
biparti dont les nœuds sont les groupes Murcko et les clusters protéiques. Chaque paire
DTI est une arête. Une composante connexe entière constitue l'unité indivisible du split.

Avant toute recherche d'équilibrage, le dépôt d'évaluation doit publier le nombre et la
taille des composantes, la part de la plus grande composante et la faisabilité des ratios
demandés. Une composante géante ne doit jamais être découpée pour atteindre artificiellement
un ratio train/test.

## Régime temporel

La preuve temporelle provient de `dti_publication_dates.parquet`. Une mesure de train doit
avoir une date admissible strictement antérieure à la coupure. Les dates manquantes ou
invalides sont exclues du régime temporel et comptées. Une date de release de base, une
date de téléchargement ou une date d'ingestion n'est jamais substituée à une date de
publication.

## Transformations apprises et contrôle final

Toute imputation, normalisation statistique, sélection de variables, réduction de
dimension ou calibration est ajustée sur le train uniquement. La validation peut servir
au choix d'hyperparamètres; le test reste fermé jusqu'à l'évaluation finale. Après écriture
des partitions, le dépôt d'évaluation doit recalculer les intersections de chaque clé
protégée et échouer au premier chevauchement.

