import sys

class Tag: # based on http://nlp.stanford.edu:8080/ner/process with classifier english.muc.7class.distsim.crf.ser.gz
  nill = 0
  location = 1
  time = 2
  person = 3
  organization = 4
  money = 5
  percent = 6
  date = 7
  

class Node:
  """ 
    One node of the parse tree.
    It is a group of words of same NamedEntityTag (e.g. George Washington).    
  """
  def __init__(self, word_list, namedentitytag, subnodes=[]):
    self.words = word_list
    self.child = subnodes
    if(namedentitytag=="O"):
      self.tag = Tag.nill
    if(namedentitytag=="LOCATION"):
      self.tag = Tag.location
    elif(namedentitytag=="TIME"):
      self.tag = Tag.time
    elif(namedentitytag=="PERSON"):
      self.tag = Tag.person
    elif(namedentitytag=="ORGANIZATION"):
      self.tag = Tag.organization
    elif(namedentitytag=="MONEY"):
      self.tag = Tag.money
    elif(namedentitytag=="PERCENT"):
      self.tag = Tag.percent
    elif(namedentitytag=="DATE"):
      self.tag = Tag.date
    else:
      self.tag = Tag.nill
      print("ERROR: unknown NamedEntityTag, set it to nill.",file=sys.stderr)
