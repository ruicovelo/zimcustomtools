from zim.notebook import Path,Page,get_notebook
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
    
    def _list_contains(self,haystack_headers,needle_headers):
        for header in needle_headers:
            if header in haystack_headers:
                return True
        return False

    def select_pagelist(self,path,include_headers,exclude_headers=None):
        page_list = self.get_pagelist(Path(path))
        selected_pagelist = []
        for page in page_list:
            page = PageWrapper(page)
            headers = page.get_headers()
            if headers:
                if exclude_headers and self._list_contains(headers,exclude_headers):
                    continue
                if include_headers:
                    if include_headers and self._list_contains(headers,include_headers):
                        selected_pagelist.append(page)
        return selected_pagelist

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

    def create(self,notebook,text=''):
        '''
        Create a new page using the default template
        '''
	template = notebook.get_template(self)
	tree = template.process_to_parsetree(notebook, self)
        self.set_parsetree(tree)
	self.parse('wiki', text, append=True) # FIXME format hard coded
	notebook.store_page(self)
        notebook.emit('stored-page',Path(self.name))
        
