import math
import pymel.core as pm


class Spherize(object):
    def __init__(self):
        sel = pm.selected()
        verts = self.prepSel(sel)

        points = PointsArray([p.getPosition() for p in verts])
        ctr = points.getCenter()

        normals = VectorsArray([n.getNormal() for n in verts])
        normalPlane = normals.averageVector()

        pointsNew = points.projectOrtho(ctr, normalPlane)

        radius = pointsNew.getDist(ctr)
        for i in range(len(pointsNew)):
            pointsNew[i] = self.sphere(ctr, radius, pointsNew[i])

        for i in range(len(pointsNew)):
            pointsNew[i] = self.linePlaneInter(points[i], normals[i], pointsNew[i], normalPlane)

        for i in range(len(verts)):
            verts[i].setPosition(pointsNew[i], space='world')

        pm.select(sel)

    def prepSel(self, sel):
        sel = pm.polyListComponentConversion(sel, tv=True)
        pm.select(sel)
        pm.polySelectConstraint(pp=3, type=0x0001)
        verts = pm.ls(sl=True, fl=True)
        return verts

    def getDist(self, ctr, points):
        dist = 0
        for p in points:
            dist += self.length(ctr, p)
        return dist / len(points)

    def sphere(self, ctr, radius, point):
        vec = point - ctr
        vec.normalize()
        vec = vec * radius
        return vec + ctr

    def linePlaneInter(self, points, normals, pointsNew, normalPlane):
        pointsNew = pointsNew - (normalPlane * 10000000)
        t = ((points - pointsNew) * normals) / (normals * normalPlane)
        intersection = (normalPlane * t) + pointsNew
        return intersection


def evenVerts(target, normal, center, radius, offset):
    pass


class PointsArray(list):
    def __init__(self, *args):
        list.__init__(self, *args)

    def getCenter(self):
        pointsSum = sum(self)
        return pointsSum / len(self)

    def projectOrtho(self, ctr, pNrm):
        newPoints = []
        for p in self:
            vec = p - ctr
            dist = vec * pNrm
            offset = pNrm * dist
            newPoints.append(p - offset)
        return PointsArray(newPoints)

    def getDist(self, ctr):
        dist = 0
        for p in self:
            dist += self.length(ctr, p)
        return dist / len(self)

    def length(self, ctr, p):
        d = 0.0
        for i in range(len(ctr)):
            d += (ctr[i] - p[i]) * (ctr[i] - p[i])
        return math.sqrt(d)


class VectorsArray(list):
    def __init__(self, *args):
        list.__init__(self, *args)

    def averageVector(self):
        vecSum = sum(self)
        return (vecSum / len(self)).normal()
