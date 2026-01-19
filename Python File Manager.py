import re
import os
import shutil
import platform
from time import sleep
from pathlib import Path
from subprocess import run
from InquirerPy import inquirer
from prompt_toolkit.validation import ValidationError
from InquirerPy.validator import EmptyInputValidator, PathValidator, Validator

blocked_extensions = [
	".exe",".com",".bat",
	".msi",".msc",".ps1",
	".vbs",".js",".jar",
	".py",".msi",".lnk",
	".sh"
]

dangerous_magic_bytes = [
    b"MZ",                     
    b"\x7FELF",                 
    b"\xCA\xFE\xBA\xBE",        
]

class PathNotEmptyValidator(Validator):
	def __init__(self, **kwargs):
		self.empty = EmptyInputValidator()
		self.path = PathValidator(**kwargs)
	def validate(self, document):
		try:
			self.empty.validate(document)
		except ValidationError:
			raise ValidationError(message="Não deixe esse campo vazio")
			
		try:
			self.path.validate(document)
		except ValidationError:
			raise ValidationError(message="Esse caminho é inválido.")
		
class ExtensionValidator(Validator):
	def __init__(self, min_len=2, max_len=4, lowercase=True, no_symbols=True):
		self.empty = EmptyInputValidator()
		self.min_len = min_len
		self.max_len = max_len
		self.lowercase = lowercase
		self.no_symbols = no_symbols
		self.symbols_pattern = re.compile(r"[^a-z0-9]")
	def validate(self, document):
		try:
			self.empty.validate(document)
		except ValidationError:
			raise ValidationError(message="Não deixe esse campo vazio")
		text = document.text.lstrip(".")
		if len(text) < self.min_len:
			raise ValidationError(message="A extensão precisa conter pelo menos 2 caracteres.")
		if len(text) > self.max_len:
			raise ValidationError(message="A extensão precisa conter menos de 5 caracteres.")
		if self.lowercase and not text.islower():
			raise ValidationError(message="A extensão precisa ser em minúscula.")
		if self.no_symbols and self.symbols_pattern.search(text):
			raise ValidationError(message="A extensão não deve conter símbolos ou caracteres especiais.")	
		
def check_os():
	r = platform.system()
	return r
		
def check_sys():
	r = [platform.system(), platform.release(), platform.architecture()]
	return r

def clear_screen():
	sys = check_os()
	if sys == "Windows":
		run("cls", shell=True)
	elif sys == "Linux":
		run("clear", shell=True)
		
def resolve_base_paths():
	common = [
		"USERPROFILE", 
		"LOCALAPPDATA", 
		"APPDATA", 
		"TMP", 
		"XDG_HOME_CONFIG", 
		"HOME"
	]
	paths = []
	for path in common:
		value = os.environ.get(path)
		if value:
			paths.append(str(value))
	return paths or [Path.home()]

def list_sub(paths: list[Path]) -> list[Path]:
	sub_dirs = []
	for path in paths:
		if not path.exists():
			print(f"Pasta {path} inexistente.")
			continue		
		if not path.is_dir():
			continue
		try:
			for sub in path.iterdir():
				if sub.is_dir():
					sub_dirs.append(sub)
		except PermissionError as e:
			print(f"Erro ao acessar a pasta: {path}")
	return sub_dirs
					
def copy_folders(paths: list[Path], dest: Path):
	try:
		dest.mkdir(parents=True, exist_ok=True)
	except PermissionError:
		print("A pasta de destino não pode ser acessada/criada.")
		return
	for p in paths:
		target = dest / p.name
		try:
			shutil.copytree(
				p, 
				target, 
				symlinks=True,
				ignore=lambda d, c: {".venv", "venv", "py_env"} & set(c),
				dirs_exist_ok=True
			)
			print(f"Pasta {p} foi copiada para o {target}.")
		except PermissionError as e:
			print(f"As pastas não puderam ser gravadas no destino.: {e}")
		except Exception as e:
			print(f"Erro durante a cópia: {e}")
				
def copy_files(files: list[Path], dest: Path):
	try:
		dest.mkdir(parents=True, exist_ok=True)
	except PermissionError:
		print("A pasta de destino não pode ser acessada/criada.")
		return
	for f in files:
		target = dest / f.name
		if target.exists():
			print(f"O arquivo {f.name} já existe no destino.")
		else:
			try:
				shutil.copy2(f, target)
				print(f"Arquivo {f} foi copiado para o {target}.")
			except PermissionError as e:
				print(f"O Arquivo não foi copiado pro destino.: {e}")
			except Exception as e:
				print(f"Erro durante a cópia: {e}")
				
def move_files(files: list[Path], dest: Path):
	try:
		dest.mkdir(parents=True, exist_ok=True)
	except PermissionError:
		print("A pasta de destino não pode ser acessada/criada.")
		return
	for f in files:
		target = dest / f.name
		if target.exists():
			print(f"O arquivo {f.name} já existe no destino.")
		else:
			try:
				shutil.move(f, target)
				print(f"Arquivo {f} foi copiado para o {target}.")
			except PermissionError as e:
				print(f"O Arquivo não foi copiado pro destino.: {e}")
			except Exception as e:
				print(f"Erro durante a cópia: {e}")

