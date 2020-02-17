.. AlphaAssign documentation master file, created by
   sphinx-quickstart on Mon Feb 17 10:12:39 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to AlphaAssign's documentation!
=======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Introduction
~~~~~~~~~~~~


|aa| is a parentage assignment algorithm. This program uses a likelihood based model to determine the sire of an individual based on a list of potential sires. AlphaAssign differs from other parentage assignment algorithms by having the option to use phase information to determine parentage. For more information on the algorithm see *Parentage assignment with low density array data and low coverage sequence data* `(Journal of Animal Breeding and Genetics) <https://onlinelibrary.wiley.com/doi/10.1111/jbg.12370>`_.

Due to the disproportionate impact of map errors with the usage of phased data, we currently do not recommend using phase information to assign parentage. However, substantial advantages can be gained by using a allele probabilities generated via an imputation algorithm (e.g. AlphaImpute or AlphaPeel) to correct for genotyping errors.

Please report bugs or suggestions on how the program / user interface / manual could be improved or made more user friendly to `John.Hickey@roslin.ed.ac.uk <John.Hickey@roslin.ed.ac.uk>`_ or `Awhalen@roslin.ed.ac.uk <awhalen@roslin.ed.ac.uk>`_.

Conditions of use
-----------------
|aa| is part of a suite of software that our group has developed. It is fully and freely available for academic use, provided that users cite it in publications. However, due to our contractual obligations with some of the funders of the research program that has developed this suite of software, all interested commercial organizations are requested to contact John Hickey (`John.Hickey@roslin.ed.ac.uk <John.Hickey@roslin.ed.ac.uk>`_) to discuss the terms of use.

Citation and Authorship
-----------------------

AlphaAssign is part of a suite of software that the AlphaGenes group has developed for imputation. It is fully and freely available to all academics. User are requested to credit its use on any publications. Due to our contractual obligations with some of funders of the research program that has developed this suite of software, all commercial organisations that wish to use it are requested to contact John Hickey` (`John.Hickey@roslin.ed.ac.uk <John.Hickey@roslin.ed.ac.uk>`_) :red:`to discuss the terms under which it can be used.

Citation:
Whalen, A., Gorjanc, G., and Hickey, J. (2018). Parentage assignment with low density array data and low coverage sequence data. Journal of Animal Breeding and Genetics.

Disclaimer
----------

While every effort has been made to ensure that |aa| does what it claims to do, there is absolutely no guarantee that the results provided are correct. Use of |aa| is at your own risk.


Run commands and spec file
~~~~~~~~~~~~~~~~~~~~~~~~~~

|aa| is a parentage assignment algorithm. To run |aa| call ``python AlphaAssign.py [options]``. All options are of the form "option=parameter". The following options are valid for |aa|:

.. csv-table:: Key run paramaters
  :header: "option", "description"
  :widths: 20, 50
   
  "potentialSires",  "A list of individuals and potential sires."
  "potentialDams",  "A list of individuals and potential dams."
  "out",             "[Required] Output file prefix."

.. csv-table:: Data import options
  :header: "option", "description"
  :widths: 20, 50

  "bfile",           "The genotype file in Plink binary format (.bed, .bim,.fam)"
  "file",            "The genotype file in AlphaGenes format."
  "seqFile [Not tested on current version.]",         "Sequence read counts in AlphaGenes format."
  "hapsFile [Not tested on current version.]",        "Genotype probabilities for phased individuals."
  "pedigree",        "An alternative pedigree file. Otherwise the pedigree is loaded from the bfile."

.. csv-table:: Additional Options
  :header: "option", "description"
  :widths: 20, 50

  "usePhase",        "[No argument] A flag  to use phase information (Not recomended). This option requires SNP information to be loaded via the bfile option."
  "fullOutput",      "[No argument] A flag to include all likelihoods in the output."
  "genoError",       "The assumed error rate for genotypes.  (Default 0.01). "
  "seqError",        "The assumed error rate for sequence reads.  (Default 0.01). "

If individuals are present in multiple files passed to AlphaAssign, AlphaAssign will use the genotype information found in the last file on this list: bfile < file < seqFile < hapsFile. By default AlphaAssign does not use phase information provided in the haps file. Instead it only uses the genotype probabilities provided in the file. Use of phase information may lead to more accurate imputation in some highly-specialized cases, however, it leads to substantial computational costs and can lower accuracy in the case of map errors.

AlphaAssign outputs three files by default. A pedigree, out.pedigree, which gives the revised pedigree with sires and dames assigned to individuals. In the case where the algorithm does not find a good candidate sire or dam it returns a "0". A second pedigree, out.pedigree.top, which gives the best guess revised pedigree with all individuals in the sire or dam files assigned a sire or a dame. A data file, out.sires, which reports for each individual by sire pair the negative log likelihood that that sire is the parent of the child and the log likelihood of a null parent, a null full sib of the parent, and a null individual from the population. If the option "fullOutput" is included, an additional file, out.sires.full, is reported which contains additional summary statistics. Similar data files for dams is also reported if a dam file is provided. 

