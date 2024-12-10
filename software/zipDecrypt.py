import zipfile
import os

key = [
    0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 
    0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 
    0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 
    0x0, 0x0
]

plaintext = [
    0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 
    0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 
    0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
    0x0, 0x0, 
]

# Uncomment the following if you want to test with another example of plaintext
# plaintext = [
#     0x4, 0x4, 0x4, 0x4, 0x4, 0x4, 0x4, 0x4, 0x4, 0x4, 
#     0x4, 0x4, 0x4, 0x4, 0x4, 0x4, 0x4, 0x4, 0x4, 0x4, 
#     0x4, 0x4, 0x4, 0x4, 0x4, 0x4, 0x4, 0x4, 0x4, 0x4, 
#     0x4, 0x4
# ]

SBox = [3, 0, 6, 13, 11, 5, 8, 14, 12, 15, 9, 2, 4, 10, 7, 1]

InvSBox = [1, 15, 11, 0, 12, 5, 2, 14, 6, 10, 13, 4, 8, 3, 7, 9]

Permutation = [
    0, 33, 66, 99, 96, 1, 34, 67, 64, 97, 2, 35, 32, 65, 98, 3, 4, 37, 70, 103, 100, 5, 38, 71, 
    68, 101, 6, 39, 36, 69, 102, 7, 8, 41, 74, 107, 104, 9, 42, 75, 72, 105, 10, 43, 40, 73, 106, 11, 
    12, 45, 78, 111, 108, 13, 46, 79, 76, 109, 14, 47, 44, 77, 110, 15, 16, 49, 82, 115, 112, 17, 50, 
    83, 80, 113, 18, 51, 48, 81, 114, 19, 20, 53, 86, 119, 116, 21, 54, 87, 84, 117, 22, 55, 52, 85, 
    118, 23, 24, 57, 90, 123, 120, 25, 58, 91, 88, 121, 26, 59, 56, 89, 122, 27, 28, 61, 94, 127, 124, 
    29, 62, 95, 92, 125, 30, 63, 60, 93, 126, 31
]

InvPermutation = [
    0, 5, 10, 15, 16, 21, 26, 31, 32, 37, 42, 47, 48, 53, 58, 63, 64, 69, 74, 79, 80, 85, 90, 95, 
    96, 101, 106, 111, 112, 117, 122, 127, 12, 1, 6, 11, 28, 17, 22, 27, 44, 33, 38, 43, 60, 49, 54, 
    59, 76, 65, 70, 75, 92, 81, 86, 91, 108, 97, 102, 107, 124, 113, 118, 123, 8, 13, 2, 7, 24, 29, 
    18, 23, 40, 45, 34, 39, 56, 61, 50, 55, 72, 77, 66, 71, 88, 93, 82, 87, 104, 109, 98, 103, 120, 
    125, 114, 119, 4, 9, 14, 3, 20, 25, 30, 19, 36, 41, 46, 35, 52, 57, 62, 51, 68, 73, 78, 67, 84, 
    89, 94, 83, 100, 105, 110, 99, 116, 121, 126, 115
]

RoundConstant = [
    2, 33, 16, 9, 36, 19, 40, 53, 26, 13, 38, 51, 56, 61, 62, 31, 14, 7, 34, 49, 24, 45, 54, 59, 
    28, 47, 22, 43, 20, 11, 4, 3, 32, 17, 8
]

TapPositions = [8, 13, 19, 35, 67, 106]

def key_update(key):
    # Convert nibble-wise variables into bit-wise variables
    tmp = [0] * 128
    buf = [0] * 128

    # Convert each nibble into its bit-wise representation
    for i in range(32):
        for j in range(4):
            tmp[(i * 4) + j] = (key[i] >> j) & 0x1

    # Perform rotation
    for i in range(127):
        buf[i] = tmp[i + 1]
    buf[127] = tmp[0]

    # Convert bit-wise variables back into nibble-wise variables
    for i in range(32):
        key[i] = buf[(4 * i)] ^ (buf[(4 * i) + 1] << 1) ^ (buf[(4 * i) + 2] << 2) ^ (buf[(4 * i) + 3] << 3)


def key_update_dec(key):
    # Convert nibble-wise variables into bit-wise variables
    tmp = [0] * 128
    buf = [0] * 128

    for i in range(32):
        for j in range(4):
            tmp[(i * 4) + j] = (key[i] >> j) & 0x1

    # Rotation
    for i in range(127):
        buf[i + 1] = tmp[i]
    buf[0] = tmp[127]

    # Convert bit-wise variables back into nibble-wise variables
    for i in range(32):
        key[i] = (buf[(4 * i)] |
                  (buf[(4 * i) + 1] << 1) |
                  (buf[(4 * i) + 2] << 2) |
                  (buf[(4 * i) + 3] << 3))


def remove_padding(input_data):
    if not input_data:  # No input to process
        return

    padding_size = 16 * input_data[-2] + input_data[-1]  # Last element indicates padding size
    # print()
    # print(padding_size)
    if padding_size > len(input_data):
        raise ValueError("Invalid padding")  # Sanity check for corrupted input
    # Remove the padding
    del input_data[-padding_size:]


