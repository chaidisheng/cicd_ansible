#!/usr/bin/env python3
# coding: utf-8
import os
import sys
import time
import tarfile
import argparse


class CicdTarCeph(object):
    def __init__(self):
        pass

    def get_strftime(self):
        return time.strftime('%Y%m%d%H%M', time.localtime(time.time()))


    def set_permissions(self, tarinfo):
        tarinfo.mode = 0o0777  # for example
        return tarinfo


    def make_tar_gz(self, output_filename, source_dirs):
        """
        一次性打包目录为tar.gz
        :param output_filename: 压缩文件名
        :param source_dir: 需要打包的目录
        :return: bool
        """
        try:
            print("{}".format(output_filename + '_{}.tar.gz'.format(self.get_strftime())))
            with tarfile.open(output_filename + '_{}.tar.gz'.format(self.get_strftime()), "w:gz") as tar:
                for source_dir in source_dirs:
                    tar.add(source_dir, arcname=os.path.basename(source_dir), filter=self.set_permissions)
            return 0
        except Exception as e:
            print(str(e))
            return None

def make_tar(args):
    try:
        cicd_tar_ceph = CicdTarCeph()
        return cicd_tar_ceph.make_tar_gz(args.output_filename, args.source_dirs)
    except Exception as e:
        print(e)
        return None
        
def parse_args():
    """
    argv parser manager
    :return: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(prog='cicd_ansible', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='cicd_ansible', epilog='see cicd_ansible documentation')
    parser.add_argument('-o', '--output_filename', type=str, default='', help='output filename')
    parser.add_argument('-s', '--source_dirs', nargs='+', required=True, help='source dirs to be packaged')
    parser.set_defaults(func=make_tar)
    return parser.parse_args()

if __name__ == "__main__":
    opts = parse_args()
    sys.exit(opts.func(opts))
