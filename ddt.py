import matplotlib.pyplot as plt
from fpdf import FPDF

# Define the S-box
s = [3, 0, 6, 13, 11, 5, 8, 14, 12, 15, 9, 2, 4, 10, 7, 1]

# Initialize the DDT table
ddt = [[0 for _ in range(16)] for _ in range(16)]

# Generate the DDT
for delta_in in range(16):
    for x in range(16):
        y1 = s[x]                     # S-box output for x
        y2 = s[x ^ delta_in]          # S-box output for x XOR delta_in
        delta_out = y1 ^ y2           # Output difference
        ddt[delta_in][delta_out] += 1 # Increment the DDT at [delta_in][delta_out]

# Plot the DDT as a heatmap
fig, ax = plt.subplots(figsize=(10, 8))
cax = ax.matshow(ddt, cmap="coolwarm", alpha=0.8)

# Add annotations to the heatmap
for i in range(16):
    for j in range(16):
        ax.text(j, i, str(ddt[i][j]), va='center', ha='center')

# Customize plot
plt.colorbar(cax)
ax.set_xticks(range(16))
ax.set_yticks(range(16))
ax.set_xticklabels([hex(x)[2:].upper() for x in range(16)])
ax.set_yticklabels([hex(x)[2:].upper() for x in range(16)])
plt.xlabel("Output Difference (Δout)", fontsize=12)
plt.ylabel("Input Difference (Δin)", fontsize=12)
plt.title("Difference Distribution Table (DDT) for Baksheesh S-box", fontsize=14)
plt.tight_layout()

# Save the plot as a PNG image
plt.savefig("ddt_heatmap.png", dpi=300)
plt.close()

# Create a PDF with the heatmap
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# Add title
pdf.cell(200, 10, txt="Difference Distribution Table (DDT)", ln=True, align="C")
pdf.cell(200, 10, txt="Baksheesh Cipher S-box", ln=True, align="C")

# Add heatmap image to the PDF
pdf.image("ddt_heatmap.png", x=10, y=40, w=190)

# Save the PDF
pdf.output("ddt_table.pdf")

print("PDF with the DDT table has been generated as 'ddt_table.pdf'.")
