package main

import (
    "crypto/rand"
    "crypto/rsa"
    "crypto/x509"
    "encoding/gob"
    "encoding/pem"
    "fmt"
    "os"
)

func main() {
    reader := rand.Reader
    bitSize := 512
    key, _ := rsa.GenerateKey(reader, bitSize)
    fmt.Println("Private key primes", key.Primes[0].String(), key.Primes[1].String())
    fmt.Println("Private key exponent", key.D.String())

    publicKey := key.PublicKey
    fmt.Println("Public key modulus", publicKey.N.String())
    fmt.Println("Public key exponent", publicKey.E)

    saveGobKey("private.key", key)
    saveGobKey("public.key", publicKey)
    savePEMKey("private.pem", key)
}

func saveGobKey(fileName string, key interface{}) {
    outFile, _ := os.Create(fileName)
    defer outFile.Close()
    encoder := gob.NewEncoder(outFile)
    err := encoder.Encode(key)
    checkError(err)
}

func savePEMKey(fileName string, key *rsa.PrivateKey) {
    outFile, _ := os.Create(fileName)
    defer outFile.Close()
    var privateKey = &pem.Block{Type: "RSA PRIVATE KEY", 
                                Bytes: x509.MarshalPKCS1PrivateKey(key)}
    pem.Encode(outFile, privateKey)
}

func checkError(err error) {
    if err != nil {
        fmt.Println("Fatal error", err.Error())
        os.Exit(1)
    }
}
