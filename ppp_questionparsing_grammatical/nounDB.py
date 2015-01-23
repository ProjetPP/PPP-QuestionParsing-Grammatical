import pickle

class Nounificator:
    """
        A class to handle the correspondances from the verbs to the nouns.
    """

    def __init__(self):
        self.verbToNouns = {}

    def __str__(self):
        return self.verbToNouns.__str__()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def display(self):
        for key in self.verbToNouns.keys():
            print('%s\t:%s' % (key,str(self.verbToNouns[key])))

    def add(self,verb,noun):
        try:
            self.verbToNouns[verb].append(noun)
        except:
            self.verbToNouns[verb] = [noun]

    def remove(self,verb,noun):
        self.verbToNouns[verb].remove(noun)
        if self.verbToNouns[verb] == []:
            self.verbToNouns.pop(verb)

    def toNouns(self,verb):
        return self.verbToNouns[verb]

    def load(self,file_name):
        f = open(file_name, 'rb')
        self.verbToNouns = pickle.load(f)
        f.close()

    def save(self,file_name):
        f = open(file_name, 'wb')
        pickle.dump(self.verbToNouns, f)
        f.close()
