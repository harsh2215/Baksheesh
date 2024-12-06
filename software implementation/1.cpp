#include <iostream>
#include <vector>
#include <fstream>
#include <iomanip>
#include <cstring>
#include <zlib.h>
#include "../enc_dec.cpp" // Include your cipher implementation

using namespace std;

// PKCS#7 Padding
void applyPadding(vector<unsigned char> &block, size_t blockSize) {
    size_t paddingSize = blockSize - block.size();
    block.resize(blockSize, paddingSize);
}

void removePadding(vector<unsigned char> &block) {
    unsigned char paddingValue = block.back();
    block.resize(block.size() - paddingValue);
}

// Convert file to vector of unsigned chars
vector<unsigned char> readFileToVector(const string &filename) {
    ifstream file(filename, ios::binary);
    if (!file.is_open()) {
        throw runtime_error("Could not open file: " + filename);
    }
    return vector<unsigned char>((istreambuf_iterator<char>(file)), istreambuf_iterator<char>());

    
}

// Write vector of unsigned chars to file
void writeVectorToFile(const string &filename, const vector<unsigned char> &data) {
    ofstream file(filename, ios::binary);
    file.write(reinterpret_cast<const char*>(data.data()), data.size());
}

// Compress data using zlib
vector<unsigned char> compressData(const vector<unsigned char> &data) {
    uLongf compressedSize = compressBound(data.size());
    vector<unsigned char> compressedData(compressedSize);

    if (compress(compressedData.data(), &compressedSize, data.data(), data.size()) != Z_OK) {
        throw runtime_error("Compression failed");
    }

    compressedData.resize(compressedSize);
    return compressedData;
}

// Decompress data using zlib
vector<unsigned char> decompressData(const vector<unsigned char> &data) {
    uLongf decompressedSize = data.size() * 4; // Initial guess for decompressed size
    vector<unsigned char> decompressedData(decompressedSize);

    while (uncompress(decompressedData.data(), &decompressedSize, data.data(), data.size()) == Z_BUF_ERROR) {
        decompressedSize *= 2;
        decompressedData.resize(decompressedSize);
    }

    decompressedData.resize(decompressedSize);
    return decompressedData;
}

int main() {
    string inputFilename = "input.txt";
    string encryptedFilename = "encrypted.bin";

    cout << "Compressing and encrypting file..." << endl;
    vector<unsigned char> data = readFileToVector(inputFilename);
    cout << "Line 72 : " << data.size() << endl;

    // Compress data

    vector<unsigned char> compressedData = compressData(data);
    cout << "Compression done" << endl;
    cout << "Line 77 : " << compressedData.size() << endl;

    // Apply padding
    applyPadding(compressedData, 32);
    cout << "After padding : " << compressedData.size() << endl;
    cout << "Line 81 : " << compressedData.size() << endl;

    // Encrypt data
    cout << "Data before encryption : " << endl;
    for(int i = 0; i < 32; i++){
        cout << (int)compressedData[i] << " ";
    }
    cout << endl;
    encryption(compressedData, key);
    cout << "Encryption done" << endl;
    cout << "Line 86 : " << compressedData.size() << endl;

    for(int i = 0; i < 32; i++){
        cout << (int)compressedData[i] << " ";
    }
    cout << endl;

    // Write encrypted data to file
    writeVectorToFile(encryptedFilename, compressedData);

    cout << "Decrypting and decompressing file..." << endl;
    vector<unsigned char> encryptedData = readFileToVector(encryptedFilename);
    cout << "Reading encrypted data from file" << endl;
    cout << "Line 94 : " << encryptedData.size() << endl;

    for(int i = 0; i < 32; i++){
        cout << (int)encryptedData[i] << " ";
    }


    // Decrypt data
    decryption(encryptedData, key);
    cout << "Decryption done" << endl;
    cout << "Line 101 : " << encryptedData.size() << endl;
    cout << "Data after decryption : " << endl;
    for(int i = 0; i < 32; i++){
        cout << (int)encryptedData[i] << " ";
    }
cout << endl;
    // Remove padding
    removePadding(encryptedData);

    // Decompress data
    vector<unsigned char> decompressedData = decompressData(encryptedData);

    // Print decompressed data to terminal
    cout << "Decompressed content:" << endl;
    cout.write(reinterpret_cast<const char*>(decompressedData.data()), decompressedData.size());
    cout << endl;

    cout << "Done." << endl;
    return 0;
}