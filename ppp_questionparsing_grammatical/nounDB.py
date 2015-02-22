import pickle
import json
import os

class TextStream:
    """
        A class to load and save files containing the nounification maps stored in txt format
    """

    def __init__(self, directSymbol = ' -> ', inverseSymbol = ' <- ', separator = ', '):
        self.directSymbol = directSymbol
        self.inverseSymbol = inverseSymbol
        self.separator = separator

    def load(self, f):
        """
            Load the content of f
        """
        verbToNounsDirect = {}
        verbToNounsInverse = {}
        for line in f:
            line = line.replace('\n', '')
            if self.directSymbol in line:
                assert self.inverseSymbol not in line
                [key, nounList] = line.split(self.directSymbol, 1)
                target = verbToNounsDirect
            elif self.inverseSymbol in line:
                assert self.directSymbol not in line
                [key, nounList] = line.split(self.inverseSymbol, 1)
                target = verbToNounsInverse
            else:
                raise Exception("[nounDB] incorrect file format.")
            for noun in nounList.split(self.separator):
                if not key in target:
                    target[key] = [noun]
                elif not noun in target[key]:
                    target[key].append(noun)
        return [verbToNounsDirect, verbToNounsInverse]

    def dump(self, data, f):
        """
            Save data into f
        """
        [verbToNounsDirect, verbToNounsInverse] = data
        l = sorted([(x, 0) for x in verbToNounsDirect.keys()] + [(x, 1) for x in verbToNounsInverse.keys()])
        for couple in l:
            if couple[1] == 0:
                f.write('%s%s%s\n' % (couple[0], self.directSymbol, self.separator.join(verbToNounsDirect[couple[0]])))
            if couple[1] == 1:
                f.write('%s%s%s\n' % (couple[0], self.inverseSymbol, self.separator.join(verbToNounsInverse[couple[0]])))

class Nounificator:
    """
        A class to handle the correspondances from the verbs to the nouns.
    """
    pickleExtension = {'pickle', 'pkl', 'p'}
    jsonExtension = {'json'}
    txtExtension = {'txt'}
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
        return '\n'.join([self.select(x) for x in l])

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def load(self, fileName):
        """
            Load the database from the file of given name (pickle or json format).
        """
        fileExtension = os.path.splitext(fileName)[1][1:]
        if fileExtension in self.pickleExtension:
            f = open(fileName, 'rb')
            module = pickle
        elif fileExtension in self.jsonExtension:
            f = open(fileName, 'r')
            module = json
        elif fileExtension in self.txtExtension:
            f = open(fileName, 'r')
            module = TextStream()
        [self.verbToNounsDirect, self.verbToNounsInverse] = module.load(f)
        f.close()

    def save(self, fileName):
        """
            Save the database into the file of given name (pickle format).
        """
        fileExtension = os.path.splitext(fileName)[1][1:]
        if fileExtension in self.pickleExtension:
            f = open(fileName, 'wb')
            pickle.dump([self.verbToNounsDirect, self.verbToNounsInverse], f)
        elif fileExtension in self.jsonExtension:
            f = open(fileName, 'w')
            json.dump([self.verbToNounsDirect, self.verbToNounsInverse], f, indent=4, sort_keys=True)
        elif fileExtension in self.txtExtension:
            f = open(fileName, 'w')
            TextStream().dump([self.verbToNounsDirect, self.verbToNounsInverse], f)
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
        return target.get(verb, [])

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
