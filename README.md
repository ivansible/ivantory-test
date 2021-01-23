# Collection: ivantory (test)

[![Github Test Status](https://github.com/ivansible/ivantory-test/workflows/test/badge.svg?branch=master)](https://github.com/ivansible/ivantory-test/actions)

Ansible inventory and collection for **testing** [ivansible](https://github.com/ivansible) roles.


## Run a role

    ansible-playbook playbooks/run-role.yml -e role=ivansible.role_name -l vag2 -e param1=value1...
    ./bin/role [ivansible].role1[,role2...] host1,host2 -e param1=value1...

Note that `role` allows you to abbreviate long role names
like `ivansible.role_name` as `.role-name` (with a leading dot). However,
if role owner is not `ivansible`, you cannot omit it. Also you should use
the full role name with `ansible-playbook`.

Also, `role` allows to:
  - use dashes instead of underscores in role names;
  - list multiple roles as well as multiple hosts separated by commas.

Tasks tagged with `ip4only` are expected to fail on ipv6-only hosts.
Please provide the `--skip-tags ip4only` switch as a workaround.

## Fix connectivity of a new box

This type of operations is called _enter_ in ivansible parlance.
Example operations follow below.

Enter a Vultr box by root password, probing for custom SSH port and
then switching to this port, create a new user (trying to make uid=1000),
and finally install python2 and authorize my default private key.
You can try IPv4 address, IPv6 address or DNS hostname after comma.

    ivantory-lin-enter 172.1.2.3 -v -u myuser -p 8822 -k files/keys/ssh.key -r secret

Enter a box already added to repository:

    ivantory-lin-enter vag2 -K default

Enter a new Vultr box initialized with root password and enable UFW:

    ivantory-lin-enter 172.1.2.3 --rootpass secret --ufw

Enter a new Vultr box initialized with SSH key:

    ivantory-lin-enter 172.1.2.3 --keyfile files/secret/keys/newbox.key

Enter a new _virtobox_ vagrant box:

    ivantory-lin-enter vag3.dev --port 8822 --new-keyfile files/secret/keys/newbox.key

Full syntax:

    ivantory-lin-enter 172.1.2.3 -e linen_pass='secret' -e linen_user=myuser -e linen_port=8822 -e linen_keyfile=default -e linen_login_methods=4 [-e linen_ufw=true]


## Refresh a linux box

    ./bin/lin-refresh host1,host2

Instantly updates time, packages and kernel on a linux machine.
Hosts in the `vagrant` group will have their `apt` packet sources
switched to _presumably_ faster `mirror.yandex.ru`.

If you list multiple targets, the script will switch to the `free`
play strategy, allowing for faster parallel upgrades.
Otherwise, the script will fall back to the `linear` strategy.


## Playbook for basic config of a development box

    ansible-playbook plays-all/workspace.yml -l host1,host2

Available parameters:

  - `refresh` (default: `no`) -- upgrade packages and kernel
  - `ivantory` (default: `no`) -- deploy `ivantory` roles and playbooks


## Reversed logins

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


## How to bootstrap ivantory on new controller

Download `deex1.key` into `~\.ssh\deex1.key` on windows.

Powershell terminal on windows:
```powershell
> cat ~\.ssh\deex1.key  # print key to windows terminal
> cd C:\abyss\vagrant\vag1
> vg up
> vg ssh  # or login from mobassh teminal
```

Bash terminal on vagrant box:
```sh
$ cat > vakey
-----BEGIN RSA PRIVATE KEY-----
... paste the key here ...
-----END RSA PRIVATE KEY-----
^D
$ chmod 600 vakey
$ port=2022
$ ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
      -R 8822:localhost:$port -i ~/vakey -p $port -l deex zeus.
```

You are logged into zeus:
```sh
$ cd devel/ivantory
$ ansible -m ping revssh  # should reply "pong"
$ ./bin/play ivantory revssh -e real_ssh_port=2022 [-e ivantory=yes]
```

Notes:
- without explicit `real_ssh_port`, the play will incorrectly detect the
  value of `ansible_port` as _8822_ and configure firewall incorrectly
- you must log into `vag1` anew for changes to take effect
- remove `vakey` when done


## OpenVZ Hosts

OpenVZ resets `/etc/hosts` on every boot.
These playbooks contain a special tag `etc_hosts` for all tasks that update hosts.


## Vagrant Boxes

- vag1 - *enter-bionic* controller _1Gb_ RAM
- vag2 - *enter-xenial*
- vag3 - *enter-bionic*
- vag4 - *enter-xenial* python2 only
- vag5 - *enter-xenial* python3 only
- vag6 - *enter-bionic* python2 only
- vag7 - *enter-bionic* python3 only
- vag8 - *bento/xenial* port _22_ user _vagrant_
- vag9 - *bento/bionic* port _22_ user _vagrant_

**python2** boxes lack:
- python3
- snapd
- ufw
- lsb-release
- lxd
- apparmor
- ubuntu-minimal
- software-properties-common
- ssh-import-id

**python3** boxes lack:
- python2
- samba-libs
- samba-common-bin


## License

GPL v3

## Author

Copyright (c) 2018-2020, [IvanDeex](https://github.com/ivandeex)