def rename_file(file_path: Path, new_name: str):
	if file_path.is_file():
		new = file_path.parent / new_name
		if new.exists():
			return
		shutil.move(file_path, new)
				
def file_reader(file_path: Path):
	if not file_path.exists() or not file_path.is_file():
		print(f"O caminho recebido ou não é arquivo ou não existe.")
		return None
	try:
		return file_path.read_text(encoding="utf-8")
	except UnicodeDecodeError:
		try:
			return file_path.read_bytes()
		except Exception as e:
			print(f"Erro ao ler o arquivo: {e}")
			return None
				
def list_folders(base: Path = Path.home()) -> list[Path]:
	folders = []
	for folder in base.rglob("*"):
		if folder.is_dir() and not folder.name.startswith("."):
			if len(folders) >= 15:
				break
			folders.append(folder)
	return folders
	
def list_files(paths: list[Path], ext: str | None = None) -> list[Path]:
	files = []
	for path in paths:
		if not path.exists() or not path.is_dir():
			continue
			
		for file in path.rglob("*"):
			try:
				if file.is_file():
					if ext is None or file.suffix.lower() == ext.lower():
						files.append(file)
			except PermissionError:
				print(f"Não foi possível acessar o {file}.")
	return files

def is_safe_to_open(file_path: Path):
	if file_path.is_file():
		try:
			if file_path.suffix.lower() in blocked_extensions:
				return False
			else:
				data = file_path.read_bytes()[:8]
				if any(data.startswith(sig) for sig in dangerous_magic_bytes):
					return False
				return True
		except OSError:
			return False
		
def open_with_os(file_path: Path):
	os = check_os()
	if is_safe_to_open(file_path):
		if os == "Windows":
			os.startfile(file_path, "open")
		elif os == "Linux":
			run(["xdg-open", str(file_path)])
	else:
		print("Esse arquivo não pode ser aberto por questões de segurança.")

def delete_tree(paths: list[Path]):
	for path in paths:
		if path.is_dir():
			if path.exists():
				shutil.rmtree(path, ignore_errors=True)
			
def remove_files(paths: list[Path]):
	for path in paths:
		if path.exists():
			os.remove(path)
			
def select_folders():
	l1 = resolve_base_paths()
	l2 = list_folders()
	inq_1 = inquirer.checkbox(
		message="Selecione a(s) pasta(s):",
		choices=l1 + l2
	).execute()
	return [Path(p) for p in inq_1]

