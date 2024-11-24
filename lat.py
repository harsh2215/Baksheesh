import matplotlib.pyplot as plt
from fpdf import FPDF

# Define the S-box
s = [3, 0, 6, 13, 11, 5, 8, 14, 12, 15, 9, 2, 4, 10, 7, 1]

# Initialize the LAT table
lat = [[0 for _ in range(16)] for _ in range(16)]

# Generate the LAT
for a in range(16):  # Input mask
    for b in range(16):  # Output mask
        count = 0
        for x in range(16):
            input_masked = bin(a & x).count('1') % 2
            output_masked = bin(b & s[x]).count('1') % 2
            if input_masked == output_masked:
                count += 1
        lat[a][b] = count - 8  # Center around 0 by subtracting half the size (16/2 = 8)

# Plot the LAT as a heatmap
fig, ax = plt.subplots(figsize=(10, 8))
cax = ax.matshow(lat, cmap="coolwarm", alpha=0.8)

# Add annotations to the heatmap
for i in range(16):
    for j in range(16):
        ax.text(j, i, str(lat[i][j]), va='center', ha='center')

# Customize plot
plt.colorbar(cax)
ax.set_xticks(range(16))
ax.set_yticks(range(16))
ax.set_xticklabels([hex(x)[2:].upper() for x in range(16)])
ax.set_yticklabels([hex(x)[2:].upper() for x in range(16)])
plt.xlabel("Output Mask (β)", fontsize=12)
plt.ylabel("Input Mask (α)", fontsize=12)
plt.title("Linear Approximation Table (LAT) for Baksheesh S-box", fontsize=14)
plt.tight_layout()

# Save the plot as a PNG image
plt.savefig("lat_heatmap.png", dpi=300)
plt.close()

# Create a PDF with the heatmap
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# Add title
pdf.cell(200, 10, txt="Linear Approximation Table (LAT)", ln=True, align="C")
pdf.cell(200, 10, txt="Baksheesh Cipher S-box", ln=True, align="C")

# Add heatmap image to the PDF
pdf.image("lat_heatmap.png", x=10, y=40, w=190)

# Save the PDF
pdf.output("lat_table.pdf")

print("PDF with the LAT table has been generated as 'lat_table.pdf'.")
