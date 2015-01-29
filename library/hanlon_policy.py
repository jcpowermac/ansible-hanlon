#!/usr/bin/python

DOCUMENTATION = '''
---
# If a key doesn't apply to your module (ex: choices, default, or
# aliases) you can use the word 'null', or an empty list, [], where
# appropriate.
module: hanlon_model
short_description: Add a new model to Hanlon
description:
    - A Hanlon model describes how a bare metal server operating system should be configured when provisioning
    this module adds a model to Hanlon.
version_added: null
author: Joseph Callen
notes: null
requirements:
    - requests
    - Hanlon server
options:
    base_url:
        description:
            - The url to the Hanlon RESTful base endpoint
        required: true
        default: null
        aliases: []
    template:
        description:
            - The available OS templates for use with Hanlon.  From the CLI ./hanlon model templates
        required: true
        default: null
        aliases: []
notes:
    - This module should run from a system that can access Hanlon directly. Either by using local_action, or using delegate_to.
    - The options for this module are dynamic based on the template type.  The req_metadata_hash and opt_metadata_hash keys map to options
'''

import requests
from ansible.module_utils.basic import *


def _jsonify(data):
    """
    Since I am doing things a little different as certain points in code execution I cannot use
    the provided AnsibleModule methods.  Instead I am modifying for specific use.
    https://github.com/ansible/ansible/blob/devel/lib/ansible/module_utils/basic.py
    :param data:
    :return: json

    """
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
    """
    :param kwargs:
    :return:
    """

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
    """
    Copied code from _load_params(self) - https://github.com/ansible/ansible/blob/devel/lib/ansible/module_utils/basic.py
    So we are going to cheat a little.  In order to use the AnsibleModule we will peek at
    the MODULE_ARGS to determine the basic configuration, model template being used and the URI of the Hanlon server.

    :returns base_url, template
    """

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

def create_new_hanlon_model(module, metadata_hash):
    """

    :param module:
    :param metadata_hash:
    :return:
    """

    req_metadata_params = dict()

    base_url = module.params['base_url']
    url = "%s/model" % base_url
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    # We need to generate the req_metadata_params to POST into Hanlon
    for metadata in metadata_hash:
        # Because we have optional metadata we only want to include params
        # that have values assigned
        if len(module.params[metadata]) != 0:
            req_metadata_params.update({
                metadata: module.params[metadata]
            })

    payload = {
        'label': module.params['label'],
        'template': module.params['template'],
        'req_metadata_params': req_metadata_params
    }

    # If we are using the boot_local and discover_only models
    # we do not want the image_uuid as its not required.
    # All other models it is required
    if (module.params['template'] != 'boot_local') or (module.params['template'] != 'discover_only'):
        payload.update({'image_uuid': module.params['image_uuid']})

    try:
        req = requests.post(url, data=json.dumps(payload), headers=headers)
        json_result = req.json()
    except Exception as e:
        module.fail_json(msg=e.message)

    return json_result


def create_argument_spec(base_url, model_template):
    """ comments here"""

    metadata_types = "@req_metadata_hash", "@opt_metadata_hash"
    metadata_hash = []
    argument_spec = dict()

    url = "%s/model/templates/%s" % (base_url, model_template)

    if (model_template == 'boot_local') or (model_template == 'discover_only'):
        argument_spec.update(image_uuid=dict(required=False))
    else:
        argument_spec.update(image_uuid=dict(required=True))

    argument_spec.update(
        base_url=dict(required=True),
        template=dict(required=True),
        label=dict(required=True))

    try:
        req = requests.get(url)
        if req.status_code != 200:
            _fail_json(msg=req.text)

        template = req.json()
    except Exception as e:
        _fail_json(msg=e.message)

    try:
        for md_type in metadata_types:
            for metadata in template['response'][md_type]:
                metadata_hash.append(metadata[1:])
                argument_spec.update({
                    metadata[1:]: dict(
                        {'required': template['response'][md_type][metadata]['required']}
                    )})
    except Exception as e:
        _fail_json(msg=e.message)

    return argument_spec, metadata_hash


def main():
    """ comments here"""

    (base_url, model_template) = peek_params()

    argument_spec, metadata_hash = create_argument_spec(base_url, model_template)

    module = AnsibleModule(argument_spec=argument_spec)

    new_model = create_new_hanlon_model(module, metadata_hash)

    uuid = new_model['response']['@uuid']

    module.exit_json(
        changed=True,
        uuid=uuid
    )


if __name__ == '__main__':
    main()
