#!/usr/bin/python

DOCUMENTATION = '''
---
module: hanlon_model
short_description: This is a sentence describing the module
# ... snip ...


1z92ygFkLsSqNz1fgCfTRG

ansible/hacking/test-module -m ./hanlon_ansible.py -a "base_url=http://192.168.122.56:8026/hanlon/api/v1/ template=redhat_7 label=centos7_model image_uuid=1z92ygFkLsSqNz1fgCfTRG hostname_prefix=centos domainname=testdomain.com root_password=trustn01"
'''

import requests
from hanlon import *


def create_new_hanlon_model(module, metadata_hash):
    """ comments here """

    req_metadata_params = dict()

    base_url = module.params['base_url']
    url = "%s/model" % base_url
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    # We need to generate the req_metadata_params to POST into Hanlon
    for metadata in metadata_hash:
        req_metadata_params.update({
            metadata: module.params[metadata]
        })

    payload = {
        'label': module.params['label'],
        'template': module.params['template'],
        'req_metadata_params': req_metadata_params
    }

    if (module.params['template'] != 'boot_local') or (module.params['template'] != 'discover_only'):
        payload.update({'image_uuid': module.params['image_uuid']})

    try:
        req = requests.post(url, data=json.dumps(payload), headers=headers)
        json_result = req.json()
    except Exception:
        module.fail_json(msg="POST failed")

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

    req = requests.get(url)

    if req.status_code != 200:
        exit(1)

    template = req.json()

    for md_type in metadata_types:
        for metadata in template['response'][md_type]:
            metadata_hash.append(metadata[1:])
            argument_spec.update({
                metadata[1:]: dict(
                    {'required': template['response'][md_type][metadata]['required']}
                )})

    print json.dumps(argument_spec)
    return argument_spec, metadata_hash


def main():
    """ comments here"""

    (base_url, model_template) = peek_params()

    argument_spec, metadata_hash = create_argument_spec(base_url, model_template)

    module = AnsibleModule(argument_spec=argument_spec)

    new_model = create_new_hanlon_model(module, metadata_hash)

    module.exit_json(changed=True, something_else=12345)


if __name__ == '__main__':
    main()
