# Étude comparative : solutions de monitoring de dérive de modèles

## Contexte

Dans le cadre de ce projet, Evidently AI a été retenu comme solution principale pour la détection de dérive (data drift et concept drift), couplé à Prometheus et Grafana pour le stockage et la visualisation des métriques. Cette section met en perspective ce choix face à des solutions managées telles que WhyLabs et Arize AI, afin de justifier les arbitrages effectués et d'ouvrir sur les limites de l'approche retenue.

**Note méthodologique** : cette comparaison s'appuie sur une analyse documentaire (documentation officielle des éditeurs, comparatifs indépendants, avis d'utilisateurs publiés) plutôt que sur un déploiement pratique de WhyLabs et d'Arize AI, ces solutions étant des plateformes commerciales sortant du périmètre technique de ce projet. Seul Evidently AI, retenu pour l'implémentation, a fait l'objet d'un test complet en conditions réelles (pipeline Docker, export Prometheus, dashboard Grafana, alerting).

## 1. Panorama des trois solutions

### Evidently AI (solution retenue)

Evidently AI est une bibliothèque Python open-source, utilisée en local dans ce projet pour calculer les scores de drift (tests statistiques, distance de Wasserstein, PSI selon les métriques) et générer des rapports HTML. Elle couvre le contrôle qualité des données, le suivi de performance et l'évaluation de sorties de modèles ou de LLM, avec plus de 100 métriques intégrées, un support des tests déclaratifs en pipeline CI/CD et un tableau de bord de suivi dans le temps.

**Positionnement observé sur le marché** : dans le classement PeerSpot (avril 2026, catégorie Model Monitoring), Evidently AI conserve la 2ᵉ place mais voit sa part d'attention reculer (16,6 %, contre 25,4 % l'année précédente), pendant qu'Arize AI progresse (23,5 %, en hausse).

### WhyLabs

WhyLabs est un outil « open-core » : la brique de profilage de données (whylogs) est open-source et peut tourner entièrement en self-hosted, tandis que la plateforme de visualisation, d'alerting et de gestion à l'échelle est un service managé payant. WhyLabs met l'accent sur la confidentialité des données (les profils statistiques sont envoyés à la plateforme plutôt que les données brutes), la conformité (SOC 2 Type II, HIPAA) et, plus récemment, la sécurité des applications LLM (détection d'injections de prompt, fuites de données).

**Tarification (repères 2026)** : un plan gratuit couvrant un projet jusqu'à 10 millions de prédictions par mois pour un utilisateur, puis un plan « Expert » à 125 $/mois (jusqu'à 3 projets, 5 utilisateurs, 100 millions de prédictions, monitoring horaire), et une offre Entreprise sur devis.

### Arize AI

Arize AI (et sa déclinaison open-source Arize Phoenix) est positionnée comme une plateforme d'observabilité ML complète, avec un accent marqué sur l'explicabilité (SHAP), l'analyse de cohortes, la détection automatique de cause racine et, plus récemment, le traçage d'applications LLM (intégrations LangChain, LlamaIndex, fournisseurs de modèles). Phoenix, la version self-hosted, est gratuite et illimitée en modèles/données ; Arize AX (le produit managé) propose un plan gratuit limité (1 utilisateur, environ 1 million de traces sur 14 jours) et un plan Pro à 50 $/mois, avec facturation à l'usage au-delà.

## 2. Tableau comparatif synthétique

