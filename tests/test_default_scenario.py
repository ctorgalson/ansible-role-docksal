import os

import testinfra.utils.ansible_runner

import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


''' ansible-role-docksal (ctorgalson.docksal_ tests. '''


@pytest.mark.parametrize('path,type', [
  ('/usr/local/bin/fin', 'file')
])
def test_docksal_files(host, path, type):
    f = host.file(path)

    if type == 'file':
        assert f.is_file
    if type == 'directory':
        assert f.is_directory

    assert f.exists


@pytest.mark.parametrize('package,version', [
  ('fin', '1.9'),
])
def test_docksal_package(host, package, version):
    c = '{} --version'.format(package)
    r = host.run(c)

    assert version in r.stdout
