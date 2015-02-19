import pickle

class Nounificator:
    """
        A class to handle the correspondances from the verbs to the nouns.
    """

    def __init__(self):
        self.verbToNounsDirect = {}
        self.verbToNounsInverse = {}

    def select(self, x):
        if x[1] == 0:
            return ('%s:\t->%s' % (x[0], self.verbToNounsDirect[x[0]]))
        else:
            return ('%s:\t<-%s' % (x[0], self.verbToNounsInverse[x[0]]))

    def __str__(self):
        l = sorted([(x, 0) for x in self.verbToNounsDirect.keys()] + [(x, 1) for x in self.verbToNounsInverse.keys()])
        return '\n'.join([self.select(x) for x in sorted(l)])

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def load(self, file_name):
        """
            Load the database from the file of given name (pickle format).
        """
        f = open(file_name, 'rb')
        self.verbToNounsDirect = pickle.load(f)
        self.verbToNounsInverse = pickle.load(f)
        f.close()

    def save(self, file_name):
        """
            Save the database into the file of given name (pickle format).
        """
        f = open(file_name, 'wb')
        pickle.dump(self.verbToNounsDirect, f)
        pickle.dump(self.verbToNounsInverse, f)
        f.close()

    def _add(self, verb, noun, target):
        try:
            if not noun in target[verb]:
                target[verb].append(noun)
        except:
            target[verb] = [noun]

    def addDirect(self, verb, noun):
        """
            Add the given noun to the direct nounifications of the given verb.
        """
        self._add(verb, noun, self.verbToNounsDirect)

    def addInverse(self, verb, noun):
        """
            Add the given noun to the inverse nounifications of the given verb.
        """
        self._add(verb, noun, self.verbToNounsInverse)

    def addListDirect(self, verb, nounList):
        """
            Add the given list of nouns to the direct nounifications of the given verb.
        """
        for noun in nounList:
            self.addDirect(verb, noun)

    def addListInverse(self, verb, nounList):
        """
            Add the given list of nouns to the inverse nounifications of the given verb.
        """
        for noun in nounList:
            self.addInverse(verb, noun)

    def _remove(self, verb, noun, target):
        target[verb].remove(noun)
        if target[verb] == []:
            target.pop(verb)

    def removeDirect(self, verb, noun):
        """
            Remove the given noun from the direct nounifications of the given verb.
        """
        self._remove(verb, noun, self.verbToNounsDirect)

    def removeInverse(self, verb, noun):
        """
            Remove the given noun from the inverse nounifications of the given verb.
        """
        self._remove(verb, noun, self.verbToNounsInverse)

    def _removeVerb(self, verb, target):
        target.pop(verb)

    def removeVerbDirect(self, verb):
        """
            Remove all the direct nounifications of the given verb.
        """
        self._removeVerb(verb, self.verbToNounsDirect)

    def removeVerbInverse(self, verb):
        """
            Remove all the inverse nounifications of the given verb.
        """
        self._removeVerb(verb, self.verbToNounsInverse)

    def _toNouns(self, verb, target):
        try:
            return target[verb]
        except KeyError:
            return []

    def directNouns(self, verb):
        """
            Return the list of direct nounifications of the given noun.
        """
        return self._toNouns(verb, self.verbToNounsDirect)

    def inverseNouns(self, verb):
        """
            Return the list of inverse nounifications of the given noun.
        """
        return self._toNouns(verb, self.verbToNounsInverse)

    def exists(self, verb):
        """
            Return True if and only if there exists (direct or inverse) nounification(s) of the given verb.
        """
        return verb in self.verbToNounsDirect or verb in self.verbToNounsInverse

    def merge(self, other):
        """
            Merge with the given nounificator.
        """
        for key, value in other.verbToNounsDirect.items():
            self.addListDirect(key, value)
        for key, value in other.verbToNounsInverse.items():
            self.addListInverse(key, value)
