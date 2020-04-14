# Ansible Role Docksal

![Molecule Test](https://github.com/ctorgalson/ansible-role-docksal/workflows/Molecule%20Test/badge.svg)

This role idempotently installs [Docksal](https://docksal.io/) on Ubuntu/Debian systems.

Specifically, the role performs the following tasks:

1. Clones the Docksal repo if `/usr/local/bin/fin` is not present,
2. Copies the binary into place,
3. Idempotently runs `fin config set --global` with any configured variables,
4. Runs `fin system reset`,
5. Runs `fin update`.

Note that Docksal usually runs in a user account, but that that user will need
sudo access. This means that when used in playbooks, one of two things has to
happen. Either:

1. The `ansible-playbook` command should be run with the `-K` flag, or
2. The `{{ docksal_user }}` should be set up with passwordless sudo access 
   (this is how this role's tests run).

## Role Variables

All of the following variables can be set, but _only_ `docksal_user` is mandatory.

| Variable name | Default value | Description |
|---------------|---------------|-------------|
| `docksal_repo`          | `https://github.com/docksal/docksal.git` | The github url to the Docksal repository. Should seldom need changing. |
| `docksal_dest`          | `/tmp/docksal` | The temporary location for the repository on the remote system. |
| `docksal_fin_path`      | `/usr/local/bin/fin` | The path to the `fin` binary, post-install. |
| `docksal_user`          | `example` | The user to install Docksal for. |
| `docksal_global_config` | `[]` | Docksal global configuration variables to pass to `fin config set --global` (see sample playbook, below, for syntax). |

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
      tasks:
        - name: "Include ansible-role-docksal"
          include_role:
            name: "ansible-role-docksal"

## License

GPLv2

## Author Information

Christopher Torgalson
