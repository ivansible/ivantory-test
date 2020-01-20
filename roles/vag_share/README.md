# vag_share (local role)

Creates a CIFS mount of temporary developer directory from vagrant host.


## Requirements

You must share your directory on the vagrant host

### Enable sharing on the virtualbox host network

![1-1.network-adapter-list](https://raw.githubusercontent.com/ivault/ivansible.vag-share/master/help/images/1-1.network-adapter-list.png)

![1-2.network-adapter-props](https://raw.githubusercontent.com/ivault/ivansible.vag-share/master/help/images/1-2.network-adapter-props.png)

### Share your folder

![3-1.explorer.folder](https://raw.githubusercontent.com/ivault/ivansible.vag-share/master/help/images/3-1.explorer.folder.png)

![3-2.explorer.props-sharing](https://raw.githubusercontent.com/ivault/ivansible.vag-share/master/help/images/3-2.explorer.props-sharing.png)

![3-3.explorer.new-sharing](https://raw.githubusercontent.com/ivault/ivansible.vag-share/master/help/images/3-3.explorer.new-sharing.png)

![3-4.explorer.set-name](https://raw.githubusercontent.com/ivault/ivansible.vag-share/master/help/images/3-4.explorer.set-name.png)

![3-5.explorer.open-perms](https://raw.githubusercontent.com/ivault/ivansible.vag-share/master/help/images/3-5.explorer.open-perms.png)

![3-6.explorer.change-perms](https://raw.githubusercontent.com/ivault/ivansible.vag-share/master/help/images/3-6.explorer.change-perms.png)

### Verify your share is on the list of computer shares

![2-1.cman-admin-tools](https://raw.githubusercontent.com/ivault/ivansible.vag-share/master/help/images/2-1.cman-admin-tools.png)

![2-2.cman-comp-mgmt](https://raw.githubusercontent.com/ivault/ivansible.vag-share/master/help/images/2-2.cman-comp-mgmt.png)

![2-3.cman-shares](https://raw.githubusercontent.com/ivault/ivansible.vag-share/master/help/images/2-3.cman-shares.png)

![2-4.cman-share-props](https://raw.githubusercontent.com/ivault/ivansible.vag-share/master/help/images/2-4.cman-share-props.png)

![2-5.cman-perms](https://raw.githubusercontent.com/ivault/ivansible.vag-share/master/help/images/2-5.cman-perms.png)


## Variables

    vag_share_host: 192.168.1.1
    vag_share_name: ''
    vag_share_user: {{ansible_user_id}}
    vag_share_pass: secret_pass
    vag_share_mount: ~/shares/host"

...


## Tags

None


## Dependencies

None


## Implementation Details

Manual creation of systemd mount/automount units requires hard-coding a mount path
in the unit file name (I deem it rather bad practice)
so we use ansible [mount module](https://docs.ansible.com/ansible/latest/modules/mount_module.html#mount-module)
and kick systemd indirectly via a specially krafted line in `/etc/fstab`.

Instead of direct mount (`mount state=mounted`) we kick systemd automounter
by including the specific [x-systemd.automount](https://askubuntu.com/questions/593174/x-systemd-automount-cifs-shares-in-fstab/859158#859158) option in the ``/etc/fstab`` mount line.
Wise people [recommend](https://askubuntu.com/questions/593174/x-systemd-automount-cifs-shares-in-fstab/859158#859158) to
daemon-reload systemd and restart the `remote-fs` target to activate automounter.
The mount will activate upon first use. We even disable on-boot mounting via the
`noauto` option. If we told [mount module state=`mounted`](https://docs.ansible.com/ansible/latest/modules/mount_module.html#mount-module) to activate the mount immediately,
systemd automount would give an error, so we set state to just `present` in /etc/fstab.

At any rate [systemd will require](http://manpages.ubuntu.com/manpages/xenial/man5/systemd.mount.5.html)
/sbin/mount.cifs so we install the `cifs-utils` package.

Since fstab is world-readable, we put [cifs credentials](https://serverfault.com/questions/367934/how-do-i-pass-credential-file-to-mount-cifs/367942#367942)
in a file with limited access.


## Running

    ./scripts/role.sh vag-share vag1


## License

MIT


## Author

Created in 2018-2020 by [IvanSible](https://github.com/ivansible)
