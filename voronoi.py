import tkinter as tk
from math import sqrt
from Trie import *
import graphic_library as gl

marginx = 20
canvas_len = 600

def draw_cartesian(canvas):
    global marginx
    canvas.create_line(marginx, canvas_len, marginx + canvas_len, canvas_len, arrow="last")
    canvas.create_line(marginx, canvas_len, 20, 0, arrow="last")
    canvas.create_text(marginx, canvas_len+10, text="(0,0)")
    canvas.create_text(canvas_len+10, canvas_len+10, text="x")
    canvas.create_text(10, 5, text="y")

def canvas_point(P):
    '''Convert (x,y) coordinates to the canvas coordinates'''
    global marginx
    return P[0] + marginx, canvas_len - P[1]

def cross(u, v):
    w = [0, 0, 0]
    w[0] = u[1] * v[2] - u[2] * v[1]
    w[1] = u[2] * v[0] - u[0] * v[2]
    w[2] = u[0] * v[1] - u[1] * v[0]
    return w

def to_left(pxmin, pxmax, p):
    pxVec3D = [pxmax[0] - pxmin[0],pxmax[1] - pxmin[1],0]
    pVec3D = [p[0] - pxmax[0], p[1] - pxmax[1], 0]
    result = cross(pxVec3D, pVec3D)
    return (result[2] >= 0)

def get_x_min(poly):
    L = sorted(poly)
    return L[0]

def get_x_max(poly):
    L = sorted(poly)
    return L[-1]

def points_left(pxmin, pxmax, poly):
    L = []
    for p in poly:
        if to_left(pxmin, pxmax, p) and p != pxmax and p != pxmin:
            L.append(p)
    return L

def points_right(pxmin, pxmax, poly):
    L = []
    for p in poly:
        if to_left(pxmin, pxmax, p) == False and p != pxmax and p != pxmin:
            L.append(p)
    return L

def tri_polygone(poly):
    '''Returns the points of a polygon sorted
    in the correct order to draw a convex polygon'''
    if(len(poly) == 0):
        return []
    pxmin = get_x_min(poly)
    pxmax = get_x_max(poly)
    LG = sorted(points_left(pxmin, pxmax, poly), reverse=1)
    LD = sorted(points_right(pxmin, pxmax, poly))
    return [pxmin] + LD + [pxmax] + LG

def draw_polygon(canvas, points):
    '''Draws a polygon on the screen'''
    if(len(points) == 0):
        return
    temp = []
    for p in points:
        temp.append(canvas_point(p))
    poly = tri_polygone(temp)
    canvas.create_polygon(poly, fill="skyblue")
    for i in range(0, len(poly)):
        p1i = i % len(poly)
        p2i = (i + 1) % len(poly)
        canvas.create_line(poly[p1i], poly[p2i], fill="darkgreen")

def draw_voronoi(canvas, diagram):
    for i in range(0, len(diagram)):
        cell = diagram[i][1]
        germ = canvas_point(diagram[i][0])
        draw_polygon(canvas, cell)
        canvas.create_text(germ[0], germ[1], text="P" + str(i))

def find_intersection(diagram, cellNumber, bisection):
    '''Returns the two ends of the cell that cuts the perpendicular bisector
    and the coordinates of the points of intersection'''
    diagram[cellNumber] = (diagram[cellNumber][0], tri_polygone(diagram[cellNumber][1]))
    cell = diagram[cellNumber][1]
    result = []
    for i in range(0, len(cell)):
        p1i = i % len(cell)
        p2i = (i + 1) % len(cell)
        s = gl.intersection_segment(bisection, cell[p1i], cell[p2i])
        if s != None:
            a0, a1 = tri_polygone([cell[p1i], cell[p2i]])
            result.append({'a':((a0[0], a0[1]),(a1[0], a1[1])), 's':(s[0], s[1])})
    return sorted(result, key=lambda i: i['s'][0])

def find_neighbor(diagram, cellNumber, edge):
    point = diagram[cellNumber][0]
    ligne = ((edge[1][0] - edge[0][0], edge[1][1] - edge[0][1]), (edge[0][0], edge[0][1]))
    return gl.belongs(diagram, gl.symmetric_point(ligne, point))

def same_point(p1, p2):
    return (sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2) <= gl.EPSILON)

def keep_good_points(poly, S0, S1, Pn1, Pp):
    L = [S0, S1]
    for p in poly:
        if p != S0 and p != S1 and gl.carre_distance(p,Pn1) >= gl.carre_distance(p,Pp):
            L.append(p)
    T = tri_polygone(L)
    return T

