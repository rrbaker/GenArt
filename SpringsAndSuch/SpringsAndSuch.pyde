from PHYSICS import Particle, Vec


w = 1000
h = 1000



def setup():
    size(w, h)
    global bob
    colorMode(HSB, 360, 100, 100)
    # fill(10, 20, 60, 100)
    noStroke()
    bob = Poly()
    bob.makeCircle(w/2, h/2, 100)
    # bob.makeLine(w/4, h/2, .75*w, h/2)
    


def draw():
    # background(240, 230, 240)
    background(0, 0, 0)
    bob.display()
    bob.spawnNode()
    bob.setIndex()
    bob.organize()
    
    # bob.points[0].attract(Particle(mouseX, mouseY))
    


class Poly(object):
    def __init__(self):
        self.points = []
    
    def setIndex(self):
        i = 0
        for p in self.points:
            p.index = i
            i += 1
    
    def spawnNode(self):
        i = floor(random(len(self.points)))
        p1 = self.points[i]
        p2 = self.points[(i+1)%len(self.points)]
        nx = lerp(p1.pos.x, p2.pos.x, 0.5)
        ny = lerp(p1.pos.y, p2.pos.y, 0.5)
        self.points.insert(i+1, Particle(nx, ny, p1.vel.x, p1.vel.y))
    
    def organize(self):
        l = len(self.points)
        for p1 in self.points:
            for p2 in self.points:
                if p1 != p2:
                    if indexInRange(p1.index, p2.index, 1, l):
                        p1.attract(p2)
                    elif indexInRange(p1.index, p2.index, 10, l):
                        p1.repulse(p2)
        # i = -1
        # for _ in range(len(self.points)):
        #     p1 = self.points[i]
        #     p2 = self.points[i+1]
            
        for p in self.points:
            p.update()
    
    def makeLine(self, x1, y1, x2, y2):
        amt = 0
        while amt < 1:
            nx = lerp(x1, x2, amt)
            ny = lerp(y1, y2, amt)
            self.points.append(Particle(nx, ny))
            amt += 0.1
    
    def makeCircle(self, cx, cy, dia):
        r = dia/2
        ang = 0
        while ang < 360:
            x = r * cos(radians(ang)) + cx
            y = r * sin(radians(ang)) + cy
            ang += 10
            self.points.append(Particle(x, y))
            
    
    def display(self):
        i = -1
        for _ in range(len(self.points)):
            p1 = self.points[i].pos
            p2 = self.points[i+1].pos
            # pushStyle()
            # stroke(10, 20, 60)
            # line(p1.x, p1.y, p2.x, p2.y)
            # popStyle()
            d = dist(p1.x, p1.y, p2.x, p2.y)
            amt = 0
            while amt < 1:
                h = map(i, 0, len(self.points), 0, 360)
                fill(h, 50, 100)
                # fill(random(255), random(255), random(255))
                mx = lerp(p1.x, p2.x, amt)
                my = lerp(p1.y, p2.y, amt)
                circle(mx, my, 5)
                amt += 0.1
            i += 1
        # for p in self.points:
        #     circle(p.pos.x, p.pos.y, 10)

def indexInRange(i1, i2, buff, l):
    for i in range(-buff, buff + 1):
        if ((i1 + i) % l) == i2: return True
    
    return False
