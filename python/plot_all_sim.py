from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

if __name__ == "__main__":
    similarity_fingerprints = '../misc/similarity_fingerprints.npz'
    with open(similarity_fingerprints, "rb") as data:
        sim_fp = np.load(data) 
        sim_fp = sim_fp['features']

    with open('../misc/compounds16978to16170.npy', 'rb') as data:
        compounds_final_indicies_from_16978 = np.load(data)

    mask=np.zeros( (16978, 16978), dtype=bool)
    mask[compounds_final_indicies_from_16978, compounds_final_indicies_from_16978] = True
    sim_fp = sim_fp[np.ix_(compounds_final_indicies_from_16978,compounds_final_indicies_from_16978)]

    coords = []
    for x in tqdm(range(sim_fp.shape[0])):
        for y in range(sim_fp.shape[0]):
            if x < y:
                coords.append((x,y))

    similarities = []
    for coord in tqdm(coords): 
        similarities.append(sim_fp[coord[0], coord[1]])
        
    x = [(similarities,'blue', 'Compound similarity')]
    plt.figure(figsize=(16,16))

    sb.set(font_scale = 0.65)
    sb.displot(x[0][0], color = x[0][1], stat="probability").set_axis_labels("Similarity", "Probability")
    plt.tight_layout()
    plt.savefig('../plots/similarities/similarities_final_p.svg')