import os
import zipfile




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

def add_padding(input_data, block_size):
    """
    Adds padding to the input data to make its length a multiple of the block size.
    
    :param input_data: List of integers (nibbles) representing the input data.
    :param block_size: Integer representing the block size.
    """
    length = len(input_data)  # Number of nibbles in input
    # print(f"\nInput length: {length}")
    
    padding_size = (block_size - (length % block_size)) % block_size
    # if padding_size == 0:
    #     padding_size = block_size  # Add a full block of padding

    padding_size += 2
    # Append padding
    input_data.extend([(padding_size-2) % 16] * (padding_size-2))
    input_data.append(padding_size >> 4)
    input_data.append(padding_size & 0x0F)


def encryption(plaintext, key, SBox, TapPositions, RoundConstant):
    add_padding(plaintext, 32)
    # print("Plaintext after padding: ", end="")
    # print("".join(format(byte, "x") for byte in plaintext))

    # Whitening the key
    for i in range(32):
        plaintext[i] ^= key[i]

    # Round function
    for r in range(35):
        # SBox substitution
        for i in range(32):
            plaintext[i] = SBox[plaintext[i]]

        # Convert nibble-wise variables into bit-wise variables
        tmp = [0] * 128
        buf = [0] * 128
        for i in range(32):
            for j in range(4):
                tmp[(i * 4) + j] = (plaintext[i] >> j) & 0x1

        # Bit permutation
        for i in range(128):
            x = (i % 4) + ((i // 16) * 4)
            y = (i - ((i // 4) % 4)) % 4
            buf[(32 * y) + x] = tmp[i]

        # Add round constant
        for idx, tap in enumerate(TapPositions):
            buf[tap] ^= (RoundConstant[r] >> idx) & 0x1

        # Convert bit-wise variables back into nibble-wise variables
        for i in range(32):
            plaintext[i] = (buf[(4 * i)] |
                            (buf[(4 * i) + 1] << 1) |
                            (buf[(4 * i) + 2] << 2) |
                            (buf[(4 * i) + 3] << 3))

        # Key update
        key_update(key)

        # Add round key
        for i in range(32):
            plaintext[i] ^= (key[i] & 0b1101)

    encryted_chunk = []

    # print(len(plaintext))

    for i in range(0, len(plaintext), 2):
        combined = (plaintext[i] << 4) | plaintext[i+1]
        encryted_chunk.append(combined)
    return bytes(encryted_chunk)

def zip_directory(directory_path, output_zipfile):
    """
    Compresses the contents of a directory into a zip file.

    :param directory_path: Path to the directory to be zipped
    :param output_zipfile: Path to the output zip file
    """
    with zipfile.ZipFile(output_zipfile, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                # Get the full file path
                file_path = os.path.join(root, file)
                # Add file to zip, preserving the directory structure
                arcname = os.path.relpath(file_path, directory_path)
                zipf.write(file_path, arcname)
    # print(f"Directory '{directory_path}' has been zipped into '{output_zipfile}'")

def main():

    directory_to_zip = input("Enter the directory's path to be zipped : ")
    directory_to_zip = os.path.expanduser(directory_to_zip)
    permission = input("'input.zip' will be removed, you want it to be removed (type 'yes' if you want to, otherwise process stops.) ? ")
    if (permission != "yes"):
        print("Process exited ...")
        return
    print()

    # Example usage
    
    output_zip_file = "input.zip"
    zip_directory(directory_to_zip, output_zip_file)

    global plaintext
    global key
    global SBox
    global InvSBox
    global Permutation
    global InvPermutation
    global TapPositions
    global RoundConstant


    input_file = "input.zip"
    output_file = "output.zip"
    with open(input_file, "rb") as infile, open(output_file, "wb") as outfile:
        while True:
            # Read 16 bytes (128 bits) at a time
            chunk = infile.read(16)
            if not chunk:
                break  # End of file
            # print(type(chunk))

            # Convert each byte into two 4-bit (hexadecimal) values
            hex_array = []
            for byte in chunk:
                hex_array.append(byte >> 4)  # Higher 4 bits
                hex_array.append(byte & 0x0F)  # Lower 4 bits
            # for byte in hex_array:
            #     print(byte, end=" ")
            
            # Encrypt the chunk (call your encryption function here)
            encrypted_chunk = encryption(hex_array, key, SBox, TapPositions, RoundConstant)
            # encrypted_chunk = chunk
            # print("\nCiphertext: ", end=" ")
            # for byte in encrypted_chunk:
            #     print(format(byte, "x"), end="")
            # print()
            # Convert encrypted_chunk to bytes if it's a list of integers
            if isinstance(encrypted_chunk, list):
                encrypted_chunk = bytes(encrypted_chunk)
            # for byte in encrypted_chunk:
            #     print(byte >> 4, end=" ")
            #     print(byte & 0x0F, end=" ")
            # print()
            # Write the encrypted chunk to the output file
            outfile.write(encrypted_chunk)
            # print(len(encrypted_chunk))

    file_path = "input.zip"
    try:
        os.remove(file_path)
        print(f"File '{file_path}' has been removed.")
    except FileNotFoundError:
        print(f"File '{file_path}' does not exist.")
    except PermissionError:
        print(f"Permission denied: Cannot delete '{file_path}'.")
    except Exception as e:
        print(f"An error occurred while trying to delete the file: {e}")

    print(f"The directory is zipped to '{output_file}'.")


if __name__ == "__main__":
    main()

