[Setup]
AppName=XMLEditor RM
AppVersion=1.3
DefaultDirName={pf}\XMLEditor RM
DefaultGroupName=XMLEditor RM
OutputBaseFilename=XMLEditorRM_Setup_1_3
SetupIconFile=recursos\meu_icone.ico
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "backups_xml\*"; DestDir: "{app}\backups_xml"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "config.json"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\XMLEditor RM"; Filename: "{app}\main.exe"
Name: "{desktop}\XMLEditor RM"; Filename: "{app}\main.exe"