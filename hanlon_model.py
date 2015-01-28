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


#{"label":"Test Model", "image_uuid":"OTP", "template":"ubuntu_oneiric",
# "req_metadata_hash":{"hostname_prefix":"test","domainname":"testdomain.com","root_password":"test4321"}}
def create_new_hanlon_model(module, req_metadata_hash, opt_metadata_hash):

    base_url = module.params['base_url']
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    url = "%s/model" % base_url

    req_metadata_params = {}

    for req_meta in req_metadata_hash:
        req_metadata_params.update({
            req_meta: module.params[req_meta]
        })


    payload = {
        'label': module.params['label'],
        'image_uuid': module.params['image_uuid'],
        'template': module.params['template'],
        'req_metadata_params': req_metadata_params
    }

    # print json.dumps(payload)

    req = requests.post(url, data=json.dumps(payload), headers=headers)

    #print json.dumps(req.json(), indent=4)

    return req.json()



def create_argument_spec(base_url, model_template):

    req_metadata_hash = []
    opt_metadata_hash = []

    url = "%s/model/templates/%s" % (base_url, model_template)
    argument_spec = dict()

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

    for req_metadata in template['response']['@req_metadata_hash']:
        req_metadata_hash.append(req_metadata[1:])
        argument_spec.update({
            req_metadata[1:]: dict(
                {'required': template['response']['@req_metadata_hash'][req_metadata]['required']}
            )})

    for opt_metadata in template['response']['@opt_metadata_hash']:
        opt_metadata_hash.append(opt_metadata[1:])
        argument_spec.update({
            opt_metadata[1:]: dict(
                {'required': template['response']['@opt_metadata_hash'][opt_metadata]['required']}
            )})

    print json.dumps(argument_spec)
    return argument_spec, req_metadata_hash, opt_metadata_hash

# Copied code from _load_params(self)
# https://github.com/ansible/ansible/blob/devel/lib/ansible/module_utils/basic.py


def peek_params():
    base_url = ""
    model = ""
    args = MODULE_ARGS
    items = shlex.split(args)

    for x in items:
        try:
            (k, v) = x.split("=", 1)
            if k == 'base_url':
                base_url = v
            elif k == 'template':
                model = v
        except Exception, e:
            exit(1)

    return base_url, model

from ansible.module_utils.basic import *


def main():

    # So we are going to cheat a little.  In order to use the AnsibleModule we will peek at
    # at the input to determine the basic configuration, model template being used and the URI
    # of the hanlon server.

    (base_url, model_template) = peek_params()

    # need check to make sure values are filled in
    argument_spec, req_metadata_hash, opt_metadata_hash = create_argument_spec(base_url, model_template)

    module = AnsibleModule(argument_spec=argument_spec)

    new_model = create_new_hanlon_model(module, req_metadata_hash, opt_metadata_hash)

    module.exit_json(changed=True, something_else=12345)


if __name__ == '__main__':
    main()
