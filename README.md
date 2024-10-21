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

Cette application sert de base/template pour en déployer d'autres sur le même modèle via Huggingface. Elle est facilement duplicable en dupliquant l'espace. Elle est décomposée en plusieurs sections pour offrir une gestion complète des documents et des dialogues avec une Intelligence Artificielle (IA).

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

Les documents (communs et personnels) sont vectorisés et stockés dans une base de données vectorielle. Cela permet à l'IA de rechercher et d'explorer ces documents pour enrichir les conversations en fonction des informations disponibles.

## Paramètres Dynamiques

Cette application permet la gestion de paramètres dynamiques configurables via l'interface utilisateur. Ces paramètres modifient le comportement de l'application et de l'IA en fonction des besoins de l'utilisateur.

## Prompts par Défaut

Des *prompts* par défaut peuvent être définis pour démarrer les conversations avec l'IA. Ces *prompts* sont personnalisables dans la section "Prompt système" des **Configurations**.

## Déploiement

Pour déployer cette application sur Huggingface :

1. Dupliquez l'espace Huggingface existant.
2. Configurez les fichiers de l'application (paramètres, prompts par défaut, etc.).
3. Assurez-vous que la base de données vectorielle est correctement co


