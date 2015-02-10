class UrlGenerator:
    def __init__(self,*kargs,**kwargs):
        pass

    def __iter__(self):
        return self
    
    def __next__(self):
        #after the last one should raise StopIteration
        pass

    def __len__(self):
        #you must implement this method 
        pass

    def __str__(self):
        #you may imply this method for option [-u] to display real urls
        #otherwise it will just return <object@hash>
        pass
