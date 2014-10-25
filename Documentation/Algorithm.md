Here is a presentation of a (possible) algorithm. See IDEAS.md for other information (and a "outdated" proposition of algorithm in section 3).

### Preprocessing

1. Identify and remove (from the tree) the question word
2. Merge via Name Entity Recognition (NER) (LOCATION, PERSON...)
3. Merge quotation (with a "QUOTA" NER identifier), ex: Who is the author of "Twenty Thousand Leagues Under the Sea"? -> "Twenty Thousand Leagues Under the Sea" is merged in a single node
4. Merge words in capital letters that are neighbors in the tree

Two restrictions are necessaries in a first time:
  - be case-sensitive. It simplifies a lot of things (and the stanford parser is case sensitive...). 
  - only process questions that start by a question word

### Tree simplification

5. See Hierarchy_analysis.md for the restricted set of dependencies to use and the transformations to perform.

### Triples production

6. Produce the triple(s) involved by the question word
7. Add the triples involved by other parts of the tree

A better description of steps 6 and 7 is provided in Hierarchy_analysis.md


