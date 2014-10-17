import sys
  

class Node:
  """ 
    One node of the parse tree.
    It is a group of words of same NamedEntityTag (e.g. George Washington).    
  """
  def __init__(self, word_list, namedentitytag='undef', dependency='undef', subnodes=[]):
    self.words = word_list      # List of words for this node (generally of size 1, at most 2 or 3)
    self.tag = namedentitytag   # String for the NamedEntityTag (e.g. 'PERSON' or 'DATE')
    self.dep = dependency       # Relation with the parent node (e.g. 'nn' or 'det' or 'root')
    self.child = subnodes       # List of children nodes
                                # parent attribute will be available after computaiton of the tree

      

def compute_tree(r):
  """
    Compute the dependence tree.
    Take in input a piece of the result produced by StanfordNLP.
    If foo is this result, then r = foo['sentences'][0]
  """
  name_to_nodes = {} # find the nodes with their original string
  for edge in r['indexeddependencies']:
    try:
      n1 = name_to_nodes[edge[1]]
    except KeyError:
      n1 = Node([edge[1]])
      name_to_nodes[edge[1]] = n1
    try:
      n2 = name_to_nodes[edge[2]]
    except KeyError:
      n2 = Node([edge[2]])
      name_to_nodes[edge[2]] = n2
    # n1 is the parent of n2
    n1.child = n1.child+[n2]
    n2.parent = n1
    n2.dependency = edge[0]
  index=1
  for word in r['words']:
    if word[0].isalnum() or word[0] == '$' or  word[0] == '%':
      w=word[0]+'-'+str(index) # key in the name_to_nodes map
      index+=1
      n = name_to_nodes[w]
      n.tag = word[1]['NamedEntityTag']
  return name_to_nodes['ROOT-0']