def insert_germ(diagram, point):
    cellNumber = gl.belongs(diagram, point)
    diagram.append((point, []))
    Pp = diagram[cellNumber][0]
    bisection = gl.perp_bisector(Pp, point)
    inter = find_intersection(diagram, cellNumber, bisection)
    firstS0 = inter[0]['s']

    S0 = inter[0]['s']
    S1 = inter[1]['s']
    a1 = inter[1]['a']

    diagram[-1][1].append(S0)
    diagram[cellNumber][1].append(S0)
    diagram[cellNumber][1].append(S1)

    PiNumber = find_neighbor(diagram, cellNumber, a1)

    temp = diagram[cellNumber][1].copy()
    diagram[cellNumber] = (diagram[cellNumber][0], keep_good_points(temp, S0, S1, point, Pp))

    while not same_point(S1, firstS0):
        Pp = diagram[PiNumber][0]

        bisection = gl.perp_bisector(Pp, point)
        inter = find_intersection(diagram, PiNumber, bisection)

        newS0 = inter[0]['s']
        newS1 = inter[1]['s']

        if same_point(S0, newS0) or same_point(S1, newS1):
            S0 = newS1
            S1 = newS0
            a1 = inter[0]['a']
        else:
            S0 = newS0
            S1 = newS1
            a1 = inter[1]['a']

        diagram[-1][1].append(S0)
        diagram[PiNumber][1].append(S0)
        diagram[PiNumber][1].append(S1)

        newPiNumber = find_neighbor(diagram, PiNumber, a1)
        PiNumber = newPiNumber

def is_border(point):
    return (abs(canvas_len - point[0]) <= gl.EPSILON) or \
           (abs(point[0]) <= gl.EPSILON) or \
           (abs(canvas_len - point[1]) <= gl.EPSILON) or \
           (abs(point[1]) <= gl.EPSILON)

def capture_corners(seed):
    L = [(0, 0),(0, canvas_len),(canvas_len, 0),(canvas_len, canvas_len)]
    return sorted(L, key= lambda p: sqrt((p[0]-seed[0])**2 + (p[1]-seed[1])**2))

voronoi_diagram = [
  ((351, 205),[ (214.23833962665532, 253.1386746795724),
                (299.54702329594477, 275.4167385677308),
                (408.01388888888886, 175.62722222222226),
                (393.6515397082658, 106.11345218800648),
                (366.34635483752254, 92.67307621536082) ]),
  ((541, 104),[]),
  ((449, 460),[]),
  ((255, 114),[]),
  ((496,  65),[]),
  ((498, 296),[]),
  ((479, 542),[]),
  ((186, 569),[]),
  ((375, 524),[]),
  ((236, 448),[ (175.11498194945847, 493.6714801444043),
                (278.0491051942384, 536.206241815801),
                (300.4867582148112, 495.1689553702796),
                (298.96055776892433, 457.0139442231076),
                (213.7531365313653, 383.2767527675277) ]),
  ((  3, 566),[]),
  ((446,  12),[]),
  ((310, 362),[ (183.6344062635929, 259.92583732057415),
                (196.76223972988186, 294.7824985931345),
                (328.3383541513593, 407.00918442321824),
                (412.731848983543, 353.8725395288802),
                (402.7564102564102, 325.45765345765335),
                (299.54702329594477, 275.4167385677308),
                (214.23833962665526, 253.1386746795724) ]),
  ((374, 230),[ (299.54702329594477, 275.4167385677308),
                (402.7564102564102, 325.4576534576536),
                (444.4714240606252, 247.08399115882537),
                (408.01388888888886, 175.62722222222226) ]),
  ((496, 195),[]),
  ((281, 396),[ (196.7622397298818, 294.7824985931345),
                (213.75313653136533, 383.2767527675277),
                (298.9605577689243, 457.01394422310756),
                (328.3383541513593, 407.00918442321824) ]),
  ((117,  69),[]),
  ((361, 443),[ (298.9605577689243, 457.0139442231066),
                (300.4867582148112, 495.1689553702796),
                (399.8827285921625, 477.9894049346881),
                (422.162037340321, 362.6612184736323),
                (412.73184898354305, 353.8725395288803),
                (328.3383541513592, 407.00918442321824) ]),
  ((156, 420),[]),
  ((472, 180),[ (393.6515397082658, 106.11345218800648),
                (408.01388888888886, 175.62722222222214),
                (444.4714240606252, 247.08399115882537),
                (447.13283208020044, 246.4874686716792),
                (510.28803777544596, 145.43913955928645),
                (485.326705940108, 122.77687776141386),
                (400.44403303902016, 105.06223298205637) ])
  ]

