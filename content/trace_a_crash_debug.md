title: How to use a 'trace' to debug a crashing program in Linux
author: Nathaniel Butterworth
date: 2023-05-17
Category: unix
Tags: debugging,linux,unix,debug

When software crashes, it usually produces a runtime error and wil give you a hint to why it is failing. Digging into the libraries and system calls and monitoring "where the program gets to" can be informative.

### Expected execution
```
user@host$ matlab
MATLAB is selecting SOFTWARE OPENGL rendering.

                                                < M A T L A B (R) >
                                      Copyright 1984-2021 The MathWorks, Inc.
                                 R2021a Update 8 (9.10.0.2198249) 64-bit (glnxa64)
                                                 February 15, 2023

 
For online documentation, see https://www.mathworks.com/support
For product information, visit www.mathworks.com.
 
>> disp("hello world")
hello world
>> 
```

### Loudly crashing - enough info to search for a solution!
```
user@host$ matlab
java.lang.NullPointerException
at javax.swing.JList$AccessibleJList$AccessibleJListChild.getAccessibleValue(JList.java:3400)
at sun.lwawt.macosx.CAccessibility$31.call(CAccessibility.java:542)
at sun.lwawt.macosx.CAccessibility$31.call(CAccessibility.java:534)
at sun.lwawt.macosx.LWCToolkit$CallableWrapper.run(LWCToolkit.java:511)
at java.awt.event.InvocationEvent.dispatch(InvocationEvent.java:302)
at java.awt.EventQueue.dispatchEventImpl(EventQueue.java:733)
at java.awt.EventQueue.access$200(EventQueue.java:103)
at java.awt.EventQueue$3.run(EventQueue.java:694)
at java.awt.EventQueue$3.run(EventQueue.java:692)
...
```


### Quietly crashing! How to debug!?
```
user@host$ matlab
MATLAB is selecting SOFTWARE OPENGL rendering.
user@host$
```


## ldd
List Dynamic Dependencies (ldd), tells you all the libraries that your application requires. Often a missing package is the source of your problems.
```
user@host$ ldd matlab

linux-vdso.so.1 (0x00007ffe4d5d1000)
libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007f3721a87000)
libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007f3721866000)
librt.so.1 => /lib/x86_64-linux-gnu/librt.so.1 (0x00007f372165e000)
libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007f372145a000)
libstdc++.so.6 => /lib/x86_64-linux-gnu/libstdc++.so.6 (0x00007f37210d6000)
libmwmclmcrrt.so.11.1 => not found
libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007f3720eba000)
libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f3720ad9000)
/lib64/ld-linux-x86-64.so.2 (0x00007f3721f10000)
```

## strace 

The output can be formidable, but the errors may be informative.

Strace intercepts and records the system calls which are called by a process and the signals which are received by a process.
       
