import sublime, sublime_plugin

ON = False
FILE_LINES = {}

def run_Jshint(window):
  window.run_command('set_build_system', {
      'file': 'Packages/JSHint/JSHint.sublime-build'
    })
  window.run_command('build')

class JshintCommand(sublime_plugin.WindowCommand):
  def run(self):
    global ON
    ON = not ON
    if ON:
      run_Jshint(self.window)
    else:
      sublime.active_window().run_command("hide_panel", {"panel": "show_results", "toggle": False})

class lineListener(sublime_plugin.EventListener):
  def on_modified(self, view):
    global FILE_LINES
    global ON
    file_name = view.file_name()
    if (ON and file_name or "").endswith(".js"):
      window = sublime.active_window()
      selected_region = view.sel()[0]
      if selected_region.size() == 0:
        text = view.substr(sublime.Region(0, view.size()))
      else:
        text = self.view.substr(sublime.Region(selected_region.begin(), selected_region.end()))

      lines = text.split("\n") or []
      if file_name not in FILE_LINES or FILE_LINES[file_name] != len(lines):
        FILE_LINES[file_name] = len(lines)
        run_Jshint(window)






