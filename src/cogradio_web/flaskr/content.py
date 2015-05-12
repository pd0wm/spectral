class Content(object):
    def __init__(self):
        self._by_uuid = {}
        self._by_position = {}
        self._by_key = {}
        self.max_y = 0

    def add(self, element, position):
        if not 0 <= position[0] <= 3:
            raise Exception('x position out of bounds')
        if not position[1] >= 0:
            raise Exception('y position out of bounds')

        self.max_y = max(self.max_y, position[1])
        
        self._by_uuid[element.uuid] = element
        self._by_position[position] = element
        self._by_key[element.key] = element
    
    @property
    def html(self):
        r = ""
        for y in range(0, self.max_y + 1):
            r += """<div class="row">\n"""
            for x in range(0, 3):
                r += """<div class="col-sm-4">\n"""
                if (x, y) in self._by_position:
                    element = self._by_position[(x,y)]
                    r += element.html + "\n"
                r += """</div>\n"""
            r += """</div>\n"""
        return r

    @property
    def values(self):
        return {k: v.update_eval for k, v in self._by_uuid.items()}

if __name__ == '__main__':
    from element import TextElement
    el1 = TextElement(key="uptime", title="Uptime", value=123)
    el2 = TextElement(key="status", title="System Status", value="Critical")
    cnt = Content()
    cnt.add(el1, (0, 1))
    cnt.add(el2, (2, 0))
    
    print cnt.html
    print cnt.values
