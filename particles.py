import pygame as pag, random
from pygame.math import Vector2

class Particles:
    def __init__(self, surface,type:int=1,movent=True,radius:int=4,lighting_number:int=3, gravity = 0,pos=(0,0),vel=[0,0],
        color = 'white', lighting_color = (20,20,20), degrad_vel= 0.1) -> None:
        self.particles = []
        self.con = 0
        self.surface = surface
        self.type = type
        self.radius = radius
        self.lighting_number = lighting_number
        self.gravity = gravity
        self.movent = movent
        self.color = color
        self.lighting_color = lighting_color
        self.degrad_vel = degrad_vel

        self.last_pos = 0

        if self.type == 3:
            # self.timer = 0
            self.particles.append([Vector2(pos), Vector2(vel),self.radius])

    def update(self, coord = (0,0), pos = None,dt= 1) -> None:
        if pos == None:pos = pag.math.Vector2(coord)
        if self.movent:
            if self.con:
                self.con = 0
                self.speed = self.last_pos - coord

                if self.type == 1:
                    if self.speed[0] != 0 or self.speed[1] != 0:
                        self.particles.append([pag.math.Vector2(pos),[random.randint(int(self.speed[0]-1),int(self.speed[0]+1)),random.randint(int(self.speed[1]-1),int(self.speed[1]+1))],random.randint(self.radius/2,self.radius*2)])
                elif self.type == 2:
                    if self.speed[0] != 0 or self.speed[1] != 0:
                        self.particles.append([pag.math.Vector2(pos), [0,0],self.radius])
            else:
                self.con = 1
                self.last_pos = pag.math.Vector2(coord)
        else:
            if self.type == 1:
                self.particles.append([pag.math.Vector2(pos), [random.randint(-3, 3), random.randint(-6, -3)], (random.random()*self.radius/2) + self.radius*2])
            elif self.type == 2:
                self.particles.append([pag.math.Vector2(pos), [0,0],self.radius])


        if self.type == 1:
            for i,part in sorted(enumerate(self.particles),reverse=True):
                part[0][0] += part[1][0]
                part[0][1] += part[1][1]
                part[1][1] += self.gravity
                part[2] -= self.degrad_vel
                if part[2] < 0:
                    self.particles.pop(i)
        elif self.type == 2:
            for i,part in sorted(enumerate(self.particles),reverse=True):
                part[2] -= self.degrad_vel
                if part [2] < 0:
                    self.particles.pop(i)
        elif self.type == 3:
            for i,part in sorted(enumerate(self.particles),reverse=True):
                part[0][0] += part[1][0]
                part[0][1] += part[1][1]
                part[2] -= 0.15
                if part[2] < 0:
                    return True


    def lighting_func(self,radius):
        surf = pag.surface.Surface((radius*2,radius*2))
        pag.draw.circle(surf, self.lighting_color, (radius,radius), radius)
        surf.set_colorkey((0,0,0))
        return surf

    def draw(self) -> None:
        if self.type == 1:
            for i,part in sorted(enumerate(self.particles),reverse=True):
                if self.lighting_number > 0:
                    radius = int(part[2])*1.5
                    self.surface.blit(self.lighting_func(radius),[int(part[0].x)-radius,int(part[0].y)-radius], special_flags= pag.BLEND_RGB_ADD)
                if self.lighting_number > 1:
                    radius = int(part[2])*2
                    self.surface.blit(self.lighting_func(radius),[int(part[0].x)-radius,int(part[0].y)-radius], special_flags= pag.BLEND_RGB_ADD)
                if self.lighting_number > 2:
                    radius = int(part[2])*3
                    self.surface.blit(self.lighting_func(radius),[int(part[0].x)-radius,int(part[0].y)-radius], special_flags= pag.BLEND_RGB_ADD)
                pag.draw.circle(self.surface, self.color, [int(part[0].x),int(part[0].y)], int(part[2]))
        elif self.type == 2:
            for i,part in sorted(enumerate(self.particles),reverse=True):
                if self.lighting_number > 0:
                    radius = int(part[2])*1.5
                    self.surface.blit(self.lighting_func(radius),[int(part[0].x)-radius,int(part[0].y)-radius], special_flags= pag.BLEND_RGB_ADD)
                if self.lighting_number > 1:
                    radius = int(part[2])*2
                    self.surface.blit(self.lighting_func(radius),[int(part[0].x)-radius,int(part[0].y)-radius], special_flags= pag.BLEND_RGB_ADD)
                if self.lighting_number > 2:
                    radius = int(part[2])*3
                    self.surface.blit(self.lighting_func(radius),[int(part[0].x)-radius,int(part[0].y)-radius], special_flags= pag.BLEND_RGB_ADD)
                pag.draw.circle(self.surface, self.color, [int(part[0][0]),int(part[0][1])], int(part[2]))
        elif self.type == 3:
            for i,part in sorted(enumerate(self.particles),reverse=True):
                if self.lighting_number > 0:
                    radius = int(part[2])*1.5
                    self.surface.blit(self.lighting_func(radius),[int(part[0].x)-radius,int(part[0].y)-radius], special_flags= pag.BLEND_RGB_ADD)
                if self.lighting_number > 1:
                    radius = int(part[2])*2
                    self.surface.blit(self.lighting_func(radius),[int(part[0].x)-radius,int(part[0].y)-radius], special_flags= pag.BLEND_RGB_ADD)
                if self.lighting_number > 2:
                    radius = int(part[2])*3
                    self.surface.blit(self.lighting_func(radius),[int(part[0].x)-radius,int(part[0].y)-radius], special_flags= pag.BLEND_RGB_ADD)
                pag.draw.circle(self.surface, self.color, [int(part[0][0]),int(part[0][1])], int(part[2]))



    def clear(self):
        self.particles.clear()
        