def folders_menu(folders: list[Path]):
    def list_subfolders_action():
        subs = list_sub(folders)
        if subs:
            inquirer.select(
                message=f"Subpastas no(s) destino(s): {folders}",
                choices=subs
            ).execute()
            input("Pressione Enter para continuar...")
        else:
            print("Nenhuma subpasta encontrada.")
            input("Pressione Enter para continuar...")

    def copy_folders_action():
        inq_3 = inquirer.text(
            message="Digite o destino (Ex: C:\\Users\\user\\Desktop): ",
            validate=PathNotEmptyValidator(is_dir=True)
        ).execute()
        copy_folders(folders, Path(inq_3))
        input("Pressione Enter para continuar...")

    def copy_files_action():
        inq_3 = inquirer.checkbox(
            message="Digite e/ou escolha os arquivos que deseja copiar:",
            choices=[str(f) for f in list_files(folders)],
            fuzzy=True
        ).execute()
        inq_4 = inquirer.text(
            message="Digite o destino do(s) arquivo(s):",
            validate=PathNotEmptyValidator(is_dir=True),
        ).execute()
        copy_files([Path(f) for f in inq_3], Path(inq_4))
        input("Pressione Enter para continuar...")

    def list_files_by_extension_action():
        while True:
            inq_3 = inquirer.text(
                message="Digite a extensão (Ex: html, py, exe):",
                validate=ExtensionValidator()
            ).execute()
            result = ["Voltar"] + [str(item) for item in list_files(folders, "." + inq_3)]
            inq_4 = inquirer.select(
                message="Arquivos encontrados: ",
                choices=result,
                validate=EmptyInputValidator(message="Não deixe esse campo vazio")
            ).execute()
            if inq_4 == "Voltar":
                break
            else:
                inq_5 = inquirer.select(
                    message="O que deseja fazer agora?:",
                    choices=[
                        "Ler arquivo",
                        "Executar arquivo",
                        "Voltar"
                    ]
                ).execute()
                if inq_5 == "Ler arquivo":
                    print(file_reader(Path(inq_4)))
                    input("Pressione Enter para continuar...")
                elif inq_5 == "Executar arquivo":
                    open_with_os(Path(inq_4))
                else:
                    break

    def move_files_action():
        while True:
            inq_3 = inquirer.checkbox(
                message="Arquivos encontrados:",
                choices=["Voltar"] + [str(item) for item in list_files(folders)],
                fuzzy=True
            ).execute()
            if "Voltar" in inq_3:
                break
            inq_4 = inquirer.text(
                message="Digite o destino do(s) arquivo(s):",
                validate=PathNotEmptyValidator(is_dir=True)
            ).execute()
            move_files([Path(f) for f in inq_3], Path(inq_4))
            input("Pressione Enter para continuar...")

    def rename_files_action():
        while True:
            inq_3 = inquirer.select(
                message="Escolha o arquivo que você quer renomear:",
                choices=["Voltar"] + [str(item) for item in list_files(folders)],
            ).execute()
            if inq_3 == "Voltar":
                break
            else:
                inq_4 = inquirer.text(
                    message="Digite o nome:",
                    validate=EmptyInputValidator(message="Não deixe esse campo vazio")
                ).execute()
                rename_file(Path(inq_3), inq_4)
                input("Pressione Enter para continuar...")

    def remove_files_action():
        while True:
            inq_3 = inquirer.checkbox(
                message="Escolha o(s) arquivo(s) que você quer remover:",
                choices=["Voltar"] + [str(item) for item in list_files(folders)],
                fuzzy=True
            ).execute()
            if "Voltar" in inq_3:
                break
            else:
                inq_4 = inquirer.confirm(
                    message="Tem certeza dessa decisão? isso é uma ação DESTRUTIVA",
                    confirm_letter="s",
                    reject_letter="n",
                    default=False
                ).execute()
                if inq_4:
                    removed, failed = [], []
                    for path in inq_3:
                        path_obj = Path(path)
                        try:
                            os.remove(path_obj)
                            if not path_obj.exists():
                                removed.append(path_obj)
                            else:
                                failed.append(path_obj)
                        except Exception:
                            failed.append(path_obj)
                    if removed:
                        print(f"Arquivos removidos: {[f.name for f in removed]}")
                    if failed:
                        print(f"Falha ao remover: {[f.name for f in failed]}")
                    input("Pressione Enter para continuar...")

    def remove_folders_action():
        inq_3 = inquirer.confirm(
            message="Tem certeza que quer remover TUDO das pastas selecionadas?",
            confirm_letter="s",
            reject_letter="n",
            default=False
        ).execute()
        if inq_3:
            inq_4 = inquirer.confirm(
                message="Tem certeza dessa decisão? isso é uma ação DESTRUTIVA",
                confirm_letter="s",
                reject_letter="n",
                default=False
            ).execute()
            if inq_4:
                removed, failed = [], []
                for folder in folders:
                    try:
                        shutil.rmtree(folder)
                        if not folder.exists():
                            removed.append(folder)
                        else:
                            failed.append(folder)
                    except Exception:
                        failed.append(folder)
                if removed:
                    print(f"Pastas removidas: {[p.name for p in removed]}")
                if failed:
                    print(f"Falha ao remover: {[p.name for p in failed]}")
                input("Pressione Enter para continuar...")
    menu_actions = {
        "Listar subpastas": list_subfolders_action,
        "Copiar pasta(s)": copy_folders_action,
        "Copiar arquivo(s)": copy_files_action,
        "Listar arquivos e filtrar por extensão": list_files_by_extension_action,
        "Listar e mover arquivos": move_files_action,
        "Renomear arquivos": rename_files_action,
        "Remover arquivos": remove_files_action,
        "Remover pasta(s) inteiras": remove_folders_action
    }
    while True:
        inq_2 = inquirer.select(
            message="Selecione a ação:",
            choices=list(menu_actions.keys()) + ["Voltar"]
        ).execute()
        if inq_2 == "Voltar":
            break
        menu_actions[inq_2]()
        clear_screen()
				
def menu():
    selected_folders: list[Path] = []
    while True:
        folder_status = f" ({len(selected_folders)} pasta(s) selecionada(s))" if selected_folders else ""
        inq_1 = inquirer.select(
            message=f"Selecione a ação{folder_status}:",
            choices=[
                "Selecionar pasta(s)",
                "Gerenciar pastas selecionadas",
                "Sair"
            ]
        ).execute()
        if inq_1 == "Sair":
            print("Saindo do programa...")
            break
        elif inq_1 == "Selecionar pasta(s)":
            # Seleção de pastas
            selected_folders = select_folders()
            if selected_folders:
                print(f"{len(selected_folders)} pasta(s) selecionada(s).")
            else:
                print("Nenhuma pasta selecionada.")
            input("Pressione Enter para continuar...")
            clear_screen()
        elif inq_1 == "Gerenciar pastas selecionadas":
            if not selected_folders:
                print("Nenhuma pasta selecionada. Primeiro selecione pastas.")
                input("Pressione Enter para continuar...")
                clear_screen()
                continue
            folders_menu(selected_folders)
if __name__ == "__main__":
	menu()
