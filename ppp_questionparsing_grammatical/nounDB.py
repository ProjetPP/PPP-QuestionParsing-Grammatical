import pickle

class Nounificator:
    """
        A class to handle the correspondances from the verbs to the nouns.
    """

    def __init__(self):
        self.verbToNounsDirect = {}  # code 0
        self.verbToNounsReverse = {} # code 1

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

    def add(self, verb, noun, n):
        if n==0:
            target = self.verbToNounsDirect
        else:
            target = self.verbToNounsReverse
        try:
            if not noun in target[verb]:
                target[verb].append(noun)
        except:
            target[verb] = [noun]

    def addList(self, verb, nounList, n):
        for t in nounList:
            self.add(verb, t, n)

    def remove(self, verb, noun, n):
        if n==0:
            target = self.verbToNounsDirect
        else:
            target = self.verbToNounsReverse
        target[verb].remove(noun)
        if target[verb] == []:
            target.pop(verb)

    def removeVerb(self, verb, n):
        if n==0:
            target = self.verbToNounsDirect
        else:
            target = self.verbToNounsReverse
        target.pop(verb)

    def toNouns(self, verb, n):
        if n==0:
            target = self.verbToNounsDirect
        else:
            target = self.verbToNounsReverse
        try:
            return target[verb]
        except KeyError:
            return []

    def exists(self, verb):
        return verb in self.verbToNounsDirect or verb in self.verbToNounsReverse

    def merge(self, t):
        for key, value in t.verbToNounsDirect.items():
            self.addList(key, value, 0)
        for key, value in t.verbToNounsReverse.items():
            self.addList(key, value, 1)
