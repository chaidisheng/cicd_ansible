import os
import re


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    requirements_dir = os.path.join(base_dir, 'ceph-deps/python3_yum_openEuler_x86')

    downloads_packages = set([])
    for req_file in os.listdir(requirements_dir):
        if re.match(r'pip3.*\.list$', req_file):
            with open(os.path.join(requirements_dir, req_file), 'r') as f:
                packages = f.readlines()
                downloads_packages.update([pkg.strip() for pkg in packages])
    
    cmdline = "pip3 download -d ./pip3 %s -i http://10.1.74.162/artifactory/api/pypi/pypi/simple/" % ' '.join(sorted(downloads_packages, key=str.lower))


if __name__  == '__main__':
    main()