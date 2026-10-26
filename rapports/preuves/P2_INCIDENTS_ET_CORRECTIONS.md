# Preuves d'incidents et corrections — intégration DTI

Ce journal conserve les états d'échec utiles au rapport. Une correction ne remplace pas
la preuve de l'anomalie initiale.

## Standardisation RDKit : lancement de test avec le mauvais point d'entrée

- État observé : le conteneur a exécuté son `ENTRYPOINT` de production au lieu du code de
  test et a cherché `/work/datasets/dti/assays/structure_standardization_work/structures_input.tsv`.
- Erreur conservée : `FileNotFoundError` sur `structures_input.tsv`.
- Cause : `docker run ... python -c ...` n'écrase pas un `ENTRYPOINT` déjà fixé.
- Correction : ajout de `--entrypoint python`.
- Preuve après correction : `RDKit container tests: PASS` pour le retrait de
  `CC(=O)[O-].[Na+]` vers `CC(=O)O`, l'InChIKey
  `QTBSBXVTEAMEQO-UHFFFAOYSA-N` et le rejet explicite d'un SMILES invalide.

## Suite locale : DLL pandas bloquées par Windows

- État observé avant et après exclusion antivirus : quatre modules de tests impossibles à
  importer, avec `ImportError: DLL load failed ... Une stratégie de contrôle d’application
  a bloqué ce fichier` sur les extensions pandas (`interval`, `missing`, `np_datetime`).
- Interprétation : l'exclusion Microsoft Defender ne désactive pas la politique de contrôle
  d'applications ; ce n'était pas un échec des calculs scientifiques.
- Correction reproductible : image Linux `toporep-phase1-tests:py312` contenant les
  dépendances verrouillées du projet.
- Preuve après correction : 27 tests exécutés, 27 réussis.

## Résolution des cibles : séparateurs BindingDB hétérogènes

- Première validation : `FAIL`, avec cinq cibles `resolved_single` portant un accession
  invalide.
- Cas révélateurs : `Q96CA5 P98170`, `Q86V67 P27815`, et des répétitions comme
  `P24462 P24462`.
- Cause : ChEMBL sépare les composants par `|`, tandis que certains enregistrements
  BindingDB utilisent un espace. La première règle ne traitait que `|`.
- Correction : séparation par `|` ou espace, puis déduplication des accessions.
- Effet : les vrais couples deviennent `resolved_multi`; les répétitions d'un même
  accession restent une protéine simple.
- Validation finale : `PASS`, 12 925 cibles simples, 1 138 multi-composants et 2 463 non
  résolues, sans clé dupliquée ni cible principale invalide.

## Captures à intégrer dans le rapport

1. console du premier test Docker et `FileNotFoundError` ;
2. console du test RDKit corrigé (`PASS`) ;
3. trace Windows des quatre imports pandas bloqués ;
4. première validation P2-07 (`FAIL`, cinq cas) ;
5. tableau des cinq accessions fautives avec leur interprétation ;
6. validation P2-07 corrigée (`PASS`) ;
7. console Docker des 27 tests réussis.

## Construction intégrée : mémoire DuckDB insuffisante

- Premier lancement P2-08–P2-10 : arrêt à l'étape `joining_and_classifying` avant
  création du Parquet temporaire.
- Erreur conservée : `Could not write ... duckdb_temp_storage_S64K-0.tmp: Cannot
  allocate memory`.
- Contexte mesuré avant l'échec : 2,654 Gio utilisés sur les 3,734 Gio alloués à Docker,
  avec une limite DuckDB initiale de 3 Gio et quatre threads.
- Cause : la requête monolithique combinait deux jointures, plusieurs fenêtres globales et
  une agrégation en liste sur 7 173 067 lignes, sans laisser assez de marge au moteur et au
  conteneur.
- Correction : pipeline en cinq matérialisations bornées, limite DuckDB de 1 Gio, deux
  threads, ordre d'insertion non préservé et déversement temporaire autorisé jusqu'à 80 Gio.
- Impact scientifique : aucun artefact validé P2-04 à P2-07 n'a été modifié; le premier
  lancement n'a produit aucune table finale partielle.

Les fichiers JSON de validation restent les preuves numériques primaires. Les captures du
rapport seront générées à partir de ces traces et accompagnées d'une légende expliquant
le symptôme, la cause, la correction et l'impact scientifique.
