from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from datetime import datetime
from ansible import constants as C
from ansible.module_utils._text import to_text
from ansible.plugins.callback.unixy import CallbackModule as CallbackBase


class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'unixy2'
    CALLBACK_NEEDS_WHITELIST = False

    def __init__(self):
        super(CallbackModule, self).__init__()
        self._last_role_name = ''

    def _get_task_display_name(self, task):
        self.task_display_name = None
        display_names = task.get_name().strip().split(" : ")
        role_name = display_names[-2] if len(display_names) > 1 else ''
        task_name = display_names[-1]
        if task_name.startswith("include"):
            return
        if role_name != self._last_role_name:
            self._last_role_name = role_name
            if role_name:
                task_name = '%s - %s' % (task_name, role_name)
        self.task_display_name = task_name

    def _run_is_verbose(self, result, verbosity=0):
        return ((self._display.verbosity > verbosity or result._result.get('_ansible_verbose_always', False) is True)
                and result._result.get('_ansible_verbose_override', False) is False)

    def _process_result_output(self, result, msg):
        label = ''
        if self._run_is_verbose(result):
            label = self._get_item_label(result._result) or ''
            if isinstance(label, dict):
                if 'key' in label:
                    label = label['key']
                elif 'name' in label:
                    label = label['name']
            label = ('%s' % label).strip()
            if label and label[0] not in '[({':
                label = '(%s)' % label
            if label:
                label = ' %s' % label

        task_host = result._host.get_name()
        task_result = "%s %s%s" % (task_host, msg, label)

        task_action = result._task.action
        result_msg = result._result.get('msg', '')
        if task_action in ('debug', 'assert') and msg == "ok" and result_msg:
            try:
                debug_msg = self._dump_results(result_msg, indent=4)
            except:
                debug_msg = to_text(result_msg)
            return "%s %s | %s: %s" % (task_host, msg, task_action, debug_msg)

        if self._run_is_verbose(result, verbosity=1):
            return "%s %s%s: %s" % (task_host, msg, label, self._dump_results(result._result, indent=4))

        if self.delegated_vars:
            task_delegate_host = self.delegated_vars['ansible_host']
            task_result = "%s -> %s %s%s" % (task_host, task_delegate_host, msg, label)

        if result_msg and result_msg != "All items completed":
            task_result += " | msg: " + to_text(result_msg)

        if result._result.get('stdout') and self._run_is_verbose(result, verbosity=0):
            task_result += " | stdout: " + result._result.get('stdout')

        if result._result.get('stderr'):
            task_result += " | stderr: " + result._result.get('stderr')

        return task_result

    def v2_playbook_on_play_start(self, play):
        name = play.get_name().strip()
        if name and play.hosts:  # replace hyphens by endash
            msg = u"\n... %s on hosts: %s ..." % (name, ",".join(play.hosts))
        else:
            msg = u"---"
        self._display.display(msg)

    def v2_playbook_on_task_start(self, task, is_conditional):
        self._get_task_display_name(task)
        if self.task_display_name is not None:
            ts = datetime.now().strftime("%H:%M:%S")
            self._display.display("%s.. %s" % (ts, self.task_display_name))

    def v2_playbook_on_handler_task_start(self, task):
        self._get_task_display_name(task)
        if self.task_display_name is not None:
            ts = datetime.now().strftime("%H:%M:%S")
            self._display.display("%s.. %s (via handler)... " % (ts, self.task_display_name))

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self._preprocess_result(result)
        if ignore_errors:
            msg = "failed (ignored)"
            display_color = C.COLOR_WARN
        else:
            display_color = C.COLOR_ERROR
            msg = "failed"
        task_result = self._process_result_output(result, msg)
        self._display.display("  " + task_result, display_color)

    def v2_runner_on_unreachable(self, result):
        self._preprocess_result(result)  # fixes bug in ansible 2.8.1
        task_result = self._process_result_output(result, "unreachable")
        self._display.display("  " + task_result, C.COLOR_UNREACHABLE)

    def v2_runner_on_start(self, host, task):
        pass  # silence warning in ansible 2.9
