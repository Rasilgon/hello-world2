#######################################################################################
# Idea: Given a number of clusters, this script will 
#     1. create a subdiretory where output data will be saved
#     2. create a script for each  parallel run of the model and
#        save in the respective subdirectory.
#     3. set a script submission function
#     4. using snow/snowfall the cluster structure is created and
#         all scripts (model runs) will be submitted to the clusters 
#
#    --> summing up: a n number of R scripts running in parallel
#
# Pros:
#     - makes easy to combine model with data transfer/arrangement tasks
#     - any function, command or task can be run in parallel: 
#           -> it only has to be included in the scripts
#Cons:
#     -to be found
#
# State:
# Already tested in both my laptop and cluster and it works!
# (this is laptop version using 3 cluster and SOCK type)
#
# Open issues:
#     - output data processing function
#     - data transfer: data volume?
#     - to couple it with model to test it
#
# The version here is just a draft, it must be written for the model and 
# include the dasastes, model, and template.
######################################################################################




######################### UTILITY FUNCTIONS ############################################################
# Submission function
callsystem<-function(script){
  script <- paste("R -f ", script)
  system(script, intern=TRUE)
}


######################### CREATE BATCH OF JOBS ##########################################################
#number of clusters available: 90
ncl =10 
clusters = array(1:ncl)
length(clusters)
# Clusters for each grid: 3 grids one per cluster
gridBreak = length(clusters)/3

# Parameters: just creating a random list for the function
size = as.list(replicate(ncl,floor(runif(1, 900,1000))))
                 
# Create a folder for the data and scripts
mainDir = getwd()
subDir = file.path(mainDir,"outputDirectory1")
for (i in 2:length(clusters)) subDir <- c(subDir, paste(mainDir, "/","outputDirectory",i,sep=""))

# List of scripts
outScripts =file.path(subDir[1], "guess1.R")
for (i in 2:ncl) outScripts <- c(outScripts, paste(subDir[i], "/","guess",i, ".R",sep=""))
# Move to the folder
#setwd(file.path(mainDir, subDir))

# Create script
for (i in 1:length(clusters)){
  #Create directory
  dir.create(file.path(subDir[i]), showWarnings = FALSE)
  # Create script
  print (outScripts[i])
  file.create(outScripts[i])
  sink(outScripts[i])
  cat("##############################\n")
  cat(sprintf("# Script for run %d \n", i))
  cat(sprintf("    setwd(\"%s\")\n", subDir[i]))#subDir[i]
  cat("##############################\n\n")
  cat ('# Model wrapper\n')
  cat ('runMyModel <- function(parList){\n')
  cat (sprintf("    setwd(\"%s\")\n", subDir[i]))#subDir[i]
  cat ("    writeparameters(template, par)\n")
  cat ("    system (\"guess ./insfile.ins\")\n")
  cat ("    getdata()\n")
  cat('}\n')
    # Close file
  cat("##############################\n\n")
  cat ('# Rejection sampler\n') 
  cat("##############################\n\n")
  cat("# prior function\n")
  cat("prior = function(n){\n")
  cat("  res <- rnorm(2*n)\n")
  cat("  res = matrix(res, ncol = 2)\n")
  cat("  return(res)\n")
  cat("  }\n")
  cat("# set size\n")
  cat(sprintf("size = %f\n", size[i]))
  cat("# test model\n")
  cat("testModel <- function(x, waitingtime  = 0.01){\n")
  cat("    Sys.sleep(waitingtime) # to test parallel speedup\n")
  cat("    return(sum(dnorm(x=x, log = T)))\n")
  cat("}\n")
  cat("# Rejection sampler\n")
  cat("rejectionSampler <- function(target, prior, size){\n")
  cat("  proposal <- prior(size)\n")
  cat("  proposalList <- as.list(data.frame(t(proposal)))\n")
  cat("  density <- sapply(proposalList, target)\n")
  cat("  print('single') #to know if is actually running single or parallel\n")
  cat("  maxDens = max(density, na.rm = T)\n")
  cat("  accepted = ifelse(runif(size,0,1) < exp(density -  maxDens), TRUE, FALSE)\n")
  cat("  result <- data.frame(cbind(proposal, density, accepted))\n")
  cat("  return(result)")
  cat("}\n")
  cat("### Single core execution ###\n")
  cat("p1 <- proc.time()\n")
  cat("result <- rejectionSampler(testModel, prior, size)\n")
  cat("a <- proc.time() - p1\n")
  cat("write.csv(result, './result.csv')\n")
  sink() 
}


########################## CREATE CLUSTER AND SUBMIT JOBS ###########################################################
# Create clusters and submit the jobs
library(Rmpi)
library(snow)
library(snowfall)
# Create cluster
sfInit(parallel=TRUE, cpus=ncl)#type="MPI"
p1 <- proc.time()
# export everything
sfExportAll() 
sfSapply(outScripts, callsystem)
proc.time() - p1
# Destroy cluster
sfStop()
########################## END ######################################################################################
