# PPP-QuestionParsing-Grammatical

Question Parsing module for the PPP using a grammatical approach.

[![Build Status](https://scrutinizer-ci.com/g/ProjetPP/PPP-QuestionParsing-Grammatical/badges/build.png?b=master)](https://scrutinizer-ci.com/g/ProjetPP/PPP-QuestionParsing-Grammatical/build-status/master)
[![Code Coverage](https://scrutinizer-ci.com/g/ProjetPP/PPP-QuestionParsing-Grammatical/badges/coverage.png?b=master)](https://scrutinizer-ci.com/g/ProjetPP/PPP-QuestionParsing-Grammatical/?branch=master)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/ProjetPP/PPP-QuestionParsing-Grammatical/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/ProjetPP/PPP-QuestionParsing-Grammatical/?branch=master)

## Introduction

The purpose of this Question Parsing module is to transform questions into trees of triples, as described into [our datamodel](https://github.com/ProjetPP/Documentation/blob/master/data-model.md), which can be handled by backend modules. 

For instance, we aim at producing the triple `(Rwanda,president,?)` from the question `Who is the president of Rwanda?`. The formal representation of this triple is:
```
{
    "type": "triple",
    "subject": {
        "value": "Rwanda",
        "type": "resource"
    },
    "predicate": {
        "value": "president",
        "type": "resource"
    }
    "object": {
        "type": "missing"
    },
}
```

See [our website](http://projetpp.github.io/) to learn more about our project and [test our question answering tool](http://askplatyp.us/).

## How to install

With a recent version of pip:

```bash
pip3 install git+https://github.com/ProjetPP/PPP-QuestionParsing-Grammatical.git
```

With an older one:

```bash
git clone https://github.com/ProjetPP/PPP-QuestionParsing-Grammatical.git
cd PPP-QuestionParsing-Grammatical
python3 setup.py install
```

Use the `--user` option if you want to install it only for the current user.

You can install the main dependencies (especially CoreNLP) using the script file `bootstrap_corenlp.sh` from https://github.com/ProjetPP/Scripts (run `bash bootstrap_corenlp.sh`).

## How to test

The `demo` folder contains some demo files and a readme `README.md` that explains how to use them.

## Overview of the main folders

* `ppp_questionparsing_grammatical/`: main code of the project
* `demo/`: demo files to test the algorithms
* `nounification/`: scripts used to compute the nounification database
* `deep_tests/` and `tests/`: unit tests of the project
* `documentation/`: some files that expose our current thinking on the project (mainly drafts)
