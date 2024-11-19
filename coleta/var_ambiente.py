import os
from dotenv import load_dotenv


def variavel_ambiente():
    env_dir = load_dotenv('../.env_dir')
    var_env = os.getenv('DIR_BD')
    print(var_env)


def main():
    variavel_ambiente()
    
if __name__=="__main__":
    main()