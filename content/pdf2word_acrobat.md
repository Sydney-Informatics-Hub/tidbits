Title: Adobe Acrobat Pro DC for PDF text extraction
Date: 2020-03-05
Author: Henry Lydecker
Category: Misc
Tags: pdf,text,adobe
Summary: Extract text from PDF files

While there are many options for extracting text from PDFs using R and
Python, at the end of the day Adobe rightly knows best about how to
extract text from PDFs. You can very easily do this with individual pdf
files using the Adobe Acrobat GUI. In order to do this automatically on
batches of files, you used to be able to call on Acrobat functions using
the shell/terminal. Unfortunately it seems that Adobe has closed off
much of this functionality (and in fact it is now agains the terms of
service).

Thankfully all is not lost: there is an Adobe approved way to batch
process pdfs: **Action Wizard**. Action Wizard sounds like something out
of Dungeons and Dragons, but it is actually a somewhat difficult to find
tool within Adobe Acrobat for performing a wide range of processes.

Finding and using the Action Wizard
===================================

By default, you likely will not see the action wizard. Here is how to
find it:

1.  Open Adobe Acrobat Pro DC. You should see the option to select the
    “Tools” tab. Click on that.
    
    ![]({attach}images/pdf2word/Screen Shot 2020-03-05 at 12.11.20 pm.png)
    
2.  You should now see tab with a bunch of different tools. Scroll down,
    or type “action wizard” into the search bar to find the wizard. Add
    the wizard to your tools.
    
    ![]({attach}images/pdf2word/Screen Shot 2020-03-05 at 12.12.48 pm.png)
    
3.  Now that you have added the wizard to your tools, click on it and
    check out all of the options that you have. Import options to note:
    Manage actions lets you…manage the actions that you have available.
    You can use this to import, enable, edit, and export actions. The
    more actions button takes to Adobe’s action exchange website.
    
    ![]({attach}images/pdf2word/Screen Shot 2020-03-05 at 12.13.22 pm.png)

Action Wizard Plugins
=====================

Action Wizard has support for building your own plugins, as well as
importing plugins that have been made by others. You can view available
plugins on Adobe’s action Exchange:

<a href="https://acrobatusers.com/actions-exchange/index.html" class="uri">https://acrobatusers.com/actions-exchange/index.html</a>

PDF to Word
-----------

Lo and behold, I found a plugin on the actions exchange that lets you
batch process and save PDF files as Word files.

![<a href="https://acrobatusers.com/actions-exchange/index.html"> This
is where you find it on the actions
exchange</a>]({attach}images/pdf2word/Screen Shot 2020-03-05 at 9.33.43 am.png)

After downloading the action, you need to import it. This is pretty easy
to figure out by clicking on manage actions. Here’s an image of what to
do just in case.

![]({attach}images/pdf2word/Screen Shot 2020-03-05 at 12.23.14 pm.png)

When run on a folder containing subfolders, the plugin functions
recursively and will read and convert all pdfs contained within the sub
folders. I ran this plugin on a set of ~900 PDFs of scientific papers,
and it took ~50 minutes to process these into .docx.

![Ew.]({attach}images/pdf2word/Screen Shot 2020-03-05 at 12.30.14 pm.png)

When I opened up one of these in Word, I saw that Acrobat has managed to
perfectly replicate the PDF’s format in Word…which is not particularly
useful. I got started writing a Visual Basic macro for saving as .txt
when I stopped and thought: why not try to customize the plugin itself!

PDF to whatever you want
------------------------

Thankfully, it is very easy to edit plugins in Action Wizard. To do
this, go back to Manage Actions, select the action you want to edit, and
then click edit. There are heaps of options here; for now we are just
interested in adjusting the options for the file saving step of this
action.

![]({attach}images/pdf2word/Screen Shot 2020-03-05 at 11.06.31 am.png)

After clicking save, the plugin is now primed to save PDF files as
whatever format you want. From experimenting with .txt and .rtf files, I
found that .rtf does the best job at converting files with multiple
columns into one sensible column of text. When this is running, it takes
in between 1 and 3 seconds to process each PDF into .rtf.

![Multiple columns have been turned into one sensible column, and the
footer stuff has been put somewhere
reasonable.]({attach}images/pdf2word/Screen Shot 2020-03-05 at 12.33.39 pm.png)

Conclusion
----------

Need to do something with PDF files? Actions in Adobe Acrobat may end up
being the best option for you. There are loads of pre-built actions on
the actions exchange, and Adobe has loads of built in options for
building or editing actions. You can also write actions in javascript if
you feel like it!
