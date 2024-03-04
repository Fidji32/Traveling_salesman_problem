#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().run_line_magic('reset', '')


# In[3]:


import numpy as np
import matplotlib.pyplot as plt
import random as rd
import copy


# In[4]:


# normalisation des coordonnées gps
def genererCoordonneesBarsEtNomsNormalisees():
    coordonnees_gps = [
        (43.604495972132185, 1.4339316846567265, "Flashback Café"),
        (43.6038603806508, 1.436052813492545, "Le Bar Basque"),
        (43.6032673204229, 1.4363527000000003, "Jenja"),
        (43.604432565378914, 1.4386421134925451, "Bar Des Zés"),
        (43.604549934114694, 1.4394285288358184, "El CIRCO BAR LATINO Y TAPAS"),
        (43.60764883376083, 1.4394702711641814, "THE GEORGE AND DRAGON"),
        (43.60634039278638, 1.4409365441790916, "buvette"),
        (43.60168657829994, 1.4406341306865467, "Le Petit Voisin"),
        (43.60094571876028, 1.4436218, "Chupitos"),
        (43.597429327387744, 1.4438735711641812, "The London Town English Pub"),
        (43.59804012588923, 1.444627613492545, "LA LOGE"),
        (43.60929360833377, 1.4447028000000002, "Le Tchin"),
        (43.609583105277295, 1.4468518545190436, "WANTED JACK SALOON"),
        (43.60392444241875, 1.4472093711641816, "Chez Joseph"),
        (43.60471700950679, 1.4486805288358182, "Oulala"),
        (43.60713716633343, 1.451311313492545, "Delirium Café"),
        (43.604991302151674, 1.4512030000000002, "The Frog & Rosbif"),
        (43.60451041689108, 1.4514433999999998, "Café Populaire"),
        (43.60596588785447, 1.4524200423283633, "Au Fût et à mesure")
    ]

    # Séparer les données en listes distinctes
    latitudes, longitudes, noms = zip(*coordonnees_gps)

    # Obtenir les min et max pour chaque coordonnée
    min_lat, min_lon = np.min(latitudes), np.min(longitudes)
    max_lat, max_lon = np.max(latitudes), np.max(longitudes)

    # Normaliser les coordonnées dans une figure de 1 par 1
    coordonnees_normalisees = [
        ((lat - min_lat) / (max_lat - min_lat), (lon - min_lon) / (max_lon - min_lon), name)
        for lat, lon, name in coordonnees_gps
    ]

    return coordonnees_normalisees

# formatage donnnées points
def formatageCoordonneesBars(population):
    cp = copy.deepcopy(population) # créer une copie profonde de la population
    XY_DONNEES = [coord[:2] for coord in genererCoordonneesBarsEtNomsNormalisees()]
    X, Y = zip(*XY_DONNEES)  # Extracting first and second columns into x and y
    return np.array(X), np.array(Y)

# évaluation de la population
def fitness(chemin):
    XY = np.column_stack((X[chemin], Y[chemin])) # génère un table bidimentionnel avec côte à côte les colonnes x et y 
    distance = np.sum(np.sqrt(np.sum((XY - np.roll(XY, -1, axis=0)) ** 2, axis=1)[:-1])) # [:-1] ne pas faire dernière ville
    return distance

# calculer la fitness de chaque chemin dans la population
def fitness_population(population):
    cp = copy.deepcopy(population) # créer une copie profonde de la population
    return [fitness(chemin) for chemin in cp]

# trier la population en fonction de la fitness de chaque chemin
def trier_population_par_fitness(population):
    cp = copy.deepcopy(population) # créer une copie profonde de la population
    return [x for _, x in sorted(zip(fitness_population(population), population))]

# génération poputation
def genererPopulationInitiale(population):
    cp = copy.deepcopy(population) # créer une copie profonde de la population
    for i in range(0, DIMENSION_POPULATION, 1):
        for j in range(0, NOMBRE_VILLES, 1):
            bool = 1
            if j == 0:
                element = rd.randint(0, NOMBRE_VILLES - 1)
            else:
                while bool == 1:
                    element = rd.randint(0, NOMBRE_VILLES - 1)
                    l = 0
                    for k in range(0, j, 1):
                        if cp[i][k] == element:
                            bool = 1
                            l = l + 1
                    if l == 0:
                        bool = 0
            cp[i][j] = element
    return cp

