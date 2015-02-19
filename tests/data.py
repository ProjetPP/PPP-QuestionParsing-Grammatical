from ppp_questionparsing_grammatical import computeTree, simplify, preprocessingMerge, DependenciesTree, normalFormProduction

# Parsing result of "John Smith lives in the United Kingdom."
def give_john_smith():
    return  {'sentences': [{'dependencies': [['root', 'ROOT', 'lives'],
                ['nn', 'Smith', 'John'],
                ['nsubj', 'lives', 'Smith'],
                ['det', 'Kingdom', 'the'],
                ['nn', 'Kingdom', 'United'],
                ['prep_in', 'lives', 'Kingdom']],
               'indexeddependencies': [['root', 'ROOT-0', 'lives-3'],
                ['nn', 'Smith-2', 'John-1'],
                ['nsubj', 'lives-3', 'Smith-2'],
                ['det', 'Kingdom-7', 'the-5'],
                ['nn', 'Kingdom-7', 'United-6'],
                ['prep_in', 'lives-3', 'Kingdom-7']],
               'parsetree': '(ROOT (S (NP (NNP John) (NNP Smith)) (VP (VBZ lives) (PP (IN in) (NP (DT the) (NNP United) (NNP Kingdom)))) (. .)))',
               'text': 'John Smith lives in the United Kingdom.',
               'words': [['John',
                 {'CharacterOffsetBegin': '0',
                  'CharacterOffsetEnd': '4',
                  'Lemma': 'John',
                  'NamedEntityTag': 'PERSON',
                  'PartOfSpeech': 'NNP'}],
                ['Smith',
                 {'CharacterOffsetBegin': '5',
                  'CharacterOffsetEnd': '10',
                  'Lemma': 'Smith',
                  'NamedEntityTag': 'PERSON',
                  'PartOfSpeech': 'NNP'}],
                ['lives',
                 {'CharacterOffsetBegin': '11',
                  'CharacterOffsetEnd': '16',
                  'Lemma': 'live',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'VBZ'}],
                ['in',
                 {'CharacterOffsetBegin': '17',
                  'CharacterOffsetEnd': '19',
                  'Lemma': 'in',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'IN'}],
                ['the',
                 {'CharacterOffsetBegin': '20',
                  'CharacterOffsetEnd': '23',
                  'Lemma': 'the',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'DT'}],
                ['United',
                 {'CharacterOffsetBegin': '24',
                  'CharacterOffsetEnd': '30',
                  'Lemma': 'United',
                  'NamedEntityTag': 'LOCATION',
                  'PartOfSpeech': 'NNP'}],
                ['Kingdom',
                 {'CharacterOffsetBegin': '31',
                  'CharacterOffsetEnd': '38',
                  'Lemma': 'Kingdom',
                  'NamedEntityTag': 'LOCATION',
                  'PartOfSpeech': 'NNP'}],
                ['.',
                 {'CharacterOffsetBegin': '38',
                  'CharacterOffsetEnd': '39',
                  'Lemma': '.',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': '.'}]]}]}

# Dot representation of the tree for "John Smith lives in the United Kingdom."
def give_john_smith_string():
    s="digraph relations {\n"
    s+="\t\"6\"[label=\"ROOT\",shape=box];\n"
    s+="\t\"6\" -> \"5\"[label=\"root\"];\n"
    s+="\t\"5\"[label=\"lives\",shape=box];\n"
    s+="\t\"5\" -> \"1\"[label=\"nsubj\"];\n"
    s+="\t\"5\" -> \"4\"[label=\"prep_in\"];\n"
    s+="\t\"1\"[label=\"Smith [PERSON]\",shape=box];\n"
    s+="\t\"1\" -> \"0\"[label=\"nn\"];\n"
    s+="\t\"0\"[label=\"John [PERSON]\",shape=box];\n"
    s+="\t\"4\"[label=\"Kingdom [LOCATION]\",shape=box];\n"
    s+="\t\"4\" -> \"2\"[label=\"det\"];\n"
    s+="\t\"4\" -> \"3\"[label=\"nn\"];\n"
    s+="\t\"2\"[label=\"the\",shape=box];\n"
    s+="\t\"3\"[label=\"United [LOCATION]\",shape=box];\n"
    s+="\tlabelloc=\"t\"\tlabel=\"John Smith lives in the United Kingdom.\";\n"
    s+="}"
    return s

# Dot representation of the tree for "John Smith lives in the United Kingdom." (prepocessing merge)
def give_john_smith_stringMerge():
    s="digraph relations {\n"
    s+="\t\"4\"[label=\"ROOT\",shape=box];\n"
    s+="\t\"4\" -> \"3\"[label=\"root\"];\n"
    s+="\t\"3\"[label=\"lives in\",shape=box];\n"
    s+="\t\"3\" -> \"0\"[label=\"nsubj\"];\n"
    s+="\t\"3\" -> \"2\"[label=\"prep\"];\n"
    s+="\t\"0\"[label=\"John Smith [PERSON]\",shape=box];\n"
    s+="\t\"2\"[label=\"United Kingdom [LOCATION]\",shape=box];\n"
    s+="\t\"2\" -> \"1\"[label=\"det\"];\n"
    s+="\t\"1\"[label=\"the\",shape=box];\n"
    s+="\tlabelloc=\"t\"\tlabel=\"John Smith lives in the United Kingdom.\";\n"
    s+="}"
    return s

# Parse result of "Who wrote foo0 and foo1?"
def give_LSD_LIB():
    return  {'sentences': [{'dependencies': [['root', 'ROOT', 'wrote'],
                ['nsubj', 'wrote', 'Who'],
                ['dobj', 'wrote', 'foo0'],
                ['conj_and', 'foo0', 'foo1']],
               'indexeddependencies': [['root', 'ROOT-0', 'wrote-2'],
                ['nsubj', 'wrote-2', 'Who-1'],
                ['dobj', 'wrote-2', 'foo0-3'],
                ['conj_and', 'foo0-3', 'foo1-5']],
               'parsetree': '(ROOT (SBARQ (WHNP (WP Who)) (SQ (VP (VBD wrote) (NP (NN foo0) (CC and) (NN foo1)))) (. ?)))',
               'text': 'Who wrote foo0 and foo1?',
               'words': [['Who',
                 {'CharacterOffsetBegin': '0',
                  'CharacterOffsetEnd': '3',
                  'Lemma': 'who',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'WP'}],
                ['wrote',
                 {'CharacterOffsetBegin': '4',
                  'CharacterOffsetEnd': '9',
                  'Lemma': 'write',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'VBD'}],
                ['foo0',
                 {'CharacterOffsetBegin': '10',
                  'CharacterOffsetEnd': '14',
                  'Lemma': 'foo0',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'NN'}],
                ['and',
                 {'CharacterOffsetBegin': '15',
                  'CharacterOffsetEnd': '18',
                  'Lemma': 'and',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'CC'}],
                ['foo1',
                 {'CharacterOffsetBegin': '19',
                  'CharacterOffsetEnd': '23',
                  'Lemma': 'foo1',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'NN'}],
                ['?',
                 {'CharacterOffsetBegin': '23',
                  'CharacterOffsetEnd': '24',
                  'Lemma': '?',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': '.'}]]}]}

# Parse result of "Obama is the United States president."
def give_obama_president_usa():
    return  {'coref': [[[['the United States president', 0, 5, 2, 6],
                ['Obama', 0, 0, 0, 1]]]],
             'sentences': [{'dependencies': [['root', 'ROOT', 'is'],
                ['nsubj', 'is', 'Obama'],
                ['det', 'president', 'the'],
                ['nn', 'president', 'United'],
                ['nn', 'president', 'States'],
                ['xcomp', 'is', 'president']],
               'indexeddependencies': [['root', 'ROOT-0', 'is-2'],
                ['nsubj', 'is-2', 'Obama-1'],
                ['det', 'president-6', 'the-3'],
                ['nn', 'president-6', 'United-4'],
                ['nn', 'president-6', 'States-5'],
                ['xcomp', 'is-2', 'president-6']],
               'parsetree': '(ROOT (S (NP (NNP Obama)) (VP (VBZ is) (NP (DT the) (NNP United) (NNPS States) (NN president))) (. .)))',
               'text': 'Obama is the United States president.',
               'words': [['Obama',
                 {'CharacterOffsetBegin': '0',
                  'CharacterOffsetEnd': '5',
                  'Lemma': 'Obama',
                  'NamedEntityTag': 'PERSON',
                  'PartOfSpeech': 'NNP'}],
                ['is',
                 {'CharacterOffsetBegin': '6',
                  'CharacterOffsetEnd': '8',
                  'Lemma': 'be',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'VBZ'}],
                ['the',
                 {'CharacterOffsetBegin': '9',
                  'CharacterOffsetEnd': '12',
                  'Lemma': 'the',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'DT'}],
                ['United',
                 {'CharacterOffsetBegin': '13',
                  'CharacterOffsetEnd': '19',
                  'Lemma': 'United',
                  'NamedEntityTag': 'LOCATION',
                  'PartOfSpeech': 'NNP'}],
                ['States',
                 {'CharacterOffsetBegin': '20',
                  'CharacterOffsetEnd': '26',
                  'Lemma': 'States',
                  'NamedEntityTag': 'LOCATION',
                  'PartOfSpeech': 'NNPS'}],
                ['president',
                 {'CharacterOffsetBegin': '27',
                  'CharacterOffsetEnd': '36',
                  'Lemma': 'president',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'NN'}],
                ['.',
                 {'CharacterOffsetBegin': '36',
                  'CharacterOffsetEnd': '37',
                  'Lemma': '.',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': '.'}]]}]}

# Parsing result of "How old are there?"
def give_how_old():
    return  {'sentences': [{'dependencies': [['root', 'ROOT', 'are'],
                ['advmod', 'old', 'How'],
                ['dep', 'are', 'old'],
                ['expl', 'are', 'there']],
               'indexeddependencies': [['root', 'ROOT-0', 'are-3'],
                ['advmod', 'old-2', 'How-1'],
                ['dep', 'are-3', 'old-2'],
                ['expl', 'are-3', 'there-4']],
               'parsetree': '(ROOT (SBARQ (WHADJP (WRB How) (JJ old)) (SQ (VBP are) (NP (EX there))) (. ?)))',
               'text': 'How old are there?',
               'words': [['How',
                 {'CharacterOffsetBegin': '0',
                  'CharacterOffsetEnd': '3',
                  'Lemma': 'how',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'WRB'}],
                ['old',
                 {'CharacterOffsetBegin': '4',
                  'CharacterOffsetEnd': '7',
                  'Lemma': 'old',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'JJ'}],
                ['are',
                 {'CharacterOffsetBegin': '8',
                  'CharacterOffsetEnd': '11',
                  'Lemma': 'be',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'VBP'}],
                ['there',
                 {'CharacterOffsetBegin': '12',
                  'CharacterOffsetEnd': '17',
                  'Lemma': 'there',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'EX'}],
                ['?',
                 {'CharacterOffsetBegin': '17',
                  'CharacterOffsetEnd': '18',
                  'Lemma': '?',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': '.'}]]}]}

# Parsing result of "Who is the United States president?"
def give_USA_president():
    return  {'sentences': [{'dependencies': [['root', 'ROOT', 'is'],
                ['dep', 'is', 'Who'],
                ['det', 'president', 'the'],
                ['nn', 'president', 'United'],
                ['nn', 'president', 'States'],
                ['nsubj', 'is', 'president']],
               'indexeddependencies': [['root', 'ROOT-0', 'is-2'],
                ['dep', 'is-2', 'Who-1'],
                ['det', 'president-6', 'the-3'],
                ['nn', 'president-6', 'United-4'],
                ['nn', 'president-6', 'States-5'],
                ['nsubj', 'is-2', 'president-6']],
               'parsetree': '(ROOT (SBARQ (WHNP (WP Who)) (SQ (VBZ is) (NP (DT the) (NNP United) (NNPS States) (NN president))) (. ?)))',
               'text': 'Who is the United States president?',
               'words': [['Who',
                 {'CharacterOffsetBegin': '0',
                  'CharacterOffsetEnd': '3',
                  'Lemma': 'who',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'WP'}],
                ['is',
                 {'CharacterOffsetBegin': '4',
                  'CharacterOffsetEnd': '6',
                  'Lemma': 'be',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'VBZ'}],
                ['the',
                 {'CharacterOffsetBegin': '7',
                  'CharacterOffsetEnd': '10',
                  'Lemma': 'the',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'DT'}],
                ['United',
                 {'CharacterOffsetBegin': '11',
                  'CharacterOffsetEnd': '17',
                  'Lemma': 'United',
                  'NamedEntityTag': 'LOCATION',
                  'PartOfSpeech': 'NNP'}],
                ['States',
                 {'CharacterOffsetBegin': '18',
                  'CharacterOffsetEnd': '24',
                  'Lemma': 'States',
                  'NamedEntityTag': 'LOCATION',
                  'PartOfSpeech': 'NNPS'}],
                ['president',
                 {'CharacterOffsetBegin': '25',
                  'CharacterOffsetEnd': '34',
                  'Lemma': 'president',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'NN'}],
                ['?',
                 {'CharacterOffsetBegin': '34',
                  'CharacterOffsetEnd': '35',
                  'Lemma': '?',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': '.'}]]}]}

# Parsing result of "Who is the president of the United States?"
def give_president_of_USA():
    return  {'sentences': [{
  'words': [
    ['Who', 
      {'CharacterOffsetBegin': '0', 
       'PartOfSpeech': 'WP', 
       'Lemma': 'who', 
       'NamedEntityTag': 'O', 
       'CharacterOffsetEnd': '3'}], 
    ['is', 
      {'CharacterOffsetBegin': '4', 
       'PartOfSpeech': 'VBZ', 
       'Lemma': 'be', 
       'NamedEntityTag': 'O', 
       'CharacterOffsetEnd': '6'}], 
    ['the', 
      {'CharacterOffsetBegin': '7', 
       'PartOfSpeech': 'DT', 
       'Lemma': 'the', 
       'NamedEntityTag': 'O', 
       'CharacterOffsetEnd': '10'}], 
    ['president', 
      {'CharacterOffsetBegin': '11', 
       'PartOfSpeech': 'NN', 
       'Lemma': 'president', 
       'NamedEntityTag': 'O', 
       'CharacterOffsetEnd': '20'}], 
    ['of', 
      {'CharacterOffsetBegin': '21', 
       'PartOfSpeech': 'IN', 
       'Lemma': 'of', 
       'NamedEntityTag': 'O', 
       'CharacterOffsetEnd': '23'}], 
    ['the', 
      {'CharacterOffsetBegin': '24', 
       'PartOfSpeech': 'DT', 'Lemma': 
       'the', 'NamedEntityTag': 'O', 
       'CharacterOffsetEnd': '27'}], 
    ['United', 
      {'CharacterOffsetBegin': '28', 
       'PartOfSpeech': 'NNP', 
       'Lemma': 'United', 
       'NamedEntityTag': 'LOCATION', 
       'CharacterOffsetEnd': '34'}], 
    ['States', 
      {'CharacterOffsetBegin': '35', 
       'PartOfSpeech': 'NNPS', 
       'Lemma': 'States', 
       'NamedEntityTag': 'LOCATION', 
       'CharacterOffsetEnd': '41'}], 
    ['?', 
      {'CharacterOffsetBegin': '41', 
       'PartOfSpeech': '.', 
       'Lemma': '?', 
       'NamedEntityTag': 'O', 
       'CharacterOffsetEnd': '42'}]], 
  'text': 'Who is the president of the United States?', 
  'dependencies': [['root', 'ROOT', 'is'], ['dep', 'is', 'Who'], ['det', 'president', 'the'], ['nsubj', 'is', 'president'], ['det', 'States', 'the'], ['nn', 'States', 'United'], ['prep_of', 'president', 'States']], 
  'indexeddependencies': [['root', 'ROOT-0', 'is-2'], ['dep', 'is-2', 'Who-1'], ['det', 'president-4', 'the-3'], ['nsubj', 'is-2', 'president-4'], ['det', 'States-8', 'the-6'], ['nn', 'States-8', 'United-7'], ['prep_of', 'president-4', 'States-8']], 
  'parsetree': '(ROOT (SBARQ (WHNP (WP Who)) (SQ (VBZ is) (NP (NP (DT the) (NN president)) (PP (IN of) (NP (DT the) (NNP United) (NNPS States))))) (. ?)))'}]}

# Parsing result of "What was the first Gilbert and Sullivan opera?"
def give_opera():
    return  {'sentences': [{
  'words': [
    ['What', 
        {'PartOfSpeech': 'WP', 
         'NamedEntityTag': 'O', 
         'CharacterOffsetBegin': '0', 
         'Lemma': 'what', 
         'CharacterOffsetEnd': '4'}], 
    ['was', 
        {'PartOfSpeech': 'VBD', 
         'NamedEntityTag': 'O', 
         'CharacterOffsetBegin': '5', 
         'Lemma': 'be', 
         'CharacterOffsetEnd': '8'}], 
    ['the', 
        {'PartOfSpeech': 'DT', 
         'NamedEntityTag': 'O', 
         'CharacterOffsetBegin': '9', 
         'Lemma': 'the', 
         'CharacterOffsetEnd': '12'}], 
    ['first', 
        {'NamedEntityTag': 'ORDINAL', 
         'NormalizedNamedEntityTag': '1.0', 
         'CharacterOffsetEnd': '18', 
         'Lemma': 'first', 
         'CharacterOffsetBegin': '13', 
         'PartOfSpeech': 'JJ'}], 
    ['Gilbert', 
        {'PartOfSpeech': 'NNP', 
         'NamedEntityTag': 'PERSON', 
         'CharacterOffsetBegin': '19', 
         'Lemma': 'Gilbert', 
         'CharacterOffsetEnd': '26'}], 
    ['and', 
        {'PartOfSpeech': 'CC', 
         'NamedEntityTag': 'O', 
         'CharacterOffsetBegin': '27', 
         'Lemma': 'and', 
         'CharacterOffsetEnd': '30'}], 
    ['Sullivan', 
        {'PartOfSpeech': 'NNP', 
         'NamedEntityTag': 'PERSON', 
         'CharacterOffsetBegin': '31', 
         'Lemma': 'Sullivan', 
         'CharacterOffsetEnd': '39'}], 
    ['opera', 
        {'PartOfSpeech': 'NN', 
         'NamedEntityTag': 'O', 
         'CharacterOffsetBegin': '40', 
         'Lemma': 'opera', 
         'CharacterOffsetEnd': '45'}], 
    ['?', 
        {'PartOfSpeech': '.', 
         'NamedEntityTag': 'O', 
         'CharacterOffsetBegin': '45', 
         'Lemma': '?', 
         'CharacterOffsetEnd': '46'}]], 
  'text': 'What was the first Gilbert and Sullivan opera?', 
  'dependencies': [['root', 'ROOT', 'was'], ['dep', 'was', 'What'], ['det', 'Gilbert', 'the'], ['amod', 'Gilbert', 'first'], ['nsubj', 'was', 'Gilbert'], ['nn', 'opera', 'Sullivan'], ['conj_and', 'Gilbert', 'opera']],   
  'indexeddependencies': [['root', 'ROOT-0', 'was-2'], ['dep', 'was-2', 'What-1'], ['det', 'Gilbert-5', 'the-3'], ['amod', 'Gilbert-5', 'first-4'], ['nsubj', 'was-2', 'Gilbert-5'], ['nn', 'opera-8', 'Sullivan-7'], ['conj_and', 'Gilbert-5', 'opera-8']], 
  'parsetree': '(ROOT (SBARQ (WHNP (WP What)) (SQ (VBD was) (NP (DT the) (JJ first) (NNP Gilbert) (CC and) (NNP Sullivan) (NN opera))) (. ?)))'}]}

# Parsing result of "Who is the chief and prime minister?"
def give_chief():
    return  {'sentences': [{

  'words': [
    ['Who', 
        {'PartOfSpeech': 'WP', 
         'CharacterOffsetBegin': '0', 
         'CharacterOffsetEnd': '3', 
         'NamedEntityTag': 'O', 
         'Lemma': 'who'}], 
    ['is', 
        {'PartOfSpeech': 'VBZ', 
         'CharacterOffsetBegin': '4', 
         'CharacterOffsetEnd': '6', 
         'NamedEntityTag': 'O', 
         'Lemma': 'be'}], 
    ['the', 
        {'PartOfSpeech': 'DT', 
         'CharacterOffsetBegin': '7', 
         'CharacterOffsetEnd': '10', 
         'NamedEntityTag': 'O', 
         'Lemma': 'the'}], 
    ['chief', 
        {'PartOfSpeech': 'NN', 
         'CharacterOffsetBegin': '11', 
         'CharacterOffsetEnd': '16', 
         'NamedEntityTag': 'O', 
         'Lemma': 'chief'}], 
    ['and', 
        {'PartOfSpeech': 'CC', 
         'CharacterOffsetBegin': '17', 
         'CharacterOffsetEnd': '20', 
         'NamedEntityTag': 'O', 
         'Lemma': 'and'}], 
    ['prime', 
        {'PartOfSpeech': 'JJ', 
         'CharacterOffsetBegin': '21', 
         'CharacterOffsetEnd': '26', 
         'NamedEntityTag': 'O', 
         'Lemma': 'prime'}], 
    ['minister', 
        {'PartOfSpeech': 'NN', 
         'CharacterOffsetBegin': '27', 
         'CharacterOffsetEnd': '35', 
         'NamedEntityTag': 'O', 
         'Lemma': 'minister'}], 
    ['?', 
        {'PartOfSpeech': '.', 
         'CharacterOffsetBegin': '35', 
         'CharacterOffsetEnd': '36', 
         'NamedEntityTag': 'O', 
         'Lemma': '?'}]], 
   'parsetree': '(ROOT (SBARQ (WHNP (WP Who)) (SQ (VBZ is) (NP (NP (DT the) (NN chief)) (CC and) (NP (JJ prime) (NN minister)))) (. ?)))', 
  'dependencies': [['root', 'ROOT', 'is'], ['dep', 'is', 'Who'], ['det', 'chief', 'the'], ['nsubj', 'is', 'chief'], ['amod', 'minister', 'prime'], ['conj_and', 'chief', 'minister']], 
  'indexeddependencies': [['root', 'ROOT-0', 'is-2'], ['dep', 'is-2', 'Who-1'], ['det', 'chief-4', 'the-3'], ['nsubj', 'is-2', 'chief-4'], ['amod', 'minister-7', 'prime-6'], ['conj_and', 'chief-4', 'minister-7']], 
  'text': 'Who is the chief and prime minister?'}]}

# Parsing result of "Is born in 1900"
def give_born():
    return {'sentences': [{'indexeddependencies': [['root', 'ROOT-0', 'born-2'], ['auxpass', 'born-2', 'Is-1'], ['prep_in', 'born-2', '1900-4']], 'parsetree': '(ROOT (FRAG (VP (VBZ Is) (VP (VBN born) (PP (IN in) (NP (CD 1900)))))))', 'words': [['Is', {'PartOfSpeech': 'VBZ', 'Lemma': 'be', 'CharacterOffsetBegin': '0', 'CharacterOffsetEnd': '2', 'NamedEntityTag': 'O'}], ['born', {'PartOfSpeech': 'VBN', 'Lemma': 'bear', 'CharacterOffsetBegin': '3', 'CharacterOffsetEnd': '7', 'NamedEntityTag': 'O'}], ['in', {'PartOfSpeech': 'IN', 'Lemma': 'in', 'CharacterOffsetBegin': '8', 'CharacterOffsetEnd': '10', 'NamedEntityTag': 'O'}], ['1900', {'Timex': '<TIMEX3 tid="t1" type="DATE" value="1900">1900</TIMEX3>', 'PartOfSpeech': 'CD', 'Lemma': '1900', 'NamedEntityTag': 'DATE', 'CharacterOffsetBegin': '11', 'CharacterOffsetEnd': '15', 'NormalizedNamedEntityTag': '1900'}]], 'dependencies': [['root', 'ROOT', 'born'], ['auxpass', 'born', 'Is'], ['prep_in', 'born', '1900']], 'text': 'Is born in 1900'}]}

# Parsing result of "President of France"
def birth_date():
    return {'sentences': [{'parsetree': '(ROOT (NP (NP (NNP President)) (PP (IN of) (NP (NNP France)))))', 'words': [['President', {'NamedEntityTag': 'O', 'CharacterOffsetBegin': '0', 'Lemma': 'President', 'CharacterOffsetEnd': '9', 'PartOfSpeech': 'NNP'}], ['of', {'NamedEntityTag': 'O', 'CharacterOffsetBegin': '10', 'Lemma': 'of', 'CharacterOffsetEnd': '12', 'PartOfSpeech': 'IN'}], ['France', {'NamedEntityTag': 'LOCATION', 'CharacterOffsetBegin': '13', 'Lemma': 'France', 'CharacterOffsetEnd': '19', 'PartOfSpeech': 'NNP'}]], 'dependencies': [['root', 'ROOT', 'President'], ['prep_of', 'President', 'France']], 'text': 'President of France', 'indexeddependencies': [['root', 'ROOT-0', 'President-1'], ['prep_of', 'President-1', 'France-3']]}]}

# Parsing result of "When is born Obama?"
def birth_place():
    return {'sentences': [{'dependencies': [['root', 'ROOT', 'born'], ['advmod', 'born', 'When'], ['auxpass', 'born', 'is'], ['dobj', 'born', 'Obama']], 'words': [['When', {'Lemma': 'when', 'CharacterOffsetEnd': '4', 'NamedEntityTag': 'O', 'PartOfSpeech': 'WRB', 'CharacterOffsetBegin': '0'}], ['is', {'Lemma': 'be', 'CharacterOffsetEnd': '7', 'NamedEntityTag': 'O', 'PartOfSpeech': 'VBZ', 'CharacterOffsetBegin': '5'}], ['born', {'Lemma': 'bear', 'CharacterOffsetEnd': '12', 'NamedEntityTag': 'O', 'PartOfSpeech': 'VBN', 'CharacterOffsetBegin': '8'}], ['Obama', {'Lemma': 'Obama', 'CharacterOffsetEnd': '18', 'NamedEntityTag': 'PERSON', 'PartOfSpeech': 'NNP', 'CharacterOffsetBegin': '13'}], ['?', {'Lemma': '?', 'CharacterOffsetEnd': '19', 'NamedEntityTag': 'O', 'PartOfSpeech': '.', 'CharacterOffsetBegin': '18'}]], 'text': 'When is born Obama?', 'indexeddependencies': [['root', 'ROOT-0', 'born-3'], ['advmod', 'born-3', 'When-1'], ['auxpass', 'born-3', 'is-2'], ['dobj', 'born-3', 'Obama-4']], 'parsetree': '(ROOT (SBARQ (WHADVP (WRB When)) (SQ (VBZ is) (VP (VBN born) (NP (NNP Obama)))) (. ?)))'}]}
    
# Parsing result of "Where is the mistake the mistake?"

def mistake():
    return {'sentences': [{'indexeddependencies': [['root', 'ROOT-0', 'is-2'], ['advmod', 'is-2', 'Where-1'], ['det', 'mistake-4', 'the-3'], ['nsubj', 'is-2', 'mistake-4'], ['det', 'mistake-6', 'the-5'], ['dep', 'mistake-4', 'mistake-6']], 'dependencies': [['root', 'ROOT', 'is'], ['advmod', 'is', 'Where'], ['det', 'mistake', 'the'], ['nsubj', 'is', 'mistake'], ['det', 'mistake', 'the'], ['dep', 'mistake', 'mistake']], 'parsetree': '(ROOT (SBARQ (WHADVP (WRB Where)) (SQ (VBZ is) (NP (DT the) (NN mistake) (NP (DT the) (NN mistake)))) (. ?)))', 'text': 'Where is the mistake the mistake?', 'words': [['Where', {'PartOfSpeech': 'WRB', 'CharacterOffsetEnd': '5', 'CharacterOffsetBegin': '0', 'NamedEntityTag': 'O', 'Lemma': 'where'}], ['is', {'PartOfSpeech': 'VBZ', 'CharacterOffsetEnd': '8', 'CharacterOffsetBegin': '6', 'NamedEntityTag': 'O', 'Lemma': 'be'}], ['the', {'PartOfSpeech': 'DT', 'CharacterOffsetEnd': '12', 'CharacterOffsetBegin': '9', 'NamedEntityTag': 'O', 'Lemma': 'the'}], ['mistake', {'PartOfSpeech': 'NN', 'CharacterOffsetEnd': '20', 'CharacterOffsetBegin': '13', 'NamedEntityTag': 'O', 'Lemma': 'mistake'}], ['the', {'PartOfSpeech': 'DT', 'CharacterOffsetEnd': '24', 'CharacterOffsetBegin': '21', 'NamedEntityTag': 'O', 'Lemma': 'the'}], ['mistake', {'PartOfSpeech': 'NN', 'CharacterOffsetEnd': '32', 'CharacterOffsetBegin': '25', 'NamedEntityTag': 'O', 'Lemma': 'mistake'}], ['?', {'PartOfSpeech': '.', 'CharacterOffsetEnd': '33', 'CharacterOffsetBegin': '32', 'NamedEntityTag': 'O', 'Lemma': '?'}]]}]}

# Parsing result of "What is the highest mountain of Tanzania?"
def tanzania():
    return {'sentences': [{'text': 'What is the highest mountain of Tanzania?', 'indexeddependencies': [['root', 'ROOT-0', 'is-2'], ['dep', 'is-2', 'What-1'], ['det', 'mountain-5', 'the-3'], ['amod', 'mountain-5', 'highest-4'], ['nsubj', 'is-2', 'mountain-5'], ['prep_of', 'mountain-5', 'Tanzania-7']], 'parsetree': '(ROOT (SBARQ (WHNP (WP What)) (SQ (VBZ is) (NP (NP (DT the) (JJS highest) (NN mountain)) (PP (IN of) (NP (NNP Tanzania))))) (. ?)))', 'words': [['What', {'CharacterOffsetBegin': '0', 'Lemma': 'what', 'NamedEntityTag': 'O', 'CharacterOffsetEnd': '4', 'PartOfSpeech': 'WP'}], ['is', {'CharacterOffsetBegin': '5', 'Lemma': 'be', 'NamedEntityTag': 'O', 'CharacterOffsetEnd': '7', 'PartOfSpeech': 'VBZ'}], ['the', {'CharacterOffsetBegin': '8', 'Lemma': 'the', 'NamedEntityTag': 'O', 'CharacterOffsetEnd': '11', 'PartOfSpeech': 'DT'}], ['highest', {'CharacterOffsetBegin': '12', 'Lemma': 'highest', 'NamedEntityTag': 'O', 'CharacterOffsetEnd': '19', 'PartOfSpeech': 'JJS'}], ['mountain', {'CharacterOffsetBegin': '20', 'Lemma': 'mountain', 'NamedEntityTag': 'O', 'CharacterOffsetEnd': '28', 'PartOfSpeech': 'NN'}], ['of', {'CharacterOffsetBegin': '29', 'Lemma': 'of', 'NamedEntityTag': 'O', 'CharacterOffsetEnd': '31', 'PartOfSpeech': 'IN'}], ['Tanzania', {'CharacterOffsetBegin': '32', 'Lemma': 'Tanzania', 'NamedEntityTag': 'LOCATION', 'CharacterOffsetEnd': '40', 'PartOfSpeech': 'NNP'}], ['?', {'CharacterOffsetBegin': '40', 'Lemma': '?', 'NamedEntityTag': 'O', 'CharacterOffsetEnd': '41', 'PartOfSpeech': '.'}]], 'dependencies': [['root', 'ROOT', 'is'], ['dep', 'is', 'What'], ['det', 'mountain', 'the'], ['amod', 'mountain', 'highest'], ['nsubj', 'is', 'mountain'], ['prep_of', 'mountain', 'Tanzania']]}]}

# Parsing result of "When is the birthday of Mickey Mouse?"
def mickey():
    return {'sentences': [{'parsetree': '(ROOT (SBARQ (WHADVP (WRB When)) (SQ (VBZ is) (NP (NP (DT the) (NN birthday)) (PP (IN of) (NP (NNP Mickey) (NNP Mouse))))) (. ?)))', 'dependencies': [['root', 'ROOT', 'is'], ['advmod', 'is', 'When'], ['det', 'birthday', 'the'], ['nsubj', 'is', 'birthday'], ['nn', 'Mouse', 'Mickey'], ['prep_of', 'birthday', 'Mouse']], 'indexeddependencies': [['root', 'ROOT-0', 'is-2'], ['advmod', 'is-2', 'When-1'], ['det', 'birthday-4', 'the-3'], ['nsubj', 'is-2', 'birthday-4'], ['nn', 'Mouse-7', 'Mickey-6'], ['prep_of', 'birthday-4', 'Mouse-7']], 'text': 'When is the birthday of Mickey Mouse?', 'words': [['When', {'CharacterOffsetBegin': '0', 'CharacterOffsetEnd': '4', 'PartOfSpeech': 'WRB', 'NamedEntityTag': 'O', 'Lemma': 'when'}], ['is', {'CharacterOffsetBegin': '5', 'CharacterOffsetEnd': '7', 'PartOfSpeech': 'VBZ', 'NamedEntityTag': 'O', 'Lemma': 'be'}], ['the', {'CharacterOffsetBegin': '8', 'CharacterOffsetEnd': '11', 'PartOfSpeech': 'DT', 'NamedEntityTag': 'O', 'Lemma': 'the'}], ['birthday', {'CharacterOffsetBegin': '12', 'CharacterOffsetEnd': '20', 'PartOfSpeech': 'NN', 'NamedEntityTag': 'O', 'Lemma': 'birthday'}], ['of', {'CharacterOffsetBegin': '21', 'CharacterOffsetEnd': '23', 'PartOfSpeech': 'IN', 'NamedEntityTag': 'O', 'Lemma': 'of'}], ['Mickey', {'CharacterOffsetBegin': '24', 'CharacterOffsetEnd': '30', 'PartOfSpeech': 'NNP', 'NamedEntityTag': 'PERSON', 'Lemma': 'Mickey'}], ['Mouse', {'CharacterOffsetBegin': '31', 'CharacterOffsetEnd': '36', 'PartOfSpeech': 'NNP', 'NamedEntityTag': 'PERSON', 'Lemma': 'Mouse'}], ['?', {'CharacterOffsetBegin': '36', 'CharacterOffsetEnd': '37', 'PartOfSpeech': '.', 'NamedEntityTag': 'O', 'Lemma': '?'}]]}]}

# Parsing result of "What is black and white?"
def black():
    return {'sentences': [{'dependencies': [['root', 'ROOT', 'black'], ['dep', 'black', 'What'], ['cop', 'black', 'is'], ['conj_and', 'black', 'white']], 'indexeddependencies': [['root', 'ROOT-0', 'black-3'], ['dep', 'black-3', 'What-1'], ['cop', 'black-3', 'is-2'], ['conj_and', 'black-3', 'white-5']], 'parsetree': '(ROOT (SBARQ (WHNP (WP What)) (SQ (VBZ is) (ADJP (JJ black) (CC and) (JJ white))) (. ?)))', 'text': 'What is black and white?', 'words': [['What', {'Lemma': 'what', 'NamedEntityTag': 'O', 'PartOfSpeech': 'WP', 'CharacterOffsetEnd': '4', 'CharacterOffsetBegin': '0'}], ['is', {'Lemma': 'be', 'NamedEntityTag': 'O', 'PartOfSpeech': 'VBZ', 'CharacterOffsetEnd': '7', 'CharacterOffsetBegin': '5'}], ['black', {'Lemma': 'black', 'NamedEntityTag': 'O', 'PartOfSpeech': 'JJ', 'CharacterOffsetEnd': '13', 'CharacterOffsetBegin': '8'}], ['and', {'Lemma': 'and', 'NamedEntityTag': 'O', 'PartOfSpeech': 'CC', 'CharacterOffsetEnd': '17', 'CharacterOffsetBegin': '14'}], ['white', {'Lemma': 'white', 'NamedEntityTag': 'O', 'PartOfSpeech': 'JJ', 'CharacterOffsetEnd': '23', 'CharacterOffsetBegin': '18'}], ['?', {'Lemma': '?', 'NamedEntityTag': 'O', 'PartOfSpeech': '.', 'CharacterOffsetEnd': '24', 'CharacterOffsetBegin': '23'}]]}]}

# Parsing result of "Is there a king of England?"
def king_england():
    return {'sentences': [{'parsetree': '(ROOT (SQ (VBZ Is) (NP (EX there)) (NP (NP (DT a) (NN king)) (PP (IN of) (NP (NNP England)))) (. ?)))', 'words': [['Is', {'Lemma': 'be', 'PartOfSpeech': 'VBZ', 'CharacterOffsetBegin': '0', 'NamedEntityTag': 'O', 'CharacterOffsetEnd': '2'}], ['there', {'Lemma': 'there', 'PartOfSpeech': 'EX', 'CharacterOffsetBegin': '3', 'NamedEntityTag': 'O', 'CharacterOffsetEnd': '8'}], ['a', {'Lemma': 'a', 'PartOfSpeech': 'DT', 'CharacterOffsetBegin': '9', 'NamedEntityTag': 'O', 'CharacterOffsetEnd': '10'}], ['king', {'Lemma': 'king', 'PartOfSpeech': 'NN', 'CharacterOffsetBegin': '11', 'NamedEntityTag': 'O', 'CharacterOffsetEnd': '15'}], ['of', {'Lemma': 'of', 'PartOfSpeech': 'IN', 'CharacterOffsetBegin': '16', 'NamedEntityTag': 'O', 'CharacterOffsetEnd': '18'}], ['England', {'Lemma': 'England', 'PartOfSpeech': 'NNP', 'CharacterOffsetBegin': '19', 'NamedEntityTag': 'LOCATION', 'CharacterOffsetEnd': '26'}], ['?', {'Lemma': '?', 'PartOfSpeech': '.', 'CharacterOffsetBegin': '26', 'NamedEntityTag': 'O', 'CharacterOffsetEnd': '27'}]], 'indexeddependencies': [['root', 'ROOT-0', 'Is-1'], ['expl', 'Is-1', 'there-2'], ['det', 'king-4', 'a-3'], ['nsubj', 'Is-1', 'king-4'], ['prep_of', 'king-4', 'England-6']], 'text': 'Is there a king of England?', 'dependencies': [['root', 'ROOT', 'Is'], ['expl', 'Is', 'there'], ['det', 'king', 'a'], ['nsubj', 'Is', 'king'], ['prep_of', 'king', 'England']]}]}

# Parsing result of "List books by Roald Dahl"
def roald():
    return {'sentences': [{'text': 'List books by Roald Dahl', 'parsetree': '(ROOT (NP (NP (NN List) (NNS books)) (PP (IN by) (NP (NNP Roald) (NNP Dahl)))))', 'indexeddependencies': [['root', 'ROOT-0', 'books-2'], ['nn', 'books-2', 'List-1'], ['nn', 'Dahl-5', 'Roald-4'], ['prep_by', 'books-2', 'Dahl-5']], 'dependencies': [['root', 'ROOT', 'books'], ['nn', 'books', 'List'], ['nn', 'Dahl', 'Roald'], ['prep_by', 'books', 'Dahl']], 'words': [['List', {'NamedEntityTag': 'O', 'PartOfSpeech': 'NN', 'CharacterOffsetEnd': '4', 'Lemma': 'list', 'CharacterOffsetBegin': '0'}], ['books', {'NamedEntityTag': 'O', 'PartOfSpeech': 'NNS', 'CharacterOffsetEnd': '10', 'Lemma': 'book', 'CharacterOffsetBegin': '5'}], ['by', {'NamedEntityTag': 'O', 'PartOfSpeech': 'IN', 'CharacterOffsetEnd': '13', 'Lemma': 'by', 'CharacterOffsetBegin': '11'}], ['Roald', {'NamedEntityTag': 'PERSON', 'PartOfSpeech': 'NNP', 'CharacterOffsetEnd': '19', 'Lemma': 'Roald', 'CharacterOffsetBegin': '14'}], ['Dahl', {'NamedEntityTag': 'PERSON', 'PartOfSpeech': 'NNP', 'CharacterOffsetEnd': '24', 'Lemma': 'Dahl', 'CharacterOffsetBegin': '20'}]]}]}

# Parsing result of "List of presidents of France"
def list_president2():
    return {'sentences': [{'indexeddependencies': [['root', 'ROOT-0', 'List-1'], ['prep_of', 'List-1', 'presidents-3'], ['prep_of', 'presidents-3', 'France-5']], 'text': 'List of presidents of France', 'parsetree': '(ROOT (NP (NP (NN List)) (PP (IN of) (NP (NP (NNS presidents)) (PP (IN of) (NP (NNP France)))))))', 'dependencies': [['root', 'ROOT', 'List'], ['prep_of', 'List', 'presidents'], ['prep_of', 'presidents', 'France']], 'words': [['List', {'Lemma': 'list', 'PartOfSpeech': 'NN', 'NamedEntityTag': 'O', 'CharacterOffsetEnd': '4', 'CharacterOffsetBegin': '0'}], ['of', {'Lemma': 'of', 'PartOfSpeech': 'IN', 'NamedEntityTag': 'O', 'CharacterOffsetEnd': '7', 'CharacterOffsetBegin': '5'}], ['presidents', {'Lemma': 'president', 'PartOfSpeech': 'NNS', 'NamedEntityTag': 'O', 'CharacterOffsetEnd': '18', 'CharacterOffsetBegin': '8'}], ['of', {'Lemma': 'of', 'PartOfSpeech': 'IN', 'NamedEntityTag': 'O', 'CharacterOffsetEnd': '21', 'CharacterOffsetBegin': '19'}], ['France', {'Lemma': 'France', 'PartOfSpeech': 'NNP', 'NamedEntityTag': 'LOCATION', 'CharacterOffsetEnd': '28', 'CharacterOffsetBegin': '22'}]]}]}

# Parsing result of "Give me the capital of France"
def capital1():
    return {'sentences': [{'parsetree': '(ROOT (S (VP (VB Give) (NP (PRP me)) (NP (NP (DT the) (NN capital)) (PP (IN of) (NP (NNP France)))))))', 'indexeddependencies': [['root', 'ROOT-0', 'Give-1'], ['iobj', 'Give-1', 'me-2'], ['det', 'capital-4', 'the-3'], ['dobj', 'Give-1', 'capital-4'], ['prep_of', 'capital-4', 'France-6']], 'text': 'Give me the capital of France', 'words': [['Give', {'NamedEntityTag': 'O', 'CharacterOffsetBegin': '0', 'CharacterOffsetEnd': '4', 'Lemma': 'give', 'PartOfSpeech': 'VB'}], ['me', {'NamedEntityTag': 'O', 'CharacterOffsetBegin': '5', 'CharacterOffsetEnd': '7', 'Lemma': 'I', 'PartOfSpeech': 'PRP'}], ['the', {'NamedEntityTag': 'O', 'CharacterOffsetBegin': '8', 'CharacterOffsetEnd': '11', 'Lemma': 'the', 'PartOfSpeech': 'DT'}], ['capital', {'NamedEntityTag': 'O', 'CharacterOffsetBegin': '12', 'CharacterOffsetEnd': '19', 'Lemma': 'capital', 'PartOfSpeech': 'NN'}], ['of', {'NamedEntityTag': 'O', 'CharacterOffsetBegin': '20', 'CharacterOffsetEnd': '22', 'Lemma': 'of', 'PartOfSpeech': 'IN'}], ['France', {'NamedEntityTag': 'LOCATION', 'CharacterOffsetBegin': '23', 'CharacterOffsetEnd': '29', 'Lemma': 'France', 'PartOfSpeech': 'NNP'}]], 'dependencies': [['root', 'ROOT', 'Give'], ['iobj', 'Give', 'me'], ['det', 'capital', 'the'], ['dobj', 'Give', 'capital'], ['prep_of', 'capital', 'France']]}]}

# Parsing result of "Give the capital of France"
def capital2():
    return {'sentences': [{'parsetree': '(ROOT (S (VP (VB Give) (NP (NP (DT the) (NN capital)) (PP (IN of) (NP (NNP France)))))))', 'words': [['Give', {'NamedEntityTag': 'O', 'Lemma': 'give', 'CharacterOffsetEnd': '4', 'CharacterOffsetBegin': '0', 'PartOfSpeech': 'VB'}], ['the', {'NamedEntityTag': 'O', 'Lemma': 'the', 'CharacterOffsetEnd': '8', 'CharacterOffsetBegin': '5', 'PartOfSpeech': 'DT'}], ['capital', {'NamedEntityTag': 'O', 'Lemma': 'capital', 'CharacterOffsetEnd': '16', 'CharacterOffsetBegin': '9', 'PartOfSpeech': 'NN'}], ['of', {'NamedEntityTag': 'O', 'Lemma': 'of', 'CharacterOffsetEnd': '19', 'CharacterOffsetBegin': '17', 'PartOfSpeech': 'IN'}], ['France', {'NamedEntityTag': 'LOCATION', 'Lemma': 'France', 'CharacterOffsetEnd': '26', 'CharacterOffsetBegin': '20', 'PartOfSpeech': 'NNP'}]], 'text': 'Give the capital of France', 'dependencies': [['root', 'ROOT', 'Give'], ['det', 'capital', 'the'], ['dobj', 'Give', 'capital'], ['prep_of', 'capital', 'France']], 'indexeddependencies': [['root', 'ROOT-0', 'Give-1'], ['det', 'capital-3', 'the-2'], ['dobj', 'Give-1', 'capital-3'], ['prep_of', 'capital-3', 'France-5']]}]}

# Parsing result of "What is the most expensive car in the world?"
def car():
    return {'sentences': [{'parsetree': '(ROOT (SBARQ (WHNP (WP What)) (SQ (VBZ is) (NP (NP (DT the) (ADJP (RBS most) (JJ expensive)) (NN car)) (PP (IN in) (NP (DT the) (NN world))))) (. ?)))', 'dependencies': [['root', 'ROOT', 'is'], ['dep', 'is', 'What'], ['det', 'car', 'the'], ['advmod', 'expensive', 'most'], ['amod', 'car', 'expensive'], ['nsubj', 'is', 'car'], ['det', 'world', 'the'], ['prep_in', 'car', 'world']], 'text': 'What is the most expensive car in the world?', 'indexeddependencies': [['root', 'ROOT-0', 'is-2'], ['dep', 'is-2', 'What-1'], ['det', 'car-6', 'the-3'], ['advmod', 'expensive-5', 'most-4'], ['amod', 'car-6', 'expensive-5'], ['nsubj', 'is-2', 'car-6'], ['det', 'world-9', 'the-8'], ['prep_in', 'car-6', 'world-9']], 'words': [['What', {'CharacterOffsetEnd': '4', 'CharacterOffsetBegin': '0', 'NamedEntityTag': 'O', 'Lemma': 'what', 'PartOfSpeech': 'WP'}], ['is', {'CharacterOffsetEnd': '7', 'CharacterOffsetBegin': '5', 'NamedEntityTag': 'O', 'Lemma': 'be', 'PartOfSpeech': 'VBZ'}], ['the', {'CharacterOffsetEnd': '11', 'CharacterOffsetBegin': '8', 'NamedEntityTag': 'O', 'Lemma': 'the', 'PartOfSpeech': 'DT'}], ['most', {'CharacterOffsetEnd': '16', 'CharacterOffsetBegin': '12', 'NamedEntityTag': 'O', 'Lemma': 'most', 'PartOfSpeech': 'RBS'}], ['expensive', {'CharacterOffsetEnd': '26', 'CharacterOffsetBegin': '17', 'NamedEntityTag': 'O', 'Lemma': 'expensive', 'PartOfSpeech': 'JJ'}], ['car', {'CharacterOffsetEnd': '30', 'CharacterOffsetBegin': '27', 'NamedEntityTag': 'O', 'Lemma': 'car', 'PartOfSpeech': 'NN'}], ['in', {'CharacterOffsetEnd': '33', 'CharacterOffsetBegin': '31', 'NamedEntityTag': 'O', 'Lemma': 'in', 'PartOfSpeech': 'IN'}], ['the', {'CharacterOffsetEnd': '37', 'CharacterOffsetBegin': '34', 'NamedEntityTag': 'O', 'Lemma': 'the', 'PartOfSpeech': 'DT'}], ['world', {'CharacterOffsetEnd': '43', 'CharacterOffsetBegin': '38', 'NamedEntityTag': 'O', 'Lemma': 'world', 'PartOfSpeech': 'NN'}], ['?', {'CharacterOffsetEnd': '44', 'CharacterOffsetBegin': '43', 'NamedEntityTag': 'O', 'Lemma': '?', 'PartOfSpeech': '.'}]]}]}

def tripleProductionData():
    '''
        Return data corresponding to a tree (root-0)--dep-->(child-1)
    '''
    root = DependenciesTree("root-0")
    child = DependenciesTree("child-1",dependency="dep",parent=root)
    root.child = [child]
    nodeToID = {root:0, child:1}
    bt = TriplesBucket()
    return (root,nodeToID,bt)
