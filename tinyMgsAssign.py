from tinyhouse import Pedigree
from tinyhouse import InputOutput 
from Assign import assignEvaluate
from Assign import mgsAssign


# python tinyimpute/tinyMgsAssign.py -out test -genotypes tmpData/genotypes.250 -potentialgrandsires tmpData/grandSires.txt

def main():
    #Read in data
    print("Read in data")
    pedigree = Pedigree.Pedigree() 
    args = InputOutput.parseArgs("AlphaMGS")
    InputOutput.readInPedigreeFromInputs(pedigree, args)
    print("Data read in")

    pedigree.setMaf()

    assignments = mgsAssign.readAssignments(args.potentialgrandsires, pedigree)

    assignInfo = mgsAssign.createAssignInfo(pedigree, args)
    # assignInfo = None

    for assignment in assignments:
        # mgsAssign.evaluateMGSTrio(assignment, assignInfo)
        mgsAssign.evaluateMGS(assignment, assignInfo)


    with open(args.out + ".grandsires", 'w+') as f:
        for assignment in assignments:
            f.write(assignment.writeLine())
            f.write('\n')

if __name__ == "__main__":
    main()