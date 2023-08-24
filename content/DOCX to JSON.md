Title: How to turn MS Word DOCX into JSON
Date: 2020-07-14
Author: Henry Lydecker
Category: Python
Tags: Python, Word, JSON

# Turn DOCX files into JSON

Do you have some Microsoft Word documents in DOCX format, but for some reason you'd like to work with JSON files? Well you are in luck! You can fairly easily convert a DOCX file into JSON.

## DOCX, aka Office Open XML

When people think of DOCX files, they usually just imagine files that look like formatted text files. However, this processed and formatted text document is actually the result of a recipe for constructing and formatting the document that is stored within DOCX. A DOCX is actually a zipped XML file: the XML file contains all of the actual text content as well as all the information needed for formatting and structuring the documents that we look at in Microsoft Word.

If you are familiar with XML and/or JSON, it should then come as no surprise that there are numerous options for converting back and forth between these two formats.

## Conversion workflow

Converting from DOCX to JSON is simple. The Python utility simplify-docx provides this functionality through the simplify function.
```
# Setup
import docx
import json
from simplify_docx import simplify
from  collections import OrderedDict

# Load source DOCX file
doc_test = docx.Document(insert_docx_file_here)
doc_test_json = simplify(doc_test)
with open('doc_test_json.json', 'w', encoding='utf-8') as f:
    json.dump(doc_test_json, f, ensure_ascii=False, indent=4)
```
And that's it! Easy right?

What does this export look like? We can loop through the objects and print it out to have a look.

```
for key, value in doc_test_clean.items():
    print(key, value)
```

```
TYPE document
VALUE [{'TYPE': 'body', 'VALUE': [{'TYPE': 'paragraph', 'VALUE': [{'TYPE': 'text', 'VALUE': 'JBRA Assisted Reproduction 2016;20(1):08-12 doi: 10.5935/1518-0557.20160003'}], 'style': {'indent': {'TYPE': 'CT_Ind', 'left': 127, 'right': 17, 'firstLine': 0}}}, {'TYPE': 'paragraph', 'VALUE': [{'TYPE': 'text', 'VALUE': 'Original Article'}], 'style': {'indent': {'TYPE': 'CT_Ind', 'left': 127, 'right': 0, 'firstLine': 0}}}, {'TYPE': 'paragraph', 'VALUE': [{'TYPE': 'text', 'VALUE': 'Strategies for the management of OHSS: Results from freezing-all cycles'}],
```
That doesn't look particularly easy to read. But we can see here that we have a JSON with numerous objects that contain text information and style information.

## Manipulating your DOCX JSON

Ok so you have a JSON now, but what if you want to remove certain parts of it? For example, what if you want to remove all tables from your document? You can loop through the objects in your JSON and make changes based on the identity of the objects.

```
# Open your JSON
doc_test_clean = json.load(open("doc_test_json.json"), object_pairs_hook=OrderedDict)
    
# Prune those tables
for i in range(len(doc_test_clean)):
    if doc_test_clean[i]["TYPE"] == "table":
        doc_test_clean.pop(i)
        break
# Save the output JSON
with open('doc_test_clean.json', 'w', encoding='utf-8') as f:
    json.dump(doc_test_clean, f, ensure_ascii=False, indent=4)
```

## Results

Here is what you get once you've converted your DOCX into a JSON. We can see that our DOCX-JSON is a "document" built from multiple different sections (e.g. "body"), that are composed of numerous paragraph/style pairs. 

```
{
    "TYPE": "document",
    "VALUE": [
        {
            "TYPE": "body",
            "VALUE": [
                {
                    "TYPE": "paragraph",
                    "VALUE": [
                        {
                            "TYPE": "text",
                            "VALUE": "JBRA Assisted Reproduction 2016;20(1):08-12 doi: 10.5935/1518-0557.20160003"
                        }
                    ],
                    "style": {
                        "indent": {
                            "TYPE": "CT_Ind",
                            "left": 127,
                            "right": 17,
                            "firstLine": 0
                        }
                    }
                },
                {
                    "TYPE": "paragraph",
                    "VALUE": [
                        {
                            "TYPE": "text",
                            "VALUE": "Original Article"
                        }
                    ],
                    "style": {
                        "indent": {
                            "TYPE": "CT_Ind",
                            "left": 127,
                            "right": 0,
                            "firstLine": 0
                        }
                    }
                },
                {
                    "TYPE": "paragraph",
                    "VALUE": [
                        {
                            "TYPE": "text",
                            "VALUE": "Strategies for the management of OHSS: Results from freezing-all cycles"
                        }
                    ],
                    "style": {
                        "indent": {
                            "TYPE": "CT_Ind",
                            "left": 123,
                            "right": 30,
                            "firstLine": 0
                        }
                    }
                }
                ]}]}
```

# "Uh, why would I want to do this?"

That is a good question that I don't have a good answer for. I originally found this method when I was trying to do some cleaning of DOCX XML files. It is pretty easy to work with the XML files inside of DOCX files, but I guess there are cases where you might prefer to work with JSON files. In that case, you now know how to turn your DOCX into JSON!
