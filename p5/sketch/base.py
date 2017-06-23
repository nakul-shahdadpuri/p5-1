#
# Part of p5: A Python package based on Processing
# Copyright (C) 2017 Abhik Pal
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

"""Base module for a sketch."""

import builtins
from functools import wraps

import pyglet

from ..opengl import renderer

_title = "p5py"
_min_width = 100
_min_height = 100

builtins.WIDTH = 800
builtins.HEIGHT = 600
builtins.FOCUSED = False
builtins.FRAMECOUNT = None
builtins.FRAMERATE = None

# builtins.PIXEL_HEIGHT = None
# builtins.PIXEL_WIDTH = None

window = pyglet.window.Window(
    width=WIDTH,
    height=HEIGHT,
    caption=_title,
    resizable=False,
    visible=False,
)

def initialize(*args, **kwargs):
    gl_version = window.context.get_info().get_version()[:3]
    renderer.initialize(gl_version)
    window.set_visible()

def _default_draw():
    renderer.clear()

def _default_setup():
    pass

def size():
    """Resize the window.
    """
    pass

def title(new_title):
    """Set the title of the p5 window.
    """

def run(draw=_default_draw, setup=_default_setup):
    """Run a sketch.
    """
    # set up required handlers depending on how the sketch is being
    # run (i.e., are we running from a standalone script, or are we
    # running inside the REPL?)

    def update(dt):
        renderer.pre_render()
        draw()
        renderer.post_render()

    initialize()
    setup()
    pyglet.clock.schedule(update)
    pyglet.app.run()

def artist(f):
    # a decorator that will wrap around the the "artists" in the
    # sketch -- these are functions that draw stuff on the screen like
    # rect(), line(), etc.
    #
    #    @_p5_artist
    #    def rect(*args, **kwargs):
    #        # code that creates a rectangular Shape object and
    #        # returns it.
    @wraps(f)
    def decorated(*args, **kwargs):
        shape = f(*args, **kwargs)
        renderer.render(shape)
        return shape
    return decorated

def test_run():
    initialize()
    def tester(dt):
        renderer.pre_render()
        renderer.test_render()
        renderer.post_render()
    pyglet.clock.schedule(tester)
    pyglet.app.run()