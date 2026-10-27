# Licences et redistribution

Le paquet documentaire peut être archivé. Les données sources et dérivées ne doivent
pas être rendues publiques en bloc avant une revue juridique source par source.

| Famille | Traitement dans le paquet DOI préparatoire |
|---|---|
| ChEMBL, Reactome | référencés avec provenance; vérifier et joindre les notices applicables |
| BindingDB | référencé; conserver attribution et conditions affichées par le fournisseur |
| LINCS/CMap | matrice non recopiée; fournir identifiant, URL, version et SHA |
| TCGA, GTEx | matrices non recopiées; respecter les politiques des portails d'origine |
| DepMap | matrice non recopiée; vérifier les conditions de la release téléchargée |
| GEO, ArrayExpress, Expression Atlas | expériences référencées individuellement; les droits peuvent dépendre des dépôts associés |
| UniProt | séquences dérivées non incluses dans l'archive documentaire |

`access_right` reste donc `restricted` dans `zenodo.json`. Ce choix n'affirme pas que
les données sont non redistribuables; il empêche seulement une publication prématurée.
Après revue, les fichiers autorisés pourront être ajoutés et le droit d'accès modifié.
