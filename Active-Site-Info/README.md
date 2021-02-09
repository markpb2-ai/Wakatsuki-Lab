## Scraper

To get the PDB files of interest from RCSB, simply use the following command

`python3 scraper.py plpro --n_results 10 --dest_path PDBs`

Note that plpro is an example keyword for scraping and n_results overwrites the default number
of results to return. Dest_path is the path to the directory specified for downloading.

## createActiveSiteInfo

Once you have a directory with PDB files, you can pull the active site information and write it 
to a csv with the following command:

`python3 createActiveSiteInfo.py PDBs`

Note that PDBs is an example of a name of a directory that stores the PDB files. 
