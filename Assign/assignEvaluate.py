import numpy as np
from scipy.stats import binom
from numba import jit
from tinyhouse import ProbMath

def performAssignement(assignInfo, assignment, args = None):

    if args.runtype in ["opp", "both"] :
        createOppHomozygoteAssignment(assignInfo, assignment, args)
    if args.runtype in ["likelihood", "both"] :
        createProbAssignment(assignInfo, assignment, args)

def createOppHomozygoteAssignment(assignInfo, assignment, args):
    child = assignment.ind
    altParent = assignment.alternativeParent
    potentialParents = assignment.potentialParents

    childGeno = child.genotypes
    if childGeno is None: childGeno = callGenotypes(assignInfo.getGenotypes(child))

    if altParent is not None: 
        if altParent.genotypes is not None: altGeno = altParent.genotypes
        else: altGeno = callGenotypes(assignInfo.getGenotypes(altParent))
    else: altGeno = None

    for cont in potentialParents.values():

        parentGeno = cont.ind.genotypes
        if parentGeno is None: parentGeno = callGenotypes(assignInfo.getGenotypes(cont.ind))

        if altGeno is None:
            cont.opp, cont.numLoci = evaluateDifferenceNoAlt(childGeno, parentGeno)
            cont.oppWithoutOtherParent = cont.opp
        else:
            cont.opp, cont.numLoci = evaluateDifferenceAlt(childGeno, parentGeno, altGeno)
            cont.oppWithoutOtherParent = evaluateDifferenceNoAlt(childGeno, parentGeno)[0]
        if cont.numLoci > 0:
            cont.pValue = binom.logsf(cont.opp, cont.numLoci, args.error)
        else: 
            cont.pValue = 1 

def callGenotypes(genoProbs) :
    combined = np.array([genoProbs[0,:], genoProbs[1,:] + genoProbs[2,:], genoProbs[3,:]])
    maxVals = combined.max(axis = 0)
    genotypes = np.argmax(combined, 0)
    genotypes[maxVals < .9] = 9
    return genotypes

def createProbAssignment(assignInfo, assignment, args = None):
    child = assignment.ind
    alternativeParent = assignment.alternativeParent
    potentialParents = assignment.potentialParents


    baseEstimates = generateNullDistributions(child, alternativeParent, assignInfo, args)
    
    for parentId, cont in potentialParents.items():
        parentGenotype = assignInfo.getGenotypes(cont.ind)
        cont.score, cont.probabilitySummaries = evaluateParent(parentGenotype, baseEstimates)

        score = cont.probabilitySummaries[0] - cont.probabilitySummaries[1]
        # print(" ")        
        # sireDist = [evaluateSimulatedParent(cont.ind, baseEstimates[0], baseEstimates) for i in range(10)]
        # fullDist = [evaluateSimulatedParent(cont.ind, baseEstimates[1], baseEstimates) for i in range(10)]
        # cont.score = 0
        # if all(score > fullDist) and any(score > sireDist): cont.score = 100

    return(potentialParents)

def evaluateSimulatedParent(realParent, targetProbabilities, nullDistributions) :

    gError = 0.01
    seqerror = 0.001
    nLoci = targetProbabilities.shape[1]

    reducedProbs = np.array([targetProbabilities[0,:],
                                targetProbabilities[1,:] + targetProbabilities[2,:],
                                    targetProbabilities[3,:] ], dtype=np.float32)
    cumProbs = np.cumsum(reducedProbs, axis = 0)
    random = np.random.rand(nLoci)

    cumProbs = cumProbs - random[None,:]
    trueGenotypes = np.argmax(cumProbs > 0, axis = 0)
    #Bad code
    if realParent.genotypes is None:
        genotypes = None
    else:
        genotypes = trueGenotypes.copy()
        genotypes[realParent.genotypes == 9] = 9 

    if realParent.reads is None:
        reads = None
    else:
        readCounts = realParent.reads[0] + realParent.reads[1]
        refCounts = np.random.binomial(readCounts, p = .5)
        altCounts = readCounts - refCounts
        reads = getReads(refCounts, altCounts, trueGenotypes)

    simulatedGenotype = ProbMath.getGenotypeProbabilities(nLoci, genotypes, reads, gError, seqerror)
    score, probabilitySummaries = evaluateParent(simulatedGenotype, nullDistributions)
    
    return probabilitySummaries[0] - probabilitySummaries[1]

