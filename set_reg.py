import os
import subprocess
import winreg as reg

def find_python_path():
    """환경 변수에서 Python 경로 찾기"""
    try:
        # 'where python' 명령 실행
        result = subprocess.run(['where', 'python'], stdout=subprocess.PIPE, text=True)
        python_paths = result.stdout.strip().split('\n')
        # 첫 번째 경로 반환 (기본 Python 설치 경로)
        if python_paths:
            return python_paths[0]
    except Exception as e:
        print(f"Error finding Python path: {e}")
    return None

def add_to_context_menu(script_path, menu_name="JaMoJSH"):
    """우클릭 메뉴에 레지스트리 등록"""
    key_paths = [
        r"*\\shell\\" + menu_name,
        r"Directory\\shell\\" + menu_name
    ]
    try:
        for key_path in key_paths:
            # shell 키 생성
            with reg.CreateKey(reg.HKEY_CLASSES_ROOT, key_path) as key:
                reg.SetValue(key, '', reg.REG_SZ, "자모 정상화 하기")
                #신창섭
                if set_icon :
                    #reg.SetValue(key, 'Icon', reg.REG_SZ, icon_path)
                    reg.SetValueEx(key, 'Icon', 0, reg.REG_SZ, icon_path)
                reg.CloseKey(key)


            # command 키 생성 및 실행 경로 설정
            command_path = key_path + r"\\command"
            with reg.CreateKey(reg.HKEY_CLASSES_ROOT, command_path) as key:
                reg.SetValue(key, '', reg.REG_SZ, f'"{python_path}" "{script_path}" "%1"')
            reg.CloseKey(key)
            
        print(f"'{menu_name}' added to context menu successfully.")
    except Exception as e:
        print(f"Error adding to context menu: {e}")

if __name__ == "__main__":
    # Python 경로 찾기
    python_path = find_python_path()
    if python_path:
        print(f"Found Python path: {python_path}")
    else:
        print("Python executable not found. Please ensure Python is installed and added to PATH.")
        input("Press Enter to exit...")
        exit()

    # 사용자 스크립트 경로 입력
    folder_path = input("Enter the full path to your folder where do_normalize.py is located (e.g., C:\\JaMoJSH): ").strip()
    script_path=folder_path+"\\do_normalize.py"
    if not os.path.exists(script_path):
        print("The specified script path does not exist.")
    else:
        # 레지스트리 등록
        print("Would you like to set the icon to custom icon?")
        print("Default is picture of God Chang-Seop.")
        print("To change icon, change icon.ico file in folder")
        yesorno=input("y/n : ")

        
        icon_path=folder_path+"\\icon.ico"
        
        if yesorno=="y" or yesorno =="Y" :
            
            if not os.path.exists(icon_path):
                print("icon.ico file does not exist.")

            set_icon=True
        elif yesorno=="n" or yesorno =="N" :
            set_icon=False
        else :
            print("Please enter y/Y or n/N")
            input("Press Enter to exit...")
        add_to_context_menu(script_path)
    
    input("Press Enter to exit...")