def decryption(ciphertext, key, round_constant, tap_positions, inv_permutation, inv_sbox):
    # Perform 35 initial key updates
    for _ in range(35):
        key_update(key)

    for r in range(35):
        # Add round key
        for i in range(32):
            ciphertext[i] ^= (key[i] & 0b1101)

        # Key update for decryption
        key_update_dec(key)

        # Convert nibble-wise variables into bit-wise variables
        tmp = [0] * 128
        buf = [0] * 128

        for i in range(32):
            for j in range(4):
                tmp[(i * 4) + j] = (ciphertext[i] >> j) & 0x1

        # Add round constant
        for i, position in enumerate(tap_positions):
            tmp[position] ^= (round_constant[34 - r] >> i) & 0x1

        # Bit permutation
        for i in range(128):
            buf[inv_permutation[i]] = tmp[i]

        # Convert bit-wise variables into nibble-wise variables
        for i in range(32):
            ciphertext[i] = (
                buf[(4 * i)]
                ^ (buf[(4 * i) + 1] << 1)
                ^ (buf[(4 * i) + 2] << 2)
                ^ (buf[(4 * i) + 3] << 3)
            )

        # Apply inverse SBox
        for i in range(32):
            ciphertext[i] = inv_sbox[ciphertext[i]]

    # Remove padding
    remove_padding(ciphertext)

    # Print the plaintext after removing padding
    # print("Plaintext after removing padding / Decrypted Text:", end=" ")
    # print("".join(f"{x:x}" for x in ciphertext))

    decryted_chunk = []
    for i in range(0, len(ciphertext), 2):
        combined = (ciphertext[i] << 4) | ciphertext[i+1]
        decryted_chunk.append(combined)
    return bytes(decryted_chunk)

def unzip_file(zip_file_path, output_directory):
    """
    Extracts the contents of a zip file into the specified directory.

    :param zip_file_path: Path to the zip file
    :param output_directory: Directory where the contents will be extracted
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    
    with zipfile.ZipFile(zip_file_path, 'r') as zipf:
        zipf.extractall(output_directory)
    
    # print(f"Contents of '{zip_file_path}' have been extracted to '{output_directory}'")

def main():
    global plaintext
    global key
    global SBox
    global InvSBox
    global Permutation
    global InvPermutation
    global TapPositions
    global RoundConstant

    input_file = input("Enter the path of the zip file to be extracted : ")
    input_file = os.path.expanduser(input_file)
    output_file = "finalput.zip"

    permission = input("'finalput.zip' will be removed, you want it to be removed (type 'yes' if you want to, otherwise process stops.) ? ")
    if (permission != "yes"):
        print("Process exited ...")
        return
    print()
    
    
    with open(input_file, "rb") as infile, open(output_file, "wb") as outfile:
        while True:
            count = 0
            # Read 17 bytes (136 bits) at a time
            chunk = infile.read(17)
            if not chunk:
                break  # End of file

            # Convert each byte into two 4-bit (hexadecimal) values
            hex_array = []
            for byte in chunk:
                hex_array.append(byte >> 4)  # Higher 4 bits
                hex_array.append(byte & 0x0F)  # Lower 4 bits
            # for byte in hex_array:
            #     print(hex(byte), end=" ")
            # print()
            
            # Encrypt the chunk (call your encryption function here)
            encrypted_chunk = decryption(hex_array, key, RoundConstant, TapPositions, InvPermutation, InvSBox)
            
            # encrypted_chunk = chunk
            # print((encrypted_chunk))
            # Write the encrypted chunk to the output file
            outfile.write(encrypted_chunk)
            # print(chunk)

    # Example usage
    zip_file_to_unzip = "finalput.zip"
    unzip_to_directory = input("Where to extract the files (path / Press Enter) ?? ")
    if (unzip_to_directory is None or unzip_to_directory == "") :
        unzip_to_directory = "output"
    elif (unzip_to_directory[-1] == "/") :
        unzip_to_directory = unzip_to_directory + "output"
        unzip_to_directory = os.path.expanduser(unzip_to_directory)
    else :
        unzip_to_directory = unzip_to_directory + "/output"
        unzip_to_directory = os.path.expanduser(unzip_to_directory)

    # Create the directory
    if not os.path.exists(unzip_to_directory):
        os.makedirs(unzip_to_directory)
        print(f"Directory '{unzip_to_directory}' created .")
    else:
       print(f"Directory '{unzip_to_directory}' already exists on the Desktop. It is being edited.")

    unzip_file(zip_file_to_unzip, unzip_to_directory)

    file_path = "finalput.zip"
    try:
        os.remove(file_path)
        print(f"File '{file_path}' has been removed.")
    except FileNotFoundError:
        print(f"File '{file_path}' does not exist.")
    except PermissionError:
        print(f"Permission denied: Cannot delete '{file_path}'.")
    except Exception as e:
        print(f"An error occurred while trying to delete the file: {e}")

    print(f"Contents are extracted to '{unzip_to_directory}'.")

    


if __name__ == "__main__":
    main()