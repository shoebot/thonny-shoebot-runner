'''
thonny-shoebotmode.

shoebot plugin for Thonny.

# NOTES TO SELF:
* documentation: https://github.com/thonny/thonny/wiki/Plugins
* maybe look at how Run > Pygame Zero Mode is programmed?
'''

import os
import pathlib
import shutil
import subprocess
import site
import sys
import threading
import time
from tkinter.messagebox import showinfo
from thonny.languages import tr
from thonny import get_workbench, THONNY_USER_DIR
from thonny import running
from thonny.ui_utils import select_sequence

__author__ = 'villares'
__credits__ = 'organisation name'


def execute_module_mode() -> None:
    '''
    there's got to be a better approach than this ...
    maybe something that employs a new Runner instance
    maybe something that changes the thonny's default run behaviour
    '''
    current_editor = get_workbench().get_editor_notebook().get_current_editor()
    current_file = current_editor.get_filename()

    if current_file is None:
        # thonny must 'save as' any new files, before it can run them
        showinfo(
          'shoebot module mode error',
          'Save your file somewhere first',
          master=get_workbench()
        )

    elif current_file and current_file.split('.')[-1] in ('py', 'shoebot', 'bot'):
        # save and run shoebot module mode
        current_editor.save_file()
        run_sketch = 'sbot'

#         run_sketch = '/home/villares/.local/bin/sbot'
        user_packages = str(site.getusersitepackages())
        site_packages = str(site.getsitepackages()[0])
        # check for shoebot run_sketch path
        if pathlib.Path(user_packages + run_sketch).is_file():
            run_sketch = pathlib.Path(user_packages + run_sketch)
        elif pathlib.Path(site_packages + run_sketch).is_file():
            run_sketch = pathlib.Path(site_packages + run_sketch)

        working_directory = os.path.dirname(current_file)
        cd_cmd_line = running.construct_cd_command(working_directory) + '\n'
        cmd_parts = ['%Run', str(run_sketch), current_file]
        ed_token = [running.EDITOR_CONTENT_TOKEN]
        exe_cmd_line = running.construct_cmd_line(cmd_parts, ed_token) + '\n'
        running.get_shell().submit_magic_command(cd_cmd_line + exe_cmd_line)


# workaround for .add_command() handler parameter that won't accept arguments
def toggle_variable_portable() -> None: toggle_variable('portable')
def toggle_variable_installed() -> None: toggle_variable('installed')


def toggle_variable(install_type: str) -> None:
    '''install_type is portable or installed'''
    var_portable = get_workbench().get_variable('run.shoebot_mode_portable')
    var_installed = get_workbench().get_variable('run.shoebot_mode_installed')

    if install_type == 'portable':
        var_installed.set(False)
        var_portable.set(not var_portable.get())

    if install_type == 'installed':
        var_portable.set(False)
        var_installed.set(not var_installed.get())

    # NOTE: don't know what this is for
    # if get_workbench().in_simple_mode():
    #     os.environ['shoebot_MODE'] = 'auto'
    # else:
    #     os.environ['shoebot_MODE'] = str(get_workbench().get_option(_OPTION_...))

    if var_portable.get() or var_installed.get():
        # activate shoebot (and download jdk if necessary)
        activate_shoebot(install_type)


def load_plugin() -> None:
    '''every thonny plug-in uses this function to load'''
    # portable button
    '''
 
 
    '''
    # non-portable / installed button
    # NOTE: perhaps this should be a toggle that in-turn affects thonny run?
    get_workbench().add_command(
    command_id='run_with_sbot',
    menu_name='tools',
    command_label="Execute with shoebot's sbot command",
    handler=execute_module_mode,
    default_sequence='<Control-b>',
    extra_sequences=[select_sequence('<Control-Alt-b>', '<Command-b>')],
    )


