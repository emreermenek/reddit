
# YouTube Shorts Video Generator  

This project is a YouTube Shorts video generator that randomly selects one clip and one music track from a list of 5 clips and 5 music files, combines them, and uploads the video to YouTube. It performs the following steps:  

1. **Selects a random clip and music track.**  
2. **Generates subtitles using OpenAI Whisper.**  
3. **Combines audio, subtitles, and video.**  
4. **Generates description, title, and tags using Gemini AI.**  
5. **Uploads the video to YouTube.**  

## Technologies and Libraries Used  

- **Torch + CUDA**: For deep learning tasks, including AI models, now utilizing GPU acceleration.  
- **OpenAI Whisper**: For automatic speech recognition (ASR) and generating subtitles.  
- **Tiktoken**: For tokenizing text, used in interaction with models.  
- **NumPy**: For numerical operations and handling arrays.  
- **Pandas**: For data manipulation and analysis.  
- **SymPy**: For symbolic mathematics (used in computations if necessary).  
- **FastAPI**: For creating an API to handle video generation requests.  
- **Starlette**: For building asynchronous web services.  
- **Requests**: For making HTTP requests.  
- **Selenium**: For automating browser tasks such as uploading to YouTube.  
- **Boto3**: For interacting with AWS services.  
- **Mypy-Boto3-DynamoDB**: For DynamoDB integration using the Mypy library.  
- **FFmpeg-Python**: For video manipulation and processing.  
- **Imageio**: For reading and writing video files.  
- **Imageio-FFmpeg**: For FFmpeg support with ImageIO.  
- **MoviePy**: For video editing, combining clips, and adding audio and text.  
- **Pydantic**: For data validation and settings management.  
- **Google-Auth**: For authenticating with Google services (YouTube API).  
- **Google-GenerativeAI**: For generating video descriptions, titles, and tags.  
- **Protobuf**: For serializing data in a format suitable for machine learning models.  
- **Trio**: For asynchronous programming.  
- **AnyIO**: For supporting asynchronous I/O operations.  

## Requirements  

Before running the project, make sure to install the necessary dependencies:  

- Install Python packages listed in `requirements.txt`.  
- Install **CUDA** for GPU acceleration.  
- Install FFmpeg.  
- Install ImageMagick.  

### CUDA Installation (GPU Acceleration)  

To improve performance and enable GPU support for Torch and Whisper, you need to install **CUDA**.  

1. Check your GPU compatibility on the [NVIDIA CUDA Toolkit website](https://developer.nvidia.com/cuda-toolkit).  
2. Download and install the latest CUDA version from [CUDA Downloads](https://developer.nvidia.com/cuda-downloads).  
3. Verify the installation by running:  

   ```bash
   nvcc --version
   ```  

4. Install PyTorch with CUDA support:  

   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```  

This ensures the application runs efficiently on your GPU instead of the CPU, significantly speeding up tasks like subtitle generation and AI processing.  

### FFmpeg Installation  

FFmpeg is required for processing video files. You can install FFmpeg by following the instructions on the [FFmpeg website](https://ffmpeg.org/download.html).  

### ImageMagick Installation  

ImageMagick is used for manipulating images. Install ImageMagick from [ImageMagick Downloads](https://imagemagick.org/script/download.php).  

## Installation  

1. Clone this repository to your local machine:  

   ```bash
   git clone https://github.com/yourusername/youtube-shorts-generator.git
   cd youtube-shorts-generator
   ```  

2. Install the required Python libraries using `pip`:  

   ```bash
   pip install -r requirements.txt
   ```  

3. Install **CUDA**, FFmpeg, and ImageMagick as per the instructions above.  

## Usage  

1. **Prepare Your Clips and Music**:  
   - Place your 5 video clips and 5 music tracks in the appropriate directories. Ensure that the file types are compatible with the script.  

2. **Run the Program**:  
   You can run the script to start the process of generating YouTube Shorts videos.  

   ```bash
   python main.py
   ```  

3. **Video Generation Flow**:  
   - The script will randomly select one video clip and one music track.  
   - It will use OpenAI Whisper (now with CUDA acceleration) to generate subtitles for the video.  
   - Then, the video, audio, and subtitles will be combined into a single file.  
   - The Gemini AI will generate a description, title, and tags for the YouTube video.  
   - The video will be uploaded to YouTube using Selenium for browser automation.  

4. **Configuration**:  
   - Configuration settings such as API keys, video directories, and YouTube credentials can be modified in the `config.json` file.  

## Configuration File: `config.json`  

Here is an example of the configuration file:  

```json
{
    "api_key": "your_openai_api_key",
    "youtube_credentials": {
        "client_id": "your_google_client_id",
        "client_secret": "your_google_client_secret",
        "refresh_token": "your_google_refresh_token"
    },
    "video_directory": "./clips/",
    "music_directory": "./music/",
    "output_directory": "./output_videos/"
}
```  

## YouTube API Integration  

Make sure you have a **Google Developer Console** project set up with access to the **YouTube Data API v3**. You will need the following credentials:  

- `client_id`  
- `client_secret`  
- `refresh_token`  

You can obtain these credentials from the [Google Developer Console](https://console.developers.google.com/).  

## Troubleshooting  

- **Video Not Uploading**: Check your YouTube API credentials and ensure the video file is in the correct format.  
- **Missing Libraries**: Ensure all dependencies are installed correctly by running `pip install -r requirements.txt`.  
- **CUDA Not Detected**: If `torch.cuda.is_available()` returns `False`, verify that CUDA is installed correctly and that your GPU supports it.  

## Future Improvements  

- Add support for multiple clips and music tracks to be selected for more diverse video outputs.  
- Enhance subtitle generation and language translation capabilities.  
- Implement error handling for more robust execution.  

## License  

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.  