voronoi_diagram_complete = [((351, 205),
  [(366.34635483752254, 92.67307621536084),
   (214.2383396266553, 253.13867467957243),
   (299.54702329594477, 275.4167385677308),
   (408.01388888888886, 175.6272222222222),
   (393.6515397082658, 106.11345218800648)]),
 ((541, 104),
  [(600, 0),
   (591.7333333333333, 0.0),
   (599.9999999999999, 189.80219780219778),
   (485.32670594010796, 122.7768777614139),
   (510.288037775446, 145.4391395592865)]),
 ((449, 460),
  [(600.0, 415.79573170731703),
   (600.0, 451.24390243902445),
   (430.4116174261393, 513.2884326489735),
   (422.16203734032104, 362.6612184736323),
   (399.8827285921626, 477.9894049346878)]),
 ((255, 114),
  [(316.85602094240835, 0.0),
   (366.3463548375226, 92.67307621536087),
   (214.23833962665523, 253.13867467957243),
   (215.83695652173913, 0.0),
   (136.09398496240604, 244.54511278195486),
   (183.6344062635928, 259.92583732057415)]),
 ((496, 65),
  [(591.7333333333333, 0.0),
   (511.81, 0.0),
   (400.4440330390202, 105.06223298205639),
   (485.32670594010807, 122.77687776141384)]),
 ((498, 296),
  [(600.0, 415.79573170731703),
   (402.7564102564103, 325.45765345765346),
   (600.0, 243.46039603960398),
   (412.7318489835432, 353.87253952888034),
   (422.1620373403208, 362.6612184736324),
   (447.13283208020107, 246.4874686716791),
   (444.4714240606251, 247.0839911588254)]),
 ((479, 542),
  [(600.0, 451.24390243902445),
   (600, 600),
   (415.40384615384625, 600.0000000000001),
   (430.4116174261391, 513.2884326489735)]),
 ((186, 569),
  [(293.23809523809524, 600.0),
   (278.0491051942383, 536.2062418158008),
   (93.9672131147541, 600.0),
   (95.4473451815874, 509.71194392317034),
   (175.11498194945864, 493.67148014440437)]),
 ((375, 524),
  [(430.4116174261393, 513.2884326489735),
   (415.40384615384625, 600.0000000000001),
   (293.23809523809524, 600.0),
   (278.04910519423834, 536.2062418158009),
   (399.8827285921627, 477.98940493468785),
   (300.486758214811, 495.16895537027966)]),
 ((236, 448),
  [(278.0491051942383, 536.2062418158008),
   (300.48675821481123, 495.1689553702794),
   (298.9605577689243, 457.0139442231076),
   (213.75313653136527, 383.27675276752774),
   (175.1149819494585, 493.67148014440437)]),
 ((3, 566),
  [(93.9672131147541, 600.0),
   (0, 600),
   (0.0, 409.68835616438355),
   (95.44734518158741, 509.71194392317045)]),
 ((446, 12),
  [(366.34635483752254, 92.67307621536084),
   (316.85602094240835, 0.0),
   (511.81, 0.0),
   (393.651539708266, 106.11345218800645),
   (400.4440330390202, 105.0622329820564)]),
 ((310, 362),
  [(214.2383396266553, 253.13867467957243),
   (299.54702329594505, 275.4167385677309),
   (402.75641025641056, 325.4576534576536),
   (328.3383541513594, 407.0091844232182),
   (412.7318489835434, 353.87253952888005),
   (183.63440626359292, 259.92583732057426),
   (196.76223972988183, 294.78249859313456)]),
 ((374, 230),
  [(402.7564102564103, 325.45765345765346),
   (299.54702329594505, 275.4167385677309),
   (444.4714240606253, 247.08399115882548),
   (408.0138888888889, 175.62722222222226)]),
 ((496, 195),
  [(600.0, 243.46039603960398),
   (599.9999999999999, 189.80219780219778),
   (510.28803777544596, 145.4391395592865),
   (447.1328320802006, 246.48746867167912)]),
 ((281, 396),
  [(298.9605577689243, 457.01394422310756),
   (328.33835415135934, 407.0091844232182),
   (196.76223972988186, 294.7824985931346),
   (213.75313653136536, 383.27675276752774)]),
 ((117, 69),
  [(215.83695652173913, 0.0),
   (0, 0),
   (-0.0, 259.66666666666663),
   (136.093984962406, 244.5451127819549)]),
 ((361, 443),
  [(399.8827285921627, 477.98940493468785),
   (422.16203734032104, 362.6612184736323),
   (412.7318489835432, 353.87253952888034),
   (328.3383541513594, 407.0091844232182),
   (298.9605577689243, 457.01394422310756),
   (300.48675821481123, 495.1689553702794)]),
 ((156, 420),
  [(213.75313653136527, 383.27675276752774),
   (196.76223972988186, 294.7824985931346),
   (183.63440626359292, 259.92583732057426),
   (136.09398496240604, 244.54511278195486),
   (-0.0, 259.66666666666663),
   (175.1149819494585, 493.67148014440437),
   (95.4473451815874, 509.71194392317034),
   (0.0, 409.68835616438355)]),
 ((472, 180),
  [(510.28803777544596, 145.4391395592865),
   (485.32670594010796, 122.7768777614139),
   (400.4440330390202, 105.06223298205639),
   (393.651539708266, 106.11345218800645),
   (408.01388888888886, 175.6272222222222),
   (444.4714240606253, 247.08399115882548),
   (447.13283208020107, 246.4874686716791)])]