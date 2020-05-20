import sys, os

__author__ = 'Nomi'

sys.path.append(os.path.dirname(sys.path[0]))

from defs import *
from utils.msa_functions import get_msa_properties

TITLES = [ID_COL, 'ntaxa', 'length']
TITLES_SIM = [ID_COL, 'replicate', 'ntaxa', 'length']

def msa_features(dic, output_name):

    exceptions = []
    data = {name: [] for name in TITLES}

    for id, rel_path in dic.items():

        msa_path = os.path.join(DATA_PATH, rel_path, REF_MSA_PHY)

        try:
            (n, length) = get_msa_properties(msa_path)
        except:
            exceptions.append(msa_path)
            continue

        data[TITLES[0]].append(id)
        data[TITLES[1]].append(n)
        data[TITLES[2]].append(length)

    df = pd.DataFrame(data)
    df = df[TITLES]
    df.to_csv(output_name, index=False)

    d = {"exceptions": exceptions}
    df = pd.DataFrame(d)
    df.to_csv("exceptions.csv")


def msa_features_simulations(dic, output_name):

    exceptions = []
    data = {name: [] for name in TITLES_SIM}

    for id, rel_path in dic.items():
        for i in range(1,N_SIM+1):

            file = INDELIBLE_TRUE.format(i=i)
            msa_path = os.path.join(DATA_PATH, rel_path, SIMULATIONS_DIR, file)

            try:
                (n, length) = get_msa_properties(msa_path)
            except:
                exceptions.append(SIMULATIONS_DIR)
                continue

            data[TITLES_SIM[0]].append(id)
            data[TITLES_SIM[1]].append(i)
            data[TITLES_SIM[2]].append(n)
            data[TITLES_SIM[3]].append(length)

    df = pd.DataFrame(data)
    df = df[TITLES_SIM]
    df.to_csv(output_name, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f', required=False,
                        help='file of paths', default="")
    parser.add_argument('-o', required=False,
                        help='output name', default="summary.csv")
    parser.add_argument('-simulations', required=False, action='store_true',
                        help='flag')
    args = parser.parse_args()

    if args.f:
        df = pd.read_csv(args.f)
        dic = df.set_index(ID_COL)[PATH_COL].to_dict()
    else:
        dic = DIC

    if args.simulations:
        msa_features_simulations(dic, args.o)
    else:
        msa_features(dic, args.o)



'''
def msa_features_simulations_old(paths_file, output_name):

    df1 = pd.read_csv(paths_file)

    exceptions = []
    frames = []
    for id in df1.index.values:

        row = df1.loc[[id]]
        path = row.at[id,PATH_COL]

        data = {name: [] for name in TITLES}
        for i in range(1,N_SIM+1):
            file = INDELIBLE_TRUE.format(i=i)
            msa_path = os.path.join(DATA_PATH, path, SIMULATIONS_DIR, file)

            try:
                (n, length) = get_msa_properties(msa_path)
            except:
                if SIMULATIONS_DIR not in exceptions:
                    exceptions.append(SIMULATIONS_DIR)
                continue

            data[TITLES[0]].append(i)
            data[TITLES[1]].append(length)

        block1 = pd.concat([row] * N_SIM).reset_index(drop=True)
        block2 = pd.DataFrame(data)[TITLES]

        frames.append(pd.concat([block1, block2], axis=1))

    result = pd.concat(frames)
    result.to_csv(output_name,index=False)
'''