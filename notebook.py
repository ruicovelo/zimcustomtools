from zim.notebook import Page,get_notebook
import re

def get_ctnotebook(path):
    return NotebookWrapper(get_notebook(path))

class Wrapper(object):
    
    def __init__(self,obj):
        self.obj=obj

    def __getattr__(self,name):
        if self.__dict__.has_key(name):
            return self.__dict__[name]
        return getattr(self.__dict__['obj'],name)

class NotebookWrapper(Wrapper):
        
    def get_page(self,path):
        return PageWrapper(self.obj.get_page(path))
        
class PageWrapper(Wrapper):
    
    def _get_headers(self,lines):
        line_pattern = re.compile('^(:[a-zA-Z0-9_ ]+)+$|^\[\[(:[a-zA-Z0-9_ ]+)+\]\]$')
        path_pattern = re.compile('(:[a-zA-Z0-9_ ]+)+')
        headers_started=False
        headers=[]
        for line in lines:
            if line_pattern.match(line):
                headers.append(path_pattern.search(line).group(0).strip()) 
                headers_started = True
            elif headers_started:
                break
        return headers

    def get_headers(self):
        '''
        Headers are links to other pages at the top of a page.
        Headers must start with : and there should only be one per line like this
        :something:else
        :something:else:more
        :otherthing
        We check for headers using the raw text file
        '''
        try:
            f=open(str(self.source),"r")
            lines = f.readlines()
            f.close()
        except IOError:
            return None
        return self._get_headers(lines)
