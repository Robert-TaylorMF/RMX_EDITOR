# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('bases.json', '.'), ('recursos\\adicionar_banco.ico', 'recursos'), ('recursos\\atualizar.ico', 'recursos'), ('recursos\\aumentar_texto.ico', 'recursos'), ('recursos\\bancos-de-dados.ico', 'recursos'), ('recursos\\colar.ico', 'recursos'), ('recursos\\copiar.ico', 'recursos'), ('recursos\\desfazer.ico', 'recursos'), ('recursos\\diminuir_texto.ico', 'recursos'), ('recursos\\editar_banco.ico', 'recursos'), ('recursos\\exportar.ico', 'recursos'), ('recursos\\imprimir.ico', 'recursos'), ('recursos\\link.ico', 'recursos'), ('recursos\\lixeira.ico', 'recursos'), ('recursos\\loading.gif', 'recursos'), ('recursos\\logo_splash.png', 'recursos'), ('recursos\\lupa.ico', 'recursos'), ('recursos\\mais.ico', 'recursos'), ('recursos\\refazer.ico', 'recursos'), ('recursos\\remover_banco.ico', 'recursos'), ('recursos\\restaurar-backup.ico', 'recursos'), ('recursos\\restaurar.ico', 'recursos'), ('recursos\\salvar.ico', 'recursos'), ('recursos\\sobre-nos.ico', 'recursos'), ('recursos\\xmleditor.ico', 'recursos')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
