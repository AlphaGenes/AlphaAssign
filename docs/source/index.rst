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


|aa| is a parentage assignment algorithm for genotype or sequence data. This program uses a likelihood based model to determine the sire of an individual based on a list of potential sires. For more information on the algorithm see *Parentage assignment with low density array data and low coverage sequence data* `(Journal of Animal Breeding and Genetics) <https://onlinelibrary.wiley.com/doi/10.1111/jbg.12370>`_.

Please report bugs or suggestions on how the program / user interface / manual could be improved or made more user friendly to `John.Hickey@roslin.ed.ac.uk <John.Hickey@roslin.ed.ac.uk>`_ or `Awhalen@roslin.ed.ac.uk <awhalen@roslin.ed.ac.uk>`_.

Conditions of use
-----------------
|aa| is part of a suite of software that our group has developed. It is fully and freely available for academic use, provided that users cite it in publications. However, due to our contractual obligations with some of the funders of the research program that has developed this suite of software, all interested commercial organizations are requested to contact John Hickey (`John.Hickey@roslin.ed.ac.uk <John.Hickey@roslin.ed.ac.uk>`_) to discuss the terms of use.

Citation:
Whalen, A., Gorjanc, G., and Hickey, J. (2018). Parentage assignment with low density array data and low coverage sequence data. Journal of Animal Breeding and Genetics.

Disclaimer
----------

While every effort has been made to ensure that |aa| does what it claims to do, there is absolutely no guarantee that the results provided are correct. Use of |aa| is at your own risk.


Run commands and spec file
~~~~~~~~~~~~~~~~~~~~~~~~~~

AlphaAssign takes in a number of command line arguments to control the program's behavior. To view a list of arguments, run AlphaAssign without any command line arguments, i.e. ``AlphaAssign`` or ``AlphaAssign -h``. 


Core Arguments 
--------------

::
  
  Core arguments
    -out prefix              The output file prefix.

The ``-out`` argument gives the output file prefix for where the outputs of AlphaAssign should be stored. AlphaAssign outputs a ``.pedigree`` file which gives the pedigree with sires assigned, a ``.pedigree.top`` which gives the best guess pedigree with individuals always assigned parents, a ``.sires`` and ``.dams`` files which give more information on the assignment statistic for the sires and dams.

Input Arguments 
----------------

::

  Input Options:
    -bfile [BFILE [BFILE ...]]
                          A file in plink (binary) format. Only stable on
                          Linux).
    -genotypes [GENOTYPES [GENOTYPES ...]]
                          A file in AlphaGenes format.
    -seqfile [SEQFILE [SEQFILE ...]]
                          A sequence data file.
    -pedigree [PEDIGREE [PEDIGREE ...]]
                          A pedigree file in AlphaGenes format.

  Multithreading Options:
    -iothreads IOTHREADS  Number of threads to use for input and output.
                          Default: 1.

AlphaAssign requires a genotype file to run. It supports  binary plink files, ``-bfile``, genotype files in the AlphaGenesFormat, ``-genotypes``, and sequence data read counts in the AlphaGenes format, ``-seqfile``. 

A pedigree file may also be supplied to provide a list of known sires using the ``-pedigree`` option. 

Binary plink files require the package ``alphaplinkpython``. This can be installed via ``pip`` but is only stable for Linux.

The parameter ``-iothreads`` controls the number of threads/processes used by AlphaAssign. AlphaAssign uses additional threads to parse and format input and output files. Setting this option to a value greater than 1 is only recommended for very large files (i.e. >10,000 individuals).


Assignment arguments: 
------------------------
::

  Core assignement arguments:
    -potentialsires POTENTIALSIRES
                          A list of potential sires for each individual.
    -potentialdams POTENTIALDAMS
                          A list of potential dams for each individual.

  Arguments to choose how sires and dams are assigned:
    -runtype RUNTYPE      opp, likelihood, both, Default: both
    -add_threshold ADD_THRESHOLD
                          Assignement score threshold for adding a new
                          individual as a parent
    -p_threshold P_THRESHOLD
                          Negative log-pvalue threshold for removing parents via
                          opposing homozygotes

  Probability Arguments:
    -error ERROR          Genotyping error rate. Default: 0.01.
    -seqerror SEQERROR    Assumed sequencing error rate. Default: 0.001.
    -usemaf               A flag to use the minor allele frequency when
                          constructing genotype estimates for the sire and
                          maternal grandsire. Not recomended for small input
                          pedigrees.

