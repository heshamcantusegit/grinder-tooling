class BoundingRectangle(object):

    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.right = left + width
        self.bottom = top + height
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def starting_point(self):
        return self.left, self.top

    def ending_point(self):
        return self.right, self.bottom
