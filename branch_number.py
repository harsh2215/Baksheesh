def hamming_weight(x):
    """Calculate the Hamming weight of a number."""
    return bin(x).count('1')

def compute_branch_number(sbox):
    """
    Calculate the differential branch number of an S-box.
    
    :param sbox: List of integers representing the S-box.
    :return: Branch number of the S-box.
    """
    n = len(sbox)  # Size of S-box
    branch_number = float('inf')  # Start with a large value

    for delta_in in range(1, n):  # Input differences (delta_in ≠ 0)
        for x in range(n):  # All possible inputs
            x_prime = x ^ delta_in  # Modified input
            if x_prime >= n:
                continue
            delta_out = sbox[x] ^ sbox[x_prime]  # Output difference
            if delta_out != 0:
                hw = hamming_weight(delta_in) + hamming_weight(delta_out)  # HW(input difference) + HW(output difference)
                branch_number = min(branch_number, hw)  # Update branch number if smaller

    return branch_number

# Define your S-box here
sbox = [3, 0, 6, 13, 11, 5, 8, 14, 12, 15, 9, 2, 4, 10, 7, 1]

# Compute and display the branch number
branch_number = compute_branch_number(sbox)
print(f"Differential Branch Number of the S-box: {branch_number}")
