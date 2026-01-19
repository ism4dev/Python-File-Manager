# 🗂️ Python File Manager

Gerenciador de arquivos e pastas desenvolvido em **Python**, voltado para **automatização de tarefas**, **suporte técnico** e **operações em Windows e Linux**.

## 🔹 Funcionalidades

- Listar pastas e subpastas
- Listar arquivos e filtrar por extensão
- Copiar e mover arquivos e pastas
- Renomear arquivos
- Remover arquivos ou pastas inteiras com confirmação
- Abertura segura de arquivos (`.exe`, `.bat`, `.py` e outros arquivos perigosos são bloqueados)
- Validações interativas sem tracebacks feios
- Compatível com Windows e Linux

---

## 🔹 Tecnologias e Competências Aplicadas

- Python 3.14
- `InquirerPy` para menus interativos
- `shutil`, `os`, `pathlib` para manipulação de arquivos e pastas
- Tratamento de exceções e validação de inputs
- Conceitos de suporte técnico e operações em Windows e Linux

---

## 🔹 Pré-requisitos

- Python 3.14 ou superior
- Dependências:

```bash
pip install InquirerPy
````

> Também pode ser compilado em executável com PyInstaller ou Nuitka para Windows (`.exe`) ou Linux (`.elf`).

---

## 🔹 Como usar (via Python)

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/python-file-manager.git
cd python-file-manager
```

2. Execute o programa:

```bash
python main.py
```

3. Navegue pelo menu interativo:

* **Selecionar pasta(s)** → Escolha uma ou mais pastas para manipulação
* **Gerenciar pastas selecionadas** → Abrir menu com operações de arquivos e pastas

---

## 🔹 Compilando em executáveis

Para manter **versões separadas de Linux e Windows**, crie um diretório `builds/` com subpastas `windows/` e `linux/`:

```
builds/
├── windows/
└── linux/
```

### PyInstaller

**Windows:**

```bash
py -m PyInstaller --onefile --name "Python File Manager" --icon path/to/icon.ico main.py
move dist/PythonFileManager.exe builds/windows/
```

**Linux:**

```bash
py -m PyInstaller --onefile --name "Python File Manager" main.py
mv dist/PythonFileManager builds/linux/PythonFileManager.elf
```

> No Linux, o ícone deve ser configurado via arquivo `.desktop` para aparecer no menu gráfico.

### Nuitka (opcional, mais rápido)

**Windows:**

```bash
python -m nuitka --onefile --windows-icon-from-ico=path/to/icon.ico main.py
move main.exe builds/windows/
```

**Linux:**

```bash
python -m nuitka --onefile main.py
mv main.elf builds/linux/
```

---

## 🔹 Estrutura do Projeto

```
python-file-manager/
│
├── main.py             # Script principal do File Manager
├── README.md           # Documentação
├── requirements.txt    # Dependências (opcional)
└── builds/             # Executáveis compilados
    ├── windows/        # Versões .exe
    └── linux/          # Versões .elf
```

---

## 🔹 Objetivo do Projeto

Primeira experiência profissional em Python aplicando:

* Suporte técnico e operações em Windows e Linux
* Automação de tarefas com Python
* Validação de inputs e manipulação segura de arquivos
* Desenvolvimento de aplicativos CLI interativos

---

## 🔹 Contato

* LinkedIn: [Seu Perfil](https://www.linkedin.com/in/seu-usuario/)
* GitHub: [Python File Manager](https://github.com/seu-usuario/python-file-manager)

```
```
