class View:
    """Handling the contents of the screen"""

    def __init__(self, owner, screen):
        self.owner = owner
        self.screen = screen
        self.x = owner.x
        self.y = owner.y
        self.rect = screen.get_rect()
        self.half_player_size = self.owner.image.get_width() // 2, self.owner.image.get_height() // 2
        # TODO: Remove redundant attribute

    def update(self, screen_size, mouse_pos, player_pos):
        self.rect.x, self.rect.y = self.owner.rect.center
        # TODO: make camera movement smoother
        # dx = mouse_pos[0] - screen_size[0] // 2
        # expected_x = screen_size[0] // 2 - dx // 2
        # if expected_x - player_pos[0] > 0:
        #     if expected_x - player_pos[0] > 10:
        #         x = player_pos[0] + 10
        #     else:
        #         x = expected_x
        # else:
        #     if expected_x - player_pos[0] < -10:
        #         x = player_pos[0] - 10
        #     else:
        #         x = expected_x
        #
        # dy = mouse_pos[1] - screen_size[1] // 2
        # expected_y = screen_size[1] // 2 - dy // 2
        # if expected_y - player_pos[1] > 0:
        #     if expected_y - player_pos[1] > 10:
        #         y = player_pos[1] + 10
        #     else:
        #         y = expected_y
        # else:
        #     if expected_y - player_pos[1] < -10:
        #         y = player_pos[1] - 10
        #     else:
        #         y = expected_y
        # return x, y
