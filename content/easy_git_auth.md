title: Use git on VMs easily and securely with SSH agent forwarding
author: Marius Mather
date: 2022-10-04
Category: misc
Tags: git, ssh

If you use git repos on a VM (or other remote server),
you'll know the pain of entering your login details
whenever you need to pull down new code.

To avoid this, you can use **SSH agent forwarding**
to use your local SSH keys in a remote session.
If you're already using SSH to log in to the server,
you just need to add the `-A` option to your SSH
command, like:

```shell
ssh -A username@host
```

With SSH forwarding:

* You don't have to enter your username/password repeatedly on
  the remote server.
* You don't have to copy SSH keys to the server, which might
  create security issues.

On the server, you need to use the SSH version
of the repo's URL, e.g. `git@github.com:USERNAME/REPOSITORY.git`.
If you're currently using the HTTPS version you can
switch with:

```shell
git remote set-url git@github.com:USERNAME/REPOSITORY.git
```

If you're just starting out with SSH and git and don't understand the above, 
[GitHub has good documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account) on
how to get set up with it.