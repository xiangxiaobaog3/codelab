package main

import (
    "fmt"
    "bytes"
    "crypto/md5"
    "crypto/des"
    // "code.google.com/p/go.crypto/blowfish"
)

func main() {
    hash := md5.New()
    bb := []byte("hello\n")
    hash.Write(bb)
    hashValue := hash.Sum(nil)
    hashSize := hash.Size()
    for i := 0; i < hashSize; i+=4 {
        var val uint32
        val = (uint32(hashValue[i]) << 24 +
               uint32(hashValue[i+1]) << 16 +
               uint32(hashValue[i+2]) << 8 +
               uint32(hashValue[i+3]))
        fmt.Printf("%x", val)
    }
    fmt.Println()
    fmt.Println(hashValue)


    // symmetric key encryption

    // des
    key := []byte("12345678")
    cipher, _ := des.NewCipher(key)
    src := []byte("hello\r\n\r\n")
    var enc [512]byte

    cipher.Encrypt(enc[0:], src[0:])
    var decrypt [8]byte
    cipher.Decrypt(decrypt[0:], enc[0:])
    result := bytes.NewBuffer(nil)
    result.Write(decrypt[0:8])
    fmt.Println(string(result.Bytes()))

}
