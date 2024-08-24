# vim:fileencoding=utf-8:noet

'''Tests for shell.py parser'''

from __future__ import (unicode_literals, division, absolute_import, print_function)

import sys

if sys.version_info < (3,):
	from io import BytesIO as StrIO
else:
	from io import StringIO as StrIO

from powerline.commands.main import get_argparser, finish_args

from tests.modules import TestCase
from tests.modules.lib import replace_attr


class TestParser(TestCase):
	def test_main_normal(self):
		parser = get_argparser()
		out = StrIO()
		err = StrIO()
		with replace_attr(sys, 'stdout', out, 'stderr', err):
			for argv, expargs in [
				(['shell', 'left'],       {'ext': ['shell'], 'side': 'left'}),
				(['shell', 'left', '-r', '.zsh'], {'ext': ['shell'], 'renderer_module': '.zsh', 'side': 'left'}),
				([
					'shell',
					'left',
					'-r', '.zsh',
					'--last-exit-code', '10',
					'--last-pipe-status', '10 20 30',
					'--jobnum=10',
					'-w', '100',
					'-c', 'common.term_truecolor=true',
					'-c', 'common.spaces=4',
					'-t', 'default.segment_data.hostname.before=H:',
					'-p', '.',
					'-p', '..',
					'-R', 'smth={"abc":"def"}',
				], {
					'ext': ['shell'],
					'side': 'left',
					'renderer_module': '.zsh',
					'last_exit_code': 10,
					'last_pipe_status': [10, 20, 30],
					'jobnum': 10,
					'width': 100,
					'config_override': {'common': {'term_truecolor': True, 'spaces': 4}},
					'theme_override': {
						'default': {
							'segment_data': {
								'hostname': {
									'before': 'H:'
								}
							}
						}
					},
					'config_path': ['.', '..'],
					'renderer_arg': {'smth': {'abc': 'def'}},
				}),
				(['shell', 'left', '-R', 'arg=true'], {
					'ext': ['shell'],
					'side': 'left',
					'renderer_arg': {'arg': True},
				}),
				(['shell', 'left', '-R', 'arg=true', '-R', 'arg='], {
					'ext': ['shell'],
					'side': 'left',
					'renderer_arg': {},
				}),
				(['shell', 'left', '-R', 'arg='], {'ext': ['shell'], 'renderer_arg': {}, 'side': 'left'}),
				(['shell', 'left', '-t', 'default.segment_info={"hostname": {}}'], {
					'ext': ['shell'],
					'side': 'left',
					'theme_override': {
						'default': {
							'segment_info': {
								'hostname': {}
							}
						}
					},
				}),
				(['shell', 'left', '-c', 'common={ }'], {
					'ext': ['shell'],
					'side': 'left',
					'config_override': {'common': {}},
				}),
				(['shell', 'left', '--last-pipe-status='], {
					'ext': ['shell'],
					'side': 'left',
					'last_pipe_status': [],
				}),
			]:
				args = parser.parse_args(argv)
				finish_args(parser, {}, args)
				for key, val in expargs.items():
					self.assertEqual(getattr(args, key), val)
				for key, val in args.__dict__.items():
					if key not in expargs:
						self.assertFalse(val, msg='key {0} is {1} while it should be something false'.format(key, val))
				self.assertFalse(err.getvalue() + out.getvalue(), msg='unexpected output: {0!r} {1!r}'.format(
					err.getvalue(),
					out.getvalue(),
				))


if __name__ == '__main__':
	from tests.modules import main
	main()