Input file formats
~~~~~~~~~~~~~~~~~~

Genotype file 
-------------

The genotype file can be provided in Plink binary format. For more information see `https://www.cog-genomics.org/plink/1.9 <https://www.cog-genomics.org/plink/1.9/formats#bed>`_

AlphaGenes Genotype file
------------------------

The genotype information can also be provided via a text file. Each row contains the individual's id and the allele counts for SNPs on the SNP array. Missing values should be coded as a 3.
Example: ::

  id1 1 0 0 2 0 1
  id2 0 0 1 2 1 2
  id3 1 0 0 0 2 1
  id4 0 1 0 1 2 1

Sequence read counts
--------------------

Sequence read counts can be provided in the AlphaGenes format. In this format there are two rows per individual, the first row is for the reference allele. The second row is for the alternative allele. Each row contains the individual's id and the read counts for that allele.
Example: ::

  id1 3 2 0 2 5 20
  id1 0 0 3 10 0 1
  id2 0 0 0 3 7 0
  id2 5 0 0 0 5 0
  id3 4 5 11 1 1 1
  id3 1 0 0 2 5 5
  id4 0 1 0 1 7 1
  id4 0 0 0 4 2 1

Haplotype file
--------------

The haplotype file provides the (phased) allele probabilities for each locus. There are four lines per individual containing the allele probability for the (aa, aA, Aa, AA) alleles where the paternal allele is listed first, and where *a* is the reference (or major) allele and *A* is the alternative (or minor) allele.  This file can generated via AlphaPeel (prefix: *.haps*).
Example: ::

  id1    0.9998    0.0001    0.0001    1.0000
  id1    0.0000    0.4999    0.4999    0.0000
  id1    0.0000    0.4999    0.4999    0.0000
  id1    0.0001    0.0001    0.0001    0.0000
  id2    0.0000    1.0000    0.0000    1.0000
  id2    0.9601    0.0000    0.0455    0.0000
  id2    0.0399    0.0000    0.9545    0.0000
  id2    0.0000    0.0000    0.0000    0.0000
  id3    0.9998    0.0001    0.0001    1.0000
  id3    0.0000    0.4999    0.4999    0.0000
  id3    0.0000    0.4999    0.4999    0.0000
  id3    0.0001    0.0001    0.0001    0.0000
  id4    1.0000    1.0000    0.0000    1.0000
  id4    0.0000    0.0000    0.0000    0.0000
  id4    0.0000    0.0000    0.0000    0.0000
  id4    0.0000    0.0000    1.0000    0.0000

Pedigree file
-------------

Additional pedigree not included in the plink file can be included in a seperate pedigree file. The format of the pedigree file is id, sireid, damid. Missing or unkown values are coded as 0.
Example: ::

  id1 0 0
  id2 0 0
  id3 id1 id2

Potential sires file
--------------------

A list of individual IDs and the ids of of potential sires. The first column gives the id of the individual. The remaining values give the id of the sire. Rows can have different numbers of potential sires.

Example: ::

  id1 sire1 sire2 sire3 sire4 sire 5
  id2 sire1 sire2 sire3 sire4 sire 5
  id3 sire2 sire3 sire4 sire 6
  id4 sire2 sire3 sire4 sire 6

Output file formats
~~~~~~~~~~~~~~~~~~~

Output file
--------------

This file gives the basic output for AlphaAssign. The first column is the id of the individual. The second column is the id of a sire. The remaining columns give the log likelihood of the sire, whether that sire was chosen, and the log likelihood of a null parent, null full sib of the parent, and a null random individual.

Example: ::

  id candidate score chosen estSire estFullSib estNull
  4001 3681 6558.87993318 1 6322.88957816 9091.85666393 11688.4672246
  4001 3165 11615.510009 0 6322.88957816 9091.85666393 11688.4672246
  4001 3385 11145.9531181 0 6322.88957816 9091.85666393 11688.4672246
  4001 3273 11359.1851049 0 6322.88957816 9091.85666393 11688.4672246
  4001 3279 11671.4021993 0 6322.88957816 9091.85666393 11688.4672246
  4002 3811 6136.86138214 1 6056.76191667 8598.68637406 11135.0289353

Full output file
----------------

This file is generated using the option "fullOutput". This file gives the full output of the algorithm. The first column is the id of the individual. The second column is the expected log likelihood and standard deviation of the log likelihood for a null parent, full sib of the parent, half sib of the parent, and random individual. The remaining columns provide the ids of each potential sire and the log likelihoods for those sires.

.. |aa| replace:: **AlphaAssign** 
