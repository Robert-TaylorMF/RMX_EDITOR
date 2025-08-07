[Setup]
AppName=XMLEditor RM
AppVersion=2.0
AppPublisher=Robert Taylor de M. Ferreira
DefaultDirName={pf}\XMLEditor RM
DefaultGroupName=XMLEditor RM
OutputDir=dist
OutputBaseFilename=XMLEditor_Installer
SetupIconFile=recursos\xmleditor.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
DisableDirPage=no
DisableProgramGroupPage=no
UninstallDisplayIcon={app}\main.exe

[Languages]
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"

[Files]
; Arquivo principal
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion

; Arquivos de configuração na raiz
Source: "bases.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "conexoes.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "versao.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "versao.json"; DestDir: "{app}"; Flags: ignoreversion

; Pasta de recursos (ícones, imagens, gifs, etc)
Source: "recursos\*"; DestDir: "{app}\recursos"; Flags: recursesubdirs createallsubdirs ignoreversion

; Outras DLLs, bibliotecas ou arquivos do PyInstaller
Source: "dist\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{group}\XMLEditor RM"; Filename: "{app}\main.exe"; WorkingDir: "{app}"
Name: "{commondesktop}\XMLEditor RM"; Filename: "{app}\main.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na área de trabalho"; GroupDescription: "Opções adicionais"

[Run]
Filename: "{app}\main.exe"; Description: "Executar XMLEditor RM agora"; Flags: nowait postinstall skipifsilent
