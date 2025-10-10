from internal.resources.enemies.turtle import Turtle
from internal.resources.enemies.spider import Spider


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
