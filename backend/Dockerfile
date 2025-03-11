FROM continuumio/miniconda3

WORKDIR /app

# Copy environment file
COPY conda-env.txt .

# Create conda environment
RUN conda create --name myenv --file conda-env.txt
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

# Install IRIS Python package
RUN pip install ./install/intersystems_irispython-5.0.1-8026-cp38.cp39.cp310.cp311.cp312-cp38.cp39.cp310.cp311.cp312-win_amd64.whl

# Copy source code
COPY . src/

# Set environment variables
ENV PYTHONPATH=/app

# Expose the port
EXPOSE 8000

# Run the application
CMD ["conda", "run", "--no-capture-output", "-n", "myenv", "python", "src/main.py"] 
