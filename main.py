#!/usr/bin/env python3

from PySide import QtGui
import random
import math

class SnowGenerator:

    def __init__(self,
        width,
        height,
        durationSeconds,
        snowCount = 80,
        snowMinSize = 2,
        snowMaxSize = 7,
        snowMinSinMult = 5,
        snowMaxSinMult = 20,
    ):
        self.width = width
        self.height = height
        self.durationSeconds = durationSeconds 
        self.snowCount = snowCount
        self.snowMinSize = snowMinSize
        self.snowMaxSize = snowMaxSize
        self.snowMinSinMult = snowMinSinMult
        self.snowMaxSinMult = snowMaxSinMult

        self.stepCount = (1000 * self.durationSeconds) // 45
        self.pixelPerStep = self.height / self.stepCount
        self.snow = QtGui.QImage('snow.png')
        self.generateSnow()

    def generateSnow(self):
        self.snow_positions = []
        self.snow_sizes = []
        self.snow_motion = []
        self.snow_sin_mult = []
        self.snow_sin_pos = []
        for i in range(self.snowCount):
            self.snow_sizes.append(random.randrange(self.snowMinSize, self.snowMaxSize + 1))
            factor = 1 - (self.snow_sizes[-1] - self.snowMinSize) / (self.snowMaxSize - self.snowMinSize)
            self.snow_sin_mult.append((self.snowMaxSinMult - self.snowMinSinMult) * factor + self.snowMinSinMult)
            self.snow_positions.append(random.randrange(int(self.snow_sin_mult[-1] * 2) + self.width) - int(self.snow_sin_mult[-1]))
            self.snow_motion.append(random.randrange(self.stepCount))
            self.snow_sin_pos.append(random.randrange(self.stepCount))

    def generateImages(self):
        buffer = QtGui.QImage(self.width, self.height, QtGui.QImage.Format_ARGB32)
        for step in range(self.stepCount):
            buffer.fill(QtGui.QColor(0, 0, 0, 0))
            painter = QtGui.QPainter(buffer)
            for snow in range(self.snowCount):
                x = self.snow_positions[snow] + math.sin(2 * ((self.snow_sin_pos[snow] + step) % self.stepCount) * math.pi / self.stepCount) * self.snow_sin_mult[snow]
                y = ((self.snow_motion[snow] + step) % self.stepCount) * self.pixelPerStep
                painter.drawImage(x, y, self.snow.scaled(self.snow_sizes[snow], self.snow_sizes[snow]))
                if y + self.snow_sizes[snow] > self.height:
                    painter.drawImage(x, -(self.height - y), self.snow.scaled(self.snow_sizes[snow], self.snow_sizes[snow]))
            painter.end()
            buffer.save('snow_{step:02d}.png'.format(step=step))

def main():
    generator = SnowGenerator(506, 263, 3)
    generator.generateImages()

if __name__ == '__main__':
    main()

