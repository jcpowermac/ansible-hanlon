#!/usr/bin/python

DOCUMENTATION = '''
---
module: hanlon_image
short_description: Add a new image to Hanlon
description:
    -
version_added: null
author: Joseph Callen
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
    type:
        description:
            - The available OS templates for use with Hanlon.  From the CLI ./hanlon model templates
        required: true
        default: null
        aliases: []
    path:
        description:
            - The path to an ISO image for either an OS, hypervisor or microkernel
        required: true
        default: null
        aliases: []
    name:
        description: null
        required: false
        default: null
        aliases: []
    version:
        description:
            - The version of the OS
        required: false
        default: null
        aliases: []

notes:
    - This module should run from a system that can access Hanlon directly. Either by using local_action, or using delegate_to.
'''

import requests
from ansible.module_utils.basic import *

def create_new_hanlon_image(module):
    """
    :param module:
    :return:
    """

    base_url = module.params['base_url']
    url = "%s/image" % base_url
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    payload = {
        'type': module.params['type'],
        'path': module.params['path']
    }

    if module.params['type'] == 'os':
        payload.update({
            'name': module.params['name'],
            'version': module.params['version']
        })

    try:
        req = requests.post(url, data=json.dumps(payload), headers=headers)
        json_result = req.json()
    except Exception as e:
        module.fail_json(msg=e.message)

    return json_result

def create_argument_spec():
    """
    :return argument_spec:
    """
    argument_spec = dict()

    argument_spec.update(
        base_url=dict(required=True),
        type=dict(required=True),
        path=dict(required=True),
        name=dict(required=False),
        version=dict(required=False)
    )
    return argument_spec


def main():
    argument_spec = create_argument_spec()
    module = AnsibleModule(argument_spec=argument_spec)
    new_image = create_new_hanlon_image(module)
    uuid = new_image['response']['@uuid']

    module.exit_json(
        changed=True,
        uuid=uuid
    )


if __name__ == '__main__':
    main()