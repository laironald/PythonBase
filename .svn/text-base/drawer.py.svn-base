import igraph.drawing 
import cairo, math, random

class MarkerDrawer(igraph.drawing.ShapeDrawer):
    def draw_path(ctx, cx, cy, w):
        w = w /(3/2.)
        cy = cy - w/4.
        adj = math.pi/5
        cxx = math.pi-adj
        cyy = 2*math.pi+adj
        ctx.arc(cx, cy, w/2., cxx, cyy)
        ctx.move_to(cx+w/2.*math.cos(cxx), cy+w/2.*math.sin(cxx))
        ctx.curve_to(cx+w/2.*math.cos(cxx), cy+w/2.*math.sin(cxx),
                     cx, cy+0.5*w+w/2.*math.sin(cxx),
                     cx, cy+w)
        ctx.curve_to(cx, cy+w,
                     cx, cy+0.5*w+w/2.*math.sin(cxx),
                     cx-w/2.*math.cos(cxx), cy+w/2.*math.sin(cxx))
        #ctx.line_to(cx, cy+w)
        #ctx.line_to(cx+w/2.*math.cos(cyy), cy+w/2.*math.sin(cyy))        
    draw_path=staticmethod(draw_path)
igraph.drawing.known_shapes['marker'] = MarkerDrawer

class ImageDrawer(igraph.drawing.ShapeDrawer):
    def draw_path(ctx, cx, cy, w):
        image = cairo.ImageSurface.create_from_png ("image.png")
        sc = float(w)/max(image.get_width(), image.get_height())
        if cx==cy:
            adjH = (w/8.)*(1-image.get_height()/image.get_width())
        else:
            adjH = (w/2.)*(1-image.get_height()/image.get_width())
        adjW = (w/4.)*(1-image.get_width()/image.get_height())
        ctx.scale (sc, sc)
        ctx.set_source_surface (image, (cx-w/2.+adjW)/sc, (cy-w/2.+adjH)/sc)
        ctx.paint()
        ctx.scale(1/sc, 1/sc)
        igraph.drawing.known_shapes["rectangle"].draw_path (ctx,
            (cx-w/2.+adjW)/sc, (cy-w/2.+adjH)/sc,
            image.get_width()/sc, image.get_height()/sc)
    draw_path=staticmethod(draw_path)
igraph.drawing.known_shapes['image'] = ImageDrawer


def drawShape(shape="marker", bottom=False,
              dimens=[32,32], canvas=[100,100],
              border=5, radius=100,
              color1=[1.,1.,1.,1.], color2=[0.,0.,0.,0.],
              filename="example.png"):
    radius = 0.01*radius*canvas[0]
    surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, dimens[0], dimens[1])
    ctx = cairo.Context (surface)
    ctx.scale (float(dimens[0])/canvas[0], float(dimens[1])/canvas[1])
    ctx.set_line_width (border)
    vshp = igraph.drawing.known_shapes[shape]
    vshp.draw_path (ctx, canvas[0]/2,
                    bottom and canvas[1]-radius/2-1e-8 or canvas[1]/2,
                    radius-border)
    ctx.set_source_rgba (*color1)
    ctx.fill_preserve ()
    ctx.set_source_rgba (*color2)
    ctx.stroke()

    surface.write_to_png (filename)

for i in range(20, 120, 20):
    drawShape(shape = "image", bottom = True, filename="ex%.3d.png" % i, radius=i, border=2, dimens=[100,100],
              color1 = [random.random(), random.random(), random.random(), 0.5],
              color2 = [0.2, 0.2, 0.2, 1.])
