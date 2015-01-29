#!/usr/bin/python

__author__ = 'jcallen'


DOCUMENTATION = '''
---

/home/jcallen/Development/ansible/hacking/test-module -m /home/jcallen/Development/ansible-hanlon/hanlon_image.py
-a "base_url=http://192.168.122.56:8026/hanlon/api/v1/ type=os name=ansible_os path=/home/hanlon/image/CentOS-7.0-1406-x86_64-Minimal.iso version=7.0"

'''

import requests
from ansible.module_utils.basic import *

def create_new_hanlon_image(module):
    """ comments here """

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
    """ comments here """
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