from fastapi import FastAPI, HTTPException

app = FastAPI(title="API Gestion École")

# ===== Base de données mémoire =====
ecole = {}
# { nom_classe: [ {id, nom, prenom, notes[]} ] }


# =====================================================
#  GESTION DES CLASSES
# =====================================================

# ️ Créer une classe
@app.post("/classes")
def creer_classe(nom: str):
    if nom in ecole:
        raise HTTPException(400, "Classe déjà existante")
    ecole[nom] = []
    return {"message": f"Classe {nom} créée"}


# ️ Supprimer une classe
@app.delete("/classes/{nom}")
def supprimer_classe(nom: str):
    if nom not in ecole:
        raise HTTPException(404, "Classe introuvable")

    del ecole[nom]
    return {"message": "Classe supprimée"}


# ️ Afficher la liste des classes
@app.get("/classes")
def liste_classes():
    return {"classes": list(ecole.keys())}


# ️ Afficher les détails d’une classe
#    - Nombre d’étudiants
#    - Liste des étudiants
@app.get("/classes/{nom}")
def details_classe(nom: str):
    if nom not in ecole:
        raise HTTPException(404, "Classe introuvable")

    return {
        "nom": nom,
        "nombre_etudiants": len(ecole[nom]),
        "etudiants": ecole[nom]
    }


# =====================================================
#  GESTION DES ÉTUDIANTS
# =====================================================

# ️ Créer un étudiant (sans classe)
@app.post("/students")
def creer_etudiant(id: str, nom: str, prenom: str):

    # Empêcher doublon global
    for liste in ecole.values():
        for etu in liste:
            if etu["id"] == id:
                raise HTTPException(400, "ID déjà utilisé")

    return {
        "id": id,
        "nom": nom,
        "prenom": prenom,
        "notes": []
    }


# ️ Ajouter un étudiant à une classe
@app.post("/classes/{nom}/students")
def ajouter_etudiant_classe(nom: str, id: str, nom_etu: str, prenom: str):

    # Vérifier si la classe existe
    if nom not in ecole:
        raise HTTPException(404, "Classe inexistante")

    # Empêcher doublon
    for liste in ecole.values():
        for etu in liste:
            if etu["id"] == id:
                raise HTTPException(400, "ID déjà utilisé")

    etu = {
        "id": id,
        "nom": nom_etu,
        "prenom": prenom,
        "notes": []
    }

    ecole[nom].append(etu)

    return {"message": "Étudiant ajouté", "etudiant": etu}


# ️ Supprimer un étudiant d’une classe
@app.delete("/students/{id}")
def supprimer_etudiant(id: str):
    for classe, liste in ecole.items():
        for etu in liste:
            if etu["id"] == id:
                liste.remove(etu)
                return {"message": f"Supprimé de la classe {classe}"}

    raise HTTPException(404, "Étudiant introuvable")


# ️ Afficher la liste des étudiants d’une classe
@app.get("/classes/{nom}/students")
def liste_etudiants_classe(nom: str):
    if nom not in ecole:
        raise HTTPException(404, "Classe introuvable")

    return ecole[nom]


# ️ Rechercher un étudiant par ID
@app.get("/students/{id}")
def rechercher_etudiant(id: str):
    for classe, liste in ecole.items():
        for etu in liste:
            if etu["id"] == id:
                return {"classe": classe, "etudiant": etu}

    raise HTTPException(404, "Étudiant introuvable")


#  Afficher les informations d’un étudiant


@app.get("/students/{id}/info")
def infos_etudiant(id: str):
    for liste in ecole.values():
        for etu in liste:
            if etu["id"] == id:
                return etu

    raise HTTPException(404, "Étudiant introuvable")


# =====================================================
#  FONCTIONNALITÉS SUPPLÉMENTAIRES
# =====================================================

#  Modifier les informations d’un étudiant
@app.put("/students/{id}")
def modifier_etudiant(id: str, nom: str, prenom: str):
    for liste in ecole.values():
        for etu in liste:
            if etu["id"] == id:
                etu["nom"] = nom
                etu["prenom"] = prenom
                return {"message": "Informations mises à jour"}

    raise HTTPException(404, "Étudiant introuvable")


#  Gérer les notes d’un étudiant (ajouter note)
@app.post("/students/{id}/notes")
def ajouter_note(id: str, note: float):
    for liste in ecole.values():
        for etu in liste:
            if etu["id"] == id:
                etu["notes"].append(note)
                return {"message": "Note ajoutée"}

    raise HTTPException(404, "Étudiant introuvable")


#  Calculer la moyenne d’un étudiant
@app.get("/students/{id}/average")
def moyenne_etudiant(id: str):
    for liste in ecole.values():
        for etu in liste:
            if etu["id"] == id:
                if not etu["notes"]:
                    return {"moyenne": None}
                return {"moyenne": sum(etu["notes"]) / len(etu["notes"])}

    raise HTTPException(404, "Étudiant introuvable")


#  Calculer la moyenne d’une classe
@app.get("/classes/{nom}/average")
def moyenne_classe(nom: str):
    if nom not in ecole:
        raise HTTPException(404, "Classe introuvable")

    notes = []
    for etu in ecole[nom]:
        notes.extend(etu["notes"])

    if not notes:
        return {"moyenne": None}

    return {"moyenne": sum(notes) / len(notes)}


#  Statistiques générales
@app.get("/stats")
def statistiques():
    total_etudiants = sum(len(liste) for liste in ecole.values())

    return {
        "nombre_classes": len(ecole),
        "nombre_total_etudiants": total_etudiants
    }
