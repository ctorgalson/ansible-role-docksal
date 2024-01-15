# Ansible Role Docksal

This role idempotently installs [Docksal](https://docksal.io/) on Ubuntu/Debian
systems. Without piping the installer script directly to `bash`.

Specifically, the role performs the following tasks:

1. gathers information about the currently installed `fin` binary, if any,
2. ensures the `/usr/local/bin/` directory exists,
3. downloads the `fin` binary directly from `https://raw.githubusercontent.com`,
4. runs `fin update`,
5. checks the `fin` binary version marking it as changed when `fin --version`
   returns a different result from when the role started.

Note that Docksal usually runs in a user account, but that that user will need
sudo access. This means that when used in playbooks, one of two things has to
happen. Either:

1. The `ansible-playbook` command should be run with the `-K` flag, or
2. The `{{ docksal_user }}` should be set up with passwordless sudo access 
   (this is how this role's tests run).

## Role Variables

| Variable name | Default value | Location | Description |
|---------------|---------------|----------|-------------|
| `docksal__bin_dir`         | `/usr/local/bin`             | `vars/main.yml`     | The directory to install the `fin` binary to. |
| `docksal__fin__path`       | `{{ docksal__bin_dir }}/fin` | `vars/main.yml`     | The full path to the installed `fin` binary.  |
| `docksal__user`            | `{{ ansible_user }}`         | `defaults/main.yml` | The user to install Docksal/fin for.          |
| `docksal__docksal_version` | `master`                     | `defaults/main.yml` | The specific version of Docksal to install.   |
| `docksal__global_config`   | `[]`                         | `defaults/main.yml` | Config  variables to set in the `docksal_user`'s `.docksal` directory. Each item must include a `key` property and a `value` property. If the item also has a property `secret` set to `true`, `no_log` will be used for the ansible task that sets the variable. |

## Example Playbook

    ---
    - name: Install and configure Docksal.
      hosts: all
      vars:
        docksal_user: "molecule"
        docksal_user_rc_file: "{{ docksal_user_home }}/.bashrc"
        docksal_global_config:
          - key: "DOCKSAL_VHOST_PROXY_IP"
            value: "0.0.0.0"
          - key: "DOCKSAL_DNS_DOMAIN"
            value: "molecule"
          - key: "SOME_PRIVATE_VARIABLE"
            value: "N1UK2mLzbsHAZoFLvj7ipgtfyR6HbONwTQZWsi24Gd02QShamLuEqCA3lcJ67mxl"
            secret: true
      tasks:
        - name: "Include ansible-role-docksal"
          include_role:
            name: "ansible-role-docksal"

## License

GPLv2

## Author Information

Christopher Torgalson
