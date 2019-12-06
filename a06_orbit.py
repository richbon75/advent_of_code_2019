
class Body:
    
    bodies = {}

    @classmethod
    def getBody(self, name):
        if name in self.bodies:
            return self.bodies[name]
        return Body(name)
    
    def __str__(self):
        if self.orbits:
            return f"Body <{self.name} orbits {self.orbits.name}>"
        return f"Body <{self.name} orbits Nothing>"
    
    def __repr__(self):
        return str(self)

    def __init__(self, name):
        if not name:
            raise ValueError("A body's gotta have a name.")
        self.name = name
        self.orbits = None
        self.bodies[name] = self
    
    def setOrbit(self, name):
        '''Set an orbit relationship - this body orbits body name'''
        self.orbits = self.getBody(name=name)
    
    def countOrbits(self, orbits=0):
        if self.orbits:
            return self.orbits.countOrbits(orbits+1)
        return orbits
    
    def pathToRoot(self, path=None):
        if path is None:
            path = list()
        path.append(self.name)
        if self.orbits:
            return self.orbits.pathToRoot(path)
        return path

# with open('a06_test.txt', 'r') as f:
# with open('a06_test2.txt', 'r') as f:
with open('a06_input.txt', 'r') as f:
    for line in f:
        line = line.strip()
        (a, b) = line.split(')')
        Body.getBody(b).setOrbit(a)

total_orbits = 0
for b in Body.bodies:
    total_orbits += Body.bodies[b].countOrbits()
print(f'(First Star) Total orbits: {total_orbits}')

youset = set(Body.getBody('YOU').pathToRoot())
sanset = set(Body.getBody('SAN').pathToRoot())
not_in_common = youset.symmetric_difference(sanset)

print(f'(Second Star) Orbital transfers from YOU to SAN: {len(not_in_common)-2}')


