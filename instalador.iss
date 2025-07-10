[Setup]
AppName=XMLEditor RM
AppVersion=1.2
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
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "bases.json"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\XMLEditor RM"; Filename: "{app}\main.exe"; WorkingDir: "{app}"
Name: "{commondesktop}\XMLEditor RM"; Filename: "{app}\main.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na área de trabalho"; GroupDescription: "Opções adicionais"

[Run]
Filename: "{app}\main.exe"; Description: "Executar XMLEditor RM agora"; Flags: nowait postinstall skipifsilent