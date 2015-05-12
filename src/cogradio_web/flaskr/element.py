import uuid

class Element(object):
    def __init__(self, key, title):
        self.uuid = uuid.uuid4().hex
        self.key = key
        self.title = title
        
    @property
    def html(self):
        raise NotImplementedError

class TextElement(Element):
    def __init__(self, key, title=None, value=None):
        super(TextElement, self).__init__(key, title)
        self._value = value

    @property
    def value(self):
        import random
        return random.randint(0,1000)
    
    @property
    def html(self):
        return """
        <div class="panel panel-default">
            <div class="panel-heading">
	      <h3 class="panel-title">{0}</h3>
	    </div>
	    <div class="panel-body" id="{1}">
	      {2}
	    </div>
	</div>""".format(self.title, self.uuid, self.value)
        

class SliderElement(Element):
    def __init__(self, key, title=None, value=None):
        super(SliderElement, self).__init__(key, title)
        self._value = value

    @property
    def value(self):
        import random
        return random.randint(0,1000)

    @property
    def html(self):
        return """
        <div class="panel panel-default">
            <div class="panel-heading">
	      <h3 class="panel-title">{0}</h3>
	    </div>
	    <div class="panel-body" id="{1}">
	      {2}
	    </div>
	</div>""".format(self.title, self.uuid, self.value)
    
if __name__ == '__main__':
    print "Hello, World!"

    el = TextElement(key="hello", title="Title", value="Hello, World")
    print el.html
