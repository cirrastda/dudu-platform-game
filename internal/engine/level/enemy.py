from internal.resources.enemies.turtle import Turtle
from internal.resources.enemies.spider import Spider
from internal.resources.enemies.robot import Robot
from internal.resources.enemies.alien import Alien
from internal.resources.enemies.airplane import Airplane


class LevelEnemy:
    def drawTurtle(game, platform):
        turtle = Turtle(
            platform[0],
            platform[1] - 30,
            platform[0],
            platform[0] + platform[2],
            game.turtle_images,
        )
        game.turtles.append(turtle)

    def drawSpider(game, platform):
        top_limit = platform[1] - 65
        bottom_limit = platform[1] - 30
        spider = Spider(
            platform[0] + platform[2] // 2,
            top_limit,
            top_limit,
            bottom_limit,
            game.spider_images,
        )
        game.spiders.append(spider)

    def drawRobot(game, platform):
        robot = Robot(
            platform[0],
            platform[1] - 57,
            platform[0],
            platform[0] + platform[2] - 57,  # Subtrair largura do robô (57px)
            game.robot_images,
            game.missile_images,
        )
        game.robots.append(robot)

    def drawAlien(game, platform):
        alien = Alien(
            platform[0],
            platform[1] - 57,
            platform[0],
            platform[0] + platform[2] - 57,  # Subtrair largura do alien (57px)
            game.alien_images,
        )
        game.aliens.append(alien)

    def drawAirplanes(game, platforms, factor):
        for i in range(factor, len(platforms), factor):
            if i < len(platforms):
                platform = platforms[i]
                LevelEnemy.drawAirplane(game, platform)

    def drawAirplane(game, platform):
        airplane = Airplane(
            platform[0] + platform[2] + 100,  # Spawnar à direita da plataforma
            platform[1] - 80,  # Altura acima da plataforma
            game.airplane_images,
        )
        game.airplanes.append(airplane)
