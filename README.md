# Seam-Carving

A Python implementation of Seam carving.

Seam carving (or liquid rescaling) is an algorithm for content-aware image resizing.


## Algorithm

1. Energy calculation with Dual-Gradient method
2. Seam identification with a DP algorithm similar to Dijkstra algorithm
3. Seam removal


## How to run

First install requirements
```bash
$ pip install -r requirements.txt
```

Run the script
```bash
$ python SeamCarving.py [INPUT_IMG_PATH] [H_PIXELS] [V_PIXELS] [MODE] [OUTPUT_FOLDER]
```

For example
```bash
$ python SeamCarving.py ../Inputs/In_0.png 50 50 quality 0_q
```

```bash
$ python SeamCarving.py ../Inputs/In_1.jpg 50 50 time 1_t
```


## Results

Input Image
<p align="center">
  <img src="https://raw.githubusercontent.com/ali-sedaghi/Seam-Carving/main/results/Inputs/In_6.jpg?token=GHSAT0AAAAAABZKT24IJPROJZQH364RVOW6YZWH2RQ" alt="Input-Image"/>
</p>

Vertical Seam
<p align="center">
  <img src="https://raw.githubusercontent.com/ali-sedaghi/Seam-Carving/main/results/Outputs/6_q/Seam_col0.jpg?token=GHSAT0AAAAAABZKT24JDPKJWMCE3XKJAQRWYZWH3KQ" alt="Vertical-Seam"/>
</p>

Horizontal Seam
<p align="center">
  <img src="https://raw.githubusercontent.com/ali-sedaghi/Seam-Carving/main/results/Outputs/6_q/Seam_row0.jpg?token=GHSAT0AAAAAABZKT24JCT6FJONYVZM2Y6CUYZWH4DA" alt="Horizontal-Seam"/>
</p>

Output Image
<p align="center">
  <img src="https://raw.githubusercontent.com/ali-sedaghi/Seam-Carving/main/results/Outputs/6_q/Final.jpg?token=GHSAT0AAAAAABZKT24ILUTHVQA27DD6DVVEYZWH42A" alt="Output-Image"/>
</p>
