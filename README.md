# Tools

This repository contains a collection of tools developed for various projects. I'm excited to share these utilities with the open‑source community. Contributions, issues, and feedback are welcome!

## Features

- **Image2Video Conversion:** Convert an image (PNG/JPG) into a video using state‑of‑the‑art models.
- Additional tools and features will be added as the project evolves.

## Setup

### Conda Environment

Follow these steps to set up your development environment using Conda:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/vincent-linktime/tools.git
   cd tools
   ```
2. **Create a Conda Environment:**
   ```bash
   conda create -n tools python=3.11
   ```
3. **Activate the Environment:**
   ```bash
   conda activate tools
   ```
4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Install the Package in Editable Mode:**
   ```bash
   pip install -e .
   ```

## Running the Image2Video Tool

Before running the tool, set your Replicate API token as an environment variable ([get your token here](https://replicate.com/account/api-tokens)):

```bash
export REPLICATE_API_TOKEN=your_replicate_api_token
```

Then, launch the tool with:

```bash
python -m tools.image2video.app
```

### How to Use

1. **Upload an Image:**  
   Use the interface to upload an image (PNG or JPG).
2. **Click "Run":**  
   The tool will process the image and generate a video.
3. **Play the Resulting Video:**  
   Once the conversion is complete, the generated video will be available to play.


## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For questions or suggestions, please open an issue or contact me via GitHub.
