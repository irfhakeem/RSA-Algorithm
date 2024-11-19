# Chat-Encryption

| Nama                  | NRP        | Task                                                                                                                                        |
| --------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Muhammad Irfan Hakim  | 5025221291 | - Mengubah Algoritma DES tugas sebelumnya agar bisa menangani input lebih dari 8 char <br> - Implementasi enkripsi dan dekripsi pada client |
| Muhammad Nabil Fadhil | 5025221200 | - Implementasi server dan client                                                                                                            |

## Penjelasan DES

Untuk membuat DES bisa menangani input character lebih dari 8, kami menggunakan pendekatan dimana kami membuat input menjadi segmen-segmen berukuran 8 character yang mana kami nantinya tidak perlu mengganti algoritma enkripsi sebelumnya.

Jadi, kami hanya membuat beberapa fungsi pembantu untuk memisahkan text dan untuk melakukan loopin pada dekripsi atau enkripsi.

---

## Penjelasan RSA

RSA bekerja dengan cara membuat 2 kunci yakni kunci private dan public. Kunci yang akan dibagikan kepada orang lain secara langsung dalam bentuk angka adalah public key yang berfungsi untuk enkripsi DES key. Kemudian untuk private key nantinya akan digunakan untuk mendekripsi DES key yang terenkripsi sebelumnya.

---

## Implementasi RSA di Client

Karena di RSA memerlukan public key yang harus sama-sama diketahui oleh kedua belah pihak maka pada awal inisialisasi client saat running, akan mengenerate sebuah public key untuk masing-masing client. Kemudian public key tersebut akan dikirimkan ke client yang berbeda.

---

## Implementasi DES di RSA

Jadi kami membuat enkripsi dan dekripsi DES tetap pada file `des.py`. Kemudian, untuk `des_key` yang berebeda di kedua client akan dienkripsi menggunakan algoritma RSA pada saat client mengirimkan pesan. Kemudian saat menerima pesan, `encrypted_key` dan `encrypted_message` akan ikut terkirim dan bisa didekripsi menggunakan algoritma dekripsi untuk rsa lalu `decrypted_key` bisa digunakan untuk dekripsi pesan.

---

## Socket Programming

Untuk implementasi socket programming, kami mengikuti tutorial dari link yang diberikan https://www.digitalocean.com/community/tutorials/python-socket-programming-server-client. Namun ada beberapa perubahan pada `server.py` karna kami menggunakan 2 client dan kami menjalankannya di localhost.
