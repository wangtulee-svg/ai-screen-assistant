; installer.iss
; Inno Setup Script ສຳລັບ AI Screen Assistant

#define MyAppName "AI Screen Assistant"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Your Name"
#define MyAppExeName "AI-Screen-Assistant.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=installer_output
OutputBaseFilename=AI-Screen-Assistant-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "src\*"; DestDir: "{app}\src"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
// ກວດສອບ Tesseract
function InitializeSetup(): Boolean;
var
  TesseractPath: String;
begin
  Result := True;
  TesseractPath := 'C:\Program Files\Tesseract-OCR\tesseract.exe';
  
  if not FileExists(TesseractPath) then
  begin
    if MsgBox('Tesseract OCR ຍັງບໍ່ໄດ້ຕິດຕັ້ງ. ທ່ານຕ້ອງການຕິດຕັ້ງບໍ່?', 
              mbConfirmation, MB_YESNO) = IDYES then
    begin
      MsgBox('ກະລຸນາດາວໂຫຼດ ແລະ ຕິດຕັ້ງ Tesseract ຈາກ:' + #13#10 +
             'https://github.com/UB-Mannheim/tesseract/wiki', 
             mbInformation, MB_OK);
    end;
  end;
end;