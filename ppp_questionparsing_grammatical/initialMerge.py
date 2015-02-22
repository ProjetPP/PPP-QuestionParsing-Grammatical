class NamedEntityMerging:
    """
        Perform several merging on the dependency tree according to the named
        entity tags.
    """
    def __init__(self, tree):
        self.tree = tree

    def _mergeChildParent(self, tree):
        """
            Merge all nodes n1, n2 such that:
                * n1 is parent of n2
                * n1 and n2 have a same namedEntityTag
            Don't merge if the 2 words are linked by a conjonction
        """
        for child in tree.child:
            self._mergeChildParent(child)
        if tree.namedEntityTag == 'undef':
            return
        sameTagChild = set()
        for child in tree.child:
            if child.namedEntityTag == tree.namedEntityTag and not child.dependency.startswith('conj'):
                sameTagChild.add(child)
        for child in sameTagChild:
            tree.merge(child, True)

    def _mergeSisterBrother(self, tree):
        """
            Merge all nodes n1, n2 such that:
                * n1 and n2 have a same parent
                * n1 and n2 have a same namedEntityTag
                * n1 and n2 have a same dependency
        """
        for child in tree.child:
            self._mergeSisterBrother(child)
        tagToNodes = {}
        for child in tree.child:
            if child.namedEntityTag == 'undef' or child.dependency.startswith('conj'):
                continue
            try:
                tagToNodes[child.namedEntityTag+child.dependency].add(child)
            except KeyError:
                tagToNodes[child.namedEntityTag+child.dependency] = set([child])
        for sameTag in tagToNodes.values():
            x = sameTag.pop()
            for other in sameTag:
                x.merge(other, True)

    def merge(self):
        """
            Perform the different merges.
        """
        self._mergeChildParent(self.tree)
        self._mergeSisterBrother(self.tree)

class PrepositionMerging:
    """
        Perform several merging on the dependency tree according to the preposition
        dependencies.
    """
    def __init__(self, tree):
        self.tree = tree

    def _mergeNode(self, tree):
        """
            Merge x -> y into 'x y' if y is a preposition
        """
        for child in tree.child:
            self._mergeNode(child)
            if child.getWords() in tree.prepositionSet:
                tree.merge(child, True)

    def _mergeEdge(self, tree):
        """
            Replace a -prep_x-> b by 'a x' -prep-> b if a is a verb, a -prep-> b otherwise
            Replace a -agent-> b by 'a by' -agent-> b
        """
        for child in tree.child:
            self._mergeEdge(child)
            if child.dependency.startswith('prep'): # prep_x or prepc_x
                preposition = ' '.join(child.dependency.split('_')[1:]) # type of the prep (of, in, ...)
                if tree.isVerb():
                    tree.appendWord(preposition)
                child.dependency = 'prep'
            if child.dependency == 'agent':
                assert tree.isVerb()
                tree.append('by')

    def merge(self):
        """
            Perform the different merges.
        """
        self._mergeNode(self.tree)
        self._mergeEdge(self.tree)
