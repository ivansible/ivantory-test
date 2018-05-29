# Inventory: ivansible

My primary ansible inventory and playbooks.


## How to test a new role

    ansible-playbook plays-all/test-role.yml -e role=ivansible.<rolename> -l dock2 -e param1=value1...


## Refresh linux box

    ansible-playbook plays-all/lin-refresh.yml -l dock2,dock3

Instantly updates time, packages and kernel on a linux machine.
Hosts in the `vagrant` group will have their `apt` packet sources
switched to presumably faster `mirror.yandex.ru`.


## Reverse logins

There is so called `revssh` host entry in the `vagrant` group.
This entry allows to perform ansible operations on hosts behind NAT
(aka. poor man's ansible pull).
The `ansible_port` setting in this entry defines reverse port
forwarding.

First, login to ansible controller while reverse-forwarding
local SSH port, e.g.:

    ssh -R 8822:localhost:22 controller.host.name

Now you can run playbooks on the controller host against the
virtual `revssh` entry:

    cd <ansible_directory>
    ansible revssh -m ping
    ansible revssh -m shell -a "hostname && uname -a"

There is only one entry, so you cannot control multiple hosts this way.


## License

GPL v3

## Author

Copyright (c) 2018, [IvanDeex](https://github.com/ivandeex)
