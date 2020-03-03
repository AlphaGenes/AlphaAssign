
from .tinyhouse import Pedigree
from .tinyhouse import InputOutput 
from .Assign import assignEvaluate
import argparse

def getArgs() :

    parser = argparse.ArgumentParser(description='')
    core_parser = parser.add_argument_group("Core arguments")
    core_parser.add_argument('-out', required=True, type=str, help='The output file prefix.')
   
    # Input options
    input_parser = parser.add_argument_group("Input Options")
    InputOutput.add_arguments_from_dictionary(input_parser, InputOutput.get_input_options(), options = ["bfile", "genotypes", "seqfile", "pedigree"]) 

    # Core assignment options
    core_assign_parser = parser.add_argument_group("Core assignement arguments")
    core_assign_parser.add_argument('-potentialsires', default=None, required=False, type=str, help='A list of potential sires for each individual.')
    core_assign_parser.add_argument('-potentialdams', default=None, required=False, type=str, help='A list of potential dams for each individual.')

    # Selection_parser
    selection_parser = parser.add_argument_group("Arguments to choose how sires and dams are assigned")
    selection_parser.add_argument('-runtype',default="both", required=False, type=str, help='opp, likelihood, both, Default: both')
    selection_parser.add_argument('-add_threshold',default=9, required=False, type=float, help='Assignement score threshold for adding a new individual as a parent')
    selection_parser.add_argument('-p_threshold',default=-9, required=False, type=float, help='Negative log-pvalue threshold for removing parents via opposing homozygotes')

    # Multithreading
    multithread_parser = parser.add_argument_group("Multithreading Options")
    InputOutput.add_arguments_from_dictionary(multithread_parser, InputOutput.get_multithread_options(), options = ["iothreads"]) 

    # General Arguments
    assign_parser = parser.add_argument_group("Probability Arguments")
    InputOutput.add_arguments_from_dictionary(assign_parser, InputOutput.get_probability_options(), options = ["error", "seqerror"]) 
    assign_parser.add_argument('-usemaf', action='store_true', required=False, help='A flag to use the minor allele frequency when constructing genotype estimates for the sire and maternal grandsire. Not recomended for small input pedigrees.')

    return InputOutput.parseArgs("AlphaAssign", parser)

def main() :
    #Read in data
    print("Read in data")
    pedigree = Pedigree.Pedigree() 
    args = getArgs()
    InputOutput.readInPedigreeFromInputs(pedigree, args)
    print("Data read in")

    assignments = []
    sireAssignements = []
    damAssignments = []

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