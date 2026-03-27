# FONCTIONS EXISTANTES
conversions.py :
	- [x] taxid_to_latin_name (suggestion de nom simplifié : taxid2name)
	- [x] latin_name_to_taxid (suggestion : name2taxid)

phylogeny.py : 
	- [x] get_ascendants : Get the lineage (list of ancestors) for a given taxid or name. 
	- [x] get_descendants : Get all descendant taxids for a given taxid or name.
		

# FONCTIONS À CRÉER MODIFIER
- [ ] get_descendants : Ajout options/autres fonctions pour retourner uniquement les feuilles, les siblings, direct children
- [ ] Créer une classe SolrRequest : méthode(s) d'exécution de requête, méthode(s) d'extraction des résultats
- [ ] get_MRCA : Améliorer pour prendre une liste en input, et une seule requête Solr (pas une par taxid) 

