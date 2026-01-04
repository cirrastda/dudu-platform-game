from internal.resources.bullet import Bullet
from internal.resources.explosion import Explosion


class Pool:
    def __init__(self, game):
        self.g = game

    def get_pooled_bullet(self, x, y, direction=1, image=None):
        """Obter bala do pool ou criar nova se necessário"""
        g = self.g
        if getattr(g, "bullet_pool", None):
            bullet = g.bullet_pool.pop()
            bullet.x = x
            bullet.y = y
            bullet.direction = direction
            bullet.image = image
            bullet.rect.x = x
            bullet.rect.y = y
            # Resetar velocidade para o padrão antes de qualquer ajuste externo
            try:
                bullet.speed = 8
            except Exception:
                pass
            return bullet
        else:
            return Bullet(x, y, direction, image)

    def return_bullet_to_pool(self, bullet):
        """Retornar bala ao pool"""
        g = self.g
        if not hasattr(g, "bullet_pool"):
            g.bullet_pool = []
        if len(g.bullet_pool) < 20:  # Limitar tamanho do pool
            g.bullet_pool.append(bullet)

    def get_pooled_explosion(self, x, y, image=None):
        """Obter explosão do pool ou criar nova se necessário"""
        g = self.g
        if getattr(g, "explosion_pool", None):
            explosion = g.explosion_pool.pop()
            explosion.x = x
            explosion.y = y
            explosion.image = image
            explosion.timer = 30  # Resetar timer para duração completa
            return explosion
        else:
            return Explosion(x, y, image)

    def return_explosion_to_pool(self, explosion):
        """Retornar explosão ao pool"""
        g = self.g
        if not hasattr(g, "explosion_pool"):
            g.explosion_pool = []
        if len(g.explosion_pool) < 10:  # Limitar tamanho do pool
            g.explosion_pool.append(explosion)