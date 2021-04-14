import json
import uuid 

from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec    # elipticcriptography: generating keypair by choosing 2 points on an eliptic curve.
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature


class Wallet:
    """
    An individual wallet for a miner
    Keeps track of the miner's balance.
    Allows a miner to authorize transactions. 
    """
    def __init__(self):
        self.address = str(uuid.uuid4())[0:8]  # generates first 8 uniquie characters in a string-format
        self.balance = STARTING_BALANCE
        self.private_key = ec.generate_private_key(
            ec.SECP256K1(),                    # Standards of efficient cryptography Prime 256-bits Koblics 1st implementation of the algo
            default_backend()
        )
        self.public_key = self.private_key.public_key()

    def sign(self, data):
        """
        Generate a signature based on the data using the local private key.
        """
        return self.private_key.sign(
            json.dumps(data).encode('utf-8'),
            ec.ECDSA(hashes.SHA256())          # ec(ECDSA)module: Eliptic cyprographicy digital signature algo.
        )         

    @staticmethod
    def verify(public_key, data, signature):
        """
        Verify a signature based on the original public key and data.
        """
        try:
            public_key.verify(
                signature,
                json.dumps(data).encode('utf-8'),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            return False 


def main():
    wallet = Wallet()
    print(f'wallet.__dict__: {wallet.__dict__}')

    data = { 'foo': 'bar' }
    signature = wallet.sign(data)
    print(f'signature: {signature}')

    #should return True
    should_be_valid = Wallet.verify(wallet.public_key, data, signature)
    print(f'should_be_valid: {should_be_valid}')

    #a randomwallet public key should return False
    should_be_invalid = Wallet.verify(Wallet().public_key, data, signature)
    print(f'should_be_invalid: {should_be_invalid}')

if __name__ == '__main__':
    main()

