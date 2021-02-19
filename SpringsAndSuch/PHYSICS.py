
class Particle(object):
    def __init__(self, x, y, vx=0, vy=0, ax=0, ay=0):
        self.pos = Vec(x, y)
        self.vel = Vec(vx, vy)
        self.acc = Vec(ax, ay)
        self.index = 0
    
    def attract(self, part):
        force = Vec(part.pos.x, part.pos.y)
        force.vecSub(self.pos)
        d = force.magnitude()
        ma = 0.025 * constrain(d, 1, 1000)
        force.vecSetMag(ma)
        self.acc.vecAdd(force)
    
    def repulse(self, part):
        force = Vec(part.pos.x, part.pos.y)
        force.vecSub(self.pos)
        d = force.magnitude()
        ma = -0.5 / constrain(d, 0.1, 1000)
        force.vecSetMag(ma)
        self.acc.vecAdd(force)
    
    def update(self):
        self.vel.vecAdd(self.acc)
        self.pos.vecAdd(self.vel)
        self.acc.scalMult(0)
        self.damp(0.96)
        
    def damp(self, val=0.9):
        self.vel.scalMult(val)

class Vec(object):
    def __init__(self, ix, iy, iz=0):
        self.x = ix
        self.y = iy
        self.z = iz
    
    def vecAdd(self, nvec):
        self.x += nvec.x
        self.y += nvec.y
    
    def vecSub(self, nvec):
        self.x -= nvec.x
        self.y -= nvec.y
    
    def scalMult(self, scal):
        self.x *= scal
        self.y *= scal
    
    def magnitude(self):
        return sqrt( sq(self.x) + sq(self.y) )
    
    def vecNorm(self):
        m = self.magnitude()
        if m == 0: return
        self.x /= m
        self.y /= m
    
    def vecLimit(self, val):
        m = self.magnitude()
        if m > val:
            self.vecSetMag(val)
    
    def vecSetMag(self, val):
        self.vecNorm()
        self.scalMult(val)
