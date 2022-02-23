import os
from typing import  List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, validator, SecretStr
from pydantic.types import FilePath
import secrets

#for decrypting secrets in Lambda env variables
import boto3
from base64 import b64decode

basedir = os.path.abspath(os.path.dirname(__file__))

#TODO: Maybe turn env key into an attribute to allow generic execution 
def get_decrypted_pw() -> str: 
    ENCRYPTED: str = os.environ['LDAP_PW']
    print(ENCRYPTED)
    # Decrypt code should run once and variables stored outside of the function
    # handler so that these are decrypted once per container
    DECRYPTED = boto3.client('kms').decrypt(CiphertextBlob=b64decode(ENCRYPTED),EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']})['Plaintext'].decode('utf-8')
    print(DECRYPTED)
    return DECRYPTED


class Settings(BaseSettings):
    #TODO: Maybe move env var getting to a function that gets and validates env vars, and sets defaults if nonexistent?
    
    API_V1_STR: str = "/api/v1"
    #LDAP_URL: str = "ldap://openldap"
    #LDAP_UN: str = "cn=admin,dc=dms,dc=local"
    #LDAP_PW: str = "Adm1n!"
    #LDAP_URL: str = "ldap://ad.dallasmakerspace.org"
    #LDAP_UN: str = "cn=,ou=service,ou=users,ou=admin,dc=dms,dc=local"

    #getenv might return type None.  Converting potential None into str to make mypy happy until a proper input validator is written
    LDAP_URL: str = str(os.getenv('LDAP_URL'))
    LDAP_UN: str = str(os.getenv('LDAP_DN'))
    #LDAP_PW: str = str(get_decrypted_pw()) # need to get env var KMS encryption working
    LDAP_PW: str = str(os.getenv('LDAP_PW'))

    #try: 
    #    LDAP_PW: str = str(get_decrypted_pw())
    #except Exception as e:
    #    print(e)

    print('LDAP_PW_Length: ' + LDAP_PW.len())
    print('Configured LDAP_URL: ' + LDAP_URL)
    print('LDAP_DN: ' + LDAP_UN)

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True


settings = Settings( basedir + "/.env")



