import math

'''
tree 1 (rooted)
path: "/groups/itay_mayrose/nomihadar/tests/treedist/rooted_vs_unrooted/5 species/true.tree"
((161100:0.00956962,4472:0.0109621)1:0.00420709,(161105:0.00616437,(161099:0.010252,161106:0.0064157)1:0.0143586)1:0.00315984);

      /-161100
   /-|
  |   \-4472
--|
  |   /-161105
   \-|
     |   /-161099
      \-|
         \-161106


tree 2 (rooted)
path: "/groups/itay_mayrose/nomihadar/tests/treedist/rooted_vs_unrooted/5 species/sim_root_by_1.tree"
((161099:0.0115345,161106:0.00765233):0.0061141,((4472:0.00980478,161100:0.00874079):0.00519018,161105:0.00782854):0.0061141);

      /-161099
   /-|
  |   \-161106
--|
  |      /-4472
  |   /-|
   \-|   \-161100
     |
      \-161105


'''

dists = []

def d(a,b):
	dists.append((a-b)**2)

'''
splits for rooted trees (rooted by 1):

common splits:
A|BCDE
B|ACDE
C|ABDE
D|ABCE
E|ABCD
AB|CDE
DE|ABC

true tree:
CDE|AB

simulated:
ABC|DE
'''

#common splits:
d(0.00956962,0.00874079)
d(0.0109621,0.00980478)
d(0.00616437,0.00782854)
d(0.010252,0.0115345)
d(0.0064157,0.00765233)
d(0.00420709,0.00519018)
d(0.0143586,0.0061141)

#non common splits:
d(0.00315984,0)
d(0,0.0061141)

print "rooted:"
print "ditsance:{} \n".format(math.sqrt(sum(dists))) #0.01114786636 - correct
dists = []


'''
tree 1:
path "/groups/itay_mayrose/nomihadar/tests/treedist/rooted_vs_unrooted/5 species/true_unrooted_ete3.tree"
((161105:0.00616437,(161099:0.010252,161106:0.0064157)1:0.0143586)1:0.00315984,161100:0.00956962,4472:0.0109621);


      /-161105
   /-|
  |  |   /-161099
  |   \-|
--|      \-161106
  |
  |--161100
  |
   \-4472


tree 2:
path "/groups/itay_mayrose/nomihadar/tests/treedist/rooted_vs_unrooted/5 species/sim.tree"
((161099:0.0115345,161106:0.00765233):0.0122282,(4472:0.00980478,161100:0.00874079):0.00519018,161105:0.00782854);

      /-161099
   /-|
  |   \-161106
  |
--|   /-4472
  |--|
  |   \-161100
  |
   \-161105

'''

'''
splits for unrooted trees:

common splits:
A|BCDE
B|ACDE
C|ABDE
D|ABCE
E|ABCD
AB|CDE
DE|ABC

'''

#common splits:
d(0.00956962,0.00874079)
d(0.0109621,0.00980478)
d(0.00616437,0.00782854)
d(0.010252,0.0115345)
d(0.0064157,0.00765233)
d(0.00420709 + 0.00315984,0.00519018)
d(0.0143586,0.0061141 + 0.0061141)

#d(0.00315984,0.00519018)
#d(0.0143586,0.0122282)

	
print "unrooted:"
print "ditsance:{} \n".format(math.sqrt(sum(dists))) #0.00415291647756 - correct
print "\n".join(map(str,dists))



#for d in dists:
#	print '{:.6f}'.format(d)
