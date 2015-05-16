import uuid


class Element(object):

    def __init__(self, key, title):
        self.uuid = uuid.uuid4().hex
        self.key = key
        self.title = title
        self.width = 1


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

    def __init__(self, key, title=None, value=None, width=1, range=(0, 1000)):
        super(SliderElement, self).__init__(key, title)
        self.value = value
        self.range = range
        self.width = width

    @property
    def update_eval(self):
        code = """$('#{0}').slider('setValue', {1})""".format(
            self.uuid, self.value)
        return code

    @property
    def js_init(self):
        code = """$('#{0}').slider();
                  $('#{0}').slider().on('change', function(ev){{
                      $.ajax({{
                        type: "POST",
                        url:'/update',
                        data: JSON.stringify({{id: "{0}",
                                value: ev.value.newValue}}),
                        contentType: 'application/json'
                        }});
                      //worker();
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
              <input id="{1}" type="text" style="width: 100%;" value="" data-slider-min="{2}" data-slider-max="{3}" data-slider-step="1" data-slider-orientation="horizontal" data-slider-selection="after" data-slider-tooltip="show">
        </div>
    </div>""".format(self.title, self.uuid, self.range[0], self.range[1])


class CheckBoxElement(Element):

    def __init__(self, key, title=None, label=None, value=False):
        super(CheckBoxElement, self).__init__(key, title)
        self.value = value
        self.label = label

    @property
    def update_eval(self):
        code = """$('#{0}').prop('checked', {1});""".format(
            self.uuid, str(self.value).lower())
        return code

    @property
    def js_init(self):
        code = """$('#{0}').on('change', function(ev){{
                    $.ajax({{
                        type: "POST",
                        url:'/update',
                        data: JSON.stringify({{id: "{0}",
                                value: this.checked}}),
                        contentType: 'application/json'
                        }});
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
            <label>{1}
              <input id="{2}" type="checkbox">
            </label>
        </div>
    </div>""".format(self.title, self.label, self.uuid)

if __name__ == '__main__':
    print "Hello, World!"

    el = TextElement(key="hello", title="Title", value="Hello, World")
    print el.html
