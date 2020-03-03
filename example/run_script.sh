mkdir outputs
# AlphaAssign is a command line python module for performing parentage assignement.
# Install AlphaAssign via pip using:
# pip install <wheel name>

#To check command line arguments run AlphaAssign without any arguments.
AlphaAssign

# Example 1: Perform parentage assignment with genotype data:

AlphaAssign -genotypes data/trueGenotypes.txt -potentialsires data/sire.list -out outputs/out_genotypes

# Example 1b: Perform parentage assignement with genotype data using number of opposing homozygous markers only.
AlphaAssign -genotypes data/trueGenotypes.txt -potentialsires data/sire.list -out outputs/out_genotypes -runtype opp -p_threshold 0.00001

# Example 2: Perform parentage assignment with sequence data:
AlphaAssign -seqfile data/sequence.2 -potentialsires data/sire.list -out outputs/out_sequence

