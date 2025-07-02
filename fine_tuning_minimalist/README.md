# Fine-tuning DistilGPT2 Model with Docker on WSL2

This guide explains how to set up and run the fine-tuning process for the DistilGPT2 model using Docker on Windows with WSL2.

## Building and Running the Docker Container

Open a WSL2 terminal in your project root and run:

```sh
docker build -t decompiler-finetune ./fine_tuning_minimalist/

docker run -it --rm -v $(pwd)/models:/app/models -v $(pwd)/data:/app/data decompiler-finetune:latest
```

- The script will start fine-tuning using the data and model you provided.
- Results and the fine-tuned model will be saved in the `model` directory.

## Troubleshooting
- **Out of Memory:** If the container stops or is killed, increase the Docker memory limit.
- **No Data Found:** Ensure your data is in the correct folders as described above.
- **Slow Training:** Training large models on CPU is slow.

## Dependencies
All required Python dependencies are installed automatically from `requirements.txt` in the Docker build process. No manual pip install is needed.

---