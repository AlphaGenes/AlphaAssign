# pyinstaller tinyMgsAssign.py --onefile -p src/

from numba import jit, float32, int32, int64, optional
try:
    from numba.experimental import jitclass
except ModuleNotFoundError:
    from numba import jitclass
import numpy as np
from collections import OrderedDict
from ..tinyhouse import ProbMath

def evaluateMGS(scoreCont, assignInfo) :
    scoreCont.scores = []

    ind = scoreCont.ind
    indGenotypes = assignInfo.penetrance[ind.idn,:,:]
    # print(ind.sire)
    if ind.sire is not None:
        sireGenotypes = assignInfo.penetrance[ind.sire.idn,:,:]
    else:
        sireGenotypes = assignInfo.mafGenotypes

    if ind.dam is not None:
        damGenotypes = assignInfo.penetrance[ind.dam.idn,:,:]
    else:
        damGenotypes = assignInfo.mafGenotypes

    # damGenotypes = assignInfo.penetrance[ind.dam.idn,:,:]

    grandSireGenotypes = peelToGrandSire(indGenotypes, sireGenotypes, damGenotypes, assignInfo.mafGenotypes)

    # print(np.transpose(indGenotypes[:,0:10]))
    # print(np.transpose(sireGenotypes[:,0:10]))
    # print(np.transpose(grandSireGenotypes[:,0:10]))

    # sysfsadfa
    for putative in scoreCont.possibilities:
        putativeGenotypes = assignInfo.penetrance[putative.idn,:,:]
        score = np.sum(np.log(np.sum(putativeGenotypes*grandSireGenotypes, 0)))
        scoreCont.scores.append(score)

    topIndex = np.argmax(scoreCont.scores)

    scoreCont.top = scoreCont.possibilities[topIndex]
    scoreCont.topScore = scoreCont.scores[topIndex]

def peelToGrandSire(indGenotypes, sireGenotypes, initialDamGenotypes, maf) :

    segTensor = ProbMath.generateSegregation(partial=True)
    damGenotypes = initialDamGenotypes*np.einsum("ai, ci, abc -> bi", sireGenotypes, indGenotypes, segTensor)
    damGenotypes = damGenotypes/np.sum(damGenotypes, 0)

    grandSireGenotypes = np.einsum("ci, bi, abc -> ai", damGenotypes, maf, segTensor)
    grandSireGenotypes = grandSireGenotypes/np.sum(grandSireGenotypes, 0)
    
    return grandSireGenotypes

def readAssignments(fileName, pedigree):
    assignments = []
    with open(fileName) as f:
        lines = f.readlines()
    for line in lines:
        parts = line.strip().split(" ")
        idx = parts[0]
        potentialSires = parts[1:]
        sires = [pedigree.individuals[idx] for idx in potentialSires]

        assignments.append(ScoreContainer(pedigree.individuals[idx], sires))
    return assignments

class ScoreContainer(object):
    def __init__(self, ind, sires) :
        self.ind = ind
        self.possibilities = sires
        # Probability Values
        self.scores = None
        self.top = None
        self.topScore = None
    def writeLine(self):

        line = str(self.ind.idx) + " " + str(self.top.idx) + " " + str(self.topScore)
        line += " " + " ".join(map(lambda ind: str(ind.idx), self.possibilities))
        line += " " + " ".join(map(str, self.scores))
        return line

def createAssignInfo(pedigree, args) :
    nLoci = pedigree.nLoci

    if pedigree.maf is None or (not args.usemaf):
        maf = np.full((nLoci), .25, dtype = np.float32)
    else:
        maf = pedigree.maf
    assignInfo = jit_assignInformation(nInd=pedigree.maxIdn, nLoci=nLoci, maf=maf)

    for ind in pedigree:
        if ind.genotypes is None: genotypes = None
        else: genotypes = ind.genotypes

        if ind.reads is None: reads = None
        else: reads = ind.reads
        
        assignInfo.penetrance[ind.idn,:,:] = ProbMath.getGenotypeProbabilities(assignInfo.nLoci, genotypes, reads, args.error, args.seqerror)

    return assignInfo


# spec = OrderedDict()
# spec['nInd'] = int64
# spec['nLoci'] = int64
# spec['penetrance'] = float32[:,:,:]
# spec['mafGenotypes'] = float32[:,:]

# @jitclass(spec)
class jit_assignInformation(object):
    def __init__(self, nInd, nLoci, maf):
        self.nInd = nInd
        self.nLoci = nLoci
        self.penetrance = np.full((nInd, 4, nLoci), .25, dtype=np.float32)

        self.mafGenotypes = np.full((4, nLoci), .25, dtype = np.float32)
        self.mafGenotypes[0,:] = maf**2
        self.mafGenotypes[1,:] = maf*(1-maf)
        self.mafGenotypes[2,:] = (1-maf)*maf
        self.mafGenotypes[3,:] = (1-maf)**2
