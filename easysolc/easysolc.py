#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
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
        self.version = None
        if solc_path:
            solc_path = solc_path
            if solc_path[-1] == '/':
                solc_path = solc_path[:-1]
            if solc_path[::-1][:4] == 'clos':
                self.solc_path = solc_path
            else:
                self.solc_path = solc_path + '/solc'
        else:
            self.solc_path = 'solc'

    def get_version(self):
        if self.version == None:
            self.version = self.invoke_solc('--version').split('\n')[1].split()[1]
        return self.version

    def invoke_solc(self, args):
        if type(args) == str:
            args = [args]
        str_args = f'{self.solc_path} ' + ' '.join(args)
        try:
            output = subprocess.check_output(
                str_args, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
            return output
        except subprocess.CalledProcessError as e:
            output = e.output.decode('utf-8')
            logging.error(output)

    def get_contract_instance(self,
                              contract_dict=None,
                              w3=None,
                              source=None,
                              contract_name=None,
                              address=None,
                              abi_file=None,
                              bytecode_file=None):
        if w3 == None:
            w3 = Web3()
        contract = None
        if source and contract_name:
            contract_dict = self.compile(source=source)[contract_name]
        if contract_dict:
            contract = w3.eth.contract(
                abi=contract_dict['abi'], bytecode=contract_dict['bytecode'], address=address)            
        elif abi_file:
            with open(abi_file, 'r') as abi_file:
                abi = json.loads(abi_file.read())
            if address:
                contract = w3.eth.contract(abi=abi, address=address)
            elif bytecode_file:
                bytecode = None
                if bytecode_file:
                    with open(bytecode_file, 'r') as bytecode_file:
                        bytecode = bytecode_file.read()
                    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
                else:
                    raise ValueError("The bytecode or the address must be provided")
        return contract

    def compile(self,
                source='*.sol',
                args=None,
                optimize=False,
                optimize_runs=200,
                pretty_json=False,
                libraries=None,
                output_dir=None,
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

        logging.info(f'Solc version: {self.get_version()}')
        logging.info(f'Compiling: {source}')

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
            if output_dir:
                args += ['--output-dir', output_dir]
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

        args += [source]
        output = self.invoke_solc(args)

        library = {}
        dict_ = {}
        output = output.split('\n')
        for i, val in enumerate(output):
            if val == "":
                output[i] = " "
        for i in range(len(output)):
            if not output[i]:
                continue
            if output[i][0] == '=':
                contract_name = output[i].split()[1].split(':')[1]
                dict_[contract_name] = {}
                i += 1
                while not output[i]:
                    i += 1
                while i < len(output) and output[i] and output[i][0] != '=':
                    if output[i][:7] == 'Binary:':
                        i += 1
                        dict_[contract_name]['bytecode'] = output[i]
                    elif output[i][:17] == 'Contract JSON ABI':
                        i += 1
                        dict_[contract_name]['abi'] = json.loads(output[i])
                    elif output[i][:4] == '// $':
                        file_path = output[i]
                        if self.parse_for_file(file_path).split(':')[1] not in library.keys():
                            library[self.parse_for_file(file_path).split(':')[1]] = "__" + output[i][3:39] + "__"
                    elif output[i] == " ":
                        pass
                    else:
                        logging.warn(output[i])
                    i += 1
        if libraries is not None and len(libraries) > 0:
            for name, contract in dict_.items():
                # print("Inserting Libraries For {}".format(name))
                # print("Libraries are: {}".format(library))
                for library_name, library_id in library.items():
                    for lib in libraries:
                        lib_name = lib.split(':')[0]
                        lib_address = lib.split(':')[1]
                        if library_name == lib_name:
                            contract['bytecode'] = self.insert_library(contract['bytecode'], library_id, lib_address)
                lib_check = contract['bytecode'].find("__$")
                if lib_check != -1:
                    raise Exception("There the library '{}' was not passed.".format(contract['bytecode'][contract][lib_check + 36]))
        return dict_

    def parse_for_file(self, string):
        directories = []
        for i, val in enumerate(string):
            if val == "/":
                directories.append(i)
        if len(directories) > 0:
            file_start = directories[len(directories) - 1] + 1
            return string[file_start:]
        else:
            return ""

    def insert_library(self, bytecode, library_id, library_address):
        while True:
            if bytecode.find(library_id) != -1:
                addr = library_address[2:]
                bytecode = bytecode.replace(library_id, addr)
            else:
                return bytecode
