Title: Safely downloading your sequence data to RDS 
Date: 2024-02-07
Author: Georgie Samaha
Category: unix 
Tags: bioinformatics,hpc,large-data

Imagine you're a biologist, geneticist, vet, or clinician. You've gone through the painstaking process of extracting some genetic material from a set of samples and sent them off for next generation sequencing to a commercial sequencing provider. Six weeks later you get an email from your chosen provider saying something like: 

```
Dear Dr Cats, 

I am pleased to inform you that your project CATGENES001 is complete. 

The data is available to download from our platform using this link: 
https://sequencing-dna-4-u/CATGENES001/CATGENES001.tar

If you prefer the command line, please use one of the following: 
wget -c -O https://sequencing-dna-4-u/CATGENES001/CATGENES001.tar

curl -o https://sequencing-dna-4-u/CATGENES001/CATGENES001.tar 

Note all links will expire in THREE(3) WEEKS!! 

Thank you, 
Sequencing4U
```

Now what? Three weeks and then your expensive data is gone forever if you don't act? Yes. How do you know if you 'prefer' the command-line? 

If you're a University of Sydney staff member or student then chances are you'll need to save your data to RDS. This means you probably have no choice but to 'prefer' the command-line, especially if you're working with genomic data and/or a large number of samples. Follow these instructions to:

