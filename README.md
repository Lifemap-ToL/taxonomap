# FONCTIONS EXISTANTES
conversions.py :
- [x] taxid_to_latin_name (suggestion de nom simplifié : taxid2name)
- [x] latin_name_to_taxid (suggestion : name2taxid)

phylogeny.py :
- [x] get_ascendants : Get the lineage (list of ancestors) for a given taxid or name. 
- [x] get_descendants : Get all descendant taxids for a given taxid or name.
		

# FONCTIONS À CRÉER MODIFIER
- [X] get_descendants : Ajout options/autres fonctions pour retourner uniquement les feuilles, les siblings, direct children
- [] Mutualiser des parties de get_descendants + get_ascendants (répétitions)
- [X] Créer une classe SolrRequest : méthode(s) d'exécution de requête, méthode(s) d'extraction des résultats
- [ ] get_MRCA : 
	- [ ] Améliorer pour prendre une liste en input
	- [ ] Une seule requête Solr (et non une par taxid) 
	- [ ] Vérification #taxid = #documents

- [ ] Afficher la version de la taxonomie utilisée (?)
- [ ] validation.py : Créer une fonction qui vérifie les listes en entrées, et pour chaque taxid de la liste vérifie : 
	- que c'est soit une str soit un int
	- si c'est une str, la convertit en int
	- vérifie qu'il s'agit d'un entier positif

