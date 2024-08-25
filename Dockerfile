# Use the official Python image from Docker Hub
FROM python:3.10

# For my sanity
RUN echo 'Acquire::http::Pipeline-Depth 0;\nAcquire::http::No-Cache true;\nAcquire::BrokenProxy true;\n' > /etc/apt/apt.conf.d/99fixbadproxy
RUN apt-get clean
RUN apt-get update
RUN apt-get install -y vim
RUN apt-get install -y ffmpeg

# Set the working directory in the container
WORKDIR /app
RUN mkdir -p fonts workspace music_samples

# Font related stuff
RUN apt-get install -y fontconfig
COPY fonts/* /usr/share/fonts/truetype/
RUN fc-cache -f -v


# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install project dependencies
RUN pip install -r requirements.txt

# To prevent an exception with ImageMagick running on Linux, comment this line out
RUN sed -i 's/policy domain="path" rights="none" pattern="@\*"\//!-- policy domain="path" rights="none" pattern="@\*"\/ --/g' /etc/ImageMagick-6/policy.xml

# Port we want to expose for gradio
EXPOSE 7860

# Set the default command to run your Python script; no command running for now
# CMD ["gradio", "/app/src/gradio_ui/app.py"]
