class Content(object):

    def __init__(self):
        self._by_uuid = {}
        self._by_position = {}
        self._by_key = {}
        self.max_y = 0

    def add(self, element, position):
        if not 0 <= position[0] <= 6:
            raise Exception('x position out of bounds')
        if not position[1] >= 0:
            raise Exception('y position out of bounds')

        self.max_y = max(self.max_y, position[1])

        self._by_uuid[element.uuid] = element
        self._by_position[position] = element
        self._by_key[element.key] = element

    def set_by_uuid(self, uuid, value):
        self._by_uuid[uuid].value = value
        self._by_uuid[uuid].has_changed = True

    @property
    def js_init(self):
        r = ""
        for k, v in self._by_uuid.items():
            r += "//" + k + "\n"
            r += v.js_init
            r += "\n"
        return r

    @property
    def html(self):
        r = ""
        for y in range(0, self.max_y + 1):
            r += """<div class="row">\n"""
            for x in range(0, 5):
                if (x, y) in self._by_position:
                    element = self._by_position[(x, y)]
                    r += """<div class="col-sm-{0}">\n""".format(element.width * 2)
                    r += element.html + "\n"
                else:
                    r += """<div class="col-sm-2">\n"""
                r += """</div>\n"""
            r += """</div>\n"""
        return r

    @property
    def update_eval(self):
        return {k: v.update_eval for k, v in self._by_uuid.items() if v.has_changed}

    @property
    def values(self):
        return {k: v.value for k, v in self._by_key.items()}

if __name__ == '__main__':
    from element import TextElement
    el1 = TextElement(key="uptime", title="Uptime", value=123)
    el2 = TextElement(key="status", title="System Status", value="Critical")
    cnt = Content()
    cnt.add(el1, (0, 1))
    cnt.add(el2, (2, 0))

    print cnt.html
    print cnt.values
