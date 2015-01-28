__author__ = 'jcallen'

from ansible.module_utils.basic import *


def create_new_hanlon_policy(module):


def main():
    module = AnsibleModule(
        argument_spec=dict(
            hanlon_url=dict(required=True, type='str'),
            hanlon_policy_template=dict(
                required=True,
                choices=[
                    'boot_local',
                    'centos_6',
                    'debian_wheezy',
                    'xenserver_tampa'], type='str'),
            esx_license=dict(required=False, type='str'),
            root_password=dict(required=False, type='str'),
            ip_range_network=dict(required=False, type='str'),
            ip_range_subnet=dict(required=False, type='str'),
            ip_range_start=dict(required=False, type='str'),
            ip_range_end=dict(required=False, type='str'),
            gateway=dict(required=False, type='str'),
            hostname_prefix=dict(required=False, type='str'),
            nameserver=dict(required=False, type='str'),
            ntpserver=dict(required=False, type='str'),
            vcenter_name=dict(required=False, type='str'),
            vcenter_datacenter_path=dict(required=False, type='str'),
            vcenter_cluster_path=dict(required=False, type='str'),
            enable_vsan=dict(required=False, type='str'),
            vsan_uuid=dict(required=False, type='str'),
            packages=dict(required=False, type='dict'),
            configure_disk_to_local=dict(required=False, type='str'),
            hostname_prefix=dict(required=False, type='str'),
            domainname=dict(required=False, type='str'),
            root_password=dict(required=False, type='str')
        )
    )

    create_new_hanlon_policy(module)




if __name__ == '__main__':
    main()