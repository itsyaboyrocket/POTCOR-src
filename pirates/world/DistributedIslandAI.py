from direct.distributed.DistributedCartesianGridAI import DistributedCartesianGridAI
from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
from direct.directnotify import DirectNotifyGlobal
from pirates.battle.Teamable import Teamable

class DistributedIslandAI(DistributedCartesianGridAI, DistributedGameAreaAI, Teamable):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedIslandAI')
    
    def __init__(self, air, islandModel, name, uid):
        DistributedGameAreaAI.__init__(self, air, islandModel, name, uid)
        DistributedCartesianGridAI.__init__(self, air, 2000, 1, 1, 1)
        Teamable.__init__(self)

        self.parentingRules = ['island', '2000:10:20']
        self.islandTransform = [1, 1, 1, 1]
        self.zoneSphereSize = [1, 1, 1]
        self.zoneSphereCenter = [1, 1]

        self.islandModel = islandModel

        self.undockable = True
        self.portCollisionSpheres = []
        self.feastFireEnabled = False
        self.fireworkShowEnabled = [False, 0]

    def generate(self):
        DistributedGameAreaAI.generate(self)
        DistributedCartesianGridAI.generate(self)

    def announceGenerate(self):
        DistributedGameAreaAI.announceGenerate(self)
        DistributedCartesianGridAI.announceGenerate(self)

    def setParentingRules(self, todo0, todo1):
        pass

    def d_setParentingRules(self, todo0, todo1):
        pass

    def b_setParentingRules(self, todo0, todo1):
        pass

    def getParentingRules(self):
        return self.parentingRules

    def setIslandTransform(self, todo0, todo1, todo2, todo3):
        pass

    def d_setIslandTransform(self, todo0, todo1, todo2, todo3):
        pass

    def b_setIslandTransform(self, todo0, todo1, todo2, todo3):
        pass

    def getIslandTransform(self):
        return self.islandTransform

    def setZoneSphereSize(self, todo0, todo1, todo2):
        pass

    def d_setZoneSphereSize(self, todo0, todo1, todo2):
        pass

    def b_setZoneSphereSize(self, todo0, todo1, todo2):
        pass

    def getZoneSphereSize(self):
        return self.zoneSphereSize

    def setZoneSphereCenter(self, todo0, todo1):
        pass

    def d_setZoneSphereCenter(self, todo0, todo1):
        pass

    def b_setZoneSphereCenter(self, todo0, todo1):
        pass

    def getZoneSphereCenter(self):
        return self.zoneSphereCenter

    def setIslandModel(self, todo0):
        pass

    def d_setIslandModel(self, todo0):
        pass

    def b_setIslandModel(self, todo0):
        pass

    def getIslandModel(self):
        return self.islandModel

    def setUndockable(self, todo0):
        pass

    def d_setUndockable(self, todo0):
        pass

    def b_setUndockable(self, todo0):
        pass

    def getUndockable(self):
        return self.undockable

    def setPortCollisionSpheres(self, todo0):
        pass

    def d_setPortCollisionSpheres(self, todo0):
        pass

    def b_setPortCollisionSpheres(self, todo0):
        pass

    def getPortCollisionSpheres(self):
        return self.portCollisionSpheres

    def makeLavaErupt(self):
        self.sendUpdate('makeLavaErupt', [])

    def requestEntryToIsland(self):
        pass

    def deniedEntryToIsland(self):
        self.sendUpdate('deniedEntryToIsland', [])

    def setFeastFireEnabled(self, todo0):
        pass

    def d_setFeastFireEnabled(self, todo0):
        pass

    def b_setFeastFireEnabled(self, todo0):
        pass

    def getFeastFireEnabled(self):
        return self.feastFireEnabled

    def setFireworkShowEnabled(self, todo0, todo1):
        pass

    def d_setFireworkShowEnabled(self, todo0, todo1):
        pass

    def b_setFireworkShowEnabled(self, todo0, todo1):
        pass

    def getFireworkShowEnabled(self):
        return self.fireworkShowEnabled