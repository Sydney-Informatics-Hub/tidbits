title: Find github pages
author: Nathaniel Butterworth
date: 2023-04-30
Category: git
Tags: git,github

To gauge how many github repos have a "github pages" within a particular an organisation, you can run:
```bash
gh api -H "Accept: application/vnd.github+json" /orgs/Sydney-Informatics-Hub/repos --jq '.[] | {name: .name, has_pages}' --paginate | grep true
```

This returns output like:
```
{"has_pages":true,"name":"training.artemis.introhpc"}
{"has_pages":true,"name":"training.artemis"}
{"has_pages":true,"name":"training.home"}
{"has_pages":true,"name":"workshopbmc"}
{"has_pages":true,"name":"lessonbmc"}
{"has_pages":true,"name":"2018_12_10_GISworkshop"}
{"has_pages":true,"name":"training.artemis.interhpc"}
{"has_pages":true,"name":"training-template-old"}
{"has_pages":true,"name":"training.artemis.gpu"}
{"has_pages":true,"name":"190318_MLR"}
{"has_pages":true,"name":"training-RNAseq"}
{"has_pages":true,"name":"190408_MLpy"}
{"has_pages":true,"name":"training-RNAseq-slides"}
{"has_pages":true,"name":"training.artemis.rds"}
{"has_pages":true,"name":"codeofconduct"}
{"has_pages":true,"name":"training.artemis.python"}
{"has_pages":true,"name":"lessons-mlpy"}
{"has_pages":true,"name":"elfr"}
{"has_pages":true,"name":"recocam"}
{"has_pages":true,"name":"training.artemis.r"}
{"has_pages":true,"name":"geopython"}
{"has_pages":true,"name":"simplelesson"}
{"has_pages":true,"name":"training.gadi.intro"}
{"has_pages":true,"name":"jenkins_docker_test"}
{"has_pages":true,"name":"training.argus.gpu"}
{"has_pages":true,"name":"training.blockchain"}
{"has_pages":true,"name":"geopython-bhp"}
{"has_pages":true,"name":"stats-resources"}
{"has_pages":true,"name":"geopython-pawsey"}
{"has_pages":true,"name":"BioCommons_RNASeq_dryRun"}
{"has_pages":true,"name":"training-template"}
{"has_pages":true,"name":"intro-git"}
{"has_pages":true,"name":"AgReFed-Workshop"}
{"has_pages":true,"name":"rna-seq-pt2-quarto"}
{"has_pages":true,"name":"rna-seq-pt1-quarto"}
{"has_pages":true,"name":"training.RNAseq.series-quarto"}
{"has_pages":true,"name":"dataharvester"}
{"has_pages":true,"name":"ParallelPython"}
{"has_pages":true,"name":"geodata-harvester"}
{"has_pages":true,"name":"PIPE-3034-obesity2"}
{"has_pages":true,"name":"customising-nfcore-workshop"}
{"has_pages":true,"name":"masterclass_RStudio_GitHub"}
{"has_pages":true,"name":"RStudio_github_versioncontrol"}
{"has_pages":true,"name":"lessons_mlr_tidymodels"}
{"has_pages":true,"name":"Git_RStudio_masterclass"}
```
