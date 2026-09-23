; installer_v3.iss
; Inno Setup Script ສຳລັບ AI Screen Assistant V3

#define MyAppName "AI Screen Assistant"
#define MyAppVersion "3.0.0"
#define MyAppPublisher "AI Assistant"
#define MyAppExeName "AI-Screen-Assistant-v3.exe"

[Setup]
AppId={{B2C3D4E5-F6A7-8901-BCDE-F23456789012}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=installer_output_v3
OutputBaseFilename=AI-Screen-Assistant-v3-Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
SetupIconFile=app_icon.ico  

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
var
  TesseractPath: String;
begin
  Result := True;
  TesseractPath := 'C:\Program Files\Tesseract-OCR\tesseract.exe';
  
  if not FileExists(TesseractPath) then
  begin
    if MsgBox('Tesseract OCR ຍັງບໍ່ໄດ້ຕິດຕັ້ງ.' + #13#10 +
              'ກະລຸນາດາວໂຫຼດ ແລະ ຕິດຕັ້ງກ່ອນ:' + #13#10 +
              'https://github.com/UB-Mannheim/tesseract/wiki', 
              mbConfirmation, MB_YESNO) = IDNO then
    begin
      Result := False;
    end;
  end;
end;