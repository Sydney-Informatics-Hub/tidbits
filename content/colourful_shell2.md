title: Add some colour to your shell: cool stuff with themes
author: Henry Lydecker
date: 2020-10-02
Category: Misc
Tags: shell,terminal,zsh

** Introduction

When working with multiple shell windows, some on a local machine and others on remote, wouldn't it be nice if you could instantly tell which was which just by looking at them?
You are in luck; there are numerous options for automatic theme switching when you use ssh.

## Simple option: MacOS terminal options

It is really easy to make your terminal change theme when you ssh. 
Go to your terminal preferences, then go to the profiles tab.
Create a new theme called "ssh", and set it to whatever colours you want.

Now that you have an ssh theme, create a new command (shift+command+n) and paste in `ssh user1234@your.remote.server.com`.
Whenever you want to connect to your remote server, you can just hit shift+command+n and hit enter.
This will open up a new terminal window connected to your remote server, using your ssh theme!

This functionality is super easy to set up and can make it a lot easier to work with shell on local and remote at the same time.
This is particularly useful when working with HPC.

## More complex: iTerm and theme switching via scripts

You can also set up automatic theme switching within the same window with some more advanced scripting.
There are many options out there on stack threads for doing this with iTerm.
I stick with using the default Terminal, however if you are an iTerm user these may be an even better option!
