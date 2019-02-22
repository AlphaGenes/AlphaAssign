
print2 = function(string){
    cat(string)
    cat("\n")
}

pedigree = read.table("baseData/pedigree.txt")
assessAssign = function(filePrefix){
    lastGen = 801:1000

    newFile = as.matrix(read.table(paste0("outputs/", filePrefix)))
    oldFile = NULL
    tryCatch({
        oldFile = as.matrix(read.table(paste0("lastStable/", filePrefix)))
        }, error = function(err){}, warning=function(err){})
    if(is.null(oldFile)) {
        print("NO OLD FILE")
        oldFile = newFile
    }


    print2(" ")
    print2(paste("Assessing Assign file:", filePrefix))
    print2(paste("Checking if outputs are equal:", all(newFile == oldFile)))

    newAcc = mean(newFile[lastGen,2] == pedigree[lastGen,2])
    oldAcc = mean(oldFile[lastGen,2] == pedigree[lastGen,2])
    print2(paste("Comparing accuracies: ", round(oldAcc, digits=3), "->", round(newAcc, digits=3)))

}
assessAssign("assign.pedigree")
assessAssign("assign.noDam.pedigree")
assessAssign("assign.seq.pedigree")


pedigreeExtended = read.table("baseData/pedigree.extended")
assessMGS = function(filePrefix){
    lastGen = 801:1000

    newFile = as.matrix(read.table(paste0("outputs/", filePrefix)))
    oldFile = NULL
    tryCatch({
        oldFile = as.matrix(read.table(paste0("lastStable/", filePrefix)))
        }, error = function(err){}, warning=function(err){})
    if(is.null(oldFile)) {
        print("NO OLD FILE")
        oldFile = newFile
    }

    print2(" ")
    print2(paste("Assessing MGS file:", filePrefix))
    print2(paste("Checking if outputs are equal:", all(newFile == oldFile)))

    newAcc = mean(newFile[,2] == pedigreeExtended[lastGen,4])
    oldAcc = mean(oldFile[,2] == pedigreeExtended[lastGen,4])
    print2(paste("Comparing accuracies: ", round(oldAcc, digits=3), "->", round(newAcc, digits=3)))

}
assessMGS("mgsAssign.grandsires")




