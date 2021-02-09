'''
The following program is a scraper that that scrapes the RCSB for PDB files that
have the given keyword in their title. It downloads the PDB file and fasta to a directory
of your choosing allowing you to specify the max number of results to be downloaded.
If the file already exists in the destination directory a duplicate is not created. 

Sample Usage: python scraper.py plpro -n 1000 --dest_path TESTS 

The above sample scrapes RCSB for the first 1000 files with the keyword plpro and 
downloads PDB and fast files to the TESTS directory, creating one if it does not
already exist
'''

import os
import time
import datetime
import json
import argparse
import requests
from urllib.parse import quote


'''
Creates an html version of the url to be decoded into the query results.
'''
def scrape(url):
    r = requests.get(url)
    html = r.content.decode("utf-8")
    return html

'''
The following function downloads a file and writes the contents of the file
to the specified directory. 
'''

def download(url, dest):
    r = requests.get(url)
    open(dest, "wb").write(r.content)

'''
The following function handles the the creation and parsing of the command line
arguments specified by the user. 
'''

def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("keyword", type=str, help="Keyword for PDB website search")
    p.add_argument("--n_results", "-n", type=int, default=5, help="Maxmium number of results to be scraped")
    p.add_argument("--dest_path", type=str, default="PDBs", help="Path where PDB files will be saved")
    p.add_argument("--verbose", "-v", action="store_true", help="Be verbose")
    return p.parse_args()

'''
The following function searches the RCSB using the specified keyword and compiles a list
of results from the query. For each of these results the PDB file and the fasta file are 
downloaded to the specified directory.  
'''

def main():
    args = parse_args()
    json_text = '{"query":{"parameters":{"value":"plpro"},"service":"text","type":"terminal","node_id":0},"return_type":"entry","request_options":{"pager":{"start":0,"rows":100},"scoring_strategy":"combined","sort":[{"sort_by":"rcsb_accession_info.initial_release_date","direction":"desc"}]}}'
    params = json.loads(json_text)
    params["query"]["parameters"]["value"] = args.keyword 
    url = "https://search.rcsb.org/rcsbsearch/v1/query?json=" + quote(json.dumps(params)) 
    print("Fetching {}".format(url))
    html = scrape(url)
    results = json.loads(html)
    pdb_list = [result["identifier"] for result in results["result_set"]]
    print("Found the following:" + pdb_list.__repr__())
    n = min(args.n_results, len(pdb_list))
    os.makedirs(args.dest_path, exist_ok=True)
    for pdb_id in pdb_list[:n]:
        dest = "{}/{}.pdb".format(args.dest_path, pdb_id)
        dest1 =  "{}/{}.fasta".format(args.dest_path, pdb_id)
        if os.path.isfile(dest):
            print("{} exists, skipping...".format(pdb_id))
            continue
        url = "https://files.rcsb.org/download/{}.pdb".format(pdb_id)
        url1 = "https://rcsb.org/fasta/entry/{}".format(pdb_id)
        print("Fetching {}".format(url))
        print("Fetching {}".format(url1))
        download(url, dest)
        download(url1, dest1)

if __name__ == "__main__":
    main()
