#include "bits/stdc++.h"
using namespace std;

vector<unsigned char> key = {0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0, 0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0, 0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0, 0x0,0x0,};

vector<unsigned char> plaintext = {0x4,0x4,0x4,0x4,0x4,0x4,0x4,0x4,0x4,0x4, 0x4,0x4,0x4,0x4,0x4,0x4,0x4,0x4,0x4,0x4, 0x4,0x4,0x4,0x4,0x4,0x4,0x4,0x4,0x4,0x4, 0x4,0x4,};

vector<unsigned char> SBox ={3, 0, 6, 13, 11, 5, 8, 14, 12, 15, 9, 2, 4, 10, 7, 1};

vector<unsigned char> InvSBox ={1, 15, 11, 0, 12, 5, 2, 14, 6, 10, 13, 4, 8, 3, 7, 9};

vector<unsigned char> Permutation={0, 33, 66, 99, 96, 1, 34, 67, 64, 97, 2, 35, 32, 65, 98, 3, 4, 37, 70, 103, 100, 5, 38, 71, 68, 101, 6, 39, 36, 69, 102, 7, 8, 41, 74, 107, 104, 9, 42, 75, 72, 105, 10, 43, 40, 73, 106, 11, 12, 45, 78, 111, 108, 13, 46, 79, 76, 109, 14, 47, 44, 77, 110, 15, 16, 49, 82, 115, 112, 17, 50, 83, 80, 113, 18, 51, 48, 81, 114, 19, 20, 53, 86, 119, 116, 21, 54, 87, 84, 117, 22, 55, 52, 85, 118, 23, 24, 57, 90, 123, 120, 25, 58, 91, 88, 121, 26, 59, 56, 89, 122, 27, 28, 61, 94, 127, 124, 29, 62, 95, 92, 125, 30, 63, 60, 93, 126, 31};

vector<unsigned char> InvPermutation={0, 5, 10, 15, 16, 21, 26, 31, 32, 37, 42, 47, 48, 53, 58, 63, 64, 69, 74, 79, 80, 85, 90, 95, 96, 101, 106, 111, 112, 117, 122, 127, 12, 1, 6, 11, 28, 17, 22, 27, 44, 33, 38, 43, 60, 49, 54, 59, 76, 65, 70, 75, 92, 81, 86, 91, 108, 97, 102, 107, 124, 113, 118, 123, 8, 13, 2, 7, 24, 29, 18, 23, 40, 45, 34, 39, 56, 61, 50, 55, 72, 77, 66, 71, 88, 93, 82, 87, 104, 109, 98, 103, 120, 125, 114, 119, 4, 9, 14, 3, 20, 25, 30, 19, 36, 41, 46, 35, 52, 57, 62, 51, 68, 73, 78, 67, 84, 89, 94, 83, 100, 105, 110, 99, 116, 121, 126, 115};

vector<unsigned char> RoundConstant= {2, 33, 16, 9, 36, 19, 40, 53, 26, 13, 38, 51, 56, 61, 62, 31, 14, 7, 34, 49, 24, 45, 54, 59, 28, 47, 22, 43, 20, 11, 4, 3, 32, 17, 8};

vector<unsigned char> TapPositions= {8, 13, 19, 35, 67, 106};
void Key_update(vector<unsigned char> &key)
{
    // convert nibble-wise variables into bit-wise variables
    vector<unsigned char> tmp(128);
    vector<unsigned char> buf(128);

    for(int i = 0; i < 32; i++){
        for(int j = 0; j < 4; j++){
            tmp[(i * 4) + j] = (key[i] >> j) & 0x1;
        }
    }

    // rotation
    for(int i = 0; i < 127; i++){
        buf[i] = tmp[i+1];
    }
    buf[127] = tmp[0];

    // convert bit-wise variables into nibble-wise variables
    for(int i = 0; i < 32; i++){
        key[i] = buf[(4 * i)] ^ (buf[(4 * i) + 1] << 1) ^ (buf[(4 * i) + 2] << 2) ^ (buf[(4 * i) + 3] << 3);
    }
}


