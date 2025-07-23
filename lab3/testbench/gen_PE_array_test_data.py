import numpy as np
import torch
import torch.nn.functional as F
import os



# Define constants
TB = 5
PE_ARRAY_H = 6
PE_ARRAY_W = 8
e = 16
r = 1
t = 1
p = 4
q = 4
IFMAP_W = 18
FILTER_ROW = 3
FILTER_COL = 3
IFMAP_H = e + FILTER_ROW - 1
OFF_XID = 31
OFF_YID = 7
OFMAP_F = IFMAP_W - FILTER_COL + 1
OFMAP_E = IFMAP_H - FILTER_ROW + 1
FILE_ID = f"_tb{TB}"
DIR_PATH = "./PE_array_test_data/" + f"tb{TB}/"
TEST_DIR_PATH = "temp/"

# Seed the random number generator
np.random.seed()

# Random Testbench
def gen_data():

    if TB == 0:
        # Debug Friendly Testbench
        ifmap = torch.full((IFMAP_H, IFMAP_W, q * r), 129, dtype=torch.int)
        filter = torch.ones((p*t, FILTER_ROW, FILTER_COL, q * r), dtype=torch.int)
        for i in range(FILTER_ROW):
            for j in range(FILTER_COL):
                filter[:, i, j, :] = i * FILTER_ROW + j
        ipsum = torch.full((OFMAP_E, OFMAP_F, p * t), -1, dtype=torch.int)
    else:
        # Random Testbench
        ifmap = torch.randint(128, 255, (IFMAP_H, IFMAP_W, q * r), dtype=torch.int)
        filter = torch.randint(-128, 128, (p * t, FILTER_ROW, FILTER_COL, q * r), dtype=torch.int)
        ipsum = torch.randint(-65536, 65535, (OFMAP_E, OFMAP_F, p * t), dtype=torch.int)

    ifmap_conv = torch.permute(ifmap, (2, 0, 1))
    ifmap_conv = ifmap_conv - 128
    filte_conv = torch.permute(filter, (0, 3, 1, 2))

    ofmap = F.conv2d(ifmap_conv, filte_conv)
    ofmap = torch.permute(ofmap, (1, 2, 0))
    ofmap += ipsum

    # Write ifmap to file
    with open(f"./PE_array_test_data/tb{TB}/ifmap" + FILE_ID + ".txt", "w") as f:
        flattened_ifmap = ifmap.flatten().numpy()
        f.write(",".join(map(str, flattened_ifmap)))

    # Write filter to file
    with open(f"./PE_array_test_data/tb{TB}/filter" + FILE_ID + ".txt", "w") as f:
        flattened_filter = filter.flatten().numpy()
        f.write(",".join(map(str, flattened_filter)))

    # Write ipsum to file
    with open(f"./PE_array_test_data/tb{TB}/ipsum" + FILE_ID + ".txt", "w") as f:
        flattened_ipsum = ipsum.flatten().numpy()
        f.write(",".join(map(str, flattened_ipsum)))

    # Write ofmap to file
    with open(f"./PE_array_test_data/tb{TB}/opsum" + FILE_ID + ".txt", "w") as f:
        flattened_ofmap = ofmap.flatten().numpy()
        f.write(",".join(map(str, flattened_ofmap)))

