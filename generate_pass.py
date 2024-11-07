import string
import secrets

def generate_pass(pass_len):
    # uppercase / lowercase / digits / punctuation
    # I think string.punctation might need to be removed in case of some characters not being in the supported standard password character????? Is this a thing????
    # 
    # Stronger passwords typically contain at least one instance of each of the following character types: upper case, lower case, numbers, and special characters.
    # Special characters include: @, &, $, % or ^. However, there is no specific obligation to include special characters for a password to be acceptable.
    # 
    # This comes from https://security-guidance.service.justice.gov.uk/password-creation-and-authentication-guide/#password-creation-and-authentication-guide
    # 
    # Will probably need removed and string.punc is returning: "#$%&'()*+,-./:;<=>?@[\]^_`{|}~  
    
    characters = string.ascii_letters + string.digits + string.punctuation


    # https://docs.python.org/3/library/secrets.html

    password = ''.join(secrets.choice(characters) for i in range(pass_len))
        
    # print(f"{password} len is: {len(password)}")

    return password
