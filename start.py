#git: khoa070104
import turtle as t
from math import ceil
from svgpathtools import svg2paths2
import numpy as np

#1
def read_svg(path="pic.svg", seg_unit=8):
    # Đọc file SVG và chuyển đổi thành danh sách các đường đa giác
    paths, attrs, svg_attr = svg2paths2(path)
    svg_size = (float(svg_attr['width'].replace('px','')),
                float(svg_attr['height'].replace('px','')) )
    viewbox = [float(f) for f in svg_attr['viewBox'].split(' ')]

    polys = []
    for path in paths:
        poly = []
        for subpaths in path.continuous_subpaths():
            points = []
            for seg in subpaths:
                interp_num = ceil(seg.length()/seg_unit)
                points.append(seg.point(np.arange(interp_num)/interp_num))
            points = np.concatenate(points)
            points = np.append(points, points[0])
            poly.append(points)
        polys.append([[(p.real, p.imag) for p in pl] for pl in poly])
    return (polys, attrs, svg_size, viewbox)


#2
def head_to(t, x, y, draw=True, have_sprite=True):
    # Di chuyển bút tới một vị trí cụ thể, với hoặc không vẽ đường dẫn và/hoặc hiển thị hình ảnh sprite
    wasdown = t.isdown()
    heading = t.towards(x,y)
    t.pen(pendown=draw)
    t.seth(heading)
    t.clearstamps()
    t.goto(x,y)
    t.stamp()
    t.pen(pendown=wasdown)


#3
def draw_polygon(t, poly, fill='black', stroke='black', have_sprite=True):
    # Vẽ một đa giác với màu fill và stroke được chỉ định
    if fill=='none':
        fill = 'black'
    t.color(stroke, fill)
    p = poly[0]
    head_to(t, p[0], -(p[1]), False, have_sprite)
    for p in poly[1:]: 
        head_to(t, p[0], -(p[1]), have_sprite=have_sprite)
    t.up()


#4
def draw_multipolygon(t, mpoly, fill='black', stroke='black', have_sprite=True):
    # Vẽ một tập hợp các đa giác với màu fill và stroke được chỉ định
    p = mpoly[0][0]
    head_to(t, p[0], -(p[1]), False, have_sprite)
    if fill != 'none':
        t.begin_fill()
    for i, poly in enumerate(mpoly):
        draw_polygon(t, poly, fill, stroke, have_sprite)
        if i != 0:
            head_to(t, p[0], -(p[1]), False, have_sprite)
    if fill != "none":
        t.end_fill()


def main():
    # Đọc và vẽ các đối tượng từ file SVG
    polys, attrs, svg_size, viewbox = read_svg()
    svg_w, svg_h = (viewbox[2] - viewbox[0], viewbox[3] - viewbox[1])
    svg_m = min(svg_w, svg_h)
    ar = svg_w / svg_h

    # Thiết lập cửa sổ vẽ turtle
    window = t.Screen()
    win_m = min(window.window_width(), window.window_height())
    if ar > 1:
        window.setup(win_m * ar, win_m)
    else:
        window.setup(win_m, win_m / ar)
    scale = win_m / svg_m

    # Cài đặt turtle và vùng vẽ
    t.reset()
    t.speed(0)
    t.setworldcoordinates(viewbox[0] * 1.1, -viewbox[3] * 1.1, viewbox[2] * 1.1, -viewbox[1] * 1.1)
    t.mode(mode='world')
    t.tracer(n=10, delay=0)

    # Vẽ từng đa giác
    for poly, attr in zip(polys, attrs):
        if 'style' in attr.keys():
            attr.update({attrs.split(':')[0]: attrs.split(':')[1] for attrs in attr['style'].split(';')})
        if 'stroke' not in attr.keys():
            attr['stroke'] = attr['fill']

        t.pen(outline=0.5 * scale)
        if 'stroke-width' in attr.keys():
            t.pen(outline=float(attr['stroke-width']) * scale, pencolor='black') 

        if 'fill' in attr.keys():
            draw_multipolygon(t, poly, fill=attr['fill'], stroke=attr['stroke'])

    # Hoàn thành vẽ
    t.tracer(n=1, delay=0)
    head_to(t, viewbox[2], -viewbox[3], False)
    t.clearstamps()
    t.penup()


if __name__ == '__main__':
    main()
