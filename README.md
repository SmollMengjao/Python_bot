# Python_bot
Ebauche, en python, d'un bot capable de récupérer les topics du site jeuxvideo.com et d'y répondre.

Le fichier Credentiels.txt permet d'établir la connexion au site.

Une clé API Gemini est nécessaire pour permettre la génération automatique de réponses. Pour l'instant le programme ne permet que l'utilisation de l'I.A Gémini. Les informations de connexion standard (Nom d'utilisateur et mot de passe) doivent également être renseignées dans le fichier crédentiels.txt. Note : Ne pas ajouter de guillemets.

Pour l'instant le bot ne laisse le choix qu'entre deux modes : Poster les messages un par un, ou 30 par 30 (sans nécessiter aucune intervention entre les messages). Dans le mode 30 messages, l'intervalle entre deux messages est fixé à deux minutes afin de ne pas générer d'alerte flood.

Le Capcha à la connexion doit être résolu manuellement. Une fois cela fait, il suffira d'appuyer sur la touche entrée pour arriver au menu.
