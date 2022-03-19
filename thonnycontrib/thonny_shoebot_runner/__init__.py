import subprocess
import sys
import os
from collections import namedtuple

from tkinter.messagebox import showinfo
from thonny import get_workbench

name = 'thonny-shoebot-runner'

ErrorMessage = namedtuple('ErrorMessage', ['error_type', 'description'])

SUCCESS = 'All done!'

NO_TEXT_TO_FORMAT = ErrorMessage(
    'Nothing to do here',
    'There is no bot to execute.'
)
PACKAGE_NOT_FOUND = ErrorMessage(
    'Package not found',
    'Could not find shoebot/sbot. Is it installed and on your PATH?',
)
NOT_COMPATIBLE = ErrorMessage(
    'File not compatible!',
    'Looks like this is not a Python file. Did you already save it?',
)

# Temporary fix: this function comes from thonny.running, but importing that
# module may conflict with outdated Thonny installations from some Linux
# repositories.
# TODO: change this with thonny.running.get_interpreter_for_subprocess when
# possible and change Thonny version required.
_console_allocated = False


# def get_interpreter_for_subprocess(candidate=None):
#     if candidate is None:
#         candidate = sys.executable
# 
#     pythonw = candidate.replace('python.exe', 'pythonw.exe')
#     if not _console_allocated and os.path.exists(pythonw):
#         return pythonw
#     else:
#         return candidate.replace('pythonw.exe', 'python.exe')


class ShoebotSbot:
    """
    Call shoebot's sbot command with the open source code document as argument

    Using subprocess, sbot is executed to run .bot or .py files displayed in
    Thonny. Whenever this plugin is executed, run_with_sbot is called. Depending
    on the result, final_title and final_message is displayed through
    tkinter.messagebox.showinfo().
    """

    def __init__(self) -> None:
        """Get the workbench to be later used to detect the file to format."""
        self.workbench = get_workbench()

    def open_folder(self) -> None:
        """Open the enclosing folder to the current file."""
        import subprocess
        import platform
        self.editor = self.workbench.get_editor_notebook().get_current_editor()
        try:
            filename = self.editor.get_filename()
        except AttributeError:
            print("Have you checked if have an open file?")
            return
        else:
            path = os.path.dirname(filename)
            print(sys.platform)
        if sys.platform == 'darwin':
            subprocess.Popen(['open', path])
        elif sys.platform == 'linux':
            subprocess.Popen(["xdg-open", path])
        else: # 'win32'
            # os.startfile(path) # I should test someday
            subprocess.Popen(["explorer", path])

    def run_with_sbot(self) -> None:
        """Handle the plugin execution."""
        self.editor = self.workbench.get_editor_notebook().get_current_editor()

        try:
            self.filename = self.editor.get_filename()
        except AttributeError:
            final_title = NO_TEXT_TO_FORMAT.error_type
            final_message = NO_TEXT_TO_FORMAT.description
        else:
            if self.filename is not None and self.filename.split('.')[-1] in (
                'py',
                'bot',
            ):
                self.editor.save_file()

                run_sbot = subprocess.run(
                    #  [get_interpreter_for_subprocess(), "-m", "black", self.filename, "-S"],
                    ['sbot', self.filename],
                    capture_output=True,
                    text=True,
                )

                if run_sbot.stderr.find('No sbot found!') != -1:
                    final_title = PACKAGE_NOT_FOUND.error_type
                    final_message = PACKAGE_NOT_FOUND.description
                else:
                    # Emojis are not supported in Tkinter.
                    emojiless_message = run_sbot.stderr.encode('ascii', 'ignore').decode()
                    if run_sbot.returncode != 0:
                        final_title = 'Oh no!'
                        final_message = '\n'.join(
                            emojiless_message.splitlines()[::2]
                        )

                        final_message = (
                            final_message[0].upper() + final_message[1:]
                        )

                    else:
                        self.editor._load_file(self.filename, keep_undo=True)
                        final_title = 'Done'
                        final_message = emojiless_message
            else:
                final_title = NOT_COMPATIBLE.error_type
                final_message = NOT_COMPATIBLE.description
        if final_message:
            showinfo(title=final_title, message=final_message)

    def load_plugin(self) -> None:
        """
        Load the plugin on runtime.

        Using self.workbench.add_command(), the plugin is registered in Thonny
        with all the given arguments.
        """
        self.workbench.add_command(
            command_id='run_with_sbot',
            menu_name='tools',
            command_label="Execute with shoebot's sbot command",
            handler=self.run_with_sbot,
            default_sequence='<Control-Alt-b>',
            extra_sequences=['<<CtrlAltBInText>>'],
        )
        self.workbench.add_command(
            command_id='open_folder',
            menu_name='tools',
            command_label="Open enclosing folder",
            handler=self.open_folder,
            default_sequence='<Alt-k>',
            extra_sequences=['<<AltKInText>>'],
        )

if get_workbench():
    run = ShoebotSbot().load_plugin()
