import numpy as np import torch import torch.nn.functional as F import os

#Define constants
    IFMAP_COL = 18 FILTER_COL = 3 INPUT_CHANNEL = 4 OFMAP_CHANNEL = 4 OFMAP_COL = IFMAP_COL - FILTER_COL + 1 FILE_ID = "_tb2" DIR_PATH = "./PE_test_data/"

#Seed the random number generator
    np.random.seed()

#== == == == == == == == == == == == == == == == == = TB0 == == == == == == == == == == == == == == == == == = #
#Debug Friendly Testbench

# #Generate ifmap with alternating 128 and 129
#ifmap = torch.full((1, IFMAP_COL, INPUT_CHANNEL), 128, dtype = torch.int)
#for col in range(IFMAP_COL):
#if col % 2 == 0:
#ifmap[0, col, : ] = 129

# #Generate filter with all elements equal to 1
#filter = torch.ones((OFMAP_CHANNEL, 1, FILTER_COL, INPUT_CHANNEL), dtype = torch.int)
#for oc in range(OFMAP_CHANNEL):
#filter[oc, 0, :, : ] = oc

# #Generate ipsum with all elements equal to - 1
#ipsum = torch.full((OFMAP_COL, OFMAP_CHANNEL), -1, dtype = torch.int)

#== == == == == == == == == == == == == == == == == = TB0 == == == == == == == == == == == == == == == == == = #

#== == == == == == == == == == == == == == == == == TB1 / TB2 == == == == == == == == == == == == == == == == == #
#Randomized Testbench

                       ifmap = torch.randint(0, 256, (1, IFMAP_COL, INPUT_CHANNEL), dtype = torch.int) filter = torch.randint(- 128, 127, (OFMAP_CHANNEL, 1, FILTER_COL, INPUT_CHANNEL), dtype = torch.int) ipsum = torch.randint(- 65536, 65535, (OFMAP_COL, OFMAP_CHANNEL), dtype = torch.int)

#== == == == == == == == == == == == == == == == == TB1 / TB2 == == == == == == == == == == == == == == == == == #

#Read ifmap from ifmap.txt
#ifmap = np.loadtxt("./test_data/ifmap_tb0.txt", delimiter = ",", dtype = np.float64)
#ifmap = torch.tensor(ifmap).reshape(1, IFMAP_COL, INPUT_CHANNEL)

#filter = np.loadtxt("./test_data/filter_tb0.txt", delimiter = ",", dtype = np.float64)
#filter = torch.tensor(filter).reshape(OFMAP_CHANNEL, 1, FILTER_COL, INPUT_CHANNEL)

#ipsum = np.loadtxt("./test_data/ipsum_tb0.txt", delimiter = ",", dtype = np.float64)
#ipsum = torch.tensor(ipsum).reshape(OFMAP_COL, OFMAP_CHANNEL)

# #Initialize ofmap
                                                                                                                                                                                                                                                                                  ofmap = torch.zeros((1, OFMAP_COL, OFMAP_CHANNEL), dtype = torch.int)

#def conv1d(ifmap, filter, ofmap):
#for f in range(len(ofmap[0])):
#for oc in range(len(ofmap[0][0])):
#for i in range(len(filter[0][0])):
#for ic in range(len(filter[0][0][0])):
#ofmap[0][f][oc] += ifmap[0][f + i][ic] * filter[oc][0][i][ic]

                                                                                                                                                                                                                                                                                                                                         def add(ofmap, ipsum) :ofmap += ipsum

                                                                                                                                                                                                                                                                                                                                                 def print_txt(ifmap, filter, ofmap) :
#Flatten ifmap and write to ifmap.txt with elements separated by commas
                                                                                                                                                                                                                                                                                                                                                               with open(DIR_PATH + "ifmap" + FILE_ID + ".txt", "w") as f:flattened_ifmap = ifmap.flatten().numpy() f.write(",".join(map(str, flattened_ifmap)))

#Write filter to filter.txt
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                with open(DIR_PATH + "filter" + FILE_ID + ".txt", "w") as f:flattened_filter = filter.flatten().numpy() f.write(",".join(map(str, flattened_filter)))

#Write ipsum to ipsum.txt
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    with open(DIR_PATH + "ipsum" + FILE_ID + ".txt", "w") as f:flattened_ipsum = ipsum.flatten().numpy() f.write(",".join(map(str, flattened_ipsum)))

#Write ofmap to ofmap.txt
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     with open(DIR_PATH + "ofmap" + FILE_ID + ".txt", "w") as f:flattened_ofmap = ofmap.flatten().numpy() f.write(",".join(map(str, flattened_ofmap)))

#print("===== start ifmap =====\n")
#print(ifmap)
#print("===== end of ifmap =====\n")

#print("===== start filter =====\n")
#print(filter)
#print("===== end of filter =====\n")

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               ifmap_conv = torch.permute(ifmap, (0, 2, 1)) ifmap_conv = ifmap_conv - 128 filte_conv = torch.permute(filter, (0, 3, 1, 2)) filte_conv = torch.unbind(filte_conv, dim = 2)[0] ofmap = F.conv1d(ifmap_conv, filte_conv) ofmap = torch.permute(ofmap, (0, 2, 1))

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       add(ofmap, ipsum) ofmap = ofmap.int() print("===== start ofmap =====\n") print(ofmap) print("===== end ofmap =====\n")

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      print_txt(ifmap, filter, ofmap)
