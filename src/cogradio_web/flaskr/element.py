import uuid

class Element(object):
    def __init__(self, key, title):
        self.uuid = uuid.uuid4().hex
        self.key = key
        self.title = title

    @property
    def update_eval(self):
        raise NotImplementedError
        
    @property
    def html(self):
        raise NotImplementedError

    @property
    def js_init(self):
        return ""

class TextElement(Element):
    def __init__(self, key, title=None, value=None):
        super(TextElement, self).__init__(key, title)
        self.value = value

    @property
    def update_eval(self):
        code = """$('#{0}').html("{1}")""".format(self.uuid, self.value)
        return code
    
    @property
    def html(self):
        return """
        <div class="panel panel-default">
            <div class="panel-heading">
	      <h3 class="panel-title">{0}</h3>
	    </div>
	    <div class="panel-body" id="{1}">
	    </div>
	</div>""".format(self.title, self.uuid)
        

class SliderElement(Element):
    def __init__(self, key, title=None, value=None):
        super(SliderElement, self).__init__(key, title)
        self.value = value

    @property
    def update_eval(self):
        code = """$('#{0}').slider('setValue', {1})""".format(self.uuid, self.value)
        return code

    @property
    def js_init(self):
        code = """$('#{0}').slider().on('change', function(ev){{
                      $.ajax({{url:'/update/{0}/' + ev.value.newValue}});
                      worker();
                   }});""".format(self.uuid)
        return code

    @property
    def html(self):
        return """
        <div class="panel panel-default">
            <div class="panel-heading">
	      <h3 class="panel-title">{0}</h3>
	    </div>
	    <div class="panel-body">
              <input id="{1}" type="text" style="width: 100%;"" value="" data-slider-min="0" data-slider-max="1000" data-slider-step="1" data-slider-orientation="horizontal" data-slider-selection="after" data-slider-tooltip="show">
	    </div>
	</div>""".format(self.title, self.uuid)
    
if __name__ == '__main__':
    print "Hello, World!"

    el = TextElement(key="hello", title="Title", value="Hello, World")
    print el.html
