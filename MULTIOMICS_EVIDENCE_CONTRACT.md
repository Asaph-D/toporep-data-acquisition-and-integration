# Contrat des preuves multi-omiques v1

## Rôle des données

L'interaction structure–cible formule l'hypothèse mécanistique primaire. Les données
publiques multi-omiques ne constituent ni une vérité universelle ni une condition
d'existence de cette hypothèse. Lorsqu'une observation compatible existe dans un
contexte biologique documenté, elle peut renforcer ou affaiblir l'hypothèse. Son
absence signifie uniquement « preuve non disponible ».

Ce choix répond directement à l'objectif de généralisation : un modèle ne doit pas
réussir seulement parce qu'il reconnaît des composés déjà très documentés. Une couche
omique, notamment LINCS, ne peut donc ni décider seule du label ni exclure les
1 200 894 composés DTI sans signature LINCS reliée.

## Invariants transmis à la modélisation

1. Le socle structure–cible reste exploitable avec ou sans donnée omique.
2. Chaque preuve est accompagnée d'un masque de disponibilité explicite.
3. Une valeur absente n'est jamais remplacée par zéro et n'est jamais interprétée
   comme une absence d'effet biologique.
4. Aucune imputation apprise n'est réalisée pendant l'acquisition et l'intégration.
5. Les signatures LINCS conservent leur cellule, dose et durée; elles ne sont pas
   moyennées globalement en une pseudo-signature de composé.
6. Les valeurs restent dans les matrices normalisées qualifiées. Les tables produites
   ici sont des index traçables vers leurs axes, pas une seconde copie transformée.
7. La modélisation devra comparer le socle seul, le socle augmenté de chaque source,
   les ablations de sources et les performances stratifiées par disponibilité.

## Interprétation autorisée

Une concordance omique contextuelle est un argument supplémentaire. Une discordance
est un argument défavorable dans ce contexte précis. Une donnée inexistante est
neutre. Ces trois états — favorable, défavorable, non observé — ne doivent jamais
être réduits à un seul booléen.
