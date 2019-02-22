
from tinyhouse import Pedigree
from tinyhouse import InputOutput 
from Assign import assignEvaluate


def main() :
    #Read in data
    print("Read in data")
    pedigree = Pedigree.Pedigree() 
    args = InputOutput.parseArgs("AlphaAssign")
    InputOutput.readInPedigreeFromInputs(pedigree, args)
    print("Data read in")

    assignments = []
    sireAssignements = []
    damAssignments = []

    # if args.checkpedigree :
    #     for ind in ped.individuals.values():
    #         father = ind.sire
    #         mother = ind.dam
    #         if father is not None: sireAssignements.append(assignEvaluate.AssignmentHolder(ind, None, [father], findSire=True))
    #         if mother is not None: damAssignments.append(assignEvaluate.AssignmentHolder(ind, None, [mother], findSire=False))

    if args.potentialsires is not None:
        sireAssignements = assignEvaluate.readInAssignments(args.potentialsires, findSire = True, pedigree=pedigree)
        assignments.extend(sireAssignements)

    if args.potentialdams is not None:
        damAssignments = assignEvaluate.readInAssignments(args.potentialdams, findSire = False, pedigree=pedigree)
        assignments.extend(damAssignments)


    assignInfo = assignEvaluate.createAssignInfo(pedigree, args) 

    for assignment in assignments:
        assignEvaluate.performAssignement(assignInfo, assignment, args)


    for assignment in assignments:
        assignment.chooseSire(args.add_threshold, args.p_threshold, runtype=args.runtype)
        assignment.updatePedigree(pedigree, useTop=False)
    pedigree.writePedigree(args.out + ".pedigree")

    for assignment in assignments:
        assignment.updatePedigree(pedigree, useTop=True)
    pedigree.writePedigree(args.out + ".pedigree.top")


    if len(sireAssignements) > 0:
        with open(args.out + ".sires", 'w+') as f:
            line = "" 
            prob = ""
            opp = ""
            header = "id candidate altParent chosen"
            if args.runtype in ["likelihood", "both"]: prob = " score estSire estFullSib esthalfSib estNull"
            if args.runtype in ["opp", "both"]: opp = " nOpposing nOpposingWOparent nLoci logP"
            line += header + prob + opp + "\n"

            f.write(line)
            for assignment in sireAssignements:
                f.write(assignment.writeLine(args))
                
    if len(damAssignments) > 0:
        with open(args.out + ".dams", 'w+') as f:
            line = "" 
            prob = ""
            opp = ""
            header = "id candidate altParent chosen"
            if args.runtype in ["likelihood", "both"]: prob = " score estSire estFullSib esthalfSib estNull"
            if args.runtype in ["opp", "both"]: opp = " nOpposing nOpposingWOparent nLoci logP"
            line += header + prob + opp + "\n"

            f.write(line)
            for assignment in damAssignments:
                f.write(assignment.writeLine(args))


if __name__ == "__main__":
    main()