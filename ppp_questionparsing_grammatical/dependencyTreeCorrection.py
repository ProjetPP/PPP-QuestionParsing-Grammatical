def addNamedEntityTag(tree, nameToNodes, words):
    """
        If a word v is between 2 words u and w that have the same NER tag,
        and v is linked to u or w by a nn relation,
        then add the tag of u and w to v
    """
    def nnDependent(n1, n2):
        return (n1.parent == n2 and n1.dependency == 'nn')\
            or (n2.parent == n1 and n2.dependency == 'nn')
    for i in range(1,len(words)-1):
        previous = nameToNodes[words[i-1]]
        current = nameToNodes[words[i]]
        next = nameToNodes[words[i+1]]
        if current.namedEntityTag == 'undef' and previous.namedEntityTag != 'undef' and previous.namedEntityTag == next.namedEntityTag:
            if nnDependent(previous, current) or nnDependent(next, current):
                current.namedEntityTag = previous.namedEntityTag

def correctTree(tree, nameToNodes, stanfordResult=None):
    """
        Correct the tree returned by the Stanford Parser, according to several heuristics.
    """
    words = sorted(nameToNodes.keys(), key = lambda x: int(x.split('-')[-1]))
    addNamedEntityTag(tree, nameToNodes, words)
