from dotenv import load_dotenv
import os

load_dotenv()

# Configurações da aplicação
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:root@127.0.0.1:3306/crypto_wallet")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd,brl"