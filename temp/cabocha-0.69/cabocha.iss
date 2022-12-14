[Setup]
AppName=CaboCha
AppVersion=0.69
AppVerName=CaboCha 0.69
DefaultDirName={pf}\CaboCha
AllowNoIcons=Yes
DefaultGroupName=CaboCha
LicenseFile=BSD
Compression=bzip
OutputBaseFileName=cabocha-0.69
OutputDir=.
AppPublisher=Taku Kudo
AppPublisherURL=http://cabocha.sourceforge.net/
ShowLanguageDialog=yes

[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: "jp"; MessagesFile: "compiler:Japanese.isl"

[Files]
Source: "AUTHORS";               DestDir: "{app}"
Source: "COPYING";               DestDir: "{app}"
Source: "BSD";                   DestDir: "{app}"
Source: "src\cabocha.exe";         DestDir: "{app}\bin"
Source: "src\cabocha-model-index.exe";     DestDir: "{app}\bin"
Source: "src\cabocha-system-eval.exe";     DestDir: "{app}\bin"
Source: "src\cabocha-learn.exe";     DestDir: "{app}\bin"
Source: "src\libcabocha.dll";      DestDir: "{app}\bin"
Source: "src\win32\libcrfpp.dll";      DestDir: "{app}\bin"
Source: "wintmp\cabocharc";    DestDir: "{app}\etc"
Source: "src\libcabocha.lib";  DestDir: "{app}\sdk"
Source: "src\libcabocha.dll";      DestDir: "{app}\bin"
Source: "wintmp\*.c";   DestDir: "{app}\sdk"
Source: "wintmp\*.cpp"; DestDir: "{app}\sdk"
Source: "src\cabocha.h";  DestDir: "{app}\sdk"
Source: "wintmp\model\*.ipa.txt";  DestDir: "{app}\model"
Source: "model\mkmodel.bat";  DestDir: "{app}\model"

[Icons]
Name: "{commonprograms}\CaboCha\CaboCha";           Filename: "{app}\bin\cabocha.exe"
Name: "{commonprograms}\CaboCha\Recompile SHIFT-JIS Model"; WorkingDir: "{app}\model"; Filename: "{app}\model\mkmodel.bat"; Parameters: "SHIFT-JIS"; Comment: "Recompile SHIFT-JIS Model"
Name: "{commonprograms}\CaboCha\Recompile UTF-8 Dictionary"; WorkingDir: "{app}\model";  Filename: "{app}\model\mkmodel.bat"; Parameters: "UTF-8"; Comment: "Recompile UTF-8 model"
Name: "{commonprograms}\CaboCha\Uninstall CaboCha"; Filename: "{app}\unins000.exe"
Name: "{commonprograms}\CaboCha\CaboCha Document";  Filename: "{app}\doc\index.html"
Name: "{userdesktop}\CaboCha"; Filename:  "{app}\bin\cabocha.exe"

[Run]
Filename: "{app}\model\mkmodel.bat"; Parameters: "{code:GetCharCode}"; WorkingDir: "{app}\model"

[UninstallDelete]
Type: files; Name: "{app}\model\*.model"
Type: files; Name: "{app}\model\charset-file.txt"

[Registry]
Root: HKLM; Subkey: "software\CaboCha"; Flags: uninsdeletekey; ValueType: string; ValueName: "cabocharc"; ValueData: "{app}\etc\cabocharc" ; Check: IsAdmin
Root: HKCU; Subkey: "software\CaboCha"; Flags: uninsdeletekey; ValueType: string; ValueName: "cabocharc"; ValueData: "{app}\etc\cabocharc"

[Code]
Program Setup;
var
  IsAdminFlg:         boolean;
  IsAdminCheckedFlg:  boolean;
  UserPage: TInputOptionWizardPage;

Function IsAdmin (): Boolean;
var
  conf: String;
begin
  if not IsAdminLoggedOn () then
  begin
    Result := false;
  end
  else
  begin
    conf := 'You have administrator privileges. Do you permit all users to run CaboCha';
    if ActiveLanguage = 'jp' then
    begin
      conf := '?????????????????????????????B?????R???s???[?^???S???[?U??CaboCha?????s???????????????';
    end
    if not IsAdminCheckedFlg then
       IsAdminFlg := MsgBox (conf, mbInformation, mb_YesNo) = idYes;
    IsAdminCheckedFlg := true;
    Result := IsAdminFlg;
  end;
end;

Function GetCharCode (Param: String): String;
var
  msg: String;
begin
  msg := 'Start compiling CaboCha dictionary. It will take 30-60secs.';
  if ActiveLanguage = 'jp' then
  begin
    msg := 'CaboCha???????????????????B????????1?????????????????????????????B';
  end;
  MsgBox(msg, mbInformation, mb_OK);
  Result := 'SHIFT-JIS';
  if UserPage.Values[0] = True then
  begin
     Result := 'SHIFT-JIS';
  end;
  if UserPage.Values[1] = True then
  begin
     Result := 'UTF-8';
  end;
end;

procedure InitializeWizard;
var
  msg : array[0..3] of String;
begin
  msg[0] := 'Dictionary Charset'
  msg[1] := 'Please choose character set';
  msg[2] := 'Please specify charset set of dictionary, then click Next.';
  if ActiveLanguage = 'jp' then
  begin
    msg[0] := '???????????R?[?h???I??'
    msg[1] := '???????????R?[?h???I???????????????B';
    msg[2] := '?C???X?g?[?????????????????R?[?h???I????(??????SHIFT-JIS)?A???????N???b?N?????????????B';
  end;
  UserPage := CreateInputOptionPage(wpWelcome, msg[0], msg[1], msg[2], True, True);
  UserPage.Add('SHIFT-JIS');
  UserPage.Add('UTF-8');
  UserPage.Values[0] := True;
end;
