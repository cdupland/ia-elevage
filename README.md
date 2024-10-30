---
title: Common
emoji: 🏢
colorFrom: purple
colorTo: indigo
sdk: streamlit
sdk_version: 1.39.0
app_file: app.py
pinned: false
---

<!-- Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference -->

# Application Template - README

## Introduction

Cette application sert de base/template pour en déployer d'autres sur le même modèle via Huggingface, en la dupliquant. Elle est décomposée en plusieurs sections pour offrir une gestion complète des documents et des dialogues avec une Intelligence Artificielle (IA).

### Structure de l'application

L'application est structurée en trois parties principales :

- **Documents**
  - *Communs*
  - *Vos Documents*
- **Configurations**
  - *Prompt système*
  - *Paramètres*
- **Dialogue**
  - *Chatbot*

### Fonctionnement des sections

#### 1. Documents

- **Documents Communs** : 
  Cette section permet de déposer des documents accessibles à tous les utilisateurs de l'application. Ces documents sont vectorisés et stockés dans une base de données vectorielle (voir section dédiée). Ils seront explorés lors des interactions avec l'IA.

- **Vos Documents** : 
  Chaque utilisateur peut uploader ses propres documents, qui seront pris en compte pendant sa session. Ces documents sont temporaires et ne sont accessibles que durant la session active de l'utilisateur.

#### 2. Configurations

- **Prompt système** :
  Cette section permet de configurer le *prompt système* utilisé lors des conversations avec l'IA. Ce prompt influence le comportement de l'IA pendant le dialogue.

- **Paramètres** :
  Ici, vous pouvez ajuster les paramètres dynamiques de l'application, tels que les préférences utilisateurs ou les options spécifiques à votre usage.

#### 3. Dialogue

- **Chatbot** :
  Une interface de discussion avec l'IA, où il est possible de choisir le modèle d'IA avec lequel interagir. Vous pouvez aussi commencer la conversation à partir d'un *prompt* pré-défini.

## Base de Données Vectorielle

La base de données vectorielle stocke de façon permanente les informations extraites des documents sous forme de vecteurs. Cette organisation facilite leur recherche et utilisation dans les conversations avec l'IA.

### Pinecone

L'application utilise **Pinecone**, une solution cloud pour la gestion de bases de données vectorielles. Pinecone simplifie la gestion des vecteurs et permet une intégration efficace avec l'application.

Pour que l'intégration fonctionne correctement, vous devez renseigner les variables d'environnement suivantes :

- **PINECONE_API_KEY** : Clé d'API fournie par Pinecone pour l'accès à votre compte.
- **PINECONE_INDEX_NAME** : Le nom de l'index Pinecone dans lequel les vecteurs seront stockés.
- **PINECONE_NAMESPACE** : Un namespace unique propre à chaque application, utilisé pour organiser les vecteurs.

Ces informations sont disponibles directement dans votre compte Pinecone, et doivent être correctement configurées pour permettre le fonctionnement de la base de données vectorielle.


## Configuration de l'application

Vous pouvez configurer votre application plus finement en la personalisant en fonction de vos besoins. Ces configurations se font dans le fichier *config.yaml* accessible dans la partie *Files* de votre espace Huggingface. La modification se fait ensuite via le bouton *'edit'*. 
Une fois, vos modifications effectuées, cliquez sur *'Commit changes to main'* pour les enregistrer et relancer automatiquement l'application.

#### Paramètres Dynamiques

Les paramètres peuvent être ajustés dans la section **variables**, en mettant la liste des variables souhaitées.
Pour chacune d'entre elles, un *label*, une *key* et optionnelement une valeur par défaut *value* sont nécessaires.
Pour être prise en compte, ces variables doivent être implémenté dans le prompt template via leur *'key'* sous la forme **{ma_variable}**

Une secode version, permet de séparer le formulaire en plusieurs parties pour mieux l'organiser.
Chaque section/partie ('part') regroupe plusieurs paramètres sous un nom et un numéro, pour faciliter leur tri.

Vous pouvez consultez directement le fichier **config.yaml** pour pluys de détails.

#### Prompt template

Vous pouvez directement spécifier votre prompt template dans la section **prompt_template** du fichier de configuration

#### Prompt system

Egalement, vous pouvez renseigner un prompt système par défaut, dans la section **prompt_system** du fichier de configuration

#### Prompts par Défaut

Des *prompts* par défaut peuvent être définis pour démarrer les conversations avec l'IA. Ces *prompts* sont personnalisables dans la section **prompts**.
La première tabulation correspond à une catégorie, permettant de faire des regroupements.
Chaque '-' représente ensuite un prompt qui sera proposé.

## Déploiement

Pour déployer cette application sur Huggingface :

1. Dupliquez l'espace Huggingface existant.
2. Renseignez les variables d'environnements. Il vous sera demandé de rentrer toutes les variables d'environnements. Vous les variables qui seront propres à votre application : 
 - **APP_NAME** : Nom de votre application
 - **PINECONE_NAMESPACE** : Espace de stockage permanent de votre application
3. Ajustez votre configuration dans le fichier *config.yaml* (voir section **Configuration de l'application**)


## Variables d'environnements
| Variable | Description 
|----------|----------
**APP_NAME**|Nom de l'application
**ANTHROPIC_API_KEY**| Clé API Anthropic
**MISTRAL_API_KEY**|Clé API Mistral
**OPENAI_API_KEY**|Clé API OpenAI
**LLAMA_API_KEY**|Clé Llama API
**PINECONE_API_KEY**|Clé API Pinecone
**PINECONE_INDEX_NAME**|Index/BDD Pinecone
**PINECONE_NAMESPACE**|Espace de stockage propre à l'application


