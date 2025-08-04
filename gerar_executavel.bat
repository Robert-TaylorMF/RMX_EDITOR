@echo off
echo Gerando executável com PyInstaller...

pyinstaller --onefile --windowed ^
  --add-data "bases.json;." ^
  --add-data "recursos\adicionar_banco.ico;recursos" ^
  --add-data "recursos\atualizar.ico;recursos" ^
  --add-data "recursos\aumentar_texto.ico;recursos" ^
  --add-data "recursos\bancos-de-dados.ico;recursos" ^
  --add-data "recursos\colar.ico;recursos" ^
  --add-data "recursos\copiar.ico;recursos" ^
  --add-data "recursos\desfazer.ico;recursos" ^
  --add-data "recursos\diminuir_texto.ico;recursos" ^
  --add-data "recursos\editar_banco.ico;recursos" ^
  --add-data "recursos\exportar.ico;recursos" ^
  --add-data "recursos\imprimir.ico;recursos" ^
  --add-data "recursos\link.ico;recursos" ^
  --add-data "recursos\lixeira.ico;recursos" ^
  --add-data "recursos\loading.gif;recursos" ^
  --add-data "recursos\logo_splash.png;recursos" ^
  --add-data "recursos\lupa.ico;recursos" ^
  --add-data "recursos\mais.ico;recursos" ^
  --add-data "recursos\refazer.ico;recursos" ^
  --add-data "recursos\remover_banco.ico;recursos" ^
  --add-data "recursos\restaurar-backup.ico;recursos" ^
  --add-data "recursos\restaurar.ico;recursos" ^
  --add-data "recursos\salvar.ico;recursos" ^
  --add-data "recursos\sobre-nos.ico;recursos" ^
  --add-data "recursos\xmleditor.ico;recursos" ^
  main.py

echo Executável gerado com sucesso!
pause