1. Download your data 
2. Extract your files from the tarball (`.tar`) 
3. Validate the integrity of your files (i.e. make sure your files aren't corrupted)

### 0. Open a terminal application on your computer 

You'll need to use a [terminal application to access the command-line and log into Artemis/RDS](https://sydney-informatics-hub.github.io/training.artemis.rds/setup.html).
* MacOS users can use the terminal application in their Applications folder 
* Windows users can install [MobaXterm](https://sydney-informatics-hub.github.io/customising-nfcore-workshop/setup.html#option-2-install-and-set-up-a-terminal-application) or Putty

Log into Artemis HPC: 
```
ssh unikey@hpc.sydney.edu.au
```

Navigate to the directory on RDS you want to download your sequence data to: 
```
cd /rds/PRJ-KITTYCATDNA
```

### 1. Download your data 

A simple way to retrieve files from web links is using the command-line utilities 'wget' or 'curl', as suggested in the email above. You could run these commands directly on the command-line but that isn't very reliable when working with large files that take a long time to download. We will instead wrap one of these commands in a PBS script that uses the dedicated data transfer queue to quickly download and move data around safely. 

Customise and copy the following example code into a script called `download_data.pbs` using the text editor nano: 
```
nano download_data.pbs
```

Fill in: 
* Your dashR project code (`#PBS -P DASHR-CODE`)
* The path to the RDS directory you want to download your data to (dir=/path/to/rds/directory) 
* The wget or curl command given by your sequencing provider 

```
#!/bin/bash 

#PBS -P KITTYCATDNA
#PBS -q dtq
#PBS -l select=1:ncpus=1:mem=50gb
#PBS -l walltime=08:00:00
#PBS -N download2rds

# Define download directory
dir=/rds/PRJ-KITTYCATDNA/raw_fastq

# Move to download directory and download
cd ${dir}
wget -c -O https://sequencing-dna-4-u/CATGENES001/CATGENES001.tar
```

Save this file (on nano `ctrl`+`x`, `ctrl`+`s`) and execute the script: 

```
qsub download_data.pbs
```

You can monitor the progress of your download by running the `jobstat` or `qstat -u <your unikey>` commands on the command-line. Once your job is complete and download has succeeded your job will have left the queue and you'll observe some files in the directory you executed the script from: 
*  `download2rds.o12345`
*  `download2rds.o12345_usage`
*  `download2rds.e12345`

Confirm your job has successfully completed by looking at the exit status row of `download2rds.o12345_usage`. If **exit status is 0** your job completed without error and you can proceed. If not 0, you'll need to identify the source of the error and rerun your download script, making necessary adjustments.   

```
cat download2rds.o12345_usage
```

### 2. Extract files from the tar archive 

Assuming your PBS job ran successfully, lets now extract your raw sequence files from the [tarball](https://www.cyberciti.biz/faq/tar-extract-linux/) you downloaded. For example, with our example link, we downloaded a file called 'CATGENES001.tar'. You can extract everything by running: 

```
tar -xf CATGENES001.tar
```

If your tar file is also further compressed with gzip (e.g. CATGENES001.tar.gz), you'll need to instead run: 
```
tar -xzf CATGENES001.tar.gz
```

Once extracted, you should now have a folder named CATGENES001 in your directory: 

```
ls -lh
```
```
total 148288722
-rwxrwx--- 1 unikey1111 RDS-FVS-KITTYCATDNA-RW    770  Feb7   14:35   download_datai.sh
-rwxrwx--- 1 unikey1111 RDS-FVS-KITTYCATDNA-RW    230M Feb7   09:36   download2rds.o12345
-rwxrwx--- 1 unikey1111 RDS-FVS-KITTYCATDNA-RW    0    Feb7   09:18   download2rds.o12345
-rwxrwx--- 1 unikey1111 RDS-FVS-KITTYCATDNA-RW    1.8K Feb7   09:36   download2rds.o12345_usage
drwxrws--- 2 unikey1111 RDS-FVS-KITTYCATDNA-RW    4.0K Jan29  12:37   CATGENES001
-rwxrwx--- 1 unikey1111 RDS-FVS-KITTYCATDNA-RW    140G Feb7   09:36   CATGENES001.tar
```

### 3. Run md5 checksums to validate files

Given we can't go back and download our data again after the provided link expires, we need to make sure our data is not corrupted in some way. We can do this using [md5](https://en.wikipedia.org/wiki/MD5) checksums. 

If you look inside the folder you just extracted, you'll likely see a file named something like `CATGENES001_md5sum.txt`. It should look something like this: 

```
4df06af823562f0d38eaf02071f7867b ./CATGENES001/sample1_R1.fq.gz
3123sddg2528950d38erzfz56787543v ./CATGENES001/sample1_R2.fq.gz
9gfd3e6hr456780987yghgfdewew4545 ./CATGENES001/sample2_R1.fq.gz
4235af82d52d8g0d38eaf02071fd8dfg ./CATGENES001/sample2_R2.fq.gz
```

Each of the alphanumeric strings provided in this file represent a unique fingerprint of their corresponding fastq file. These unique hashes have been generated by the sequencing company on the original fastq files they generated after sequencing your data. We need to recalculate the md5 checksum of each fastq file to verify their integrity. If the checksums match the original values, the files are identical to the originals and we can be assured they are not corrupted. We do this by running: 

```
md5sum -c CATGENES001_md5sum.txt
```

Depending on the size of your files, you may not be able to run this on the command-line on Artemis due to resource constraints. To avoid this, submit it as another PBS job, using the following script `check_md5sum.pbs`:

```
#!/bin/bash

#PBS -P KITTYCATDNA
#PBS -q dtq
#PBS -l select=1:ncpus=1:mem=50gb
#PBS -l walltime=48:00:00
#PBS -N download2rds

# Move into directory you want to save sequences to
cd ${dir}

# Check file integrity
md5sum -c ${tar_file}/${tar_file}_md5sum.txt > md5_check.txt
```

Execute with: 
```
qsub check_md5sum.pbs
```

Once the job has completed you'll have created a text file `md5_check.txt` that should : 

```
cat md5_check.txt
```
```
./CATGENES001/sample1_R1.fq.gz: OK
./CATGENES001/sample1_R2.fq.gz: OK
./CATGENES001/sample2_R1.fq.gz: OK
./CATGENES001/sample2_R2.fq.gz: OK
```

If the calculated checksum matches the provided checksum, md5sum reports "OK" for that file; otherwise, it reports "FAILED" to indicate a checksum mismatch or file corruption. If this is the case, check if your download command has failed at any point and if that doesn't resolve the issue, contact your sequencing provider for advice. 

### 4. Or do it all at once

Edit this script according to add your own DashR/RDS account name, desired location to download your files, and the link provided by your sequencing company: 

```
#!/bin/bash 

#PBS -P 
#PBS -q dtq
#PBS -l select=1:ncpus=1:mem=50gb
#PBS -l walltime=08:00:00
#PBS -N download2rds

# Set variables
dir=
tar_file=
download_link=

# Move into directory you want to save sequences to
cd ${dir}

# Download tar archive
wget -c -O ${tar_file}.tar ${download_link}

# Extract files
tar -xf ${tar_file}.tar

# Check file integrity
md5sum -c ${tar_file}/${tar_file}_md5sum.txt > ${tar_file}/md5_check.txt
```

### Useful resources

* [SIH Intro to Artemis training materials](https://sydney-informatics-hub.github.io/training.artemis/)
* [Artemis user guide](https://sydneyuni.atlassian.net/wiki/spaces/RC/pages/185827329/Artemis+User+Guide)

Happy HPCing! :D 