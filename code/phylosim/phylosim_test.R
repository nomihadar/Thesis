library("phylosim")
library("poweRlaw")
library("VGAM")
#indel parameters

ALPHA = 1.05
IR = 0.0002
TREE_PATH = "/groups/itay_mayrose/nomihadar/simulations/dataset_small/ref_tree/ExaML_result.ref_tree.tree"
# GTR: a={CT} b={AT} c={GT} d={AC} e={CG} (f={AG})
# frequencies [T, C, A, G] 

# Tree-Length: 22.097424
# rate A <-> C: 1.102806  rate d
# rate A <-> G: 1.974188  rate f
# rate A <-> T: 2.196005  rate b
# rate C <-> G: 0.421446  rate e
# rate C <-> T: 7.683843  rate a
# rate G <-> T: 1.000000  rate c
# 
# freq pi(A): 0.248430
# freq pi(C): 0.222536
# freq pi(G): 0.275285
# freq pi(T): 0.253749


    
rates = list(a = {CT}, b = {AT}, c = {GT}, 
             d = {AC}, e = {CG}, f = 1)
bases = c({fT}, {fC}, {fA}, {fG})
sub_process = GTR(rate.params = rates, base.freqs = bases)

tolerance_probs_table = read.table("gap_percent_output.txt")
tolerance_probs = tolerance_probs_table[[1]]
rl = length(tolerance_probs)

root_seq = NucleotideSequence(length={root_length})
length_dis = expression(rplcon(1, 1,{A})) 

del_process = ContinuousDeletor(rate={IR},dist=length_dis, 
								max.length={max_gaps_length})

insert_process = ContinuousInsertor(rate={IR}, dist=length_dis,
									max.length={max_gaps_length})

attachProcess(root_seq,sub_process)
attachProcess(root_seq,del_process)
attachProcess(root_seq,insert_process)

plusInvGamma(root_seq, sub_process, pinv = 0, shape = 0.1, ncat = 16)

setDeletionTolerance(root_seq, del_process, tolerance_probs, 1:root_seq$length)

template = NucleotideSequence(length=10)
attachProcess(template,sub_process)
insert_process$writeProtected = FALSE
insert_process$templateSeq = template

sampleStates(root_seq)
sim = PhyloSim(root.seq = root_seq, phylo = read.tree({tree_path}));
Simulate(sim)
saveAlignment(sim,file="18S_sim.fas", skip.internal = TRUE)