@jit(nopython=True)
def getReads(refCounts, altCounts, genotypes) :
    nLoci = len(genotypes)
    read0 = np.full(nLoci, 0, dtype = np.int16)
    read1 = np.full(nLoci, 0, dtype = np.int16)

    for i in range(nLoci) :
        if genotypes[i] == 0:
            read0[i] = refCounts[i] + altCounts[i]
        if genotypes[i] == 1:
            read0[i] = refCounts[i]
            read1[i] = altCounts[i]
        if genotypes[i] == 2:
            read1[i] = refCounts[i] + altCounts[i]
    return (read0, read1)

def generateNullDistributions(child, alternativeParent, assignInfo, args):
    nullGenotypes = assignInfo.getMaf()

    segregation = ProbMath.generateSegregation(partial=True)

    childGeno = assignInfo.getGenotypes(child)
    altGeno = assignInfo.getGenotypes(alternativeParent)

    parentGenotypes = np.einsum("bi, ci, abc -> ai", altGeno, childGeno, segregation)  
    
    grandParentGenotypes = np.einsum("ci, abc -> abi", parentGenotypes, segregation)  
    
    if args.usemaf: grandParentGenotypes = np.einsum("abi, ai, bi -> abi", grandParentGenotypes, nullGenotypes, nullGenotypes)  

    grandSireGenotypes = np.einsum("abi, bi -> ai", grandParentGenotypes, nullGenotypes)

    fullSibGenotypes = np.einsum("abi, abc -> ci", grandParentGenotypes, segregation)  
    halfSibGenotypes = np.einsum("ai, bi, abc -> ci", grandSireGenotypes, nullGenotypes, segregation)  

    if args.usemaf: parentGenotypes = parentGenotypes*nullGenotypes

    parentGenotypes = parentGenotypes/np.sum(parentGenotypes, 0)
    fullSibGenotypes = fullSibGenotypes/np.sum(fullSibGenotypes, 0)
    halfSibGenotypes = halfSibGenotypes/np.sum(halfSibGenotypes, 0)

    # print(parentGenotypes)
    # print(fullSibGenotypes)
    # print(halfSibGenotypes)
    
    # import sys
    # sys.exit()
    return((parentGenotypes, fullSibGenotypes, halfSibGenotypes, nullGenotypes))


# def createProbAssignment_OLD(ped, child, potentialParents, alternativeParent=None, args = None):
#     nRegions = 1000
#     regions = getRegions(nRegions, ped.nLoci)
#     baseEstimates = generateNullDistributions(child, alternativeParent, ped)
    
#     childGenotypes = getGenotypeProbabilities(child, ped)
#     alternativeGenotypes = getGenotypeProbabilities(alternativeParent, ped, useMafWhenNull = True)

#     for parentId, cont in potentialParents.items():
#         parentGenotype = getGenotypeProbabilities(cont.ind, ped)
#         subLoci = None
#         if nRegions > ped.nLoci:
#             subLoci = None
#         elif args.subsample == "coverage":
#             subLoci = subsample(childGenotypes, parentGenotype, alternativeGenotypes, ped.maf, regions)
#         elif args.subsample == "midpoint":
#             subLoci = [ int((region[0] + region[1])/2) for region in regions]
#         cont.score, cont.probabilitySummaries, tmp = evaluateParent(parentGenotype, baseEstimates, subLoci)
#     return(potentialParents)