# pas utile car trop gourmand
# affichage de la population
def affichagePopulation(population):
    cp = copy.deepcopy(population) # créer une copie profonde de la population
    for i, chemin in enumerate(cp): 
        d = fitness(chemin)
        print(f'Proposition chemin {i} : {cp[i]}, fitness = {d}')
        plt.figure()  # Crée une nouvelle figure à chaque itération
        plt.plot(X[chemin], Y[chemin], marker = 'o', color = COULEURS[i]) # dessine le graphe
        plt.title(f'Proposition chemin {i}: {cp[i]}, fitness = {d}') # ajoute un titre au graphe
 
# affichage de la population
def affichageMeilleurCheminPopulation(population):
    cp = copy.deepcopy(population) # créer une copie profonde de la population
    for i, chemin in enumerate(cp):
        if i == 0:
            d = fitness(chemin)
            print(f'Proposition chemin {i} : {cp[i]}, fitness = {d}')
            plt.figure()  # Crée une nouvelle figure à chaque itération
            plt.plot(X[chemin], Y[chemin], marker = 'o', color = COULEURS[i]) # dessine le graphe
            plt.title(f'Proposition chemin {i}: {cp[i]}, fitness = {d}') # ajoute un titre au graphe

# ajouter la ville de départ à la fin du chemin
def ajoutVilleDepartFinChemin(population):
    cp = copy.deepcopy(population) # créer une copie profonde de la population
    for chemin in cp:
        chemin.append(chemin[0])
    return cp

# génère deux fils à partir de deux parents
def croisement(parent_a, parent_b, population):
    cp = copy.deepcopy(population) # créer une copie profonde de la population
    n = len(parent_a) # obtient la longueur des parents
    start = rd.randint(0, n - 1) # indice de début de la coupe
    end = rd.randint(0, n - 1) # indice de fin de la coupe
    if start > end: # vérification début est bien le début
        start, end = end, start
    
    # initialisation des fils de la taille des parents
    fils1 = [-1] * n
    fils2 = [-1] * n
    
    # copie de la coupe parent dans les enfants
    fils1[start:end] = parent_a[start:end]
    fils2[start:end] = parent_b[start:end]
    
    # remplissage des parties manquantes des fils en copiant les éléments des parents
    for i in range(n):
        if parent_b[i] not in fils1:
            if -1 in fils1:
                index = fils1.index(-1)
                fils1[index] = parent_b[i]
        if parent_a[i] not in fils2:
            if -1 in fils2:
                index = fils2.index(-1)
                fils2[index] = parent_a[i]
                
    # récupération des éléments manquants de chaque parent
    missing_a_fils2 = [x for x in parent_a if x not in fils2]
    missing_b_fils1 = [x for x in parent_b if x not in fils1]

    # complétion des fils
    for i in range(n):
        if fils1[i] == -1:
            if missing_a_fils2:
                fils1[i] = missing_a_fils2.pop(0)
        if fils2[i] == -1:
            if missing_b_fils1:
                fils2[i] = missing_b_fils1.pop(0)
    
    # ajout des fils dans la population
    return mutation(fils1), mutation(fils2)

# permet de croisser deux à deux tous les membre d'une population
def croissement_population(population):
    cp = copy.deepcopy(population) # créer une copie profonde de la population
    rd.shuffle(cp)  # Mélanger aléatoirement la population
    nombre_couples = len(cp)//2
    for i in range (0, nombre_couples):
        fils1, fils2 = croisement(cp[-2+2*i], cp[-1+2*i], cp) # croissement deux à deux
        cp.append(fils1)
        cp.append(fils2)
        
    return cp

# réalise la sélection par rang
def selectionParRang(population):
    cp = copy.deepcopy(population) # créer une copie profonde de la population
    population_fitness_tri = trier_population_par_fitness(ajoutVilleDepartFinChemin(cp)) # tri population selon fitness
    population_fitness_tri = [chemin[:-1] for chemin in population_fitness_tri] # enlever le debut en fin de chemin
    faibles = len(population_fitness_tri)//2 # taille de la population faible
    for _ in range(faibles): # supprimer les 'faible' éléments à partir de la fin
        population_fitness_tri.pop(-1)
    return population_fitness_tri

# réalise une mutation sur un fils de la population
def mutation(fils):
    if round(rd.uniform(0, 1), 2) >= 0.95 : # mutation avec 5% de chance
        # sélection aléatoire des villes à permuter
        ville_a = rd.randint(0, NOMBRE_VILLES - 1)
        ville_b = rd.randint(0, NOMBRE_VILLES - 1)
        while ville_a == ville_b :
            ville_b = rd.randint(0, NOMBRE_VILLES - 1)
        fils_ville_a = fils[ville_a]
        fils[ville_a] = fils[ville_b]
        fils[ville_b] = fils_ville_a
    return fils


# In[5]:


