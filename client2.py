import socket
import pickle
from rsa import generate_keypair, hybrid_encrypt, hybrid_decrypt

def client_program():
    host = '127.0.0.1'
    port = 3000

    # Generate RSA key pair
    print("Starting...")
    public_key, private_key = generate_keypair()

    # DES key sebagai string
    des_key = "client02"  # pastikan panjang key 8 karakter
    print("testing")

    client_name = "client2"  # Nama client

    try:
        # Inisialisasi socket dan koneksi
        client_socket = socket.socket()
        client_socket.connect((host, port))
        print("Connected to server")

        # Kirim public key dan private key ke server
        client_socket.send(pickle.dumps((public_key, private_key)))
        print("Sent public and private key to server")

        # Terima public key lawan dari server
        other_client_public_key = pickle.loads(client_socket.recv(4096))
        print("Received other client's public key")

        message = input(" -> ")

        while message.lower().strip() != 'bye':
            if message:
                try:
                    # Enkripsi pesan menggunakan public key lawan
                    encrypted_message, encrypted_des_key = hybrid_encrypt(
                        message,
                        des_key,
                        other_client_public_key
                    )

                    # Buat paket data dengan menambahkan public key pengirim
                    data_packet = {
                        'encrypted_message': encrypted_message,
                        'encrypted_des_key': encrypted_des_key,
                        'sender_public_key': public_key,  # Tambahkan public key pengirim
                        'sender_name': client_name  # Tambahkan nama pengirim
                    }

                    # Kirim paket terenkripsi
                    client_socket.send(pickle.dumps(data_packet))

                except Exception as e:
                    print(f"Error encrypting message: {e}")
                    continue

            # Terima dan dekripsi pesan
            try:
                encrypted_data = pickle.loads(client_socket.recv(4096))
                if encrypted_data:
                    # Verifikasi pengirim menggunakan public key
                    sender_public_key = encrypted_data['sender_public_key']
                    sender_name = encrypted_data['sender_name']  # Ambil nama pengirim
                    
                    # Dekripsi menggunakan private key sendiri
                    decrypted_message = hybrid_decrypt(
                        encrypted_data['encrypted_message'],
                        encrypted_data['encrypted_des_key'],
                        private_key
                    )
                    print(f'Received from {sender_name}: {decrypted_message}')
            except Exception as e:
                print(f"Error receiving/decrypting message: {e}")
                continue

            message = input(" -> ")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        client_socket.close()
        print("Connection closed")

if __name__ == '__main__':
    client_program()