from src.entities.CharacterBase import CharacterBase
import pygame
import math

class Player(CharacterBase):
    def __init__(self, game, world, entity_id, position, size, animation_handler, max_speed, max_health):
        super().__init__(game, world, entity_id, position, size, animation_handler, max_speed, max_health)

        self._hotbar = [None for x in range(10)] # Fixed to size 10 hardcoded
        self._hotbar_pointer = 0
        self._hotbar[0] = self._game.item_factory.create_item(self._game, self._world, "grass_block")

    @property
    def hotbar(self):
        return self._hotbar

    @property
    def hotbar_pointer(self):
        return self._hotbar_pointer

    @hotbar_pointer.setter
    def hotbar_pointer(self, value):
        if type(value) is int and 0 <= value <= 9:
            self._hotbar_pointer = value

    def get_state_data(self):
        data = {}
        data["position"] = self._position
        data["health"] = self._health
        data["velocity"] = self._velocity
        data["hotbar_pointer"] = self._hotbar_pointer
        data["hotbar"] = []

        for index, item in enumerate(self._hotbar):
            data["hotbar"][index] = item.convert_data()
        return data

    def load_state_data(self, data):
        self._position = data["position"],
        self._health = data["health"],
        self._velocity = data["velocity"]
        self._hotbar_pointer = data["hotbar_pointer"]

        for index, item in enumerate(data):
            if item is not None:
                self._hotbar[index] = self._game.item_factory.create_item(item[0], item[1])

    def update(self):
        if self._health <= 0:
            self.kill()
            return

        self._animation_handler.update()
        self._texture = pygame.transform.scale(self._animation_handler.current_frame, self._size)

        for index, item in enumerate(self._hotbar):
            if item is not None:
                if item.quantity == 0:
                    self._hotbar[index] = None
                    print("deleting")
                    del item
            else:
                continue

        deltatime = self._game.clock.get_time() / 1000
        self._velocity[1] += math.trunc(800 * deltatime)
        self.handle_inputs(deltatime)

        if abs(self._velocity[0]) > self._max_speed[0]:
            self._velocity[0] = self._max_speed[0] if self._velocity[0] > 0 else -self._max_speed[0]

        if abs(self._velocity[1]) > self._max_speed[1]:
            self._velocity[1] = self._max_speed[1] if self._velocity[1] > 0 else -self._max_speed[1]

        self._position[0] += math.trunc(self._velocity[0] * deltatime)
        self._hitbox.update(self._world.camera.get_screen_position(self._position), self._size)
        self.handle_collisions("horizontal")

        self._position[1] += math.trunc(self._velocity[1] * deltatime)
        self._hitbox.update(self._world.camera.get_screen_position(self._position), self._size)
        self.handle_collisions("vertical")

        if self._hotbar[self._hotbar_pointer] is not None:
            self._hotbar[self._hotbar_pointer].update(self._position)

    def handle_inputs(self, deltatime):
        keys_pressed = self._game.keys_pressed

        if keys_pressed[pygame.K_d]:
            if self._velocity[0] < 0:
                self._velocity[0] = 0
            self._velocity[0] += math.trunc(800 * deltatime)
        elif keys_pressed[pygame.K_a]:
            if self._velocity[0] > 0:
                self._velocity[0] = 0
            self._velocity[0] -= math.trunc(800 * deltatime)
        else:
            if not self._is_in_air:
                self._animation_handler.play_animation_from_id("idle")
            self._velocity[0] *= 0.4

            if abs(self._velocity[0]) < 1:
                self._velocity[0] = 0
            else:
                self._velocity[0] = math.trunc(self._velocity[0])

        if keys_pressed[pygame.K_w]:
            if not self._is_in_air:
                self.jump()

    def handle_collisions(self, axis):
        hitboxes_to_check = []
        for x in range(3):
            for y in range(3):
                region_check_x = self._position[0] + (x-1)*800
                region_check_y = self._position[1] + (y-1)*800

                if self._world.check_region_exists_at_position((region_check_x, region_check_y)):
                    hitboxes_to_check += self._world.get_region_at_position((region_check_x, region_check_y)).get_block_hitboxes()
                else:
                    print("Region invalid")

        if axis.lower() == "horizontal":
            for block, hitbox in hitboxes_to_check:
                if self._hitbox.colliderect(hitbox):
                    if self._velocity[0] > 0:
                        self._velocity[0] = 0
                        self._position[0] = block.position[0] - self._size[0]
                        self._hitbox.right = hitbox.left
                    elif self._velocity[0] < 0:
                        self._velocity[0] = 0
                        self._position[0] = block.position[0] + 40
                        self._hitbox.left = hitbox.right

        elif axis.lower() == "vertical":
            has_vertically_collided_below = False
            for block, hitbox in hitboxes_to_check:
                if self._hitbox.colliderect(hitbox):
                    if self._velocity[1] > 0:
                        self._velocity[1] = 0
                        self._position[1] = block.position[1] - self._size[1]
                        self._hitbox.bottom = hitbox.top
                        has_vertically_collided_below = True
                    elif self._velocity[1] < 0:
                        self._velocity[1] = 0
                        self._position[1] = block.position[1] + 40
                        self._hitbox.top = hitbox.bottom

            if has_vertically_collided_below:
                self._is_in_air = False
            else:
                self._is_in_air = True

    def jump(self):
            self._velocity[1] = -300

    def draw(self):
        self._game.window.blit(self._texture, self._world.camera.get_screen_position(self._position))
        #pygame.draw.rect(self._game.window, (0, 0, 0), pygame.Rect(self._world.camera.get_screen_position(self._position), self._size))
        #pygame.draw.rect(self._game.window, (255, 0, 0), self._hitbox)