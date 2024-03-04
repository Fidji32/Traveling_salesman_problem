#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('reset', '')


# In[2]:


import numpy as np
import matplotlib.pyplot as plt
import random as rd
import copy


# In[3]:


# générer coordonées villes
def genererCoordonneesVilles():
    # génère 5 (NOMBRE_VILLES) nombres aléatoires dans l'intervalle [0, 1]
    return np.random.uniform(0, 1, NOMBRE_VILLES), np.random.uniform(0, 1, NOMBRE_VILLES)

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


# In[4]:


NOMBRE_VILLES = 20 # défini le nombre de villes à parcourir
DIMENSION_POPULATION = 10 # défini le nombre de la population
COULEURS = plt.cm.viridis(np.linspace(0, 1, DIMENSION_POPULATION)) # génère une liste de couleur selon DIMENSION_POPULATION
NOMBRE_GENERATIONS = 10000
# génération coordonnées villes
X, Y = genererCoordonneesVilles()


# In[5]:


# utilise l'algorithme de génétique sur x génération pour le problème du voyageur de commerce
def main(generation):
    # variable rassemblant toutes les populations des différentes générations
    liste_populations = []
    population = []
    
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


# In[6]:


# affichage position villes
plt.scatter(X, Y, s = 70)


# In[7]:


liste_population_generation = main(NOMBRE_GENERATIONS)
# for i in range (0, NOMBRE_GENERATIONS + 1):
#     print(f'Population {i}')
#     print(f'taille {len(liste_population_generation[i])}')
#     print(liste_population_generation[i])
affichageMeilleurCheminPopulation(ajoutVilleDepartFinChemin(liste_population_generation[0]))
affichageMeilleurCheminPopulation(ajoutVilleDepartFinChemin(liste_population_generation[-1]))


# In[ ]:





# In[ ]:




