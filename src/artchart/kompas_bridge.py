from . import colors


class KompasBridge_v7():
    def __init__(self,
            kompas_api7_module,
            kompas6_constants,
            kompas_document_2d):

        self.consts = kompas6_constants

        # api 7
        self.api7 = kompas_api7_module
        self.doc2d = kompas_document_2d
        self.vlm = self.doc2d.ViewsAndLayersManager

        self.macro_objects = dict()
        self.macro_object_containers = dict()
        self.layers = dict()

    def init(self, config):
        self.view_init(config.get("view_name"))

        self.dc = self.api7.IDrawingContainer(self.view)

        self.ls = self.view.Layers
        self.dts = self.dc.DrawingTexts
        self.lss = self.dc.LineSegments
        self.rs  = self.dc.Rectangles
        self.mos = self.dc.MacroObjects


    def view_init(self, view_name = None):
        if view_name:
            self.view = self.vlm.Views.Add(self.consts.vt_Normal)
            self.view.Name = view_name
            self.view.X = 0
            self.view.Y = 0
            self.view.Scale = 1.0
            self.view.Update()
        else:
            self.view = self.vlm.Views.ActiveView


    def draw_rect(self, x0, y0, w, h, style = 1):
        rect = self.rs.Add()
        rect.X = x0
        rect.Y = y0
        rect.Width = w
        rect.Height = h
        rect.Style = style
        rect.Update()
        return rect


    def draw_line(self, x1, y1, x2, y2, style = 1):
        line = self.lss.Add()
        line.X1 = x1
        line.Y1 = y1
        line.X2 = x2
        line.Y2 = y2
        line.Style = style
        line.Update()
        return line


    def draw_text(self, x0, y0, text):
        dt = self.dts.Add()
        dt.Allocation = self.consts.ksAlCentre
        dt.X = x0
        dt.Y = y0

        it = self.api7.IText(dt)
        it.Style = self.consts.ksTSDefault
        it.Str = text

        dt.Update()
        return dt


    def layer_new(self, name = "Слой", color = colors.RANDOM):
        L = self.ls.Add()
        L.Color = color
        L.Name = name
        L.Update()
        self.layers[name] = L


    def macro_start(self, name = "Макро", to_layer = False, color = colors.RANDOM):
        macro = self.mos.Add()
        macro.Name = name

        if to_layer:
            if (color == colors.RANDOM):
                color = colors.random_color()

            self.layer_new(name, color = color)
            macro.LayerNumber = self.layers[name].LayerNumber

        self.macro_objects[name] = macro


    def macro_add(self, name = "Макро", obj = None):
        m = self.macro_objects.get(name)
        if (m):
            m.AddObjects(obj)
        else:
            # TODO: Warning
            pass


    def macro_end(self, name = "Макро"):
        self.macro_objects[name].Update()
