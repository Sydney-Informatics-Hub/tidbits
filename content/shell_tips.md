title: Shell Tips
author: Henry Lydecker
date: 2022-07-06
Category: misc
Tags: shell,hpc

A collection of misc commands and short snippets that might make your life a lot easier when using the shell locally, on remote, or on hpc.

### Table of Contents
  * [Check permissions](#check-permissions)
  * [Change permissions](#change-permissions)
  * [Count all files](#count-all-files)
  * [Count all files of a certain type](#count-all-files-of-a-certain-type)
  * [Force Quit a Pesky App That Won't Quit](#force-quit-a-pesky-app-that-wont-quit)
  * [HPC job resource monitoring](#hpc-job-resource-monitoring)
  * [Find all .txt files and then run some code on each of them](#find-all-txt-files-and-then-run-some-code-on-each-of-them)
  * [Remove any line not beginning with "apples" from text files in this folder](#remove-any-line-not-beginning-with-apples-from-text-files-in-this-folder)  
  * [Rsync from local folder to folder on HPC](#rsync-from-local-folder-to-folder-on-HPC)  
  * [Set up and use ssh keys for remote access to RDS](#set-up-and-use-ssh-keys-for-remote-access-to-RDS)  

## Check permissions

```bash
ls -lah
```

## Change permissions

If you want to change the permissons for a directory and its contents, use this:

```bash
chmod a+rwx <some_dir> -R
```

Where `a` is all users, `rwx` means Read + Write + eXecute, `<some_dir>` is a directory you want to change permissions for, and `-R` applies these changes to all contents recursively. Can also use this [chmod calculator](https://chmodcommand.com/) to generate specific permissions in numerical and symbolic formats.  

## Count all files

```bash
find . -type f | wc -l
```

## Count all files of a certain type(s)

There are several ways to count all files of a certain type(s), but this is by far the fastest simple shell command.

For example, if you want to recursively look through a directory and count all files of several different extentsions (in this case images):

```bash
find . -type f | sed -e 's/.*\.//' | sort | uniq -c | sort -n | grep -Ei '(tiff|bmp|jpeg|jpg|png|gif)$'
```


## Find all .txt files and then run some code on each of them

```bash
find -name "*.txt" -exec <command>
```

## Remove any line not beginning with "apples" from text files in this folder

```bash
sed -i '' '/^apples/!d' *.txt
```

## Force quit a pesky app that won't quit

Imagine you are trying to quit an application (e.g. Docker) or killa process using activity monitor, but for some reason the application keeps coming back or won't quit.

```bash
osascript -e 'quit app "Docker"'
```

This will effecitevly nuke the app for you.

## Rsync from local folder to folder on HPC

```bash
rsync -tvxPr /local/path/to/files unikey@hpc.sydney.edu.au:/remote/path/to/copy/to
```

## Check when your HPC job should start

If you have a bunch of jobs in the queue on artemis, you might want to check when they are expected to start.

```bash
qstat -u <your_unikey> -T
```

## HPC job resource monitoring 

[Scripts availabile here](https://github.com/Sydney-Informatics-Hub/HPC_usage_reports) will pull compute (CPU, memory, walltime etc) resource consumption from PBS job logs into tab-delimited format and to report queue time from job history. Usage reporting scripts are currently available for:

- University of Sydney's Artemis  
- National Compute Infrastructure's Raijin 
- National Compute Infrastructure's Gadi  
- University of Queensland's Flashlite  

Run the script from within the directory that contains the usage log files to be read. Optionally, can include the prefix of the usage logs as an argument on the command line. For example, to collate resource usage from Gadi PBS job logs, run: 
```
perl /g/data/er01/gadi_usage_report_v1.1.pl <log file prefix>
```
To live fast and free, add the following alias to your .bashrc profile:
```
alias joblogs='perl /g/data/er01/HPC_usage_reports/gadi_usage_report_v1.1.pl'
```
And run from within the directory housing log files, with: 
```
joblogs
```

An example of the output: 

|#JobName         |CPUs_requested|CPUs_used|Mem_requested|Mem_used|CPUtime |CPUtime_mins|Walltime_req|Walltime_used|Walltime_mins|JobFS_req|JobFS_used|Efficiency|Service_units|Job_exit_status|Date      |Time    |
|-----------------|--------------|---------|-------------|--------|--------|------------|------------|-------------|-------------|---------|----------|----------|-------------|---------------|----------|--------|
|amber_T115991B2.o|16            |16       |190.0GB      |65.47GB |03:58:20|238.33      |02:00:00    |00:41:19     |41.32        |100.0MB  |0B        |0.36      |65.42        |0              |2022-05-09|18:10:57|
|amber_T519706C1.o|16            |16       |190.0GB      |73.16GB |03:35:27|215.45      |02:00:00    |00:37:43     |37.72        |100.0MB  |0B        |0.36      |59.72        |0              |2022-05-09|18:06:46|
|amber_T530707.o  |16            |16       |190.0GB      |73.96GB |02:53:58|173.97      |02:00:00    |00:33:51     |33.85        |100.0MB  |0B        |0.32      |53.60        |0              |2022-05-09|18:02:30|
|amber_T531207.o  |16            |16       |190.0GB      |70.38GB |03:25:54|205.90      |02:00:00    |00:37:04     |37.07        |100.0MB  |0B        |0.35      |58.69        |0              |2022-05-09|18:05:28|
|amber_T547109.o  |16            |16       |190.0GB      |73.53GB |03:33:23|213.38      |02:00:00    |00:42:44     |42.73        |100.0MB  |0B        |0.31      |67.66        |0              |2022-05-09|18:10:41|
|amber_T563810.o  |16            |16       |190.0GB      |68.73GB |02:55:47|175.78      |02:00:00    |00:30:21     |30.35        |100.0MB  |0B        |0.36      |48.05        |0              |2022-05-09|17:57:43|

## How to SCP if there are spaces in folder names

Add three `\\\` after every space.

Like so:
```bash
folder\\\ with\\\ spaces/*
```

## Set up and use ssh keys for remote access to RDS

Connecting to RDS (research-data-ext.sydney.edu.au) remotely is only permissable via an SFTP connection. If you're working on a server external to the University (i.e. NCI Gadi) and need to transfer data to and from the RDS and this system, you can connect to the RDS on the command line with: 

```
sftp <UNIKEY>@research-data-ext.sydney.edu.au
```

You will be prompted to provide your password with: 

```
Authorised users only. All activity may be monitored and reported.
Password:
```
However, if you are attempting to connect to RDS and transfer files via a PBS job, where the scheduling of these operations is driven by a batch controlled workflow, relying on entering a password or passphrase at the time of the operation is not feasible. In this case, you will need to **set up password-free ssh keys**. You can do this with the following process: 

**On the remote server, wanting to access RDS** 
1. Log into the remote server 
2. `cd ~`
3. `ls .ssh` (If this doesnt exist, then `mkdir .ssh`)
4. `chmod 700 .ssh`
5. `ssh-keygen` Just press enter when prompted, saving the key in ~/.ssh/id_rsa and enter for no passphrase
6. `cd .ssh` You will now see two files, id_rsa (private key) and id_rsa.pub (your public key)
7. `chmod 700 id_rsa*`
8. `cat ~/.ssh/id_rsa.pub >> authorized_keys` this will create the authorized_keys file that you will copy to RDS to allow password-free connection
9. `chmod 700 authorized_keys`
10. `sftp <UNIKEY>@research-data-ext.sydney.edu.au` 
11. You will be prompted to provide your password, same as above. Once your login is successful you will be in remotely logged into your home directory on RDS/Artemis.
12. `cd .ssh` If this doesn't exist, then run `mkdir ~/.ssh`
13. `put authorized_keys` This will transfer authorized_keys on Gadi to your current directory. With sftp, it will look for the file relative to where you launched sftp. You can check where you are on Gadi using lls
14. Logout using ctrl+z and 
15. Test the sftp connection again by trying to log in, same as above. You should not need to use a password this time. 

**Something to keep in mind**   
Using ssh keys is *very* sensitive to file and directory permissions on both sides – and it looks not just at the key itself, but also the .ssh folder and your home directory. If you somehow managed to mess your keys up (like me) and cannot get the password-free method to work, you probably have messed up permissions of your ~/.ssh directories, as well as the authorized_keys and id_rsa.pub files.  