AlphaAssign requires as inputs either a ``-potentialsires`` or ``-potentialdams`` argument. This argument gives a list of sires or dams to assign for each individual.

The ``-runtype`` determines how assignments are done. The options are to do assignments using the number opposing homozygous loci, ``opp``, via a likelihood model or both. For the likelihood model the ``-add_threshold`` determines the log likelihood values needed to either add a putative parent or reject a parent. For opposing homozygous values ``-p_threshold`` determines the p-value threshold required reject the top parent with opposing homozygous loci. The p-value is determined by a binomial test using the genotyping error rate.


The ``-error``, ``-seqerror`` control the genotyping error rate and sequence error rate. Changing these to values that more closely reflect the true data may increase accuracy in some cases.

The flag ``-usemaf`` changes whether the minor allele frequency is used to estimate the putative genotypes of the parents. This can increase accuracy if large number of individuals are included in the genotype file.

Input file formats
~~~~~~~~~~~~~~~~~~

Genotype file 
-------------

Genotype files contain the input genotypes for each individual. The first value in each line is the individual's id. The remaining values are the genotypes of the individual at each locus, either 0, 1, or 2 (or 9 if missing). The following examples gives the genotypes for four individuals genotyped on four markers each.

Example: ::

  id1 0 2 9 0 
  id2 1 1 1 1 
  id3 2 0 2 0 
  id4 0 2 1 0

Sequence file
-------------

The sequence data file is in a similar Sequence data is given in a similar format to the genotype data. For each individual there are two lines. The first line gives the individual's id and the read counts for the reference allele. The second line gives the individual's id and the read counts for the alternative allele.

Example: ::

  id1 4 0 0 7 # Reference allele for id1
  id1 0 3 0 0 # Alternative allele for id1
  id2 1 3 4 3
  id2 1 1 6 2
  id3 0 3 0 1
  id3 5 0 2 0
  id4 2 0 6 7
  id4 0 7 7 0

Pedigree file
-------------

Each line of a pedigree file has three values, the individual's id, their father's id, and their mother's id. "0" represents an unknown id.

Example: ::

  id1 0 0
  id2 0 0
  id3 id1 id2
  id4 id1 id2

Binary plink file
-----------------

AlphaPeel supports the use of binary plink files using the package ``AlphaPlinkPython``. AlphaPeel will use the pedigree supplied by the ``.fam`` file if a pedigree file is not supplied. Otherwise the pedigree file will be used and the ``.fam`` file will be ignored. 

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

This file gives the basic output for AlphaAssign. The first column is the id of the individual. The second column is the id of a sire. The remaining columns give the id of a known parent, whether the parent was selected as the most likely parent, the final weight placed on the sire (higher means more likely to be the true sire), and then the scores for the sire distribution, fullsib, halfsib and null distributions. There are an additional three columns which give the number of opposing homozygous loci with and without taking a known parent into account, the number of loci evaluated, and the log-p value of observing that number of opposing homozygous loci with the input error rate.

Example: ::

  id candidate altParent chosen score estSire estFullSib esthalfSib estNull nOpposing nOpposingWOparent nLoci logP
  801 657 0 0 136.28771 0.0 -136.28772 -222.13818 -326.5254 0 0 1000 -4.3172176e-05
  801 735 0 0 0.0 -50.85962 0.0 -51.37207 -126.38208 67 67 1000 -76.93231
  801 703 0 0 22.15454 0.0 -22.154541 -85.90723 -170.91504 40 40 1000 -29.8377
  801 609 0 0 22.997680 0.0 -22.99768 -87.28125 -172.93481 40 40 1000 -29.8377
  801 629 0 0 25.065185 0.0 -25.065186 -88.16138 -171.9967 38 38 1000 -26.96456
  801 763 0 0 0.0 -77.24463 0.0 -40.976196 -104.28198 72 72 1000 -87.05572755433364
  801 715 0 0 0.0 -39.41833 0.0 -53.59961 -130.56909 63 63 1000 -69.11322704626824

.. |aa| replace:: AlphaAssign
