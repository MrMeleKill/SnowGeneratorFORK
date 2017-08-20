#!/usr/bin/env python3

from PySide import QtGui
import random
import math

class BubbleGenerator:

    def __init__(self,
        width,
        height,
        durationSeconds,
        bubbleCount = 30,
        bubbleMinSize = 8,
        bubbleMaxSize = 30,
        bubbleMinSinMult = 5,
        bubbleMaxSinMult = 20,
    ):
        self.width = width
        self.height = height
        self.durationSeconds = durationSeconds 
        self.bubbleCount = bubbleCount
        self.bubbleMinSize = bubbleMinSize
        self.bubbleMaxSize = bubbleMaxSize
        self.bubbleMinSinMult = bubbleMinSinMult
        self.bubbleMaxSinMult = bubbleMaxSinMult

        self.stepCount = (1000 * self.durationSeconds) // 40
        self.pixelPerStep = self.height / self.stepCount
        self.bubble = QtGui.QImage('bubble.png')
        self.generateBubbles()

    def generateBubbles(self):
        self.bubble_positions = []
        self.bubble_sizes = []
        self.bubble_motion = []
        self.bubble_sin_mult = []
        self.bubble_sin_pos = []
        for i in range(self.bubbleCount):
            self.bubble_sizes.append(random.randrange(self.bubbleMinSize, self.bubbleMaxSize + 1))
            factor = 1 - (self.bubble_sizes[-1] - self.bubbleMinSize) / (self.bubbleMaxSize - self.bubbleMinSize)
            self.bubble_sin_mult.append((self.bubbleMaxSinMult - self.bubbleMinSinMult) * factor + self.bubbleMinSinMult)
            self.bubble_positions.append(random.randrange(
                int(self.bubble_sin_mult[-1]) + 1,
                self.width - self.bubble_sizes[-1] - int(self.bubble_sin_mult[-1])
            ))
            self.bubble_motion.append(random.randrange(self.stepCount))
            self.bubble_sin_pos.append(random.randrange(self.stepCount))

    def generateImages(self):
        buffer = QtGui.QImage(self.width, self.height, QtGui.QImage.Format_ARGB32)
        for step in range(self.stepCount):
            buffer.fill(QtGui.QColor(0, 0, 0, 0))
            painter = QtGui.QPainter(buffer)
            for bubble in range(self.bubbleCount):
                x = self.bubble_positions[bubble] + math.sin(2 * ((self.bubble_sin_pos[bubble] + step) % self.stepCount) * math.pi / self.stepCount) * self.bubble_sin_mult[bubble]
                y = ((self.bubble_motion[bubble] + step) % self.stepCount) * self.pixelPerStep
                painter.drawImage(x, y, self.bubble.scaled(self.bubble_sizes[bubble], self.bubble_sizes[bubble]))
                if y + self.bubble_sizes[bubble] > self.height:
                    painter.drawImage(x, -(self.height - y), self.bubble.scaled(self.bubble_sizes[bubble], self.bubble_sizes[bubble]))
            painter.end()
            buffer.save('bubbles_{step:02d}.png'.format(step=step))

def main():
    generator = BubbleGenerator(384, 263, 2)
    generator.generateImages()

if __name__ == '__main__':
    main()

