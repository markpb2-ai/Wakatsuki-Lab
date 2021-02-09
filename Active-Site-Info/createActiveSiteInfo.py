# The following program is a program that enables the user to find the active site information for a 
# directory of PDB entries and output a csv file with the active site information to the pdb directory.
import os
import json
import argparse
import requests
import logging
from urllib.parse import quote
from typing import List

def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("directory_name", type=str, help="Where PDB files are stored")
    p.add_argument("--verbose", "-v", action="store_true", help="Be verbose")
    return p.parse_args()


def get_uniprot_act_residues(json, act_file):
    uniprot_act_residues = []
    if('data' in json and 'annotations' in json['data'] and len(json['data']['annotations']) != 0 and 'features' in json['data']['annotations'][0]):
        new_json = json['data']['annotations']
    else: 
        act_file.write("N/A\n")
        return []
    new_entry = ""
    for j in range(len(new_json)):  
        for i in range(len(new_json[j]['features'])):
            if (new_json[j]['features'][i]['type'] == 'ACTIVE_SITE'):
                uniprot_act_residues.append(new_json[j]['features'][i]['feature_positions'][0]["beg_seq_id"])
                new_entry = new_entry + str(new_json[j]['features'][i]['feature_positions'][0]["beg_seq_id"]) + ":"
    if(len(new_entry) == 0):
        new_entry = "N/A\n"
    else:
        new_entry = str(new_entry[:len(new_entry)-1]) + "\n"
    act_file.write(new_entry)
    return uniprot_act_residues  


def find_binding(pdb_code, pdb_filename, dname, abspath, pdb_fasta_name, act_file) :
    act_file.write("{}, ".format(str(pdb_code)))
    url = requests.get("https://1d-coordinates.rcsb.org/graphql?query=%7B%0A%20%20annotations(%0A%20%20%20%20reference:PDB_INSTANCE%0A%20%20%20%20sources:%5BUNIPROT%5D%0A%20%20%20%20queryId:%22{}.A%22%0A%20%20)%7B%0A%20%20%20%20target_id%0A%20%20%20%09features%20%7B%0A%20%20%20%20%20%20feature_id%0A%20%20%20%09%20%20description%0A%20%20%20%09%20%20name%0A%20%20%20%09%20%20provenance_source%0A%20%20%20%09%20%20type%0A%20%20%20%20%20%20feature_positions%20%7B%0A%20%20%20%20%20%20%20%20beg_ori_id%0A%20%20%20%20%20%20%20%20beg_seq_id%0A%20%20%20%20%20%20%20%20end_ori_id%0A%20%20%20%20%20%20%20%20end_seq_id%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D".format(pdb_code))
    uniprot_act_residues = get_uniprot_act_residues(url.json(), act_file)
    print("uniprot_act_residues:", uniprot_act_residues)

def main():
    args = parse_args()
    abspath = os.path.abspath(args.directory_name)
    dname = os.path.dirname(abspath)
    os.chdir(abspath)
    pubmed_id_dict = {}
    act_file = open("act_seq.csv", "w")
    act_file.write("PDB_CODE, ACTIVE SITE RESIDUES\n")
    for entry in os.scandir(abspath):
        if entry.path.endswith(".pdb") and entry.is_file():
            pdb_code = str(entry)[11:(len(str(entry))-6)]
            pdb_fasta_name = pdb_code + ".fasta"
            find_binding(pdb_code, str(entry)[11:(len(str(entry))-2)], dname, abspath, pdb_fasta_name, act_file)
    act_file.close()
if __name__ == "__main__":
    main()