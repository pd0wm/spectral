import uuid


class Element(object):

    def __init__(self, key, title):
        self.uuid = uuid.uuid4().hex
        self.key = key
        self.title = title
        self.width = 1

    @property
    def js_init(self):
        return ""


# class TextElement(Element):

#     def __init__(self, key, title=None, value=None):
#         super(TextElement, self).__init__(key, title)
#         self.value = value

#     @property
#     def update_eval(self):
#         self.has_changed = False
#         code = """$('#{0}').html("{1}")""".format(self.uuid, self.value)
#         return code

#     @property
#     def html(self):
#         return """
#         <div class="panel panel-default">
#             <div class="panel-heading">
#           <h3 class="panel-title">{0}</h3>
#         </div>
#         <div class="panel-body" id="{1}">
#         </div>
#     </div>""".format(self.title, self.uuid)


class SliderElement(Element):

    def __init__(self, key, title=None, value=None, width=1, range=(0, 1000), step=1, scale='linear'):
        super(SliderElement, self).__init__(key, title)
        self.value = value
        self.range = range
        self.width = width
        self.step = step
        self.scale = scale

        self.context = {
            'title': self.title,
            'id': self.uuid,
            'min': self.range[0],
            'max': self.range[1],
            'scale': self.scale,
            'step': self.step
        }
        self.template = "element_slider.html"

    @property
    def js_init(self):
        return "Control.register(new SliderElement('{0}', '{1}'));".format(self.uuid, self.key)


class CheckboxElement(Element):

    def __init__(self, key, title=None, label=None, value=False):
        super(CheckboxElement, self).__init__(key, title)
        self.value = value
        self.label = label

        self.context = {
            'title': self.title,
            'label': self.label,
            'id': self.uuid
        }
        self.template = "element_checkbox.html"

    @property
    def js_init(self):
        return "Control.register(new CheckboxElement('{0}', '{1}'));".format(self.uuid, self.key)


class VisualisationElement(Element):

    def __init__(self, key, title=None, value=None, default_type='fft', default_datatype='src_data', width=3):
        super(VisualisationElement, self).__init__(key, title)
        self.width = width
        self.value = value
        self.default_type = default_type
        self.default_datatype = default_datatype

        self.context = {
            'vtype': self.default_type,
            'dtype': self.default_datatype,
            'id': self.uuid
        }
        self.template = "element_visualisation.html"

    @property
    def js_init(self):
        return "Control.register(new VisualisationElement('{0}', '{1}'));".format(self.uuid, self.key)


class SweepElement(Element):

    def __init__(self, key, title=None, value=None, default_datatype='src_data', width=6):
        super(SweepElement, self).__init__(key, title)
        self.width = width
        self.value = value
        self.default_datatype = default_datatype

    @property
    def update_eval(self):
        pass

    @property
    def js_init(self):
        code = """
        Visualisation.init("{0}");
        $("#{0}").on("change", ".visualisation-data", function() {{
            Visualisation.init("{0}");
        }});""".format(self.uuid)
        return code

    @property
    def html(self):
        return """
        <div class="visualisation sweep" id="{0}">
            <div class="visualisation-header" style="overflow:auto;">
                <h3 style="float:left;"></h3>
                <table class="visualisation-control" style="float:right;">
                    <tr class="visualisation-data">
                      <td><label><input type="radio" name="{0}-data" value="src_data" {1}/>Original</label></td>
                      <td><label><input type="radio" name="{0}-data" value="rec_data" {2}/>Reconstructed</label></td>
                    </tr>
                </table>
            </div>
            <div class="visualisation-container" id="{0}-container" ></div>
        </div>""".format(
            self.uuid,
            'checked' if self.default_datatype == 'src_data' else '',
            'checked' if self.default_datatype == 'rec_data' else ''
            )
