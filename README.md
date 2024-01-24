
# Web Cereal

![Web Cereal Logo](https://github.com/segin-GH/web-cereal/assets/98380527/b0314f50-1c09-4c0d-90fc-e6041abff6bd)

Web Cereal provides a fast and lightweight solution for managing your serial data over the web. Discover more on our [official website](https://web-cereal.segin.in).

## Getting Started

Follow these steps to get Web Cereal up and running on your system:

### Prerequisites

- Git
- Node.js `v20.10.0` (Download [here](https://github.com/nodesource/distributions))
- Python (for the Oats agent)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/segin-GH/web-cereal.git
   ```

2. **Frontend Setup**
   Navigate to the 'cereal' directory and install dependencies:
   ```bash
   cd cereal
   npm install
   npm run dev
   ```

3. **Backend Setup (Oats Agent)**
   Move to the 'oats' directory and start the agent:
   ```bash
   cd ../oats
   ./dist/oats-agent/oats-agent
   ```

4. **View Logs**
   Access logs by navigating to the 'logs' directory:
   ```bash
   cd ../logs
   ```

## Development Setup

Here's how you can set up Web Cereal for development:

### Frontend Development

1. **Navigate to the Frontend Directory**
   ```bash
   cd cereal
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Launch Development Server**
   ```bash
   npm run dev
   ```

### Backend Development (Oats Agent)

1. **Navigate to the Oats Directory**
   ```bash
   cd ../oats/oats-agent
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Oats Agent**
   ```bash
   ./run.py
   ```

4. **Access Logs**
   ```bash
   cd ../logs
   ```


# Contributing to Web Cereal

Web Cereal welcomes contributions from developers of all skill levels. If you're looking to contribute, follow these steps:

## 1. Explore the Issues
Start by exploring the [issues](https://github.com/segin-GH/web-cereal/issues) on the GitHub repository. Pick an issue that interests you or propose a new feature or bug fix in a new branch if you are propsing a fix to `dev/v1.1.0` then name you branch `fix/v1.1.0_thecoolfix`.


Remember, every contribution, whether big or small, is valuable to the project. Happy coding!