def gen_ID():
    group_H = (e + PE_ARRAY_W - 1) // PE_ARRAY_W
    merged_PE_ARRAY_W = PE_ARRAY_W * group_H
    merged_PE_ARRAY_H = PE_ARRAY_H // group_H

    array_H_tile = merged_PE_ARRAY_H // FILTER_ROW
    array_W_tile = merged_PE_ARRAY_W // e
    t_H = array_H_tile // r
    t_W = t // t_H

    # print(f"r_H = {r_H}, r_W = {r_W}, t_H = {t_H}, t_W = {t_W}")
    # print(f"merged_num = {merge_num}")
    # print(f"merged_PE_ARRAY_H = {merged_PE_ARRAY_H}, merged_PE_ARRAY_W = {merged_PE_ARRAY_W}")

    #  ifmap
    ifmap_XID = torch.zeros((PE_ARRAY_H, PE_ARRAY_W), dtype=torch.int)
    for i in range(PE_ARRAY_H):
        for j in range(PE_ARRAY_W):
            if (j < (merged_PE_ARRAY_W // e) * e):
                ifmap_XID[i, j] = (j // (e * t_W)) * (e + FILTER_ROW - 1) + (((i // merged_PE_ARRAY_H) * PE_ARRAY_W + j) % e) + (i % (FILTER_ROW))
            else :
                ifmap_XID[i, j] = OFF_XID

    ifmap_YID = torch.zeros(PE_ARRAY_H, dtype=torch.int)
    for i in range(PE_ARRAY_H):
        ifmap_YID[i] = i // (PE_ARRAY_H // r)

    # filter
    filter_XID = torch.zeros((PE_ARRAY_H, PE_ARRAY_W), dtype=torch.int)
    for i in range(PE_ARRAY_H):
        for j in range (PE_ARRAY_W):
            filter_XID[i,j] = (j // e) * FILTER_ROW + (i % FILTER_ROW)
    filter_YID = torch.zeros(PE_ARRAY_H, dtype=torch.int)
    for i in range(PE_ARRAY_H):
        filter_YID[i] = i // (PE_ARRAY_H // t_H)

    # ipsum
    ipsum_XID = torch.zeros((PE_ARRAY_H, PE_ARRAY_W), dtype=torch.int)
    for i in range(PE_ARRAY_H):
        for j in range(PE_ARRAY_W):
            if ((i % FILTER_ROW) == 0):
                ipsum_XID[i,j] = (i // merged_PE_ARRAY_H) * PE_ARRAY_W + j
            else:
                ipsum_XID[i,:] = OFF_XID

    ipsum_YID = torch.zeros(PE_ARRAY_H, dtype=torch.int)
    for i in range(PE_ARRAY_H):
        if ((i % FILTER_ROW) == 0):
            ipsum_YID[i] = (i // (group_H * FILTER_ROW))
        else:
            ipsum_YID[i] = OFF_YID

    opsum_XID = torch.zeros((PE_ARRAY_H, PE_ARRAY_W), dtype=torch.int)
    for i in range(PE_ARRAY_H):
        for j in range(PE_ARRAY_W):
            if((i % FILTER_ROW) == (FILTER_ROW - 1)):
                opsum_XID[i,j] = (i // merged_PE_ARRAY_H) * PE_ARRAY_W + j
            else:
                opsum_XID[i,:] = OFF_XID

    opsum_YID = torch.zeros(PE_ARRAY_H, dtype=torch.int)
    for i in range(PE_ARRAY_H):
        if((i % FILTER_ROW) == (FILTER_ROW - 1)):
            opsum_YID[i] = i // (FILTER_ROW * group_H)
        else:
            opsum_YID[i] = OFF_YID
    # Write ifmap config chain ID to ifmap_config_chain_ID_tb0.txt
    with open(DIR_PATH + "ifmap_config_chain_XID" + FILE_ID + ".txt", "w") as f:
        flattened_ifmap_XID = ifmap_XID.flatten().numpy()
        f.write(",".join(map(str, flattened_ifmap_XID)))
    with open(DIR_PATH + "ifmap_config_chain_YID" + FILE_ID + ".txt", "w") as f:
        flattened_ifmap_YID = ifmap_YID.flatten().numpy()
        f.write(",".join(map(str, flattened_ifmap_YID)))

    # Write filter config chain ID to filter_config_chain_ID_tb0.txt
    with open(DIR_PATH + "filter_config_chain_XID" + FILE_ID + ".txt", "w") as f:
        flattened_filter_XID = filter_XID.flatten().numpy()
        f.write(",".join(map(str, flattened_filter_XID)))
    with open(DIR_PATH + "filter_config_chain_YID" + FILE_ID + ".txt", "w") as f:
        flattened_filter_YID = filter_YID.flatten().numpy()
        f.write(",".join(map(str, flattened_filter_YID)))

    # Write ipsum config chain ID to ipsum_config_chain_ID_tb0.txt
    with open(DIR_PATH + "ipsum_config_chain_XID" + FILE_ID + ".txt", "w") as f:
        flattened_ipsum_XID = ipsum_XID.flatten().numpy()
        f.write(",".join(map(str, flattened_ipsum_XID)))
    with open(DIR_PATH + "ipsum_config_chain_YID" + FILE_ID + ".txt", "w") as f:
        flattened_ipsum_YID = ipsum_YID.flatten().numpy()
        f.write(",".join(map(str, flattened_ipsum_YID)))

    # Write opsum config chain ID to opsum_config_chain_ID_tb0.txt
    with open(DIR_PATH + "opsum_config_chain_XID" + FILE_ID + ".txt", "w") as f:
        flattened_opsum_XID = opsum_XID.flatten().numpy()
        f.write(",".join(map(str, flattened_opsum_XID)))
    with open(DIR_PATH + "opsum_config_chain_YID" + FILE_ID + ".txt", "w") as f:
        flattened_opsum_YID = opsum_YID.flatten().numpy()
        f.write(",".join(map(str, flattened_opsum_YID)))

def print_txt(ifmap, filter, ipsum, ofmap):
    # Flatten ifmap and write to ifmap.txt with elements separated by commas
    with open(DIR_PATH + "ifmap" + FILE_ID + ".txt", "w") as f:
        flattened_ifmap = ifmap.flatten().numpy()
        f.write(",".join(map(str, flattened_ifmap)))

    # Write filter to filter.txt
    with open(DIR_PATH + "filter" + FILE_ID + ".txt", "w") as f:
        flattened_filter = filter.flatten().numpy()
        f.write(",".join(map(str, flattened_filter)))

    # Write ipsum to ipsum.txt
    with open(DIR_PATH + "ipsum" + FILE_ID + ".txt", "w") as f:
        flattened_ipsum = ipsum.flatten().numpy()
        f.write(",".join(map(str, flattened_ipsum)))

    # Write ofmap to ofmap.txt
    with open(DIR_PATH + "opsum" + FILE_ID + ".txt", "w") as f:
        flattened_ofmap = ofmap.flatten().numpy()
        f.write(",".join(map(str, flattened_ofmap)))

def check():
    ifmap = torch.tensor(np.loadtxt(f"PE_array_test_data/tb/ifmap_tb{TB}.txt", delimiter=",", dtype=int).reshape(IFMAP_H, IFMAP_W, INPUT_CH))
    filt = torch.tensor(np.loadtxt(f"PE_array_test_data/filter_tb{TB}.txt", delimiter=",", dtype=int).reshape(OUTPUT_CH, 3, 3, INPUT_CH))
    ipsum = torch.torch.tensor(np.loadtxt(f"PE_array_test_data/ipsum_tb{TB}.txt", delimiter=",", dtype=int).reshape(OUTPUT_CH, OFMAP_E, OFMAP_F))

    ifmap_file = open(TEST_DIR_PATH + "ifmap_check.txt", "w")
    filter_file = open(TEST_DIR_PATH + "filter_check.txt", "w")
    ipsum_file = open(TEST_DIR_PATH + "ipsum_check.txt", "w")

    ifmap = ifmap - 128

    for c in range(q * r):
        for h in range(4):
            for w in range(4):
                print(f'{ifmap[h,w,c].item():3d}', end=' ', file=ifmap_file)
            print('', file=ifmap_file)
        print('', file=ifmap_file)

    for n in range (p * t):
        print("M = ", n, file=filter_file)
        for c in range(q * r):
            for r in range(3):
                for s in range(3):
                    print(f'{filt[n,r,s,c].item():3d}', end=' ', file=filter_file)
                print('', file=filter_file)
            print('', file=filter_file)


    for n in range (p * t):
        for e in range(2):
            for f in range(2):
                print(f'{ipsum[e,f,n].item():3d}', end=' ', file=ipsum_file)
            print('', file=ipsum_file)
        print('', file=ipsum_file)

    ifmap_file.close()
    filter_file.close()
    ipsum_file.close()

    # print_txt(ifmap, filter, ofmap)

def gcd(x, y):
    while y:
        x, y = y, x % y
    return x

gen_ID()
gen_data()





# ifmap_conv = torch.permute(ifmap, (2, 0, 1))
# ifmap_conv = ifmap_conv - 128
# filte_conv = torch.permute(filter, (0, 3, 1, 2))

# ofmap = F.conv2d(ifmap_conv, filte_conv)
# ofmap = torch.permute(ofmap, (1, 2, 0))
# ofmap += ipsum
# print_txt(ifmap, filter, ofmap)

# ofmap_test = torch.zeros((OFMAP_E, OFMAP_F, OUTPUT_CH), dtype=torch.int)

# for e in range(OFMAP_E):
#     for f in range(OFMAP_F):
#         for n in range(OUTPUT_CH):
#             for r in range(FILTER_ROW):
#                 for s in range(FILTER_COL):
#                     for c in range(INPUT_CH):
#                         ofmap_test[e, f, n] += (ifmap[e + r, f + s, c] - 128) * filter[n, r, s, c]
#             ofmap_test[e, f, n] += ipsum[e, f, n]
