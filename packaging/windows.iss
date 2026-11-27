#ifndef AppVersion
#define AppVersion "0.1.0-alpha.2"
#endif
#ifndef OutputName
#define OutputName "ENGLERN-0.1.0-alpha.2-windows-x64-standard-setup"
#endif
[Setup]
AppId=ENGLERN.Desktop
AppName=ENGLERN
AppVersion={#AppVersion}
DefaultDirName={localappdata}\Programs\ENGLERN
DefaultGroupName=ENGLERN
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
OutputDir=..\release
OutputBaseFilename={#OutputName}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
CloseApplications=yes
UninstallDisplayIcon={app}\ENGLERN.exe
[Files]
Source: "..\dist\ENGLERN\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; Flags: unchecked
[Icons]
Name: "{group}\ENGLERN"; Filename: "{app}\ENGLERN.exe"
Name: "{autodesktop}\ENGLERN"; Filename: "{app}\ENGLERN.exe"; Tasks: desktopicon
[Run]
Filename: "{app}\ENGLERN.exe"; Description: "Launch ENGLERN"; Flags: nowait postinstall skipifsilent
