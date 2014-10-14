from corenlp import StanfordCoreNLP

corenlp_dir = "../Scripts/stanford-corenlp-full-2014-08-27/"
corenlp = StanfordCoreNLP(corenlp_dir)  # wait a few minutes...

result = corenlp.raw_parse("What is birth date of the wife of the first black president of the United States?")

print(result['sentences'][0]['dependencies'])