void encryption(vector<unsigned char> & p, vector<unsigned char> &key)
{

    // whitening the key
    for(int i = 0; i < 32; i++){
        p[i] ^= key[i];
    }

    // round function
    for(int r =0; r < 35 ;r++)
    {

        // using Sbox
        for(int i = 0; i < 32; i++){
            p[i] = SBox[p[i]];
        }

        // convert nibble-wise variables into bit-wise variables
        // permutation
        vector<unsigned char> tmp(128);
        vector<unsigned char> buf(128);

        for(int i = 0; i < 32; i++){
            for(int j = 0; j < 4; j++){
                tmp[(i * 4) + j] = (p[i] >> j) & 0x1;
            }
        }

        // bit permutation
        for(int i = 0; i < 128; i++){
            buf[Permutation[i]] = tmp[i];
        }

        // add constant
        buf[TapPositions[0]] ^= RoundConstant[r] & 0x1;
        buf[TapPositions[1]] ^= (RoundConstant[r] >> 1) & 0x1;
        buf[TapPositions[2]] ^= (RoundConstant[r] >> 2) & 0x1;
        buf[TapPositions[3]] ^= (RoundConstant[r] >> 3) & 0x1;
        buf[TapPositions[4]] ^= (RoundConstant[r] >> 4) & 0x1;
        buf[TapPositions[5]] ^= (RoundConstant[r] >> 5) & 0x1;


        // convert bit-wise variables into nibble-wise variables
        for(int i = 0; i < 32; i++){
            p[i] = buf[(4 * i)] ^ (buf[(4 * i) + 1] << 1) ^ (buf[(4 * i) + 2] << 2) ^ (buf[(4 * i) + 3] << 3);
        }

        // key update
        Key_update(key);

        // add round key
        for(int i = 0; i < 32; i++){
            p[i] ^= (key[i] & 0b1101);
        }


    }
}

void Key_update_dec(vector<unsigned char> &key)
{
    // convert nibble-wise variables into bit-wise variables
    vector<unsigned char> tmp(128);
    vector<unsigned char> buf(128);

    for(int i = 0; i < 32; i++){
        for(int j = 0; j < 4; j++){
            tmp[(i * 4) + j] = (key[i] >> j) & 0x1;
        }
    }

    // rotation
    for(int i = 0; i < 127; i++){
        buf[i + 1] = tmp[i];
    }
    buf[0] = tmp[127];

    // convert bit-wise variables into nibble-wise variables
    for(int i = 0; i < 32; i++){
        key[i] = buf[(4 * i)] ^ (buf[(4 * i) + 1] << 1) ^ (buf[(4 * i) + 2] << 2) ^ (buf[(4 * i) + 3] << 3);
    }
}

void decryption(vector<unsigned char> &c , vector<unsigned char> &key)
{
    for(int  i=0; i < 35; i++)
    {
        Key_update(key);
    }

    for(int r=0; r < 35 ;r++)
    {
        // add round key
        for(int i = 0; i < 32; i++){
            c[i] ^= (key[i] & 0b1101);
        }

        Key_update_dec(key);

        // convert nibble-wise variables into bit-wise variables
        // permutation
        vector<unsigned char> tmp(128);
        vector<unsigned char> buf(128);

        for(int i = 0; i < 32; i++){
            for(int j = 0; j < 4; j++){
                tmp[(i * 4) + j] = (c[i] >> j) & 0x1;
            }
        }

        //add constant
        tmp[TapPositions[0]] ^= RoundConstant[34-r] & 0x1;
        tmp[TapPositions[1]] ^= (RoundConstant[34-r] >> 1) & 0x1;
        tmp[TapPositions[2]] ^= (RoundConstant[34-r] >> 2) & 0x1;
        tmp[TapPositions[3]] ^= (RoundConstant[34-r] >> 3) & 0x1;
        tmp[TapPositions[4]] ^= (RoundConstant[34-r] >> 4) & 0x1;
        tmp[TapPositions[5]] ^= (RoundConstant[34-r] >> 5) & 0x1;

        // bit permutation
        for(int i = 0; i < 128; i++){
            buf[InvPermutation[i]] = tmp[i];
        }

        for(int i=0; i < 32; i++)
        {
            c[i]=  buf[(4 * i)] ^ (buf[(4 * i) + 1] << 1) ^ (buf[(4 * i) + 2] << 2) ^ (buf[(4 * i) + 3] << 3);
        }

        // using Sbox
        for(int i = 0; i < 32; i++){
            c[i] = InvSBox[c[i]];
        }
    }
}

int main() {
    cout<< "plain text : ";
    for(int i = 0; i < 32; i++){
        cout << (int)plaintext[i];
    }
    encryption(plaintext, key);
    cout << endl;
    cout << "key : ";
    for(int i = 0; i < 32; i++){
        cout << hex << (int)key[i];
    }
    cout << endl;
    cout << "cipher text : ";
    for(int i = 0; i < 32; i++){
        cout << hex << (int)plaintext[i];
    }
    cout << endl;


    decryption(plaintext, key);
    cout << "decrypted text : ";
    for(int i = 0; i < 32; i++){
        cout << (int)plaintext[i];
    }
    
    return 0;
}