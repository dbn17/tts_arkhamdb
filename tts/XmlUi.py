fstring = """
<button
  onClick="{onClick}"
  position="{position}"
  width="{width}"
  height="{height}"
  fontsize="{fontsize}">
{text}
</button>
"""
  
class Button:

    def __init__(self, onClick, position, width, height, fontsize, text):
        self.onClick = onClick
        self.position = position
        self.width = width
        self.height = height
        self.fontsize = fontsize
        self.text = text

    def render(self):
        strPos = [str(p) for p in self.position]
        r = fstring.format(onClick=self.onClick, position=" ".join(strPos),
                           width=self.width, height=self.height,
                           fontsize=self.fontsize, text=self.text)
        r = r.replace("\n", "\\n")
        r = r.replace('"', '\\"')
        return r
