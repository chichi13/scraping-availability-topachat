Une classe abstraite qui sert à définir 2 méthodes :
    - Une qui serait de set clé:date_expiration
    - Une qui serait de récupérer une clé si elle existe

class AbstractStorage():
    def getKey():
        raise Exception("Method")

class LocalStorage(AbstractStorage):
    def getKey(self):
        return self.blabla