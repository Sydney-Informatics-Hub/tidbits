Title: Useful Mac OS tips
Date: 2020-03-09
Author: Joel Nothman
Category: Misc
Tags: macos

# Some favourite keyboard shortcuts:

* Switch tabs: `⌘-shift-[` and `⌘-shift-]` ; Close tab: `⌘-w`
* Open Spotlight to search for things: `⌘-space`
* Once you’ve found something in Spotlight, use `⌘-click` to open its containing folder
* Screen capture `⌘-ctrl-shift-4`: allows you to select a rectangle, which will then be available in clipboard (paste straight into email or save by opening Preview and `⌘-n`)
* Switch Application: `⌘-tab` (hold `⌘` to select)
* Switch Window within application: `⌘-~`
* Page up/down/home/end: `Fn-up/down/left/right`

# Command-line tips

* Use `open` to open an app, or to open a file
* Use `pbcopy` to dump the output of a command to the clipboard
* Use `pbpaste` to dump the clipboard to standard output (for piping into a program or a file)
* Drag files into the command-line to get their path (see below)

# Some other neat things:

* An icon in the status bar like ![]({attach}images/mac_tips/word_doc.png) or ![]({attach}images/mac_tips/folder.png) can be dragged (yes, even a file you have open in word).
    * Drag it into your Terminal app to get the path to that file.
    * Drag it into your email to attach it.
    * Drag it into your web browser to upload it (in some contexts).
    * This one’s pretty cool: drag it into a Save As or Open dialog (where you get to select a file) to go to the file’s directory!
    * You may want to use `⌘-tab` and `⌘-~`to navigate to the destination window while dragging.
* The icon next to the URL in your browser – such as the padlock here ![]({attach}images/mac_tips/padlock.png) – can also be dragged, so you can insert the web address in your terminal or email.
* Install [ITerm2](https://www.iterm2.com/) and install its shell integration. Among other things it gives you a status bar showing you what processes 
  are running in that shell, the git branch / status, etc.
* Is Time Machine backup taking too long? Open terminal and enter `sudo sysctl debug.lowpri\_throttle_enabled=0` to speed up the process.
 
