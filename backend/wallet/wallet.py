import json
import uuid 

from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec    # elipticcriptography: generating keypair by choosing 2 points on an eliptic curve.
from cryptography.hazmat.primitives.asymmetric.utils import (
    encode_dss_signature,
    decode_dss_signature
) #digital signature standard
from cryptography.hazmat.primitives import hashes, serialization
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
        self.serialize_public_key()

    def sign(self, data):
        """
        Generate a signature based on the data using the local private key.
        """
        return decode_dss_signature(self.private_key.sign(
            json.dumps(data).encode('utf-8'),
            ec.ECDSA(hashes.SHA256())          # ec(ECDSA)module: Eliptic cyprographicy digital signature algo.
        ))

    def serialize_public_key(self):
        """
        Reset the public key to its serialized version.
        """
        self.public_key = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')


    @staticmethod
    def verify(public_key, data, signature):
        """
        Verify a signature based on the original public key and data.
        """
        # turn public key string backinto public key object
        deserialized_public_key = serialization.load_pem_public_key(
            public_key.encode('utf-8'),
            default_backend()
        )

        #print(f'\nsignature: {signature}\n')
        (r, s) = signature

        try:
            deserialized_public_key.verify(
                encode_dss_signature(r, s),
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