# def getRegions(nRegions, nLoci) :
#     regions = []
#     regionSize = nLoci/(nRegions -1)

#     for i in range(nRegions) :
#         start = i*regionSize
#         stop = min( (i+1)*regionSize, nLoci-1)
#         regions.append( (int(start), int(stop)))

#     return regions

def evaluateParent(indGenotypes, targets) :
    scores = []
    for targetGenotypes in targets  :
        combined = np.sum(indGenotypes*targetGenotypes, 0)
        # combined = np.einsum("ai, ai -> i", indGenotypes, targetGenotypes)
        # combinedSquared = np.einsum("ai, ai -> i", indGenotypes, targetGenotypes**2)
        score = np.sum(np.log(combined))
        scores.append(score)

    score, scoresArray = collapseScores(scores)
    return (score, scoresArray)

def collapseScores(scoresList) :
    scores = np.array(scoresList)
    scores -= np.max(scores)

    diff = logSum(scores) - logSum(scores[1:])

    return(diff, scores)

def logSum(llArray) :
    maxVal = np.max(llArray)
    llArray = llArray.copy() - maxVal

    retVal = maxVal + np.sum(np.exp(llArray))
    return retVal


@jit(nopython=True)
def evaluateDifferenceNoAlt(childGeno, parentGeno) :
    nLoci = 0
    nOpp = 0
    for i in range(len(childGeno)):
        if childGeno[i] != 9 and parentGeno[i] != 9:
            nLoci += 1
            if (childGeno[i] == 0 and parentGeno[i] == 2) or (childGeno[i] == 2 and parentGeno[i] == 0):
                nOpp += 1
    return (nOpp, nLoci)

@jit(nopython=True)
def evaluateDifferenceAlt(childGeno, parentGeno, altGeno) :
    nLoci = 0
    nOpp = 0
    for i in range(len(childGeno)):
        if childGeno[i] != 9 and parentGeno[i] != 9:
            nLoci += 1
            c = childGeno[i]
            if c == 1 and altGeno[i] == 0:
                c = 2
            if c == 1 and altGeno[i] == 2:
                c = 0
            if (c == 0 and parentGeno[i] == 2) or (c == 2 and parentGeno[i] == 0):
                nOpp += 1

    return (nOpp, nLoci)


def readInAssignments(fileName, findSire, pedigree) :
    assignments = []
    with open(fileName) as f:
        lines = f.readlines()
    for line in lines:
        parts = line.strip().split(" ")
        idx = parts[0]
        potentialSires = parts[1:]
        sires = [pedigree.individuals[idx] for idx in potentialSires]
        
        if findSire: altParent = pedigree.individuals[idx].dam
        else: altParent = pedigree.individuals[idx].sire

        assignments.append(AssignmentHolder(pedigree.individuals[idx], altParent, sires, findSire))
    return assignments


class ScoreContainer(object) :

    def __init__(self, ind) :
        self.ind = ind

        # Probability Values
        self.score = None
        self.probabilitySummaries = None

        #Opposing Homozygote Values
        self.numLoci = None
        self.opp = None
        self.oppWithoutOtherParent  = None
        self.pValue = None

        self.chosen=False


