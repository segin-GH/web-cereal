# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['run.py'],
             pathex=['~/code/web-cereal/oats/oats-agent'],
             binaries=[],
             datas=[],
             hiddenimports=[
                         'engineio.async_drivers.eventlet',
                         'eventlet',
                         'eventlet.hubs.epolls',
                         'eventlet.hubs.kqueue',
                         'eventlet.hubs.selects',
                         'dns', 
                         'dns.dnssec',
                         'dns.e164',
                         'dns.hash',
                         'dns.namedict',
                         'dns.tsigkeyring',
                         'dns.update',
                         'dns.versioned',
                         'dns.zone'
                      ],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='oats-agent',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='oats-agent')

