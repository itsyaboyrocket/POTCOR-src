# Source Generated with Decompyle++
# File: ShipPilot.pyc (Python 2.4)

from pandac.PandaModules import *
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.InputStateGlobal import inputState
from direct.task.Task import Task
from direct.controls.PhysicsWalker import PhysicsWalker
import math

class ShipPilot(PhysicsWalker):
    notify = directNotify.newCategory('ShipPilot')
    wantDebugIndicator = base.config.GetBool('want-avatar-physics-indicator', 0)
    MAX_STRAIGHT_SAIL_BONUS = 2.1000000000000001
    STRAIGHT_SAIL_BONUS_TIME = 18.0
    REVERSE_STRAIGHT_SAIL_BONUS_TIME = -8.0
    TURNING_BONUS_REDUCTION = 3.0
    
    def __init__(self, gravity = -32.173999999999999, standableGround = 0.70699999999999996, hardLandingForce = 16.0):
        PhysicsWalker.__init__(self, gravity, standableGround, hardLandingForce)
        self._ShipPilot__speed = 0.0
        self._ShipPilot__rotationSpeed = 0.0
        self._ShipPilot__slideSpeed = 0.0
        self._ShipPilot__vel = Vec3(0.0)
        self.currentTurning = 0.0
        self.ship = None
        self.pusher = None
        self.straightHeading = 0
        self.cNodePath = None
        self.actorNode = None

    
    def setWalkSpeed(self, forward, jump, reverse, rotate):
        PhysicsWalker.setWalkSpeed(self, forward, 0, reverse, rotate)

    
    def setWallBitMask(self, bitMask):
        self.wallBitmask = bitMask

    
    def adjustWallBitMask(self, oldMask, newMask):
        self.wallBitmask = self.wallBitmask & ~oldMask
        self.wallBitmask |= newMask
        if self.cNodePath and not self.cNodePath.isEmpty():
            self.cNodePath.node().setFromCollideMask(self.wallBitmask)
        

    
    def setFloorBitMask(self, bitMask):
        self.floorBitmask = bitMask

    
    def setShip(self, ship):
        self.setAvatar(ship)

    
    def setAvatar(self, ship):
        if ship is None:
            if self.ship is not None and base.controlForce.getPhysicsObject() == self.ship.node().getPhysicsObject():
                base.controlForce.clearPhysicsObject()
                base.controlForce.setVector(Vec3(0))
            
            self.takedownPhysics()
            self.setCollisionsActive(0)
            self.ship = ship
        else:
            base.controlForce.setPhysicsObject(ship.node().getPhysicsObject())
            self.ship = ship
            self.setupPhysics(ship)
            self.setCollisionsActive(1)

    
    def initializeCollisions(self, collisionTraverser, cRootNodePath, bow, stern, starboard, port):
        self.cTrav = collisionTraverser
        self.cRootNodePath = cRootNodePath
        self.bowPos = bow.getPos(cRootNodePath)
        self.sternPos = stern.getPos(cRootNodePath)
        self.starboardPos = starboard.getPos(cRootNodePath)
        self.portPos = port.getPos(cRootNodePath)

    
    def setupCollisions(self):
        if self.pusher:
            return None
        
        self.pusher = CollisionHandlerPusher()
        self.pusher.setInPattern('enter%in')
        self.pusher.setOutPattern('exit%in')
        sRadius = abs(self.portPos - self.starboardPos[0] / 2.0)
        cNode = CollisionNode('SP.cNode')
        frontPos = self.bowPos[1] + sRadius
        rearPos = self.sternPos[1] - sRadius
        cBowSphere = CollisionSphere(0.0, frontPos, 0.0, sRadius)
        cSternSphere = CollisionSphere(0.0, rearPos, 0.0, sRadius)
        midSphereRadius = max(sRadius, (rearPos - frontPos - sRadius * 2) / 2)
        cMidSphere = CollisionSphere(0.0, frontPos + (rearPos - frontPos) / 2, 0.0, midSphereRadius)
        cNode.addSolid(cBowSphere)
        cNode.addSolid(cMidSphere)
        cNode.addSolid(cSternSphere)
        shipIColRoot = self.ship.getInteractCollisionRoot()
        self.cNodePath = shipIColRoot.attachNewNode(cNode)
        shipLen = abs(self.sternPos[1] - self.bowPos[1])
        self.cNodePath.setScale(1, 1, 1)
        self.pusher.addCollider(self.cNodePath, self.shipNodePath)
        self.pusher.setHorizontal(True)
        self.ship.getWallCollisions().stash()

    
    def setCollisionsActive(self, active = 1):
        if active:
            self.setupCollisions()
        
        if self.collisionsActive != active:
            self.collisionsActive = active
            self.collisionsActive = active
            shipCollWall = self.ship.getWallCollisions()
            if active:
                self.cNodePath.node().setFromCollideMask(self.wallBitmask)
                self.cNodePath.node().setIntoCollideMask(BitMask32.allOff())
                self.cTrav.addCollider(self.cNodePath, self.pusher)
                shipCollWall.stash()
            else:
                self.cTrav.removeCollider(self.cNodePath)
                shipCollWall.unstash()
                self.oneTimeCollide()
        

    
    def deleteCollisions(self):
        del self.cTrav
        if hasattr(self, 'cNodePath'):
            self.cNodePath.removeNode()
            self.cNodePath = None
            del self.pusher
        

    
    def setupPhysics(self, shipNodePath):
        if shipNodePath is None:
            return None
        
        self.takedownPhysics()
        self.shipNodePath = shipNodePath
        self.actorNode = shipNodePath.node()

    
    def takedownPhysics(self):
        pass

    
    def setTag(self, key, value):
        self.cNodePath.setTag(key, value)

    
    def setAvatarPhysicsIndicator(self, indicator):
        self.cNodePath.show()
        if indicator:
            change = render.attachNewNode('change')
            change.setScale(0.10000000000000001)
            indicator.reparentTo(change)
            indicatorNode = render.attachNewNode('physVelocityIndicator')
            indicatorNode.setPos(self.shipNodePath, 0.0, 0.0, 6.0)
            indicatorNode.setColor(0.0, 0.0, 1.0, 1.0)
            change.reparentTo(indicatorNode)
            self.physVelocityIndicator = indicatorNode
            contactIndicatorNode = render.attachNewNode('physContactIndicator')
            contactIndicatorNode.setScale(0.25)
            contactIndicatorNode.setP(90.0)
            contactIndicatorNode.setPos(self.shipNodePath, 0.0, 0.0, 5.0)
            contactIndicatorNode.setColor(1.0, 0.0, 0.0, 1.0)
            indicator.instanceTo(contactIndicatorNode)
            self.physContactIndicator = contactIndicatorNode
        else:
            print 'failed load of physics indicator'

    
    def avatarPhysicsIndicator(self, task):
        self.physVelocityIndicator.setPos(self.shipNodePath, 0.0, 0.0, 6.0)
        physObject = self.actorNode.getPhysicsObject()
        a = physObject.getVelocity()
        self.physVelocityIndicator.setScale(math.sqrt(a.length()))
        a += self.physVelocityIndicator.getPos()
        self.physVelocityIndicator.lookAt(Point3(a))
        contact = self.actorNode.getContactVector()
        if contact == Vec3.zero():
            self.physContactIndicator.hide()
        else:
            self.physContactIndicator.show()
            self.physContactIndicator.setPos(self.shipNodePath, 0.0, 0.0, 5.0)
            point = Point3(contact + self.physContactIndicator.getPos())
            self.physContactIndicator.lookAt(point)
        return Task.cont

    
    def displayDebugInfo(self):
        onScreenDebug.add('w controls', 'ShipPilot')
        onScreenDebug.add('w ship', self.ship)
        onScreenDebug.add('w isAirborne', self.isAirborne)
        onScreenDebug.add('posDelta1', self.shipNodePath.getPosDelta(render).pPrintValues())
        physObject = self.actorNode.getPhysicsObject()
        physObject = physObject.getVelocity()
        onScreenDebug.add('w physObject vec', physObject.pPrintValues())
        onScreenDebug.add('w physObject len', '% 10.4f' % physObject.length())
        onScreenDebug.add('orientation', self.actorNode.getPhysicsObject().getOrientation().pPrintValues())

    
    def handleAvatarControls(self, task):
        if not self.ship:
            return Task.done
        
        physObject = self.actorNode.getPhysicsObject()
        contact = self.actorNode.getContactVector()
        forward = inputState.isSet('forward')
        reverse = inputState.isSet('reverse')
        if not inputState.isSet('slideLeft'):
            pass
        turnLeft = inputState.isSet('turnLeft')
        if not inputState.isSet('slideRight'):
            pass
        turnRight = inputState.isSet('turnRight')
        slide = inputState.isSet('slide')
        slideLeft = 0
        slideRight = 0
        jump = inputState.isSet('jump')
        if self.ship.getIsAutoSailing():
            forward = 1
            reverse = 0
        else:
            forward = 0
        dt = ClockObject.getGlobalClock().getDt()
        minSpeed = (self.ship.acceleration + self.ship.speedboost) * self.ship.speednerf
        minStraightSail = (1.0 / self.MAX_STRAIGHT_SAIL_BONUS) * self.STRAIGHT_SAIL_BONUS_TIME * self.ship.speednerf
        if reverse:
            if self.straightHeading < 0:
                self.straightHeading -= dt * self.TURNING_BONUS_REDUCTION * 2.0
            else:
                self.straightHeading -= dt * self.TURNING_BONUS_REDUCTION * 4.0
        elif self.straightHeading < minStraightSail and forward:
            self.straightHeading += dt * 1.5
        elif self.ship.threatCounter:
            self.straightHeading = min(minStraightSail, self.straightHeading)
        elif turnLeft and turnRight or not forward:
            if forward and self.straightHeading - dt * self.TURNING_BONUS_REDUCTION < minStraightSail and self.straightHeading >= minStraightSail:
                self.straightHeading = minStraightSail
            else:
                self.straightHeading -= dt * self.TURNING_BONUS_REDUCTION
        elif forward:
            self.straightHeading += dt
        
        if reverse:
            self.straightHeading = max(self.REVERSE_STRAIGHT_SAIL_BONUS_TIME, self.straightHeading)
        else:
            self.straightHeading = max(0.0, min(self.STRAIGHT_SAIL_BONUS_TIME, self.straightHeading))
        straightSailBonus = 0.0
        straightSailBonus = self.straightHeading / self.STRAIGHT_SAIL_BONUS_TIME
        straightSailBonus = min(self.MAX_STRAIGHT_SAIL_BONUS, straightSailBonus * self.MAX_STRAIGHT_SAIL_BONUS)
        self._ShipPilot__speed = self.ship.acceleration
        avatarSlideSpeed = self.ship.acceleration * 0.5 * straightSailBonus
        if forward or reverse:
            if (slideLeft or -avatarSlideSpeed) and slideRight:
                pass
        self._ShipPilot__slideSpeed = avatarSlideSpeed
        if not slide:
            if (turnLeft or self.ship.turnRate) and turnRight:
                pass
        self._ShipPilot__rotationSpeed = -(self.ship.turnRate)
        self._ShipPilot__speed *= straightSailBonus * self.ship.speednerf
        self._ShipPilot__speed += self.ship.speedboost
        self._ShipPilot__slideSpeed *= straightSailBonus
        debugRunning = inputState.isSet('debugRunning')
        if debugRunning:
            self._ShipPilot__speed *= base.debugRunningMultiplier
            self._ShipPilot__slideSpeed *= base.debugRunningMultiplier
            self._ShipPilot__rotationSpeed *= 1.25
        
        self.currentTurning += self._ShipPilot__rotationSpeed
        if self.currentTurning > self.ship.maxTurn:
            self.currentTurning = self.ship.maxTurn
        elif self.currentTurning < -(self.ship.maxTurn):
            self.currentTurning = -(self.ship.maxTurn)
        
        if turnLeft or turnRight:
            mult = 0.90000000000000002
        elif forward or reverse:
            mult = 0.81999999999999995
        else:
            mult = 0.80000000000000004
        self.currentTurning *= mult
        if self.currentTurning < 0.001 and self.currentTurning > -0.001:
            self.currentTurning = 0.0
        
        self._ShipPilot__rotationSpeed = self.currentTurning
        messenger.send('setShipSpeed-%s' % self.ship.getDoId(), [
            self._ShipPilot__speed,
            self.getMaxSpeed()])
        if self.wantDebugIndicator:
            self.displayDebugInfo()
        
        if self.needToDeltaPos:
            self.setPriorParentVector()
            self.needToDeltaPos = 0
        
        physVel = physObject.getVelocity()
        physVelLen = physVel.length()
        if not physVel.almostEqual(Vec3(0), 0.10000000000000001) and self._ShipPilot__speed and self._ShipPilot__slideSpeed or self._ShipPilot__rotationSpeed:
            distance = self._ShipPilot__speed
            goForward = True
            if distance < 0:
                goForward = False
            
            slideDistance = self._ShipPilot__slideSpeed
            rotation = self._ShipPilot__rotationSpeed
            if debugRunning:
                rotation *= 4
            
            self._ShipPilot__vel = Vec3(Vec3.forward() * distance + Vec3.right() * slideDistance)
            rotMat = Mat3.rotateMatNormaxis(self.shipNodePath.getH(), Vec3.up())
            step = rotMat.xform(self._ShipPilot__vel)
            newVector = Vec3(step)
            if goForward:
                maxLen = self._ShipPilot__speed
            else:
                maxLen = self.ship.reverseAcceleration
            if newVector.length() > maxLen:
                if not debugRunning:
                    pass
                if not base.localAvatar.getTurbo():
                    newVector.normalize()
                    newVector *= maxLen
                
            base.controlForce.setVector(newVector)
            o = physObject.getOrientation()
            r = LRotationf()
            r.setHpr(Vec3(rotation * dt, 0.0, 0.0))
            physObject.setOrientation(o * r)
            self.actorNode.updateTransform()
            messenger.send('avatarMoving')
        else:
            goForward = True
        self.actorNode.setContactVector(Vec3.zero())
        oldPosDelta = self.shipNodePath.getPosDelta(render)
        oldDt = dt
        if oldDt:
            self.ship.worldVelocity = oldPosDelta * (1 / oldDt)
        
        if self.wantDebugIndicator:
            onScreenDebug.add('w __oldPosDelta vec', oldPosDelta.pPrintValues())
            onScreenDebug.add('w __oldPosDelta len', '% 10.4f' % oldPosDelta.length())
            onScreenDebug.add('w __oldDt', '% 10.4f' % oldDt)
            onScreenDebug.add('w worldVelocity vec', self.ship.worldVelocity.pPrintValues())
            onScreenDebug.add('w worldVelocity len', '% 10.4f' % self.ship.worldVelocity.length())
        
        if hasattr(self.ship, 'currentTurning'):
            self.ship.currentTurning = self.currentTurning
        
        return Task.cont

    
    def getMaxSpeed(self):
        return self.ship.acceleration * self.MAX_STRAIGHT_SAIL_BONUS + self.ship.speedboost

    
    def getVelocity(self):
        return self._ShipPilot__vel

    
    def enableAvatarControls(self):
        self.straightHeading = 0
        self.setCollisionsActive(1)
        taskName = 'ShipControls-%s' % (id(self),)
        taskMgr.remove(taskName)
        taskMgr.add(self.handleAvatarControls, taskName, 25)
        if self.physVelocityIndicator:
            taskMgr.add(self.avatarPhysicsIndicator, 'ShipControlsIndicator%s' % (id(self),), 35)
        
        if self.ship:
            self.ship.localControl = True
        

    
    def disableAvatarControls(self):
        base.controlForce.setVector(Vec3(0))
        self.straightHeading = 0
        taskName = 'ShipControls-%s' % (id(self),)
        taskMgr.remove(taskName)
        taskName = 'ShipControlsIndicator%s' % (id(self),)
        taskMgr.remove(taskName)
        if self.ship:
            self.ship.worldVelocity = Vec3(0)
        
        self._ShipPilot__speed = 0
        self._ShipPilot__vel = 0
        if self.actorNode:
            self.actorNode.getPhysicsObject().setVelocity(0)
        
        if self.ship:
            messenger.send('setShipSpeed-%s' % self.ship.getDoId(), [
                self._ShipPilot__speed,
                self.getMaxSpeed()])
            self.ship.localControl = False