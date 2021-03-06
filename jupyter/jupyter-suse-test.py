#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import argparse
import hpccm

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Jupyter notebook container generator')
    parser.add_argument('--environment', type=str,
                        help='Conda environment file')
    parser.add_argument('--format', type=str, default='docker',
                        choices=['docker', 'singularity'],
                        help='Container specification format (default: docker)')
    parser.add_argument('--image', type=str, default='ubuntu:18.04',
                        help='Base container image (default: ubuntu:18.04)')
    parser.add_argument('--notebook', required=True, type=str,
                        help='Jupyter notebook file')
    parser.add_argument('--packager', type=str, default='pip',
                        choices=['anaconda', 'pip'],
                        help='Python package manager (default: pip)')
    parser.add_argument('--requirements', type=str,
                        help='pip requirements file')
    args = parser.parse_args()

    ### Create Stage
    stage = Stage0

    ### Base image
    stage += hpccm.primitives.baseimage(image=args.image, _docker_env=False, bootstrap="docker-daemon")

    ### Install Python and Jupyter (and requirements / environment)
    if args.packager == 'pip':
        stage += hpccm.building_blocks.python(python2=False)
        stage += hpccm.building_blocks.pip(packages=['ipython', 'jupyter'],
                                           pip='pip3',
                                           requirements=args.requirements)
    elif args.packager == 'anaconda':
        stage += hpccm.building_blocks.conda(environment=args.environment,
                                             eula=True,
                                             packages=['ipython', 'jupyter', 'jupyterhub'])

    ### Make the port accessible (Docker only)
    stage += hpccm.primitives.raw(docker='EXPOSE 8888')

    ### Add the notebook itself
    stage += hpccm.primitives.copy(src=args.notebook, dest='/notebook/',
                                   _mkdir=True)

    ### Set container specification output format
    hpccm.config.set_container_format(args.format)

    ### Output container specification
    print(stage)

