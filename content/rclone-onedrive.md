title: CLI transfer to OneDrive
author: Georgie Samaha
date: 2023-07-27
Category: unix
Tags: rclone,onedrive,sharepoint

Since the death of Cloudstor (RIP), we've had to rely on OneDrive to share data with external collaborators who cannot gain access to USyd supported compute platforms. When working with large datasets, up/downloading data to OneDrive requires a CLI solution that can be automated and sped up. 

While OneDrive has its own user interface for accessing the OneDrive API from the command-line its functionality is limited. [Rclone](https://rclone.org/onedrive/) is also capable of interacting with the OneDrive API, support other cloud services beyond OneDrive, and offers advanced features like synchronising directories and data verification using checksums.

### Configuration when you don't have sudo permissions (i.e. on Artemis/RDS) 

NOTE: on Artemis/rds you will not be able to open the provided link. To avoid this you'll have to configure rclone on your local machine. So ensure it is installed on a machine with external network access before you start this process. See section below for installation instructions. 

If on Artemis/RDS, load the module: 
```
module load rclone/1.62.2
```

Then start an interactive session to configure your installation and follow the steps below to configure for OneDrive: 
```
rclone config
```

1. Select new remote (n)
2. Name your remote (e.g. Georgie-OneDrive)
3. Select 'onedrive' as storage type
4. Leave client ID and secret empty (hit enter a few times)
5. Do not edit advanced config (n), use auto config (y)
6. When asked whether or not to use a web bowser to authenticate rclone, select no (n)
7. On your local machine (requires rclone is installed) run `rclone authorize "onedrive"`
8. Copy the provided secret token and paste it in Artemis/rds terminal 
9. Select 'onedrive' as config type 
10. Specify which drive to use
11. Accept configuration (y)
12. Quit config (q)

### Configuration when you do have sudo permissions

Start by installing and configuring rclone if on a VM or local machine: 
```
sudo apt install rclone
```

Then start an interactive session to configure your installation and follow the steps below to configure for OneDrive: 
```
rclone config
```

1. Select new remote (n)
2. Name your remote (e.g. Georgie-OneDrive)
3. Select 'onedrive' as storage type
4. Leave client ID and secret empty (hit enter a few times)
5. Do not edit advanced config (n), use auto config (y)
6. Open link in your browser, accept permission request 
7. Back on CLI, select onedrive
8. Specify which drive to use
9. Accept configuration (y)
10. Quit config (q)

### Transfer data 
Once configuration is set you can view your rclone configuration with: 
```
rclone config show
```

To transfer data to your configured OneDrive account, simply run: 
```
rclone copy <source>:<path> <dest>:<path> 
```

For example:
```
rclone copy ./genome-1.bam Georgie-OneDrive:Documents/Genome-1
```

Where I am transfering the file `genome-1.bam` to my pre-configured OneDrive remote named `Georgie-OneDrive` at the path `Documents/Genome-1`

To transfer data from rds or Artemis to OneDrive via a PBS job using the dtq queue: 

```
#!/bin/bash
#PBS -P SIHsandbox
#PBS -N transfer
#PBS -q dtq
#PBS -l select=1:ncpus=1:mem=20gb
#PBS -l walltime=05:00:00
#PBS -W umask=022
#PBS -j oe
#PBS -m e
#PBS -M georgina.samaha@sydney.edu.au

module load rclone 

source= # file/directory to transfer
destination= # name of configured onedrive drive
path= # onedrive path 

rclone copy ${source} ${destination}:${path}
```
