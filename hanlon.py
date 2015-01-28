__author__ = 'jcallen'

from ansible.module_utils.basic import *

# Since I am doing things a little different as certain points in code execution I cannot use
# the provided AnsibleModule methods.  Instead I am modifying for specific use.
# https://github.com/ansible/ansible/blob/devel/lib/ansible/module_utils/basic.py


def _jsonify(self, data):
    for encoding in ("utf-8", "latin-1", "unicode_escape"):
        try:
            return json.dumps(data, encoding=encoding)
        # Old systems using simplejson module does not support encoding keyword.
        except TypeError, e:
            return json.dumps(data)
        except UnicodeDecodeError, e:
            continue
    _fail_json(msg='Invalid unicode encoding encountered')


def _fail_json(**kwargs):

    assert 'msg' in kwargs, "implementation error -- msg to explain the error is required"
    kwargs['failed'] = True
    print _jsonify(kwargs)
    sys.exit(1)


# Copied code from _load_params(self)
# https://github.com/ansible/ansible/blob/devel/lib/ansible/module_utils/basic.py
#
# So we are going to cheat a little.  In order to use the AnsibleModule we will peek at
# at the MODULE_ARGS to determine the basic configuration, model template being used and the URI
# of the Hanlon server.

def peek_params():
    base_url = ""
    template = ""
    args = MODULE_ARGS
    items = shlex.split(args)

    for x in items:
        try:
            (k, v) = x.split("=", 1)
            if k == 'base_url':
                base_url = v
            elif k == 'template':
                template = v
        except Exception, e:
            _fail_json(msg="this module requires key=value arguments (%s)" % items)

    if len(base_url) == 0:
        _fail_json(msg="missing base_url argument")
    if len(template) == 0:
        _fail_json(msg="missing template argument")

    return base_url, template