```
user@host$ strace -v matlab
execve("/opt/matlab/bin/glnxa64/MATLAB", ["/opt/matlab/bin/glnxa64/MATLAB"], ["MODULE_VERSION_STACK=3.2.10", "HOSTNAME=hpc055", "PBS_ACCOUNT=RDS-CORE-SIHnextgen-"..., "TERM=xterm-256color", "SHELL=/bin/bash", "HISTSIZE=1000", "TMPDIR=/tmp/pbs.6846183.pbsserve"..., "PYTHON_PATH=:/home/nbut3013/ptBa"..., "PBS_JOBNAME=STDIN", "PBS_ENVIRONMENT=PBS_INTERACTIVE", "QTDIR=/usr/lib64/qt-3.3", "QTINC=/usr/lib64/qt-3.3/include", "PBS_O_WORKDIR=/home/nbut3013", "SINGULARITY_COMMAND=run", "NCPUS=2", "USER_PATH=/usr/local/singularity"..., "USER=nbut3013", "PBS_TASKNUM=1", "LS_COLORS=rs=0:di=38;5;27:ln=38;"..., "LD_LIBRARY_PATH=/.singularity.d/"..., "PBS_O_HOME=/home/nbut3013", "SINGULARITY_NAME=matlab-ubu.img", "PBS_MOMPORT=15003", "PBS_O_QUEUE=defaultQ", "PBS_O_LOGNAME=nbut3013", "PATH=/home/nbut3013/anaconda2/bi"..., "MODULE_VERSION=3.2.10", "MAIL=/var/spool/mail/nbut3013", "PBS_O_LANG=en_AU.UTF-8", "PBS_JOBCOOKIE=0000000038FCE62400"..., "PWD=/project/RDS-CORE-SIHnextgen"..., "_LMFILES_=/usr/local/Modules/mod"..., "PBS_NODENUM=0", "LANG=en_US.UTF-8", "MODULEPATH=/usr/local/Modules/ve"..., "TZ=Etc/UTC", "PBS_JOBDIR=/home/nbut3013", "LOADEDMODULES=singularity/3.7.0", "SINGULARITY_ENVIRONMENT=/.singul"..., "PS1=Singularity> ", "PBS_O_SHELL=/bin/bash", "SINGULARITY_BIND=", "PBS_JOBID=6846183.pbsserver", "HISTCONTROL=ignoredups", "SHLVL=2", "HOME=/home/nbut3013", "PBS_O_HOST=login3.hpc.sydney.edu"..., "LOGNAME=nbut3013", "QTLIB=/usr/lib64/qt-3.3/lib", "CVS_RSH=ssh", "PBS_QUEUE=interactive", "MODULESHOME=/usr/local/Modules/3"..., "PBS_O_MAIL=/var/spool/mail/nbut3"..., "OMP_NUM_THREADS=2", "LESSOPEN=||/usr/bin/lesspipe.sh "..., "SINGULARITY_CONTAINER=/project/S"..., "BASH_FUNC_module()=() {  eval `/"..., "PBS_O_SYSTEM=Linux", "PBS_NODEFILE=/var/spool/PBS/aux/"..., "G_BROKEN_FILENAMES=1", "PBS_O_PATH=/home/nbut3013/anacon"..., "_=/usr/bin/strace"]) = 0
brk(NULL)                               = 0x5d3000
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
readlink("/proc/self/exe", "/opt/matlab/bin/glnxa64/MATLAB", 4096) = 30
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
open("/opt/matlab/bin/glnxa64/tls/x86_64/libmwi18n.so", O_RDONLY|O_CLOEXEC) = -1 ENOENT (No such file or directory)
stat("/opt/matlab/bin/glnxa64/tls/x86_64", 0x7ffff310fcb0) = -1 ENOENT (No such file or directory)
open("/opt/matlab/bin/glnxa64/tls/libmwi18n.so", O_RDONLY|O_CLOEXEC) = -1 ENOENT (No such file or directory)
stat("/opt/matlab/bin/glnxa64/tls", 0x7ffff310fcb0) = -1 ENOENT (No such file or directory)
open("/opt/matlab/bin/glnxa64/x86_64/libmwi18n.so", O_RDONLY|O_CLOEXEC) = -1 ENOENT (No such file or directory)
stat("/opt/matlab/bin/glnxa64/x86_64", 0x7ffff310fcb0) = -1 ENOENT (No such file or directory)
...
3000 lines truncated
```


## ltrace
Intercepts and records the dynamic library calls which are called by the executed process and the signals which are received by that process.  It can also intercept and print the system calls executed by the program.

```
user@host$ ltrace matlab
memcpy(0x7ffcc608fc70, "int8", 4)                = 0x7ffcc608fc70
memcpy(0x990c50, "int8", 4)                      = 0x990c50
memcpy(0x7ffcc608fc70, "int16", 5)               = 0x7ffcc608fc70
memcpy(0x7ffcc608fc70, "int16", 5)               = 0x7ffcc608fc70
memcpy(0x990ca0, "int16", 5)                     = 0x990ca0
memcpy(0x7ffcc608fc70, "int32", 5)               = 0x7ffcc608fc70
memcpy(0x7ffcc608fc70, "int32", 5)               = 0x7ffcc608fc70
memcpy(0x990cf0, "int32", 5)                     = 0x990cf0
memcpy(0x7ffcc608fc70, "int64", 5)               = 0x7ffcc608fc70
memcpy(0x7ffcc608fc70, "int64", 5)               = 0x7ffcc608fc70
memcpy(0x990d40, "int64", 5)                     = 0x990d40
memcpy(0x7ffcc608fc70, "uint8", 5)               = 0x7ffcc608fc70
```


