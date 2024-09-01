# 🌟 Cache-Cool

**Cache-Cool** is a simple LLM (Large Language Model) caching proxy for saving your LLM calls. It acts as a caching layer for LLM API calls, such as OpenAI or Claude, to improve performance and reduce costs by avoiding redundant requests to the LLM providers. The caching is implemented using both MongoDB and JSON files.

## 📌 Project Details

- **GitHub Repository**: [https://github.com/msnp1381/Cache-Cool](https://github.com/msnp1381/Cache-Cool)
- **Project Name**: Cache-Cool
- **Project Description**: A simple LLM caching proxy for saving your LLM calls.

## 🚀 Features

- **💾 Cache Responses**: Caches responses from LLM API calls to reduce redundancy.
- **⚙️ Dynamic Configuration**: Allows dynamic configuration of LLM service and caching mechanisms via the `/configure` endpoint.
- **🔄 Supports Multiple LLMs**: Configurable to support different LLM services (e.g., OpenAI, Claude).
- **📂 Uses MongoDB and JSON for Caching**: Leverages both MongoDB and JSON files for caching API responses.

## 📡 Endpoints

- **POST /{schema_name}/chat/completions**:

> ***schema_name*** is defined in **confing.yaml**
  
Forwards chat completion requests to the configured LLM service or returns cached responses.

- **GET /configure**: Retrieves current configuration details.
- **PUT /configure**: Updates configuration settings dynamically.

## 🛠️ Getting Started

### Prerequisites

Before you start, make sure you have:

- **🐳 Docker**: Installed on your system. [Download Docker here](https://www.docker.com/products/docker-desktop)
- **🍃 MongoDB**: A running MongoDB instance for caching (local or remote).
- **🍅 Redis**: Optional A running Redis instance for caching.

### 📥 Installation

#### Option 1: Using Docker

1. **Clone the repository**:

   First, download the project files:

   ```bash
   git clone https://github.com/msnp1381/cache-cool.git
   cd cache-cool
   ```

2. **Build the Docker Image**:

   Now, create a Docker image for the project:

   ```bash
   docker build -t cache-cool .
   ```

3. **Run the Docker Container**:

   Make sure MongoDB is running and accessible. Update the `config.yaml` with your MongoDB connection details, then run:

   ```bash
   docker run -p 8000:8000 --env-file .env cache-cool
   ```

   Replace `.env` with your environment file containing necessary environment variables (like MongoDB URI).

4. **Access the Application**:

   Open your browser and go to [http://localhost:8000](http://localhost:8000) to start using Cache-Cool!

#### Option 2: Using `requirements.txt` and Running Locally

1. **Clone the repository**:

   First, download the project files:

   ```bash
   git clone https://github.com/msnp1381/cache-cool.git
   cd cache-cool
   ```

2. **Install Python Dependencies**:

   If you prefer using `requirements.txt`, install the dependencies as follows:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Run the Application with Uvicorn**:

   Start the FastAPI application using Uvicorn:

   ```bash
   uvicorn app.main:app --reload
   ```

   This will start the server at [http://localhost:8000](http://localhost:8000).

### ⚙️ Configuration

cache-cool uses a `config.yaml` file for initial configuration. You can also update configurations dynamically using the `/configure` endpoint.

#### Example config.yaml

```yaml
llm_schemas:
  openai:
    endpoint: "https://api.openai.com/v1/chat/completions"
    headers:
      - "Content-Type: application/json"
      - "Authorization: Bearer {api_key}"
    temperature_threshold: 0.8
  claude:
    endpoint: "https://api.claude.ai/v1/chat/completions"
    headers:
      - "Content-Type: application/json"
      - "Authorization: Bearer {api_key}"
    temperature_threshold: 0.85
  avalai:
    endpoint: "https://api.avalapis.ir/v1/chat/completions"
    headers:
      - "Content-Type: application/json"
      - "Authorization: {api_key}"
    temperature_threshold: 0.85

mongodb:
  uri: "mongodb://localhost:27017"
  db_name: "llm_cache_db"
  collection_name: "cache"

json_cache_file: "cache.json"

redis:
  enabled: false
  host: "localhost"
  port: 6379
  db: 0

current_llm_service: "openai"
use_json_cache: true
use_mongo_cache: true
```

### 📡 API Usage

Here’s how to use the API once the service is running:

#### Example Request

look at **usage.ipynb**

### 🤝 Contributing

We welcome contributions! Here’s how you can help:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

### 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 📧 Contact

If you have any questions or issues, feel free to contact us at [mohamadnematpoor@gmail.com](mailto:mohamadnematpoor@gmail.com).

Happy caching! 🚀
