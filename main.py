import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import NumericProperty, ReferenceListProperty,\
	ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock


class PongPaddle(Widget):
	score = NumericProperty(0)
	velocity_y = 0
	beta = 2

	def bounce_ball(self, ball):
		if self.collide_widget(ball):
			vx, vy = ball.velocity
			offset = (ball.center_y - self.center_y) / (self.height / 2)
			bounced = Vector(-1 * vx, vy)
			vel = bounced * 1.1
			ball.velocity = vel.x, vel.y + offset
	
	#Заставить двигаться планку плавнее
	#Добавить отскок от границ поля
	def move(self,dy=1):
		self.pos[1] += self.velocity_y*5

class PongBall(Widget):
#class PongBall(BoxLayout):
	velocity_x = NumericProperty(0)
	velocity_y = NumericProperty(0)
	velocity = ReferenceListProperty(velocity_x, velocity_y)

	def move(self):
		self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
	ball = ObjectProperty(None)
	player1 = ObjectProperty(None)
	player2 = ObjectProperty(None)

	def serve_ball(self, vel=(4, 0)):
		self.ball.center = self.center
		self.ball.velocity = vel

	def update(self, dt):
		self.ball.move()
		self.player1.move()

		#bounce ball off paddles
		self.player1.bounce_ball(self.ball)
		self.player2.bounce_ball(self.ball)

		#bounce ball off bottom or top
		if (self.ball.y < self.y) or (self.ball.top > self.top):
			self.ball.velocity_y *= -1

		#went off a side to score point?
		if self.ball.x < self.x:
			self.player2.score += 1
			self.serve_ball(vel=(4, 0))
		if self.ball.x > self.width:
			self.player1.score += 1
			self.serve_ball(vel=(-4, 0))

	def on_touch_move(self, touch):
		if touch.x < self.width / 3:
			self.player1.center_y = touch.y
		if touch.x > self.width - self.width / 3:
			self.player2.center_y = touch.y
	
	def key_event(self, keyboard, keycode, text, modifiers):
		if keycode[1]=='up':
			self.player1.velocity_y = 1
		if keycode[1]=='down':
			self.player1.velocity_y = -1

class PongApp(App):
	def build(self):
		game = PongGame()
		Mykeyboard = Window.request_keyboard(None, game)
		Mykeyboard.bind(on_key_down=game.key_event)
		game.serve_ball()
		#Clock.schedule_interval(game.update, 1.0 / 60.0)
		return game


if __name__ == '__main__':
	PongApp().run()
