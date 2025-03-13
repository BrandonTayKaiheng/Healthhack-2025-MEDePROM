FROM continuumio/miniconda3

WORKDIR /app

# Copy environment file
COPY req.txt .
COPY install/ install/

# Create conda environment
RUN conda create --name myenv --file req.txt

# Install IRIS Python package properly
# RUN conda run -n myenv python -m pip install ./install/intersystems_irispython-5.0.1-8026-cp38.cp39.cp310.cp311.cp312-cp38.cp39.cp310.cp311.cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

# Copy source code
COPY . src/

# Set environment variables
ENV PYTHONPATH=/app

# Expose the port
EXPOSE 8000

# Run the application
CMD ["conda", "run", "--no-capture-output", "-n", "myenv", "python", "src/main.py"] 
