author: Cali Willet
date: 2025-02-20
Category: Gadi
Tags: shell,terminal,nci,gadi,hpc,software,module

# Making your self-installed tools on NCI Gadi compatible with module commands

Gadi has a lot of global apps and specialised environments with shared tools. You can also use singularity containers. If you need to self-install a tool, it can be useful to have this tool work with module commands such as `module avail` and `module load`. 

Follow the steps below to achieve this. 

## 0. Add a module path to profile

Each user must have the following line saved in their `.bash_profile` in order for the module load commands to work:


```bash 
printf "export MODULEPATH=${MODULEPATH}:/g/data/<project>/apps/Modules/modulefiles\n" >> .bash_profile
```

Then either run `souce .bash_profile` or refresh terminal to re-load profile. 

This step need only be done ONCE per NCI project/apps install path. 


## 1. Install the software 

Ideally, install the software into somewhere persistent (not scratch, since this is subject to 100-day purge). For tools only you will use, `/home` is fine. For tools others in your NCI project may benefit from, `/g/data` is the ideal place. 

Make the following directory structure:

```bash
mkdir -p /g/data/<project>/apps/<toolname>/<tool-version>
```
Install into this directory following developer’s instructions for installation. You may need to manually move the complete install folder into the above version directory. The  directory structure is critical here. 


## 2. Create a .base file

Make the following directory structure and create a `.base` file:

```bash
mkdir -p /g/data/<project>/apps/Modules/modulefiles/<software>
touch /g/data/<project>/apps/Modules/modulefiles/<software>/.base
```

Ensure the name <software> exactly matches that used for the install path. 

Add content to and save the `.base` file, following the examples shown below. 

### Basic .base file example

This is a standard `.base` file that can be copy pasted and used as-is for your tool (provided you adhere to the prescribed directory paths exactly). Some tools have dependencies that should be co-loaded, or require other specific paths added to `path` - see the second example for those requirements. 

```bash
#%Module1.0#####################################################################
##
## $name modulefile
##

set ver [lrange [split [ module-info name ] / ] 1 1 ]
set name [lrange [split [ module-info name ] / ] 0 0 ]
set loading [module-info mode load]
set desc [join [read [ open "/g/data/<project>/apps/Modules/modulefiles/$name/.desc" ] ] ]

proc ModulesHelp { } {
  puts stderr "\tThis module sets the envinronment for $name v$ver"
}

module-whatis   "$desc (v$ver)"

prepend-path PATH /g/data/<project>/apps/$name/$ver
```

### .base file with dependent software and additional paths

In this example, loading the tool also loads the dependency `java`. The tool also requires the `pipelines` directory to be added to path: 

```
#%Module1.0#####################################################################
##
## $name modulefile
##

set ver [lrange [split [ module-info name ] / ] 1 1 ]
set name [lrange [split [ module-info name ] / ] 0 0 ]
set loading [module-info mode load]
set desc [join [read [ open "/g/data/<project>>/apps/Modules/modulefiles/$name/.desc" ] ] ]

proc ModulesHelp { } {
  puts stderr "\tThis module sets the envinronment for $name v$ver"
}

module-whatis   "$desc (v$ver)"

if { $loading && ![ is-loaded java ] } {
  module load java
}


prepend-path PATH /g/data/<project>>/apps/$name/$ver
prepend-path PATH /g/data/<project>/apps/$name/$ver/pipelines
```

## 3. Create a .desc file

This is a short description of the tool. 

```bash
printf "This tool does abc for xyz data in record time\n" >  /g/data/<project>/apps/Modules/modulefiles/<software>/.desc
```

## 4. Link the .base file to the software version 

```bash
ln -s  /g/data/<project>/apps/Modules/modulefiles/<software>/.base <version>
```
Ensure that `version` exactly matches that used to name the software install directory 

## 5. Test the module

```bash
module load <software>/<version>
<software> [args] # eg run a help or version command
```

Also ask other group members to test, to ensure you have nothing unique to your environment that is required for the tool. 



