import json
from pathlib import Path
import tempfile
from unittest.mock import patch

from easysolc import Solc


def test_solc_arguments_are_literal_and_globs_still_expand():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        compiler = root / 'compiler dir' / 'solc'
        compiler.parent.mkdir()
        compiler.write_text('#!/usr/bin/env python3\nimport json,sys\nprint(json.dumps(sys.argv[1:]))\n')
        compiler.chmod(0o755)
        solc = Solc(str(compiler))
        attack = 'file.sol; touch should-not-run'
        assert json.loads(solc.invoke_solc(['--bin', attack])) == ['--bin', attack]
        assert not (root / 'should-not-run').exists()

        paths = [root / 'first.sol', root / 'second.sol']
        for path in paths:
            path.write_text('contract C {}')
        with patch.object(solc, 'get_version', return_value='0.8'), patch.object(
            solc, 'invoke_solc', return_value='',
        ) as invoke:
            assert solc.compile(source=str(root / '*.sol')) == {}
        assert invoke.call_args.args[0][-2:] == [str(path) for path in paths]


def test_contract_headers_preserve_paths_with_spaces_and_colons():
    solc = Solc()
    for source in ('/tmp/Hello world.sol', '/tmp/source:part/Hello world.sol'):
        output = f'======= {source}:Hello =======\nBinary:\n6000\nContract JSON ABI\n[]\n'
        with patch.object(solc, 'get_version', return_value='0.8'), patch.object(
            solc, 'invoke_solc', return_value=output,
        ):
            assert solc.compile(source=source) == {'Hello': {'bytecode': '6000', 'abi': []}}
