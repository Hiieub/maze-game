import pygame
import cv2
import mediapipe as mp

class Player:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.player_size = 20
        # self.rect = pygame.Rect(self.x, self.y, self.player_size, self.player_size)
        # self.color = (0, 0, 255)
        self.velX = 0
        self.velY = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 2
        
        self.player_image = pygame.image.load("img/player/player.png").convert_alpha()
        self.player_image = pygame.transform.scale(self.player_image, (self.player_size, self.player_size))

        # Mediapipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1)
        self.mp_draw = mp.solutions.drawing_utils
        self.hand_landmarks = None
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

    def process_hand_gesture(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    
                    cv2.circle(frame, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
            
            self.hand_landmarks = result.multi_hand_landmarks[0]

            index_finger_tip = self.hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]

            screen_width, screen_height = pygame.display.get_surface().get_size()
            hand_x = int(index_finger_tip.x * screen_width)
            hand_y = int(index_finger_tip.y * screen_height)

            self.left_pressed = False
            self.right_pressed = False
            self.up_pressed = False
            self.down_pressed = False

            center_x, center_y = screen_width // 2, screen_height // 2  

            if hand_x < center_x - 20:
                self.left_pressed = True  # trasi
            elif hand_x > center_x + 20:
                self.right_pressed = True  # phải

            if hand_y < center_y - 20:
                self.up_pressed = True  # lên
            elif hand_y > center_y + 20:
                self.down_pressed = True  # xuôngs
              
            distance_from_center = ((hand_x - center_x) ** 2 + (hand_y - center_y) ** 2) ** 0.5
            
            # if distance_from_center < 20:  
            #     self.color = (255, 0, 0)  
            #     # self.player_size = 15  
            # else:
            #     self.color = (0, 0, 255)  
            #     # self.player_size = 10  

    def get_current_cell(self, x, y, grid_cells):
        for cell in grid_cells:
            if cell.x == x and cell.y == y:
                return cell

    def check_move(self, tile, grid_cells, thickness):
        current_cell_x, current_cell_y = self.x // tile, self.y // tile
        current_cell = self.get_current_cell(current_cell_x, current_cell_y, grid_cells)
        current_cell_abs_x, current_cell_abs_y = current_cell_x * tile, current_cell_y * tile

        if self.left_pressed:
            if current_cell.walls['left'] and self.x <= current_cell_abs_x + thickness:
                self.left_pressed = False
        if self.right_pressed:
            if current_cell.walls['right'] and self.x >= current_cell_abs_x + tile - (self.player_size + thickness):
                self.right_pressed = False
        if self.up_pressed:
            if current_cell.walls['top'] and self.y <= current_cell_abs_y + thickness:
                self.up_pressed = False
        if self.down_pressed:
            if current_cell.walls['bottom'] and self.y >= current_cell_abs_y + tile - (self.player_size + thickness):
                self.down_pressed = False

    def draw(self, screen):
        # self.rect = pygame.Rect(int(self.x), int(self.y), self.player_size, self.player_size)  
        # pygame.draw.rect(screen, self.color, self.rect)
        # tải player
        # player_image = pygame.image.load("img/player/idle/0.png").convert_alpha()
        # player_image = pygame.transform.scale(player_image, (self.player_size, self.player_size))
    
        # screen.blit(player_image, (int(self.x), int(self.y)))
        screen.blit(self.player_image, (int(self.x), int(self.y)))

    def update(self, tile, grid_cells, thickness):
        self.check_move(tile, grid_cells, thickness)
    
        self.velX = -self.speed if self.left_pressed and not self.right_pressed else self.speed if self.right_pressed and not self.left_pressed else 0
        self.velY = -self.speed if self.up_pressed and not self.down_pressed else self.speed if self.down_pressed and not self.up_pressed else 0

        self.x += self.velX
        self.y += self.velY

        self.rect = pygame.Rect(int(self.x), int(self.y), self.player_size, self.player_size)