| Critère | Evidently AI | WhyLabs | Arize AI |
|---|---|---|---|
| Modèle | Open-source (lib Python) | Open-core (whylogs OSS + SaaS payant) | OSS (Phoenix) + SaaS payant (Arize AX) |
| Coût pour ce projet | Gratuit, aucune limite | Gratuit jusqu'à 10M prédictions/mois | Gratuit en self-hosted (Phoenix) |
| Déploiement | 100 % local / conteneurisable | Profils locaux, dashboard cloud | Local (Phoenix) ou cloud (AX) |
| Intégration Prometheus/Grafana | Native (export manuel via `prometheus_client`, comme dans ce projet) | Non nécessaire, dashboard propre à la plateforme | Non nécessaire, dashboard propre à la plateforme |
| Confidentialité des données | Totale (rien ne sort de l'infrastructure) | Élevée (seuls des profils statistiques transitent) | Variable selon Phoenix (local) ou AX (cloud) |
| Alerting intégré | Non (nécessite Grafana/Prometheus, comme construit ici) | Oui, natif | Oui, natif |
| Explicabilité (SHAP, cause racine) | Limitée | Limitée | Point fort |
| Support LLM / GenAI | Oui, en expansion | Oui, axé sécurité (prompt injection) | Oui, point fort historique |
| Courbe d'apprentissage | Faible à modérée | Modérée | Modérée à élevée |
| Conformité entreprise (SOC 2, HIPAA) | Non applicable (pas de service géré) | Oui | Oui (offres entreprise) |

## 3. Pourquoi Evidently AI pour ce projet

Le choix d'Evidently AI, associé à une stack Prometheus/Grafana montée soi-même, répond à plusieurs contraintes propres à un projet pédagogique :

- **Coût nul et absence de dépendance externe** : aucune donnée ne transite vers un service tiers, aucune limite de volume, aucune création de compte.
- **Transparence pédagogique** : construire soi-même l'exporteur de métriques, la configuration Prometheus et les tableaux de bord Grafana oblige à comprendre chaque maillon de la chaîne (calcul du score → stockage → visualisation → alerte), alors qu'une solution managée masque une partie de cette mécanique derrière son propre dashboard.
- **Contrôle total sur les métriques exposées** : le choix des seuils, des couleurs de threshold, du format des alertes reste entièrement entre nos mains, ce qui correspond à l'objectif du sujet (« instrumenter un pipeline »), plutôt que consommer un pipeline déjà instrumenté.

## 4. Limites de l'approche retenue

Cette étude comparative met aussi en évidence ce que l'architecture actuelle n'offre pas, par rapport aux solutions managées :

- **Pas d'explicabilité intégrée** : Evidently AI signale qu'une feature dérive, mais WhyLabs et surtout Arize AI vont plus loin en aidant à comprendre *pourquoi* (analyse de cause racine, cohortes, valeurs SHAP).
- **Alerting et notification construits à la main** : dans ce projet, la chaîne alerte → webhook a dû être assemblée manuellement via Grafana Alerting. Chez WhyLabs et Arize, l'alerting est nativement intégré à la plateforme, avec des règles pré-configurées.
- **Scalabilité** : la stack actuelle (un script qui relit un fichier JSON toutes les 10 secondes) convient à une démonstration, mais ne serait pas adaptée à un flux de données réel à haute fréquence sans réingénierie (passage à un vrai pipeline de streaming, stockage de séries temporelles plus robuste, etc.).
- **Absence de fonctionnalités de conformité** : pour un cas d'usage réglementé (santé, finance), les certifications proposées par WhyLabs (HIPAA, SOC 2) apporteraient une garantie que l'architecture actuelle n'offre pas.

## 5. Conclusion

Le marché du monitoring de modèles se structure aujourd'hui autour de deux logiques complémentaires : des bibliothèques open-source légères comme Evidently AI, adaptées à la compréhension fine du pipeline et à des contraintes de coût ou de confidentialité strictes, et des plateformes managées comme WhyLabs ou Arize AI, qui apportent de l'alerting prêt à l'emploi, de l'explicabilité avancée et des garanties de conformité, au prix d'une dépendance à un service tiers et d'un coût croissant avec le volume de données.

Pour ce projet, l'assemblage Evidently AI + Prometheus + Grafana a permis de démontrer, de bout en bout, la détection automatique d'une dérive et le déclenchement d'une alerte — répondant directement à la problématique posée — tout en restant gratuit, auto-hébergé et pédagogiquement transparent. Une évolution vers un usage en production réelle gagnerait cependant à évaluer une solution managée (ou une architecture hybride, comme le suggèrent plusieurs comparatifs du secteur combinant plusieurs outils selon les besoins) pour bénéficier de l'alerting natif et de l'explicabilité qu'elles proposent.

## Sources

- PeerSpot, comparatifs Arize AI vs Evidently AI et Arize AI vs WhyLabs (avril / novembre 2026)
- Winder.ai, *A Comparison of Machine Learning Model Monitoring Tools and Products*
- Monte Carlo, *The 17 Best AI Observability Tools* (juillet 2026)
- G2, fiches produit et tarifs WhyLabs / Arize AI (2026)
- Neel Mishra, *Evidently vs whylogs vs NannyML vs Arize*
