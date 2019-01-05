#!/usr/bin/env python
# -*- coding: utf-8 -*-

from web3 import Web3
import json
import subprocess
import logging


class Solc:
    def __init__(self, solc_path=''):
        logging.getLogger().setLevel(logging.INFO)
        logging.basicConfig(
            format='%(asctime)-15s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
        if solc_path:
            solc_path = solc_path
            if solc_path[-1] == '/':
                solc_path = solc_path[:-1]
            if solc_path[::-1][:4] == 'clos':
                self.solc_path = solc_path
                return
            self.solc_path = solc_path + '/solc'
            return
        self.solc_path = 'solc'

    @staticmethod
    def get_contract(abi_filepath, bytecode_filepath):
        with open(abi_filepath, 'r') as abi_file:
            abi = json.loads(abi_file.read())
        with open(bytecode_filepath, 'r') as bytecode_file:
            bytecode = bytecode_file.read()
        contract = Web3().eth.contract(abi=abi, bytecode=bytecode)
        return contract

    def compile(self,
                source='*.sol',
                args=None,
                optimize=False,
                optimize_runs=200,
                pretty_json=False,
                libraries=None,
                output_dir='.',
                overwrite=True,
                combined_json=None,
                gas=False,
                standard_json=False,
                assemble=False,
                yul=False,
                strict_assembly=False,
                machine=None,
                link=False,
                metadata_literal=False,
                allow_paths=None,
                ignore_missing=False,
                ast=False,
                ast_json=False,
                ast_compact_json=False,
                asm=False,
                asm_json=False,
                opcodes=False,
                bin_=True,
                bin_runtime=False,
                abi=True,
                hashes=False,
                userdoc=False,
                devdoc=False,
                metadata=False):
        if type(args) == str:
            args = args.split()
        if not args:
            args = []
            if optimize:
                args.append('--optimize')
                args += ['--optimize-runs', optimize_runs]
            if pretty_json:
                args.append('--pretty-json')
            if libraries:
                if type(libraries) == str:
                    libraries = libraries.split()
                args += ['--libraries'] + libraries
            if overwrite:
                args.append('--overwrite')
            if combined_json:
                if type(combined_json) == str:
                    combined_json = combined_json.split()
                args += ['--combined-json'] + combined_json
            if gas:
                args.append('--gas')
            if standard_json:
                args.append('--standard-json')
            if assemble:
                args.append('--assemble')
            if yul:
                args.append('--yul')
            if strict_assembly:
                args.append('--strict_assembly')
            if machine:
                args.append('--machine')
            if link:
                args.append('--link')
            if metadata_literal:
                args.append('--metadata-literal')
            if allow_paths:
                if type(allow_paths) == str:
                    allow_paths = allow_paths.split()
                args += ['--allow-paths'] + allow_paths
            if ignore_missing:
                args.append('--ignore-missing')
            if ast:
                args.append('--ast')
            if ast_json:
                args.append('--ast-json')
            if ast_compact_json:
                args.append('--ast-compact-json')
            if asm:
                args.append('--asm')
            if asm_json:
                args.append('--asm-json')
            if opcodes:
                args.append('--opcodes')
            if bin_:
                args.append('--bin')
            if bin_runtime:
                args.append('--bin-runtime')
            if abi:
                args.append('--abi')
            if hashes:
                args.append('--hashes')
            if userdoc:
                args.append('--userdoc')
            if devdoc:
                args.append('--devdoc')
            if metadata:
                args.append('--metadata')

        args += ['--output-dir', output_dir, source]
        args = [self.solc_path] + args

        try:
            output = subprocess.check_output(
                ' '.join(args), shell=True, stderr=subprocess.STDOUT)
            logging.info(output.decode('utf-8'))
        except subprocess.CalledProcessError as e:
            logging.error(e.output.decode('utf-8'))
