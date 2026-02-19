import pygame
import time
import math
import numpy as np
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
screen = pygame.display.set_mode((600, 600))
running = True
amplitude = 100
frequency = 0.01
speed = 0.01
clock = pygame.time.Clock()
last_freq = None
angle = 0
slider_rect = pygame.Rect(50, 550, 200, 20)
knob_radius = 10
knob_x = slider_rect.left
dragging = False
minimumelectrons = 1
maximumelectrons = 8
electrons = 1
sound_timer = 0

def generate_sound(freq, duration=0.05, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = np.sin(2 * math.pi * freq * t)

    audio = (wave * 32767).astype(np.int16)

    stereo_audio = np.column_stack((audio, audio))

    return pygame.sndarray.make_sound(stereo_audio)
channel = pygame.mixer.Channel(0)
while running:
        clock.tick(120)
        screen.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                knob_rect = pygame.Rect(knob_x - knob_radius, 560 - knob_radius, knob_radius*2, knob_radius*2)
                if knob_rect.collidepoint(event.pos):
                    dragging = True

            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False

            if event.type == pygame.MOUSEMOTION and dragging:
                knob_x = max(slider_rect.left, min(event.pos[0], slider_rect.right))
        x = 100 * math.cos(math.radians(angle))
        y = 100 * math.sin(math.radians(angle))
        
        proton = pygame.draw.circle(screen, "red", (200, 200), 10)
        slider_percent = (knob_x - slider_rect.left) / slider_rect.width
        electrons = int(minimumelectrons + slider_percent * (maximumelectrons - minimumelectrons))
        electrons = max(1, electrons)
        for i in range(electrons):
            offset_angle = angle + (360 / electrons) * i
            x = 100 * math.cos(math.radians(offset_angle))
            y = 100 * math.sin(math.radians(offset_angle))
            pygame.draw.circle(screen, "blue", (int(x + 200), int(y + 200)), 5)

        wave_y = amplitude * math.sin(math.radians(angle))
        min_freq = 200
        max_freq = 1000

        normalized = (wave_y + amplitude) / (2 * amplitude)
        sound_freq = min_freq + normalized * (max_freq - min_freq)
        wavehead = pygame.draw.circle(screen, "white", (300, int(wave_y+200)), 5)
        wavehead.center = (300, wave_y+200)
        pygame.draw.line(screen, "white", (300, 200), (300, wave_y+200))

        
        
        
        for x_pos in range(300, 600):
            y_pos = amplitude * math.sin(frequency * x_pos - math.radians(angle))
            wave = pygame.draw.circle(screen, "white", (x_pos, int(y_pos+200)), 2)
        pygame.draw.rect(screen, "gray", slider_rect)
        pygame.draw.circle(screen, "white", (knob_x, 560), knob_radius)
        pygame.display.flip()
        angle += 2
        

        if last_freq is None or abs(sound_freq - last_freq) > 10:
            channel.fadeout(30)
            tone = generate_sound(sound_freq)
            channel.play(tone, loops=-1, fade_ms=30)
            last_freq = sound_freq
        channel.set_volume(electrons / maximumelectrons)

