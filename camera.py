import settings

class Camera:
    """Smooth horizontal camera that leads the player forward."""
    def __init__(self):
        self.x = 0

    def update(self, target_rect):
        """
        Move camera so that the target appears at (0.5 - CAMERA_LEAD) * screen width.
        We lerp toward the desired x for a bit of smoothing.
        """
        desired_x = target_rect.centerx - settings.SCREEN_WIDTH * (0.5 - settings.CAMERA_LEAD)
        if desired_x < 0:
            desired_x = 0  # don’t scroll into negative space yet
        self.x += (desired_x - self.x) * settings.CAMERA_LERP

    def apply(self, rect):
        """Return a shifted copy of *rect* accounting for camera offset."""
        return rect.move(-int(self.x), 0)
