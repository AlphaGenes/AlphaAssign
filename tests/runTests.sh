
AlphaAssign -genotypes baseData/trueGenotypes.txt \
                        -pedigree baseData/pedigree.txt \
                        -out outputs/assign \
                        -potentialsires baseData/sire.list

AlphaAssign -genotypes baseData/trueGenotypes.txt \
                        -pedigree baseData/pedigree.noDam \
                        -out outputs/assign.noDam \
                        -potentialsires baseData/sire.list

AlphaAssign -seqfile baseData/sequence.2 \
                        -pedigree baseData/pedigree.txt \
                        -out outputs/assign.seq \
                        -potentialsires baseData/sire.list

AlphaAssign -genotypes baseData/trueGenotypes.txt \
                        -pedigree baseData/pedigree.txt \
                        -out outputs/assign.check \
                        -checkpedigree

AlphaAssign -genotypes baseData/trueGenotypes.txt \
                        -pedigree baseData/pedigree.txt \
                        -out outputs/assign.check.opp \
                        -checkpedigree \
                        -runtype opp 



#AlphaMGSAssign

AlphaMGSAssign -genotypes baseData/trueGenotypes.txt \
                        -pedigree baseData/pedigree.noDam \
                        -out outputs/mgsAssign \
                        -potentialgrandsires baseData/grandsire.list


Rscript checkResults.r