class AssignmentHolder(object):
    def __init__(self, ind, altParent, potentialSires, findSire = True):
        self.ind = ind

        self.findSire = findSire

        self.potentialParents = {ind.idx:ScoreContainer(ind) for ind in potentialSires}
        
        self.chosen = None
        self.top = None
        self.alternativeParent = altParent

    def chooseSire(self, threshold, p_threshold, runtype):

        if runtype == "opp" :
            scores = np.array([container.pValue for container in self.potentialParents.values()])
            containers = np.array([container for container in self.potentialParents.values()])

            bestInd = containers[np.argmax(scores)]
            self.top = bestInd.ind
            if bestInd.pValue > p_threshold :
                self.chosen = bestInd.ind

        if runtype in ["likelihood", "both"]:
            if runtype == "likelihood":
                containers = np.array([container for container in self.potentialParents.values()])
            if runtype == "both":
                containers = np.array([container for container in self.potentialParents.values() if container.pValue > p_threshold])

            scores = np.array([container.score for container in containers ])
            bestInd = containers[np.argmax(scores)]
            self.top = bestInd.ind

            if bestInd.score > threshold :
                self.chosen = bestInd.ind

    def writeLine(self, args) :

        chosen = self.chosen
        line = "" 
        for pidx, item in self.potentialParents.items() :
            wasChosen = 0
            if self.chosen is not None: wasChosen = int(item.ind.idx == chosen.idx)
            if self.alternativeParent is None: alt = "0"
            else: alt = self.alternativeParent.idx
            header = f"{self.ind.idx} {item.ind.idx} {alt} {wasChosen} "
            
            prob = ""
            if args.runtype in ["likelihood", "both"]:
                score = item.score
                summary = " ".join(str(e) for e in item.probabilitySummaries)
                prob = f"{score} {summary} "
            
            opp = ""
            if args.runtype in ["opp", "both"]:
                opp = " ".join([str(item.opp), str(item.oppWithoutOtherParent), str(item.numLoci), str(item.pValue)])

            line += header + prob + opp + "\n"
        return line


    def updatePedigree(self, pedigree, useTop = False):
        if self.findSire: parent = self.ind.sire
        else: parent = self.ind.dam

        if useTop:
            newSire = self.top

        else:
            newSire  = self.chosen
        if newSire is not None:
            if self.findSire: self.ind.sire = newSire
            if not self.findSire: self.ind.dam = newSire
        else:
            if self.findSire: self.ind.sire = None
            if not self.findSire: self.ind.dam = None

def createAssignInfo(pedigree, args) :
    nLoci = pedigree.nLoci
    
    assignInfo = assignInformation(nInd=pedigree.maxIdn, nLoci=nLoci)
    
    for ind in pedigree:        

        geno = ind.genotypes
        reads = ind.reads
        if reads is not None:
            geno = None
        assignInfo.penetrance[ind.idn,:,:] = ProbMath.getGenotypeProbabilities(assignInfo.nLoci, geno, reads, args.error, args.seqerror)
    assignInfo.pentranceSetup = True
    
    #I think we bypass pedigree maf, just because we want to use the sequence data too.

    if args.usemaf:
        maf = np.full(nLoci, 0, dtype = np.float32)
        for ind in pedigree:
            maf += assignInfo.getDosages(ind)
        maf = maf/(2*assignInfo.nInd)
        assignInfo.setMaf(maf)
        np.savetxt("maf.txt", maf)
    return assignInfo

class assignInformation(object):
    def __init__(self, nInd, nLoci):
        self.nInd = nInd
        self.nLoci = nLoci

        self.pentranceSetup = False
        self.penetrance = np.full((nInd, 4, nLoci), .25, dtype=np.float32)
        self.mafGenotypes = np.full((4, nLoci), .25, dtype = np.float32)

    def getMaf(self):
        return self.mafGenotypes

    def setMaf(self, maf) :
        self.mafGenotypes[0,:] = maf**2
        self.mafGenotypes[1,:] = maf*(1-maf)
        self.mafGenotypes[2,:] = (1-maf)*maf
        self.mafGenotypes[3,:] = (1-maf)**2

    def getGenotypes(self, ind) :
        if ind is None: return self.mafGenotypes
        if self.pentranceSetup :
            return self.penetrance[ind.idn,:,:]
        else:
            return ProbMath.getGenotypeProbabilities(assignInfo.nLoci, ind.genotypes, ind.reads, args.error, args.seqerror)

    def getDosages(self, ind):
        genoProbs = self.getGenotypes(ind)
        return np.dot(np.array([0,1,1,2]), genoProbs)


