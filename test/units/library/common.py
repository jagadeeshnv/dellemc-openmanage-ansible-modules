# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.0.7
# Copyright (C) 2019-2020 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
from units.modules.utils import set_module_args
from units.modules.utils import AnsibleFailJson, AnsibleExitJson
from units.compat.mock import MagicMock


class Constants:
    device_id1 = 1234
    device_id2 = 4321
    service_tag1 = "MXL1234"
    service_tag2 = "MXL5467"


class AnsibleFailJSonException(Exception):
    def __init__(self, msg, **kwargs):
        super(AnsibleFailJSonException, self).__init__(msg)
        self.fail_msg = msg
        self.fail_kwargs = kwargs


class FakeAnsibleModule:

    def _run_module(self, module_args, check_mode=False):
        module_args.update({'_ansible_check_mode': check_mode})
        set_module_args(module_args)
        with pytest.raises(AnsibleExitJson) as ex:
            self.module.main()
        return ex.value.args[0]

    def _run_module_with_fail_json(self, module_args):
        set_module_args(module_args)
        with pytest.raises(AnsibleFailJson) as exc:
            self.module.main()
        result = exc.value.args[0]
        return result

    def get_module_mock(self, params=None):
        if params is None:
            params = {}

        def fail_func(msg, **kwargs):
            raise AnsibleFailJSonException(msg, **kwargs)

        module = MagicMock()
        module.fail_json.side_effect = fail_func
        module.params = params
        return module