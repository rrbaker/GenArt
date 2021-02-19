
w = 500   ## WIDTH
h = 500   ## HEIGHT

qtc = 4     ## Quadtree capacity
num = 5000  ## Number of particles
dis = 20    ## Target proximity from other particles
parts = []  ## Empty array for all the particles

def setup():
    global pc
    size(w, h)
    rectMode(CENTER)
    fill(10, 20, 60)
    noStroke()
    
    ## Randomly place some particles in the center
    for _ in range(num):
        x = random(.2*w, .8*w)
        y = random(.2*h, .8*h)
        parts.append(Particle(x, y))

    pc = Sim(parts, dis, qtc)
    pc.refresh()

def draw():
    background(255)
    text(str(floor(frameRate)) + "__" + str(len(parts)), 10, 10)
    # for _ in range(100):
    #     np = []
    #     x = random(w)
    #     y = random(h)
        # pc.data.query(Rectangle(x, y, 50, 50), np)
        # pc.data.insert(Particle(x, y))
    pc.data.show()
    # pc.data = None
    pc.data = QuadTree(pc.bound, qtc)
    for p in parts:
        pc.data.insert(p)
    # pc.run()
    # pc.refresh()

class Sim(object):
    def __init__(self, particles, prox, dataMax):
        self.particles = particles  ## Array of Particles
        self.prox = prox            ## Target proximity from other particles
        
        self.bound = Rectangle(w*.5, h*.5, w, h)
        self.data = QuadTree(self.bound, dataMax)
    
    def run(self):
        self.refresh()
        self.posistion()
        self.display()
    
    def refresh(self):
        self.data.refresh()
        for p in self.particles:
            self.data.insert(p)
    
    def posistion(self):
        for p in self.particles:
            area = Rectangle(p.pos.x, p.pos.y, self.prox, self.prox)
            nearPoints = []
            self.data.query(area, nearPoints)
            for newp in nearPoints:
                p.bounce(newp)
                newp.bounce(p)
            p.move()
            p.walls()

    def display(self):
        for p in self.particles:
            circle(p.pos.x, p.pos.y, 5)

class Particle(object):
    def __init__(self, ix, iy):
        self.pos = Vec(ix, iy)
        self.vel = Vec(random(-5, 5), random(-5, 5))
        self.acc = Vec(0, 0)
    
    def bounce(self, part):
        force = Vec(part.pos.x, part.pos.y)
        force.vecSub(self.pos)
        d = constrain(force.magnitude(), .01, 20)
        ma = -10 / d
        force.vecSetMag(ma)
        self.acc.vecAdd(force)
    
    def walls(self):
        if self.pos.x < 50: 
            self.vel.x *= -1
            self.pos.x = 50
        elif self.pos.x > w - 50:
            self.vel.x *= -1
            self.pos.x = w - 50
        if self.pos.y < 50:
            self.vel.y *= -1
            self.pos.y = 50
        elif self.pos.y > h - 50:
            self.vel.y *= -1
            self.pos.y = h-50
        
    def move(self):
        self.vel.vecAdd(self.acc)
        self.pos.vecAdd(self.vel)
        self.vel.scalMult(0.9)
        self.acc.scalMult(0.)
        
class Vec(object):
    def __init__(self, ix, iy):
        self.x = ix
        self.y = iy
        
    def vecAdd(self, nvec):
        self.x += nvec.x
        self.y += nvec.y
        
    def scalMult(self, scal):
        self.x *= scal
        self.y *= scal

    def magnitude(self):
        return sqrt(sq(self.x) + sq(self.y))
    
    def vecSub(self, nvec):
        self.x -= nvec.x
        self.y -= nvec.y
        
    def vecNorm(self):
        h = self.magnitude()+1
        self.x /= h
        self.y /= h
        
    def vecLimit(self, lim):
        h = self.magnitude()
        if h > lim:
            self.vecSetMag(lim)
            
    def vecSetMag(self, val):
        self.vecNorm()
        self.x *= val
        self.y *= val
        
class Rectangle(object):
    def __init__(self, ix, iy, iw, ih):
        self.x = ix
        self.y = iy
        self.w = iw
        self.h = ih
        self.hw = self.w*0.5
        self.hh = self.h*0.5
    
    def contains(self, p):
        return (
            p.pos.x >= self.x - self.hw and
            p.pos.x < self.x + self.hw and
            p.pos.y >= self.y - self.hh and
            p.pos.y < self.y + self.hh)
        
    def intersects(self, area):
        return not (
                area.x - area.hw > self.x + self.hw or
                area.x + area.hw < self.x - self.hw or
                area.y - area.hh > self.y + self.hh or
                area.y + area.hh < self.y - self.hh)
        
class QuadTree(object):
    def __init__(self, boundary, n):
        self.boundary = boundary
        self.capacity = n
        self.points = []
        self.divided = False
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None
        
    def refresh(self):
        self.points = []
        if self.divided:
            self.northeast = None
            self.northwest = None
            self.southeast = None
            self.southwest = None
        self.divided = False
        
    def insert(self, newPoint):
        if not self.boundary.contains(newPoint):
            return False
        if len(self.points) < self.capacity:
            self.points.append(newPoint)
            return True
        else:
            if not self.divided:
                self.subdivide()
                
            if   self.southeast.insert(newPoint): return True
            elif self.northwest.insert(newPoint): return True
            elif self.northeast.insert(newPoint): return True
            elif self.southwest.insert(newPoint): return True
            
    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h
        wh = 0.5 * w
        hh = 0.5 * h
        qw = 0.25 * w
        qh = 0.25 * h
        
        ne = Rectangle(x + qh, y - qh, wh, hh)
        self.northeast = QuadTree(ne, self.capacity)
        
        nw = Rectangle(x - qh, y - qh, wh, hh)
        self.northwest = QuadTree(nw, self.capacity)
        
        se = Rectangle(x + qh, y + qh, wh, hh)
        self.southeast = QuadTree(se, self.capacity)
        
        sw = Rectangle(x - qh, y + qh, wh, hh)
        self.southwest = QuadTree(sw, self.capacity)
        
        self.divided = True
        
    def query(self, area, found):
        if not self.boundary.intersects(area): return
        else:
            for p in self.points:
                if area.contains(p): found.append(p)
            if self.divided:
                self.northeast.query(area, found)
                self.northwest.query(area, found)
                
                self.southwest.query(area, found)
                self.southeast.query(area, found)

        return found
    
    def show(self):
        if self.divided:
            x = self.boundary.x
            y = self.boundary.y
            hw = self.boundary.hw
            hh = self.boundary.hh
            
            pushStyle()
            noFill()
            stroke(255, 200, 200)
            line(x - hw, y, x + hw, y)
            line(x, y - hh, x, y + hh)
            popStyle()

            self.northeast.show()
            self.northwest.show()
            self.southeast.show()
            self.southwest.show()
