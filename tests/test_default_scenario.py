import os

import testinfra.utils.ansible_runner

import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


''' ansible-role-docksal (ctorgalson.docksal_ tests. '''


@pytest.mark.parametrize('path,type', [
    ('/usr/local/bin/fin', 'file'),
    ('/home/molecule/.docksal/docksal.env', 'file')
])
def test_docksal_files(host, path, type):
    f = host.file(path)

    assert f.is_file
    assert f.exists


@pytest.mark.parametrize('package,version', [
    ('fin', '1.9'),
])
def test_docksal_package(host, package, version):
    c = '{} --version'.format(package)
    r = host.run(c)

    assert version in r.stdout


@pytest.mark.parametrize('variable', [
    'DOCKSAL_VHOST_PROXY_IP="0.0.0.0"',
    'DOCKSAL_DNS_DOMAIN="molecule"',
])
def test_docksal_global_config(host, variable):
    f = host.file('/home/molecule/.docksal/docksal.env')

    assert variable in f.content_string
