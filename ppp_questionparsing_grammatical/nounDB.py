import pickle

class Nounificator:
    """
        A class to handle the correspondances from the verbs to the nouns.
    """

    direct = 0
    reverse = 1

    def __init__(self):
        self.verbToNounsDirect = {}
        self.verbToNounsReverse = {}

    def select(self, x):
        if x[1] == 0:
            return ('%s:\t->%s' % (x[0], self.verbToNounsDirect[x[0]]))
        else:
            return ('%s:\t<-%s' % (x[0], self.verbToNounsReverse[x[0]]))

    def __str__(self):
        l = sorted([(x, 0) for x in self.verbToNounsDirect.keys()] + [(x, 1) for x in self.verbToNounsReverse.keys()])
        return '\n'.join([self.select(x) for x in sorted(l)])

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def load(self, file_name):
        f = open(file_name, 'rb')
        self.verbToNounsDirect = pickle.load(f)
        self.verbToNounsReverse = pickle.load(f)
        f.close()

    def save(self, file_name):
        f = open(file_name, 'wb')
        pickle.dump(self.verbToNounsDirect, f)
        pickle.dump(self.verbToNounsReverse, f)
        f.close()

    def _add(self, verb, noun, mapChoice):
        if mapChoice == self.direct:
            target = self.verbToNounsDirect
        elif mapChoice == self.reverse:
            target = self.verbToNounsReverse
        try:
            if not noun in target[verb]:
                target[verb].append(noun)
        except:
            target[verb] = [noun]

    def addDirect(self, verb, noun):
        self._add(verb, noun, self.direct)

    def addReverse(self, verb, noun):
        self._add(verb, noun, self.reverse)

    def addListDirect(self, verb, nounList):
        for t in nounList:
            self.addDirect(verb, t)

    def addListReverse(self, verb, nounList):
        for t in nounList:
            self.addReverse(verb, t)

    def _remove(self, verb, noun, mapChoice):
        if mapChoice == self.direct:
            target = self.verbToNounsDirect
        elif mapChoice == self.reverse:
            target = self.verbToNounsReverse
        target[verb].remove(noun)
        if target[verb] == []:
            target.pop(verb)

    def removeDirect(self, verb, noun):
        self._remove(verb, noun, self.direct)

    def removeReverse(self, verb, noun):
        self._remove(verb, noun, self.reverse)

    def _removeVerb(self, verb, mapChoice):
        if mapChoice == self.direct:
            target = self.verbToNounsDirect
        elif mapChoice == self.reverse:
            target = self.verbToNounsReverse
        target.pop(verb)

    def removeVerbDirect(self, verb):
        self._removeVerb(verb, self.direct)

    def removeVerbReverse(self, verb):
        self._removeVerb(verb, self.reverse)

    def _toNouns(self, verb, mapChoice):
        if mapChoice == self.direct:
            target = self.verbToNounsDirect
        elif mapChoice == self.reverse:
            target = self.verbToNounsReverse
        try:
            return target[verb]
        except KeyError:
            return []

    def directNouns(self, verb):
        return self._toNouns(verb, self.direct)

    def reverseNouns(self, verb):
        return self._toNouns(verb, self.reverse)

    def exists(self, verb):
        return verb in self.verbToNounsDirect or verb in self.verbToNounsReverse

    def merge(self, t):
        for key, value in t.verbToNounsDirect.items():
            self.addListDirect(key, value)
        for key, value in t.verbToNounsReverse.items():
            self.addListReverse(key, value)
