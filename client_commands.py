def help():
    print "-----Lista de Comandos----"
    print "- checkdir -> apresenta as pastas e arquivos presentes no diretorio corrente."
    print "- cd path_to_dir -> permite acesso ao diretorio 'path_to_dir.'"
    print "- mv org_file dest_dir -> move 'org_file' para o diretorio 'path_to_dir'."
    print "- rm file -> remove o arquivo ou diretorrio de nome 'file'."
    print "- makedir dirname -> cria um nove diretorio de nome 'dirname'."
    print "- upload path_to_file -> faz o upload de um arquivo em 'path_to_file' para o servidor."
    print "- download file -> faz o download do arquivo 'file' para a sua maquina"
    print "- CTRL+X -> Sai do programa e fecha a conexao"
    return

def checkdir():
    print 'execute checkdir'
    return

def cd(path_to_dir):
    print "Access 'path_to_dir'"
    return

def mv(org_file, dest_dir):
    print "move ", org_file, "to ", dest_dir
    return

def rm(file):
    print "remove file"
    return

def makedir():
    print "create directory ", dirname
    return

def upload(path_to_file):
    print "upload file from ", path_to_file
    return

def download(file):
    print "download ", file
    return
