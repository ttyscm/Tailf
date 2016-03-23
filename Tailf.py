# coding: utf-8

import time
import threading

import sublime
import sublime_plugin


_thread = None
_stop = False
_path = sublime.load_settings('Tailf.sublime-settings').get('path')


def tail_f():
	global _stop, _path
	f = open(_path)
	f.seek(0, 2)
	while True:
		if _stop:
			break
		pos = f.tell()
		line = f.readline()
		if not line:
			time.sleep(0.5)
			f.seek(pos)
		else:
			print line,

	f.close()
	_stop = False


class TailfStartCommand(sublime_plugin.ApplicationCommand):

	def run(self):
		global _thread, _path
		if not _path:
			sublime.message_dialog('cannot find "path" in Tailf.sublime-settings.')
			return

		if _thread is not None and _thread.is_alive():
			sublime.status_message('thread is already started.')
			return

		_thread = threading.Thread(target=tail_f)
		_thread.start()
		sublime.status_message('thread started.')


class TailfStopCommand(sublime_plugin.ApplicationCommand):

	def run(self):
		global _thread, _stop
		if _thread is not None and _thread.is_alive():
			_stop = True
			_thread.join()
			_thread = None
		sublime.status_message('thread stopped.')


class TailfStatusCommand(sublime_plugin.ApplicationCommand):

	def run(self):
		global _thread
		print _thread
		print sublime.load_settings('Tailf.sublime-settings').get('path')
