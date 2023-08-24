title: Setting up SSH for an easy login to VMs etc
author: Joel Nothman
date: 2021-03-03
Category: Misc
Tags: shell,vms,hosting,ssh

Make it easier to SSH into your VMs.

## You shouldn't need to enter your username

```sh
$ mkdir -p ~/.ssh   # make sure you have an SSH config directory
$ cat >> ~/.ssh/config << EOF

Host *.sydney.edu.au
    User <PUT-YOUR-UNIKEY-HERE>
EOF
```

This add some lines to `~/.ssh/config`, that tell `ssh` that if you try to login to a machine whose name ends with
.sydney.edu.au, it should not use your current `$USER` name, but should use the value inserted in `<PUT-YOUR-UNIKEY-HERE>` above.

Now try:

```sh
$ ssh research-data-int.sydney.edu.au
```

## You shouldn't need to enter a password

If you do not have a private key set up on your current machine (check `ls
~/.ssh/id_*` for files not ending `.pub`), use:

```sh
$ ssh-keygen -t rsa
```

Once you have a private key set up, you can copy your public key to the VM,
which should be the last time you enter your password for that VM:

```sh
$ ssh-copy-id <PUT-THE-VM-HOSTNAME-HERE>
```

SECURITY WARNING: think carefully about putting a private key on a machine that others have sudo powers on. It's giving them the keys to wherever the corresponding public key exists.

## You shouldn't need to remember the VM name

If you prefer an alias to writing out the full VM name, you can make another entry in `~/.ssh/config`:

```sh
$ cat >> ~/.ssh/config << EOF

Host <ALIAS>
    User <PUT-YOUR-UNIKEY-HERE>
    HostName <PUT-THE-VM-HOSTNAME-HERE>.srv.sydney.edu.au
EOF 
```

This applies only to `ssh` (and `scp`, `sftp`, etc.), making `<ALIAS>` a shorthand for login into `<PUT-THE-VM-HOSTNAME-HERE>.srv.sydney.edu.au`.

For example, this might be a useful addition to `~/.ssh/config`:

```
Host hpc
    User wxyz1234
    HostName hpc.sydney.edu.au

Host rds
    User wxyz1234
    HostName research-data-int.sydney.edu.au
```
