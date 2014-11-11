import cv2
import cv2.cv
import numpy as np
import sys
import math


class Point:
    def __init__(self, x, y, z, r, g, b):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.g = g
        self.b = b


    def getCoord(self):
        return [self.x, self.y, self.z]

    def getColor(self):
        return [self.r, self.g, self.b]


class Texture:
    '''put texture to polygon'''

    def __init__(self, image):
        self.texture = image
        self.a = 0.0
        self.b = 0.0
        self.c = 0.0
        self.d = 0.0

    def __del__(self):
        self.texture = None

    def defineSize(self, polygon):
        maxw = -1.0
        maxh = -1.0
        minw = 10000000.0
        minh = 10000000.0
        x = 0.0
        y = 0.0
        for i in range(len(polygon.Texel)):
            if polygon.Texel[i].u > maxw:
                maxw = polygon.Texel[i].u
            if polygon.Texel[i].u < minw:
                minw = polygon.Texel[i].u
            if polygon.Texel[i].v > maxh:
                maxh = polygon.Texel[i].v
            if polygon.Texel[i].v < minh:
                minh = polygon.Texel[i].v
                # ax = x+1.0/polygon.Texel[i].u
                # ay = y+1.0/polygon.Texel[i].v
        return maxw, maxh, minw, minh

    def distanceT(self, p1, p2):
        return math.fabs(p1[0] - p2[0]), math.fabs(p1[1] - p2[1])

        # return math.sqrt(math.pow(2, p1[0]-p2[0])+math.pow(2, p1[1]-p2[1]))

    def setPlane(self, polygon):
        p1 = polygon.Vertex[1].x - polygon.Vertex[0].x
        p2 = polygon.Vertex[1].y - polygon.Vertex[0].y
        p3 = polygon.Vertex[1].z - polygon.Vertex[0].z
        p4 = polygon.Vertex[2].x - polygon.Vertex[0].x
        p5 = polygon.Vertex[2].y - polygon.Vertex[0].y
        p6 = polygon.Vertex[2].z - polygon.Vertex[0].z
        a = p2 * p6 - p3 * p5
        b = p3 * p4 - p1 * p6
        c = p1 * p5 - p2 * p4
        d = a * polygon.Vertex[0].x + b * polygon.Vertex[0].y + c * polygon.Vertex[0].z
        d = -1.0 * d
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def getZ(self, rx, ry):
        return -1.0 * ((self.a * rx + self.b * ry + self.d) / self.c)

    def isTexel(self, polygon, p):
        for i in range(len(polygon.Texel)):
            if p[0] == polygon.Texel[i].u and p[1] == polygon.Texel[i].v:
                return True
        return False

    def insidePolygon(self, polygon, p):
        i = 0
        j = len(polygon.Texel) - 1
        result = False
        if self.isTexel(polygon, p):
            return True
        for i in range(len(polygon.Texel)):
            if ((polygon.Texel[i].v > p[1]) != (polygon.Texel[j].v > p[1])) and (p[0] < (
                                (polygon.Texel[j].u - polygon.Texel[i].u) * (p[1] - polygon.Texel[i].v) / (
                                    polygon.Texel[j].v - polygon.Texel[i].v) + polygon.Texel[i].u)):
                if result is False:
                    result = True
                else:
                    result = False
            # print ((polygon.Vertex[i].y>p[1])!=(polygon.Vertex[j].y>p[1])), " ",(polygon.Vertex[i].y>p[1]), " ", (polygon.Vertex[j].y>p[1])
            j = i
        # print result
        #print p, " ", result
        return result

    def getCoord(self, polygon, texel):
        num = len(polygon.Texel)
        lix = []
        liy = []
        li = []
        ax = 0.0
        ay = 0.0
        aa = 0.0
        dd = 0.0
        du = 0.0
        dv = 0.0
        rx = 0.0
        ry = 0.0
        rz = 0.0
        for i in range(num):
            du, dv = self.distanceT(texel, [polygon.Texel[i].u, polygon.Texel[i].v])
            # print texel, " ",  [polygon.Texel[i].u, polygon.Texel[i].v]
            '''if du!=0:
                lix.append(du)
                ax = ax + 1.0/du
            if dv!=0:
                liy.append(dv)
                ay = ay + 1.0/dv'''
            dd = math.sqrt(du * du + dv * dv)
            if dd != 0:
                li.append(dd)
                aa = aa + 1.0 / dd
            else:
                return [polygon.Vertex[i].x, polygon.Vertex[i].y, polygon.Vertex[i].z]
        '''for i in range(len(lix)):
            lix[i] = 1.0/(lix[i]*ax)
        for i in range(len(liy)):
            liy[i] = 1.0/(liy[i]*ay)'''
        for i in range(len(li)):
            if li[i] != 0:
                li[i] = 1.0 / (li[i] * aa)
        for i in range(num):
            rx = rx + li[i] * polygon.Vertex[i].x
            ry = ry + li[i] * polygon.Vertex[i].y
            rz = rz + li[i] * polygon.Vertex[i].z
            '''
            rx = rx+lix[i]*polygon.Vertex[i].x
            ry = ry+liy[i]*polygon.Vertex[i].y
            rz = self.getZ(rx, ry)'''
        return [rx, ry, rz]

    def polygonDivide2D(self, border, n, option):

        if n == 4:
            #print border
            [[a, b], [c, d], [e, f], [g, h]] = border
            [A, B, C, D] = border
            E, F, G, H, I = [(a + c) / 2.0, (d + b) / 2.0], [(e + c) / 2.0, (d + f) / 2.0], [(g + e) / 2.0, (h + f) / 2.0], [(a + g) / 2.0, (h + b) / 2.0], [(a + e) / 2.0, (b + f) / 2.0]
            if option == 0:
                border1 = [A, E, I, H]
                border2 = [E, B, F, I]
                border3 = [I, F, C, G]
                border4 = [H, I, G, D]
                return [border1, border2, border3, border4]
            elif option == 2:
                border1 = [A, E, G, D]
                border2 = [E, B, C, G]
                return [border1, border2]
            elif option == 1:
                border1 = [A, B, F, H]
                border2 = [H, F, C, D]
                return [border1, border2]
        elif n == 3:
            [[a, b], [c, d], [e, f]] = border
            [A, B, C] = border
            E, F, G = [(a + c) / 2.0, (d + b) / 2.0], [(e + c) / 2.0, (d + f) / 2.0], [(e + a) / 2.0, (f + b) / 2.0]
            border1 = [A, E, G]
            border2 = [B, F, E]
            border3 = [E, F, G]
            border4 = [F, C, G]
            return [border1, border2, border3, border4]

    def polygonDivide3D(self, border, n, option):
        if n == 4:
            [[a, b, i], [c, d, j], [e, f, k], [g, h, l]] = border
            [A, B, C, D] = border
            E, F, G, H, I = [(a + c) / 2.0, (d + b) / 2.0, (i + j) / 2.0], [(e + c) / 2.0, (d + f) / 2.0,
                                                                            (k + j) / 2.0], [(g + e) / 2.0,
                                                                                             (h + f) / 2.0,
                                                                                             (k + l) / 2.0], [
                                (a + g) / 2.0, (h + b) / 2.0, (i + l) / 2.0], [(a + e) / 2.0, (b + f) / 2.0,
                                                                               (i + k) / 2.0]
            if option == 0:
                border1 = [A, E, I, H]
                border2 = [E, B, F, I]
                border3 = [I, F, C, G]
                border4 = [H, I, G, D]
                return [border1, border2, border3, border4]
            elif option == 2:
                border1 = [A, E, G, D]
                border2 = [E, B, C, G]
                return [border1, border2]
            elif option == 1:
                border1 = [A, B, F, H]
                border2 = [H, F, C, D]
                return [border1, border2]
        elif n == 3:
            [[a, b, g], [c, d, h], [e, f, i]] = border
            [A, B, C] = border
            E, F, G = [(a + c) / 2.0, (d + b) / 2.0, (g + h) / 2.0], [(e + c) / 2.0, (d + f) / 2.0, (i + h) / 2.0], [(e + a) / 2.0, (f + b) / 2.0, (g + i) / 2.0]
            border1 = [A, E, G]
            border2 = [B, F, E]
            border3 = [E, F, G]
            border4 = [F, C, G]
            return [border1, border2, border3, border4]

    def coord4D(self, polygon, vtxBorder, txBorder, mems, size):
        option = 0
        threshold = 0.5
        if abs(txBorder[0][0] - txBorder[1][0]) < threshold and abs(txBorder[2][0] - txBorder[3][0]) < threshold and abs(txBorder[0][0]-txBorder[2][0]) < threshold and abs(txBorder[1][0] - txBorder[3][0]) < threshold:
            option = 1
        if abs(txBorder[0][1] - txBorder[1][1]) < threshold and abs(txBorder[2][1] - txBorder[3][1]) < threshold and abs(txBorder[0][1] - txBorder[2][1]) < threshold and abs(txBorder[1][1] - txBorder[3][1]) < threshold:
            if option == 0:
                option = 2
            else:
                option = -1
        #print abs(txBorder[0][0] - txBorder[2][0]) < 2 and abs(txBorder[1][0] - txBorder[3][0]) < 2, abs(txBorder[0][1] - txBorder[2][1]) < 2 and abs(txBorder[1][1] - txBorder[3][1]) < 2, option
        if option == -1:
            i = math.floor((txBorder[0][0] + txBorder[2][0]) / 2.0) - size[1]
            j = math.floor((txBorder[0][1] + txBorder[2][1]) / 2.0) - size[3]
            x = (vtxBorder[0][0] + vtxBorder[2][0]) / 2.0
            y = (vtxBorder[0][1] + vtxBorder[2][1]) / 2.0
            z = (vtxBorder[0][2] + vtxBorder[2][2]) / 2.0
            if i < 0:
                i = 0
            if j < 0:
                j = 0
            if i >= len(mems[0]):
                #print "i = ", i
                i = len(mems[0])-1
            if j >= len(mems[0][0]):
                j = len(mems[0])-1
                #print "j = ", j
            #print len(mems[0]), len(mems[0][0]), i, j
            mems[0][i][j], mems[1][i][j], mems[2][i][j] = x, y, z
            #print "Reach The End"
            return 0
        elif option == 1:
            tx = self.polygonDivide2D(txBorder, 4, 0)
            vtx = self.polygonDivide3D(vtxBorder, 4, 0)
        elif option == 2:
            tx = self.polygonDivide2D(txBorder, 4, 0)
            vtx = self.polygonDivide3D(vtxBorder, 4, 0)
        else:
            tx = self.polygonDivide2D(txBorder, 4, 0)
            vtx = self.polygonDivide3D(vtxBorder, 4, 0)
        for i in range(len(tx)):
            self.coord4D(polygon, vtx[i], tx[i], mems, size)

    def coord3D(self, polygon, vtxBorder, txBorder, mems, size):
        option = 0
        threshold = 0.5
        if abs(txBorder[0][0] - txBorder[1][0]) < threshold and abs(txBorder[1][0] - txBorder[2][0]) < threshold and abs(txBorder[2][0]-txBorder[0][0]) < threshold:
            option = 1
        if abs(txBorder[0][1] - txBorder[1][1]) < threshold and abs(txBorder[1][1] - txBorder[2][1]) < threshold and abs(txBorder[2][1] - txBorder[0][1]) < threshold:
            if option == 0:
                option = 2
            else:
                option = -1
        #print abs(txBorder[0][0] - txBorder[2][0]) < 2 and abs(txBorder[1][0] - txBorder[3][0]) < 2, abs(txBorder[0][1] - txBorder[2][1]) < 2 and abs(txBorder[1][1] - txBorder[3][1]) < 2, option
        if option == -1:
            i = math.floor((txBorder[0][0] + txBorder[1][0] + txBorder[2][0]) / 3.0) - size[1]
            j = math.floor((txBorder[0][1] + txBorder[1][1] + txBorder[2][1]) / 3.0) - size[3]
            x = (vtxBorder[0][0] + vtxBorder[1][0]+vtxBorder[2][0]) / 3.0
            y = (vtxBorder[0][1] + vtxBorder[1][1]+vtxBorder[2][1]) / 3.0
            z = (vtxBorder[0][2] + vtxBorder[1][2]+vtxBorder[2][2]) / 3.0
            if i < 0:
                i = 0
            if j < 0:
                j = 0
            if i >= len(mems[0]):
                #print "i = ", i
                i = len(mems[0])-1
            if j >= len(mems[0][0]):
                j = len(mems[0])-1
                #print "j = ", j
            #print len(mems[0]), len(mems[0][0]), i, j
            mems[0][i][j], mems[1][i][j], mems[2][i][j] = x, y, z
            #print "Reach The End"
            return 0
        elif option == 1:
            tx = self.polygonDivide2D(txBorder, 3, 0)
            vtx = self.polygonDivide3D(vtxBorder, 3, 0)
        elif option == 2:
            tx = self.polygonDivide2D(txBorder, 3, 0)
            vtx = self.polygonDivide3D(vtxBorder, 3, 0)
        else:
            tx = self.polygonDivide2D(txBorder, 3, 0)
            vtx = self.polygonDivide3D(vtxBorder, 3, 0)
        for i in range(len(tx)):
            self.coord3D(polygon, vtx[i], tx[i], mems, size)

    def coord(self, polygon, mems, size):
        #print len(polygon.Texel)
        if len(polygon.Texel) == 4:
            #print len(polygon.Texel), "= 4"
            vtxBorder = [[polygon.Vertex[0].x, polygon.Vertex[0].y, polygon.Vertex[0].z],[polygon.Vertex[1].x, polygon.Vertex[1].y, polygon.Vertex[1].z], [polygon.Vertex[2].x, polygon.Vertex[2].y, polygon.Vertex[2].z], [polygon.Vertex[3].x, polygon.Vertex[3].y, polygon.Vertex[3].z]]
            txBorder = [[polygon.Texel[0].u, polygon.Texel[0].v], [polygon.Texel[1].u, polygon.Texel[1].v], [polygon.Texel[2].u, polygon.Texel[2].v], [polygon.Texel[3].u, polygon.Texel[3].v]]
            self.coord4D(polygon, vtxBorder, txBorder, mems, size)
        elif len(polygon.Texel) == 3:
            vtxBorder = [[polygon.Vertex[0].x, polygon.Vertex[0].y, polygon.Vertex[0].z], [polygon.Vertex[1].x, polygon.Vertex[1].y, polygon.Vertex[1].z], [polygon.Vertex[2].x, polygon.Vertex[2].y, polygon.Vertex[2].z]]
            txBorder = [[polygon.Texel[0].u, polygon.Texel[0].v], [polygon.Texel[1].u, polygon.Texel[1].v], [polygon.Texel[2].u, polygon.Texel[2].v]]
            self.coord3D(polygon, vtxBorder, txBorder, mems, size)
        else:
            for i in range(1, len(polygon.Texel)-1, 1):
                vtxBorder = [[polygon.Vertex[0].x, polygon.Vertex[0].y, polygon.Vertex[0].z], [polygon.Vertex[i].x, polygon.Vertex[i].y, polygon.Vertex[i].z], [polygon.Vertex[i+1].x, polygon.Vertex[i+1].y, polygon.Vertex[i+1].z]]
                txBorder = [[polygon.Texel[0].u, polygon.Texel[0].v], [polygon.Texel[i].u, polygon.Texel[i].v], [polygon.Texel[i+1].u, polygon.Texel[i+1].v]]
                self.coord3D(polygon, vtxBorder, txBorder, mems, size)

    def putTexture(self, polygon):
        self.setPlane(polygon)
        plist = []
        maxw, maxh, minw, minh = self.defineSize(polygon)

        minw = int(round(minw))
        maxw = int(round(maxw))
        minh = int(round(minh))
        maxh = int(round(maxh))
        # print minw, " ", maxw, " ", minh, " ", maxh
        mem = np.zeros((maxw - minw, maxh - minh))
        count = 0
        memdpx = np.zeros((maxw - minw, maxh - minh))
        memdpy = np.zeros((maxw - minw, maxh - minh))
        memdpz = np.zeros((maxw - minw, maxh - minh))
        lastPoint = Point(0, 0, 0, 0, 0, 0)
        mems = [memdpx, memdpy, memdpz]
        size = [maxw, minw, maxh, minh]

        # cache all required calculation

        #print polygon.Texel[0].u, polygon.Texel[1].u, polygon.Texel[2].u, polygon.Texel[3].u
        #print polygon.Texel[0].v, polygon.Texel[1].v, polygon.Texel[2].v, polygon.Texel[3].v
        #print minw, maxw, minh, maxh
        self.coord(polygon, mems, size)
        for i in range(minw, maxw):
            for j in range(minh, maxh):
                if self.insidePolygon(polygon, [float(i), float(j)]):
                    mem[i - minw][j - minh] = 1
                    # print mem[i-minw][j-minh]
                    #print memdpx[i - minw][j - minh], memdpy[i - minw][j - minh], memdpz[i - minw][j - minh]
        extendtype = -1

        '''for i in range (len(mem)):
            for j in range(len(mem[i])):
                print mem[i][j]'''
        threshold = 1
        temppl = []
        for i in range(minw, maxw - threshold, threshold):
            #if i == minw:
            #    print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
            #print "(", i, minw,")"
            for j in range(minh, maxh - threshold, threshold):
                extendtype = 10000
                if mem[i - minw][j - minh] == 1:
                    dp = [memdpx[i - minw][j - minh], memdpy[i - minw][j - minh], memdpz[i - minw][j - minh]]
                    lastPoint = Point(dp[0], dp[1], dp[2], self.texture[j, i, 0], self.texture[j, i, 1],
                                      self.texture[j, i, 2])
                    if dp[0]!=0 or dp[1]!=0 or dp[2]!=0:
                        extendtype = extendtype + 1
                        plist.append(lastPoint)
                        count = count + 1;
                    #if i == minw:
                     #   temppl.append(lastPoint)
                if mem[i + threshold - minw][j - minh] == 1:
                    dp = [memdpx[i + threshold - minw][j - minh], memdpy[i + threshold - minw][j - minh],
                          memdpz[i + threshold - minw][j - minh]]
                    if dp[0]!=0 or dp[1]!=0 or dp[2]!=0:
                        lastPoint = Point(dp[0], dp[1], dp[2], self.texture[j, i + threshold, 0], self.texture[j, i + threshold, 1],
                                          self.texture[j, i + threshold, 2])
                        extendtype = extendtype + 10
                        plist.append(lastPoint)
                        count = count + 1;
                    #if i == minw:
                     #   temppl.append(lastPoint)
                if mem[i + threshold - minw][j + threshold - minh] == 1:
                    dp = [memdpx[i + threshold - minw][j + threshold - minh], memdpy[i + threshold - minw][j + threshold - minh],
                          memdpz[i + threshold - minw][j + threshold - minh]]
                    #print i, j, self.texture.shape
                    if dp[0]!=0 or dp[1]!=0 or dp[2]!=0:
                        lastPoint = Point(dp[0], dp[1], dp[2], self.texture[j + threshold, i + threshold, 0], self.texture[j + threshold, i + threshold, 1],
                                          self.texture[j + threshold, i + threshold, 2])
                        extendtype = extendtype + 100
                        plist.append(lastPoint)
                        count = count + 1;
                    #if i == minw:
                     #   temppl.append(lastPoint)
                if mem[i - minw][j + threshold - minh] == 1:
                    dp = [memdpx[i - minw][j + threshold - minh], memdpy[i - minw][j + threshold - minh],
                          memdpz[i - minw][j + threshold - minh]]
                    if dp[0]!=0 or dp[1]!=0 or dp[2]!=0:
                        lastPoint = Point(dp[0], dp[1], dp[2], self.texture[j + threshold, i, 0], self.texture[j + threshold, i, 1],
                                          self.texture[j + threshold, i, 2])
                        extendtype = extendtype + 1000
                        plist.append(lastPoint)
                        count = count + 1;
                    #if i == minw:
                     #   temppl.append(lastPoint)
                #if i == minw:
                #    print "i = w, count = ", count
                if count == 3:
                    plist.append(lastPoint)
                    #continue
                elif count == 2:
                    p2 = plist.pop()
                    p1 = plist.pop()
                    '''
                    ex = lambda x, y: 2*x-y
                    if extendtype == 10011:
                        if i+threshold<maxw and j-threshold>=minw:
                            dp1 = [memdpx[i - minw][j - threshold - minh], memdpy[i - minw][j - threshold - minh], memdpz[i - minw][j - threshold - minh]]
                            dp2 = [memdpx[i + threshold - minw][j - threshold - minh], memdpy[i + threshold - minw][j - threshold - minh], memdpz[i + threshold - minw][j - threshold - minh]]
                            dp1 = map( ex, p1.getCoord(), dp1)
                            dp2 = map( ex, p2.getCoord(), dp2)
                            plist.append(p1)
                            plist.append(p2)
                            plist.append(Point(dp2[0], dp2[1], dp2[2], p2.r, p2.g, p2.b))
                            #plist.append(Point(dp2[0], dp2[1], dp2[2], 0, 255, 0))
                            plist.append(Point(dp1[0], dp1[1], dp1[2], p1.r, p1.g, p1.b))
                            #plist.append(Point(dp1[0], dp1[1], dp1[2], 255, 0, 0))
                    elif extendtype == 10101:
                        continue
                    elif extendtype == 11001:
                        if j+threshold<maxh and i-threshold>=minw:
                            dp1 = [memdpx[i - threshold- minw][j - minh], memdpy[i - threshold- minw][j - minh], memdpz[i - threshold- minw][j - minh]]
                            dp2 = [memdpx[i - threshold - minw][j + threshold - minh], memdpy[i - threshold - minw][j + threshold - minh], memdpz[i - threshold - minw][j + threshold - minh]]
                            dp1 = map( ex, p1.getCoord(), dp1)
                            dp2 = map( ex, p2.getCoord(), dp2)
                            plist.append(p1)
                            plist.append(Point(dp1[0], dp1[1], dp1[2], p1.r, p1.g, p1.b))
                            #plist.append(Point(dp1[0], dp1[1], dp1[2], 255, 0, 0))
                            plist.append(Point(dp2[0], dp2[1], dp2[2], p2.r, p2.g, p2.b))
                            #plist.append(Point(dp2[0], dp2[1], dp2[2], 0, 255, 0))
                            plist.append(p2)
                    elif extendtype == 10110:
                        if i+2*threshold<maxw and j+threshold<maxh and i-minw>=0:
                            dp1 = [memdpx[i + 2*threshold- minw][j - minh], memdpy[i + 2*threshold- minw][j - minh], memdpz[i + 2*threshold- minw][j - minh]]
                            dp2 = [memdpx[i + 2*threshold - minw][j + threshold - minh], memdpy[i + 2*threshold - minw][j + threshold - minh], memdpz[i + 2*threshold - minw][j + threshold - minh]]
                            dp1 = map( ex, p1.getCoord(), dp1)
                            dp2 = map( ex, p2.getCoord(), dp2)
                            plist.append(Point(dp1[0], dp1[1], dp1[2], p1.r, p1.g, p1.b))
                            #plist.append(Point(dp1[0], dp1[1], dp1[2], 255, 0, 0))
                            plist.append(p1)
                            plist.append(p2)
                            plist.append(Point(dp2[0], dp2[1], dp2[2], p2.r, p2.g, p2.b))
                            #plist.append(Point(dp2[0], dp2[1], dp2[2], 0, 255, 0))
                    elif extendtype == 11010:
                        continue
                    elif extendtype == 11100:
                        if i+threshold<maxw and j+2*threshold<maxh and i-minw>=0:
                            dp1 = [memdpx[i + threshold - minw][j +2*threshold- minh], memdpy[i + threshold - minw][j +2*threshold- minh], memdpz[i + threshold - minw][j +2*threshold- minh]]
                            dp2 = [memdpx[i - minw][j +2*threshold- minh], memdpy[i - minw][j +2*threshold- minh], memdpz[i - minw][j +2*threshold- minh]]
                            dp1 = map( ex, p1.getCoord(), dp1)
                            dp2 = map( ex, p2.getCoord(), dp2)
                            plist.append(Point(dp2[0], dp2[1], dp2[2], p2.r, p2.g, p2.b))
                            #plist.append(Point(dp2[0], dp2[1], dp2[2], 0, 255, 0))
                            plist.append(Point(dp1[0], dp1[1], dp1[2], p1.r, p1.g, p1.b))
                            #plist.append(Point(dp2[0], dp2[1], dp2[2], 0, 255, 0))
                            plist.append(p1)
                            plist.append(p2)
                            '''
                elif count == 1:
                    plist.pop()
                elif count == 4:
                    #print "else i is ", i, "minw is ", minw
                    '''
                    if i == minw:
                        print "i is minw =",i
                        p1 = temppl[0]
                        p2 = temppl[3]
                        ex = lambda x, y: 2*x-y
                        dp1 = temppl[1].getCoord()[:]
                        dp2 = temppl[2].getCoord()[:]
                        dp1 = map( ex, p1.getCoord(), dp1)
                        dp2 = map( ex, p2.getCoord(), dp2)
                        plist.append(Point(dp2[0], dp2[1], dp2[2], p2.r, p2.g, p2.b))
                        plist.append(p1)
                        plist.append(p2)
                        plist.append(Point(dp1[0], dp1[1], dp1[2], p1.r, p1.g, p1.b))
                        '''
                count = 0
                temppl = []
            #print "i = ", i, "minw = ", minw
        # print "zzzzzzzzzzzzzzzzzzzzzz"
        return plist
						

				
		