Donnees = genererCoordonneesBarsEtNomsNormalisees()
NOMBRE_VILLES = len(Donnees) # défini le nombre de villes à parcourir
DIMENSION_POPULATION = 10 # défini le nombre de la population
COULEURS = plt.cm.viridis(np.linspace(0, 1, DIMENSION_POPULATION)) # génère une liste de couleur selon DIMENSION_POPULATION
NOMBRE_GENERATIONS = 10000
# génération coordonnées villes
X, Y = formatageCoordonneesBars(Donnees)


# In[6]:


# utilise l'algorithme de génétique sur x génération pour le problème du voyageur de commerce
def main(generation):
    # variable rassemblant toutes les populations des différentes générations
    liste_populations = []
    
    # génération population initiale
    population = [([0] * NOMBRE_VILLES) for _ in range(DIMENSION_POPULATION)] # initialisation population à 0
    population = genererPopulationInitiale(population)
    # ajout dans la liste des populations
    liste_populations.append(population)
    
    # algorithme de génétique sur x génération
    for i in range (0, generation) :
        population = selectionParRang(croissement_population(population))
        liste_populations.append(population)
    return liste_populations


# In[7]:


liste_population_generation = main(NOMBRE_GENERATIONS)
# for i in range (0, NOMBRE_GENERATIONS + 1):
# for i in range (0, NOMBRE_GENERATIONS + 1):
#     print(f'Population {i}')
#     print(f'taille {len(liste_population_generation[i])}')
#     print(liste_population_generation[i])
#     affichageMeilleurCheminPopulation(ajoutVilleDepartFinChemin(liste_population_generation[i]))


# In[157]:


# Utilisation de la fonction
coordonnees_bars_et_noms_normalisees = genererCoordonneesBarsEtNomsNormalisees()

# Création de la figure
fig, ax = plt.subplots(figsize=(15, 12))

# Tracer les points
for lat, lon, name in coordonnees_bars_et_noms_normalisees:
    ax.scatter(lon, lat, label=name)

# Ajouter des annotations avec le nom des villes à côté des points
for lat, lon, name in coordonnees_bars_et_noms_normalisees:
    ax.annotate(name, (lon, lat), textcoords="offset points", xytext=(5, 5), ha='left')

# Ajouter des labels aux axes
ax.set_xlabel('Longitude normalisée')
ax.set_ylabel('Latitude normalisée')

# Tracer le chemin en pointillé
chemin_indices = ajoutVilleDepartFinChemin(liste_population_generation[-1])[0]
chemin_coords = np.array([(coordonnees_bars_et_noms_normalisees[i][1], coordonnees_bars_et_noms_normalisees[i][0]) for i in chemin_indices])
ax.plot(chemin_coords[:, 0], chemin_coords[:, 1], linestyle='dotted', color='black', label='Chemin', linewidth=0.5, dash_capstyle='round')

# calcul fitness meilleur chemin génération finale
d = fitness(chemin_indices)

# Ajouter un titre à la figure
ax.set_title(f'Proposition chemin dernière génération: {chemin_indices}, fitness = {d}')

# Afficher la légende
ax.legend()

# Afficher la figure
plt.show()


# In[8]:


# Utilisation de la fonction
coordonnees_bars_et_noms_normalisees = genererCoordonneesBarsEtNomsNormalisees()

# Création de la figure
fig, ax = plt.subplots(figsize=(15, 12))

# Tracer les points
for lat, lon, name in coordonnees_bars_et_noms_normalisees:
    ax.scatter(lon, lat, label=name)

# Ajouter des annotations avec le nom des villes à côté des points
for lat, lon, name in coordonnees_bars_et_noms_normalisees:
    ax.annotate(name, (lon, lat), textcoords="offset points", xytext=(5, 5), ha='left')

# Ajouter des labels aux axes
ax.set_xlabel('Longitude normalisée')
ax.set_ylabel('Latitude normalisée')

# Tracer le chemin en pointillé
chemin_indices = ajoutVilleDepartFinChemin(liste_population_generation[0])[0]
chemin_coords = np.array([(coordonnees_bars_et_noms_normalisees[i][1], coordonnees_bars_et_noms_normalisees[i][0]) for i in chemin_indices])
ax.plot(chemin_coords[:, 0], chemin_coords[:, 1], linestyle='dotted', color='black', label='Chemin', linewidth=0.5, dash_capstyle='round')

# calcul fitness meilleur chemin génération finale
d = fitness(chemin_indices)

# Ajouter un titre à la figure
ax.set_title(f'Proposition chemin dernière génération: {chemin_indices}, fitness = {d}')

# Afficher la légende
ax.legend()

# Afficher la figure
plt.show()


# In[ ]:




